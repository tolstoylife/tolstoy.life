---
created: 2025-11-05
modified: 2025-11-05
title: "Retrieve a Message Batch"
url: https://docs.claude.com/en/api/retrieving-message-batches
category: api
description: "This endpoint is idempotent and can be used to poll for Message Batch completion. To access the results of a Message Batch, make a request to the `results_url` field in the response."
tags:
  - api
related:
  - '[[get-api-key]]'
  - '[[list-api-keys]]'
  - '[[update-api-key]]'
  - '[[get-claude-code-usage-report]]'
  - '[[create-invite]]'
---

# Retrieve a Message Batch

get /v1/messages/batches/{message_batch_id}
This endpoint is idempotent and can be used to poll for Message Batch completion. To access the results of a Message Batch, make a request to the `results_url` field in the response.

Learn more about the Message Batches API in our [[batch-processing|user guide]]

---

**Source:** [Official Documentation](https://docs.claude.com/en/api/retrieving-message-batches)
