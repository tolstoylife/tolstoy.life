---
created: 2025-11-05
modified: 2025-11-05
title: "Retrieve Message Batch Results"
url: https://docs.claude.com/en/api/retrieving-message-batch-results
category: api
description: "Streams the results of a Message Batch as a `.jsonl` file."
tags:
  - api
related:
  - '[[get-api-key]]'
  - '[[list-api-keys]]'
  - '[[update-api-key]]'
  - '[[get-claude-code-usage-report]]'
  - '[[create-invite]]'
---

# Retrieve Message Batch Results

get /v1/messages/batches/{message_batch_id}/results
Streams the results of a Message Batch as a `.jsonl` file.

Each line in the file is a JSON object containing the result of a single request in the Message Batch. Results are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

Learn more about the Message Batches API in our [[batch-processing|user guide]]

> [!warning]
> The path for retrieving Message Batch results should be pulled from the batch's `results_url`. This path should not be assumed and may change.

<ResponseExample>
  ```JSON 200 theme={null}
  {"custom_id":"my-second-request","result":{"type":"succeeded","message":{"id":"msg_014VwiXbi91y3JMjcpyGBHX5","type":"message","role":"assistant","model":"claude-sonnet-4-5-20250929","content":[{"type":"text","text":"Hello again! It's nice to see you. How can I assist you today? Is there anything specific you'd like to chat about or any questions you have?"}],"stop_reason":"end_turn","stop_sequence":null,"usage":{"input_tokens":11,"output_tokens":36}}}}
  {"custom_id":"my-first-request","result":{"type":"succeeded","message":{"id":"msg_01FqfsLoHwgeFbguDgpz48m7","type":"message","role":"assistant","model":"claude-sonnet-4-5-20250929","content":[{"type":"text","text":"Hello! How can I assist you today? Feel free to ask me any questions or let me know if there's anything you'd like to chat about."}],"stop_reason":"end_turn","stop_sequence":null,"usage":{"input_tokens":10,"output_tokens":34}}}}
  ```

  ```JSON 4XX theme={null}
  {
    "type": "error",
    "error": {
      "type": "invalid_request_error",
      "message": "<string>"
    }
  }
  ```
</ResponseExample>

---

**Source:** [Official Documentation](https://docs.claude.com/en/api/retrieving-message-batch-results)
