import dspy
from typing import List, Dict, Any
from pex_data_loader import load_los, load_saqs, load_atomic_saqs, JSON_PATH, CSV_PATH, SAQ_ATOMIC_PATH

# 1. Load Data
print("Loading PEX Data...")
los = load_los(JSON_PATH)
saqs = load_saqs(CSV_PATH)
atomic_saqs = load_atomic_saqs(SAQ_ATOMIC_PATH)
print(f"Loaded {len(los)} LOs, {len(saqs)} SAQs, and {len(atomic_saqs)} Atomic SAQs")

# 2. Define Custom Retriever with Nuanced Logic
class PEXRetriever(dspy.Retrieve):
    def __init__(self, los, saqs, atomic_saqs, k=5):
        super().__init__(k=k)
        self.los = los
        self.saqs = saqs
        self.atomic_saqs = atomic_saqs

    def forward(self, query_or_queries, k=None):
        k = k if k is not None else self.k
        query = query_or_queries if isinstance(query_or_queries, str) else query_or_queries[0]
        query_lower = query.lower()
        keywords = query_lower.split()

        results = []

        # Helper: Calculate derived score
        def calc_score(content, meta_text, extra_boost=0):
            score = 0
            text_to_search = (content + " " + meta_text).lower()

            # Exact phrase match
            if query_lower in text_to_search:
                score += 20

            # Keyword matches
            for word in keywords:
                if word in text_to_search:
                    score += 2

            # Boost logic
            score += extra_boost
            return score

        # Search LOs
        for lo in self.los:
            meta_str = " ".join([f"{k}:{v}" for k,v in lo['metadata'].items()])
            # Boost for type matches
            boost = 5 if 'field' in lo['metadata'] and any(w in lo['metadata']['field'].lower() for w in keywords) else 0

            score = calc_score(lo['content'] + " " + lo['id'], meta_str, boost)

            if score > 0:
                results.append(dspy.Prediction(
                    text=f"LO [{lo['id']}]: {lo['content'][:300]}...",
                    score=score,
                    type='LO',
                    id=lo['id'],
                    full_content=lo['content'],
                    metadata=lo['metadata']
                ))

        # Search Atomic SAQs
        for saq in self.atomic_saqs:
            # Boost for entity matches
            boost = 10 if any(entity.get('label', '').lower() in query_lower for entity in saq['entities']) else 0

            score = calc_score(saq['content'], saq['entity_text'], boost)

            if score > 0:
                results.append(dspy.Prediction(
                    text=f"Atomic SAQ [{saq['id']}]: {saq['content'][:200]}...",
                    score=score,
                    type='AtomicSAQ',
                    id=saq['id'],
                    full_content=saq['content'],
                    entities=saq['entities']
                ))

        # Search CSV SAQs (Legacy fallback if Atomic doesn't cover everything)
        for saq in self.saqs:
            score = calc_score(saq['question'] + " " + saq['comment'], "")
            if score > 0:
                 results.append(dspy.Prediction(
                    text=f"SAQ [{saq['id']}]: {saq['question'][:200]}...",
                    score=score,
                    type='SAQ',
                    id=saq['id'],
                    full_content=f"Q: {saq['question']}\nComment: {saq['comment']}"
                ))

        # Sort and return top k unique results (by ID)
        unique_results = {}
        for r in sorted(results, key=lambda x: x.score, reverse=True):
            if r.id not in unique_results:
                unique_results[r.id] = r

        return list(unique_results.values())[:k]

# 3. Define Signatures
class GenerateSuggestion(dspy.Signature):
    """Generate comprehensive study suggestions based on retrieved medical curriculum content."""
    topic = dspy.InputField(desc="Medical topic to study")
    context = dspy.InputField(desc="Retrieved LOs and SAQs relevant to the topic")

    suggestion_1 = dspy.OutputField(desc="Primary suggestion focusing on core physiological/pharmacological principles")
    suggestion_2 = dspy.OutputField(desc="Secondary suggestion focusing on clinical application or pathology")
    suggestion_3 = dspy.OutputField(desc="Tertiary suggestion focusing on data interpretation or comparative analysis")

# 4. Define Generation Module
class PEXGenerator(dspy.Module):
    def __init__(self, retriever):
        super().__init__()
        self.retriever = retriever
        self.generate = dspy.Predict(GenerateSuggestion)

    def forward(self, topic):
        # Retrieve context
        passages = self.retriever(topic, k=8)

        context_str = "\n\n".join([
            f"[{p.type} {p.id}]\n{p.full_content}\n" +
            (f"Entities: {', '.join([e['label'] for e in p.entities])}" if hasattr(p, 'entities') else "")
            for p in passages
        ])

        print(f"DEBUG: Retrieved {len(passages)} passages for context.")

        # Generate suggestions
        prediction = self.generate(topic=topic, context=context_str)
        return prediction

# 5. Main Execution
if __name__ == "__main__":
    # Configure Gemini using dspy.LM (version 2.6.x style)
    try:
        lm = dspy.LM(
            model='openai/gemini-3-flash-preview', # Prefix might be needed for litellm backend
            api_key='sk-no-key-required',
            api_base='http://localhost:8318/v1',
            max_tokens=2048,
            temperature=0.7
        )
    except AttributeError:
         # Fallback for slightly older versions if dspy.LM isn't the main entry
         # Check if we can use dspy.OpenAI (it might have been imported differently or moved)
         # In DSPy 2.6+, many providers are consolidated.
         # Let's try explicit dspy.configure with litellm params
         try:
             lm = dspy.OpenAI( # This often wraps litellm in many versions
                 model='gemini-3-flash-preview',
                 api_key='sk-no-key-required',
                 api_base='http://localhost:8318/v1',
                 max_tokens=2048
             )
         except:
             # Final attempt: direct dspy.configure with kwargs (experimental)
             # But let's assume dspy.LM works for 2.6.x as it's the modern interface
             print("Could not initialize dspy.LM. Attempting legacy dspy.OpenAI...")
             pass

    dspy.settings.configure(lm=lm)

    retriever = PEXRetriever(los, saqs, atomic_saqs, k=10)
    module = PEXGenerator(retriever)

    # Topic to generate suggestions for
    topic = "cerebral blood flow"

    print(f"\n{'='*60}")
    print(f"Generating Study Suggestions for: {topic}")
    print(f"{'='*60}\n")

    try:
        pred = module(topic=topic)

        print(f"Suggestion 1 (Principles):\n{pred.suggestion_1}\n")
        print(f"{'-'*60}\n")
        print(f"Suggestion 2 (Application):\n{pred.suggestion_2}\n")
        print(f"{'-'*60}\n")
        print(f"Suggestion 3 (Analysis):\n{pred.suggestion_3}\n")

    except Exception as e:
        print(f"Error during generation: {e}")
        import traceback
        traceback.print_exc()
