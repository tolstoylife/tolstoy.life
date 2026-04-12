---
created: 2025-11-05
modified: 2025-11-05
title: "Delete a Message Batch"
url: https://docs.claude.com/en/api/deleting-message-batches
category: api
description: "Delete a Message Batch."
tags:
  - api
related:
  - '[[get-api-key]]'
  - '[[list-api-keys]]'
  - '[[update-api-key]]'
  - '[[get-claude-code-usage-report]]'
  - '[[create-invite]]'
---

# Delete a Message Batch

delete /v1/messages/batches/{message_batch_id}
Delete a Message Batch.

Message Batches can only be deleted once they've finished processing. If you'd like to delete an in-progress batch, you must first cancel it.

Learn more about the Message Batches API in our [[batch-processing|user guide]]

---

**Source:** [Official Documentation](https://docs.claude.com/en/api/deleting-message-batches)
