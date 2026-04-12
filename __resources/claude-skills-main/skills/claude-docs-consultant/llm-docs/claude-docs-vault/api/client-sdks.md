---
created: 2025-11-05
modified: 2025-11-05
title: "Client SDKs"
url: https://docs.claude.com/en/api/client-sdks
category: api
description: "We provide client libraries in a number of popular languages that make it easier to work with the Claude API."
tags:
  - api
  - sdk
related:
  - '[[get-api-key]]'
  - '[[list-api-keys]]'
  - '[[update-api-key]]'
  - '[[get-claude-code-usage-report]]'
  - '[[create-invite]]'
---

# Client SDKs

We provide client libraries in a number of popular languages that make it easier to work with the Claude API.

> [!note]
> Additional configuration is needed to use Anthropic's Client SDKs through a partner platform. If you are using Amazon Bedrock, see [[claude-on-amazon-bedrock|this guide]]; if you are using Google Cloud Vertex AI, see [[claude-on-vertex-ai|this guide]].

## Python

[Python library GitHub repo](https://github.com/anthropics/anthropic-sdk-python)

Example:

```Python Python theme={null}
import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="my_api_key",
)
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(message.content)
```

Accepted `model` strings:

```Python  theme={null}

---

**Source:** [Official Documentation](https://docs.claude.com/en/api/client-sdks)
