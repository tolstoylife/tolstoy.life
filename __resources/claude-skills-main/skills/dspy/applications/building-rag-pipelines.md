# Building RAG Pipelines

Retrieval-Augmented Generation (RAG) is a core pattern in DSPy. DSPy treats retrieval as just another module that can be optimized.

## Basic RAG

```python
import dspy

class RAG(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()
        # Retrieve module
        self.retrieve = dspy.Retrieve(k=num_passages)
        # Generate module (Chain of Thought)
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        # 1. Retrieve
        context = self.retrieve(question).passages

        # 2. Generate
        return self.generate(context=context, question=question)
```

## Configuring Retrieval

You need to configure a retrieval model (RM) globally or locally.

```python
# ColBERTv2 (Hosted)
colbert = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')

# ChromaDB (Local)
from dspy.retrieve.chromadb_rm import ChromadbRM
chroma = ChromadbRM(collection_name="my_docs", persist_directory="./db")

# Configure globally
dspy.settings.configure(rm=colbert)
```

## Advanced RAG Patterns

### RAG with Reranking

Retrieve more passages than needed, then use a `Predict` module to score/filter them.

```python
class RerankedRAG(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=10)
        self.rerank = dspy.Predict("question, passage -> relevance: float")
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        passages = self.retrieve(question).passages

        # Score each passage
        scored = []
        for p in passages:
            score = self.rerank(question=question, passage=p).relevance
            scored.append((score, p))

        # Top 3
        top_3 = sorted(scored, reverse=True)[:3]
        context = [p for _, p in top_3]

        return self.generate(context=context, question=question)
```

### Multi-Hop RAG

For questions requiring information from multiple sources.

```python
class MultiHopRAG(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=3)
        self.gen_query = dspy.ChainOfThought("question -> search_query")
        self.gen_answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        # Hop 1
        q1 = self.gen_query(question=question).search_query
        passages1 = self.retrieve(q1).passages

        # Hop 2 (conditioned on first result)
        q2 = self.gen_query(question=f"Orig: {question}, Found: {passages1}").search_query
        passages2 = self.retrieve(q2).passages

        return self.gen_answer(context=passages1 + passages2, question=question)
```

## Optimization

The beauty of DSPy RAG is that you can optimize the *generation* to deal with noisy retrieval, OR optimize the *queries* to improve retrieval, simply by providing (Question, Answer) examples. You don't necessarily need labeled "relevant passages" – the optimizer infers what works.
