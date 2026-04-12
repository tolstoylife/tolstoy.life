---
created: 2025-11-05
modified: 2025-11-05
title: "Long context prompting tips"
url: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/long-context-tips
category: docs
subcategory: build-with-claude
tags:
  - docs
  - build-with-claude
  - prompt
related:
  - '[[batch-processing]]'
  - '[[citations]]'
  - '[[context-editing]]'
  - '[[context-windows]]'
  - '[[embeddings]]'
---

# Long context prompting tips

> [!note]
> While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [[extended-thinking-tips|here]].

Claude's extended context window (200K tokens for Claude 3 models) enables handling complex, data-rich tasks. This guide will help you leverage this power effectively.

## Essential tips for long context prompts

* **Put longform data at the top**: Place your long documents and inputs (\~20K+ tokens) near the top of your prompt, above your query, instructions, and examples. This can significantly improve Claude's performance across all models.

  > [!note]
> Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs.

* **Structure document content and metadata with XML tags**: When using multiple documents, wrap each document in `<document>` tags with `<document_content>` and `<source>` (and other metadata) subtags for clarity.

  > [!info]- Example multi-document structure
> ```xml  theme={null}
>     <documents>
>       <document index="1">
>         <source>annual_report_2023.pdf</source>
>         <document_content>
>           {{ANNUAL_REPORT}}
>         </document_content>
>       </document>
>       <document index="2">
>         <source>competitor_analysis_q2.xlsx</source>
>         <document_content>
>           {{COMPETITOR_ANALYSIS}}
>         </document_content>
>       </document>
>     </documents>
>
>     Analyze the annual report and competitor analysis. Identify strategic advantages and recommend Q3 focus areas.
>     ```

* **Ground responses in quotes**: For long document tasks, ask Claude to quote relevant parts of the documents first before carrying out its task. This helps Claude cut through the "noise" of the rest of the document's contents.

  > [!info]- Example quote extraction
> ```xml  theme={null}
>     You are an AI physician's assistant. Your task is to help doctors diagnose possible patient illnesses.
>
>     <documents>
>       <document index="1">
>         <source>patient_symptoms.txt</source>
>         <document_content>
>           {{PATIENT_SYMPTOMS}}
>         </document_content>
>       </document>
>       <document index="2">
>         <source>patient_records.txt</source>
>         <document_content>
>           {{PATIENT_RECORDS}}
>         </document_content>
>       </document>
>       <document index="3">
>         <source>patient01_appt_history.txt</source>
>         <document_content>
>           {{PATIENT01_APPOINTMENT_HISTORY}}
>         </document_content>
>       </document>
>     </documents>
>
>     Find quotes from the patient records and appointment history that are relevant to diagnosing the patient's reported symptoms. Place these in <quotes> tags. Then, based on these quotes, list all information that would help the doctor diagnose the patient's symptoms. Place your diagnostic information in <info> tags.
>     ```

***


> [!info] Prompt library
> Get inspired by a curated selection of prompts for various tasks and use cases.

  > [!info] GitHub prompting tutorial
> An example-filled tutorial that covers the prompt engineering concepts found in our docs.

  > [!info] Google Sheets prompting tutorial
> A lighter weight version of our prompt engineering tutorial via an interactive spreadsheet.


---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/long-context-tips)
