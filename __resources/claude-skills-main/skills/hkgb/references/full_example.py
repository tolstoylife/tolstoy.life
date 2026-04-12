"""
Hybrid Knowledge Graph Bridge - Complete Implementation Example

This script demonstrates the integration pattern between a domain graph (structured CSV)
and a lexical graph (LLM extraction from unstructured documents).

Customize the schema, CSV structure, and Cypher queries for your specific domain.
"""

import os
from dotenv import load_dotenv
load_dotenv()

import asyncio
import csv

from neo4j import GraphDatabase
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from neo4j_graphrag.experimental.components.text_splitters.fixed_size_splitter import FixedSizeSplitter

# =============================================================================
# NEO4J CONNECTION
# =============================================================================

neo4j_driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    auth=("neo4j", "password")
)
neo4j_driver.verify_connectivity()

# =============================================================================
# STEP 1: LEXICAL GRAPH SCHEMA SPECIFICATION
# Customize these for your domain
# =============================================================================

NODE_TYPES = [
    # Simple labels
    "Entity",
    "Concept",
    "Process",
    # Enriched with description (guides LLM extraction)
    {
        "label": "Outcome", 
        "description": "A result, benefit, or consequence of a process or action."
    },
    # With typed properties
    {
        "label": "Reference",
        "description": "An external resource such as a document, article, or dataset.",
        "properties": [
            {"name": "name", "type": "STRING", "required": True}, 
            {"name": "type", "type": "STRING"}
        ]
    },
]

RELATIONSHIP_TYPES = [
    "RELATED_TO",
    "PART_OF",
    "USED_IN",
    "LEADS_TO",
    "REFERENCES"
]

# Valid triplet patterns - LLM can only extract conforming combinations
PATTERNS = [
    ("Entity", "RELATED_TO", "Entity"),
    ("Concept", "RELATED_TO", "Entity"),
    ("Process", "PART_OF", "Entity"),
    ("Process", "LEADS_TO", "Outcome"),
    ("Reference", "REFERENCES", "Entity"),
]

# =============================================================================
# STEP 2: EXTRACTION PIPELINE CONFIGURATION
# =============================================================================

llm = OpenAILLM(
    model_name="gpt-4o",
    model_params={
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
)

embedder = OpenAIEmbeddings(model="text-embedding-ada-002")

text_splitter = FixedSizeSplitter(chunk_size=500, chunk_overlap=100)

kg_builder = SimpleKGPipeline(
    llm=llm,
    driver=neo4j_driver, 
    neo4j_database="neo4j", 
    embedder=embedder, 
    from_pdf=True,
    text_splitter=text_splitter,
    schema={
        "node_types": NODE_TYPES,
        "relationship_types": RELATIONSHIP_TYPES,
        "patterns": PATTERNS
    },
)

# =============================================================================
# STEP 3: STRUCTURED SOURCE TO DICTIONARY
# Customize CSV path and expected columns for your domain
# =============================================================================

data_path = "./data/"

records = csv.DictReader(
    open(os.path.join(data_path, "metadata.csv"), encoding="utf8", newline='')
)
# Expected columns: filename, entity_id, category, author, ...

# =============================================================================
# STEP 5: CYPHER JOIN QUERY
# Customize for your domain entity structure
# =============================================================================

cypher = """
MATCH (d:Document {path: $file_path})
MERGE (e:DomainEntity {id: $entity_id})
SET e.category = $category,
    e.author = $author
MERGE (d)-[:BELONGS_TO]->(e)
"""

# =============================================================================
# MAIN LOOP
# =============================================================================

for record in records:

    # STEP 4: Add common key to dictionary
    # This key MUST match Document.path created by the pipeline
    record["file_path"] = os.path.join(data_path, record["filename"])
    print(f"Processing: {record['file_path']}")

    # Generate lexical graph (creates Document node with path property)
    result = asyncio.run(
        kg_builder.run_async(file_path=record["file_path"])
    )

    # Join with domain graph using common key
    query_result, summary, keys = neo4j_driver.execute_query(
        cypher,
        parameters_=record,
        database_="neo4j"
    )
    print(f"  Extracted: {result}")
    print(f"  Graph updates: {summary.counters}")

# =============================================================================
# BRIDGE VERIFICATION
# =============================================================================

print("\n--- Bridge Integrity Check ---")

# Check for orphan documents (lexical graph not linked to domain graph)
orphans_query = """
MATCH (d:Document)
WHERE NOT EXISTS { (d)-[:BELONGS_TO]->(:DomainEntity) }
RETURN d.path AS orphan
"""

orphan_records, _, _ = neo4j_driver.execute_query(
    orphans_query,
    database_=os.getenv("NEO4J_DATABASE")
)

if orphan_records:
    print("WARNING: Orphan documents detected (broken bridge):")
    for rec in orphan_records:
        print(f"  - {rec['orphan']}")
else:
    print("OK: All documents linked to domain graph")

# Check for domain entities without documents
missing_query = """
MATCH (e:DomainEntity)
WHERE NOT EXISTS { (:Document)-[:BELONGS_TO]->(e) }
RETURN e.id AS missing
"""

missing_records, _, _ = neo4j_driver.execute_query(
    missing_query,
    database_=os.getenv("NEO4J_DATABASE")
)

if missing_records:
    print("WARNING: Domain entities without documents:")
    for rec in missing_records:
        print(f"  - {rec['missing']}")
else:
    print("OK: All domain entities have linked documents")

neo4j_driver.close()
