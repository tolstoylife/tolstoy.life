import dspy
from typing import List
from pex_data_loader import load_los, load_saqs, JSON_PATH, CSV_PATH

# 1. Load Data
print("Loading PEX Data...")
los = load_los(JSON_PATH)
saqs = load_saqs(CSV_PATH)
print(f"Loaded {len(los)} LOs and {len(saqs)} SAQs")

# 2. Define Custom Retriever (Simple Keyword/Content Matcher for Demo)
class LocalPEXRetriever(dspy.Retrieve):
    def __init__(self, los, saqs, k=5):
        super().__init__(k=k)
        self.los = los
        self.saqs = saqs

    def forward(self, query_or_queries, k=None):
        k = k if k is not None else self.k
        query = query_or_queries if isinstance(query_or_queries, str) else query_or_queries[0]
        query_lower = query.lower()

        results = []

        # Search LOs
        for lo in self.los:
            # Simple scoring: count query word occurrences
            score = 0
            content_lower = (lo['content'] + " " + lo['id']).lower()
            if query_lower in content_lower:
                score += 10
            for word in query_lower.split():
                if word in content_lower:
                    score += 1

            if score > 0:
                results.append(dspy.Prediction(
                    text=f"LO [{lo['id']}]: {lo['content'][:200]}...",
                    score=score,
                    type='LO',
                    id=lo['id'],
                    full_content=lo['content']
                ))

        # Search SAQs
        for saq in self.saqs:
            score = 0
            content_lower = (saq['question'] + " " + saq['comment']).lower()
            if query_lower in content_lower:
                score += 10
            for word in query_lower.split():
                if word in content_lower:
                    score += 1

            if score > 0:
                results.append(dspy.Prediction(
                    text=f"SAQ [{saq['id']}] ({saq['pass_rate']}): {saq['question']}",
                    score=score,
                    type='SAQ',
                    id=saq['id'],
                    full_content=saq['question'] + "\nComment: " + saq['comment']
                ))

        # Sort by score and take top k
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:k]

# 3. Define Signature
class RetrievePEXInfo(dspy.Signature):
    """Retrieve Learning Objectives and SAQs relevant to a medical topic."""
    topic = dspy.InputField(desc="medical topic or concept")
    results = dspy.OutputField(desc="list of relevant LOs and SAQs with details")

# 4. Define Module
class PEXResearchModule(dspy.Module):
    def __init__(self, retriever):
        super().__init__()
        self.retriever = retriever

    def forward(self, topic):
        # Retrieve
        passages = self.retriever(topic)

        # Format results (in a real scenario, an LM would synthesize this)
        formatted_results = []
        for p in passages:
            formatted_results.append(f"[{p.type}] {p.text}")

        return dspy.Prediction(results=formatted_results)

# 5. Execution Demo
if __name__ == "__main__":
    # Configure settings (no LM needed for pure retrieval if we don't use Predict)
    # dspy.settings.configure(lm=dspy.OpenAI(model='gpt-3.5-turbo'))

    retriever = LocalPEXRetriever(los, saqs, k=10)
    module = PEXResearchModule(retriever)

    # Test queries
    queries = ["haematology", "anemia", "transfusion", "coagulation"]

    print(f"\n{'='*50}")
    print(f"DSPy PEX Retrieval Demo")
    print(f"{'='*50}")

    for q in queries:
        print(f"\nQuery: {q}")
        print("-" * 30)
        pred = module(topic=q)
        for res in pred.results:
            print(res)
