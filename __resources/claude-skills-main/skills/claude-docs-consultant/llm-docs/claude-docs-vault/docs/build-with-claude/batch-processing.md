---
created: 2025-11-05
modified: 2025-11-05
title: "Batch processing"
url: https://docs.claude.com/en/docs/build-with-claude/batch-processing
category: docs
subcategory: build-with-claude
tags:
  - docs
  - build-with-claude
related:
  - '[[citations]]'
  - '[[context-editing]]'
  - '[[context-windows]]'
  - '[[embeddings]]'
  - '[[extended-thinking]]'
---

# Batch processing

Batch processing is a powerful approach for handling large volumes of requests efficiently. Instead of processing requests one at a time with immediate responses, batch processing allows you to submit multiple requests together for asynchronous processing. This pattern is particularly useful when:

* You need to process large volumes of data
* Immediate responses are not required
* You want to optimize for cost efficiency
* You're running large-scale evaluations or analyses

The Message Batches API is our first implementation of this pattern.

***

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/build-with-claude/batch-processing)
