---
name: manus-data-science
description: Data science agent with Pandas, scikit-learn, matplotlib/seaborn visualization, time-series forecasting, and HuggingFace model integration. 12+ specialized HF models for NER, sentiment, embeddings, and zero-shot classification.
allowed-tools: Read, Bash, Grep, Glob
---

# Manus Data Science Agent

Data analysis and ML in `~/manus-chatbot/agents/implementations/data_scientist_agent.py`.

## Capabilities

- **Pandas** dataframe operations and analysis
- **scikit-learn** ML (classification, regression, clustering)
- **matplotlib/seaborn** visualization
- **Time-series** forecasting
- **Statistical analysis** and hypothesis testing

## HuggingFace Models (`agents/huggingface_models.py`)

| Model | Task |
|-------|------|
| Skill extraction | Extract skills from text |
| Named Entity Recognition | Identify entities in text |
| Sentence embeddings | Semantic similarity |
| Sentiment analysis | Positive/negative/neutral |
| Zero-shot classification | Classify without training |
| Text summarization | Compress long text |
| Question answering | Extract answers from context |
| Text generation | Generate text completions |
| Token classification | NER, POS tagging |
| Translation | Multi-language support |
| Fill-mask | Predict masked tokens |
| Feature extraction | Dense vector representations |

## API

```bash
curl -X POST http://localhost:8000/api/v1/chat/message \
  -d '{"message": "Load sales.csv and show monthly revenue trends with a chart"}'
```
