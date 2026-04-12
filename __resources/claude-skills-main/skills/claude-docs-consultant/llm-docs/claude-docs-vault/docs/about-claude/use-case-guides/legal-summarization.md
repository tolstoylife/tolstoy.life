---
created: 2025-11-05
modified: 2025-11-05
title: "Legal summarization"
url: https://docs.claude.com/en/docs/about-claude/use-case-guides/legal-summarization
category: docs
subcategory: about-claude
description: "This guide walks through how to leverage Claude's advanced natural language processing capabilities to efficiently summarize legal documents, extracting key information and expediting legal research. With Claude, you can streamline the review of contracts, litigation prep, and regulatory work, saving time and ensuring accuracy in your legal processes."
tags:
  - docs
  - about-claude
related:
  - '[[glossary]]'
  - '[[model-deprecations]]'
  - '[[choosing-a-model]]'
  - '[[migrating-to-claude-4]]'
  - '[[overview]]'
---

# Legal summarization

This guide walks through how to leverage Claude's advanced natural language processing capabilities to efficiently summarize legal documents, extracting key information and expediting legal research. With Claude, you can streamline the review of contracts, litigation prep, and regulatory work, saving time and ensuring accuracy in your legal processes.

> Visit our [summarization cookbook](https://github.com/anthropics/anthropic-cookbook/blob/main/skills/summarization/guide.ipynb) to see an example legal summarization implementation using Claude.

## Before building with Claude

### Decide whether to use Claude for legal summarization

Here are some key indicators that you should employ an LLM like Claude to summarize legal documents:

> [!info]- You want to review a high volume of documents efficiently and affordably
> Large-scale document review can be time-consuming and expensive when done manually. Claude can process and summarize vast amounts of legal documents rapidly, significantly reducing the time and cost associated with document review. This capability is particularly valuable for tasks like due diligence, contract analysis, or litigation discovery, where efficiency is crucial.
  > [!info]- You require automated extraction of key metadata
> Claude can efficiently extract and categorize important metadata from legal documents, such as parties involved, dates, contract terms, or specific clauses. This automated extraction can help organize information, making it easier to search, analyze, and manage large document sets. It's especially useful for contract management, compliance checks, or creating searchable databases of legal information.
  > [!info]- You want to generate clear, concise, and standardized summaries
> Claude can generate structured summaries that follow predetermined formats, making it easier for legal professionals to quickly grasp the key points of various documents. These standardized summaries can improve readability, facilitate comparison between documents, and enhance overall comprehension, especially when dealing with complex legal language or technical jargon.
  > [!info]- You need precise citations for your summaries
> When creating legal summaries, proper attribution and citation are crucial to ensure credibility and compliance with legal standards. Claude can be prompted to include accurate citations for all referenced legal points, making it easier for legal professionals to review and verify the summarized information.
  > [!info]- You want to streamline and expedite your legal research process
> Claude can assist in legal research by quickly analyzing large volumes of case law, statutes, and legal commentary. It can identify relevant precedents, extract key legal principles, and summarize complex legal arguments. This capability can significantly speed up the research process, allowing legal professionals to focus on higher-level analysis and strategy development.

### Determine the details you want the summarization to extract

There is no single correct summary for any given document. Without clear direction, it can be difficult for Claude to determine which details to include. To achieve optimal results, identify the specific information you want to include in the summary.

For instance, when summarizing a sublease agreement, you might wish to extract the following key points:

```python  theme={null}
details_to_extract = [
    'Parties involved (sublessor, sublessee, and original lessor)',
    'Property details (address, description, and permitted use)', 
    'Term and rent (start date, end date, monthly rent, and security deposit)',
    'Responsibilities (utilities, maintenance, and repairs)',
    'Consent and notices (landlord\'s consent, and notice requirements)',
    'Special provisions (furniture, parking, and subletting restrictions)'
]
```

### Establish success criteria

Evaluating the quality of summaries is a notoriously challenging task. Unlike many other natural language processing tasks, evaluation of summaries often lacks clear-cut, objective metrics. The process can be highly subjective, with different readers valuing different aspects of a summary. Here are criteria you may wish to consider when assessing how well Claude performs legal summarization.

> [!info]- Factual correctness
> The summary should accurately represent the facts, legal concepts, and key points in the document.
  > [!info]- Legal precision
> Terminology and references to statutes, case law, or regulations must be correct and aligned with legal standards.
  > [!info]- Conciseness
> The summary should condense the legal document to its essential points without losing important details.
  > [!info]- Consistency
> If summarizing multiple documents, the LLM should maintain a consistent structure and approach to each summary.
  > [!info]- Readability
> The text should be clear and easy to understand. If the audience is not legal experts, the summarization should not include legal jargon that could confuse the audience.
  > [!info]- Bias and fairness
> The summary should present an unbiased and fair depiction of the legal arguments and positions.

See our guide on [[define-success|establishing success criteria]] for more information.

***

## How to summarize legal documents using Claude

### Select the right Claude model

Model accuracy is extremely important when summarizing legal documents. Claude Sonnet 4.5 is an excellent choice for use cases such as this where high accuracy is required. If the size and quantity of your documents is large such that costs start to become a concern, you can also try using a smaller model like Claude Haiku 4.5.

To help estimate these costs, below is a comparison of the cost to summarize 1,000 sublease agreements using both Sonnet and Haiku:

* **Content size**
  * Number of agreements: 1,000
  * Characters per agreement: 300,000
  * Total characters: 300M

* **Estimated tokens**
  * Input tokens: 86M (assuming 1 token per 3.5 characters)
  * Output tokens per summary: 350
  * Total output tokens: 350,000

* **Claude Sonnet 4.5 estimated cost**
  * Input token cost: 86 MTok \* \$3.00/MTok = \$258
  * Output token cost: 0.35 MTok \* \$15.00/MTok = \$5.25
  * Total cost: \$258.00 + \$5.25 = \$263.25

* **Claude Haiku 3 estimated cost**
  * Input token cost: 86 MTok \* \$0.25/MTok = \$21.50
  * Output token cost: 0.35 MTok \* \$1.25/MTok = \$0.44
  * Total cost: \$21.50 + \$0.44 = \$21.96

> [!tip]
> Actual costs may differ from these estimates. These estimates are based on the example highlighted in the section on [prompting](#build-a-strong-prompt).

### Transform documents into a format that Claude can process

Before you begin summarizing documents, you need to prepare your data. This involves extracting text from PDFs, cleaning the text, and ensuring it's ready to be processed by Claude.

Here is a demonstration of this process on a sample pdf:

```python  theme={null}
from io import BytesIO
import re

import pypdf
import requests

def get_llm_text(pdf_file):
    reader = pypdf.PdfReader(pdf_file)
    text = "\n".join([page.extract_text() for page in reader.pages])

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text) 

    # Remove page numbers
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text) 

    return text

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/about-claude/use-case-guides/legal-summarization)
