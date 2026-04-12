---
created: 2025-11-05
modified: 2025-11-05
title: "Cancel a Message Batch"
url: https://docs.claude.com/en/api/canceling-message-batches
category: api
description: "Batches may be canceled any time before processing ends. Once cancellation is initiated, the batch enters a `canceling` state, at which time the system may complete any in-progress, non-interruptible requests before finalizing cancellation."
tags:
  - api
related:
  - '[[get-api-key]]'
  - '[[list-api-keys]]'
  - '[[update-api-key]]'
  - '[[get-claude-code-usage-report]]'
  - '[[create-invite]]'
---

# Cancel a Message Batch

post /v1/messages/batches/{message_batch_id}/cancel
Batches may be canceled any time before processing ends. Once cancellation is initiated, the batch enters a `canceling` state, at which time the system may complete any in-progress, non-interruptible requests before finalizing cancellation.

The number of canceled requests is specified in `request_counts`. To determine which requests were canceled, check the individual results within the batch. Note that cancellation may not result in any canceled requests if they were non-interruptible.

Learn more about the Message Batches API in our [[batch-processing|user guide]]

---

**Source:** [Official Documentation](https://docs.claude.com/en/api/canceling-message-batches)
