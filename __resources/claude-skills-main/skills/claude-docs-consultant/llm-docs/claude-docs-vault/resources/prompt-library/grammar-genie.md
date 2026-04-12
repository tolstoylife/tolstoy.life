---
created: 2025-11-05
modified: 2025-11-05
title: "Grammar genie"
url: https://docs.claude.com/en/resources/prompt-library/grammar-genie
category: resources
subcategory: prompt-library
description: "Transform grammatically incorrect sentences into proper English."
tags:
  - resources
  - prompt-library
  - prompt
related:
  - '[[adaptive-editor]]'
  - '[[airport-code-analyst]]'
  - '[[alien-anthropologist]]'
  - '[[alliteration-alchemist]]'
  - '[[babels-broadcasts]]'
---

# Grammar genie

Transform grammatically incorrect sentences into proper English.

> Copy this prompt into our developer [Console](https://console.anthropic.com/dashboard) to try it for yourself!

|        | Content                                                                                                                                                                                                                                                                                     |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| System | Your task is to take the text provided and rewrite it into a clear, grammatically correct version while preserving the original meaning as closely as possible. Correct any spelling mistakes, punctuation errors, verb tense issues, word choice problems, and other grammatical mistakes. |
| User   | I can haz cheeseburger?                                                                                                                                                                                                                                                                     |

## Example Output

May I have a cheeseburger?

***

## API Request



**Python**

```Python  theme={null}
    import anthropic

    client = anthropic.Anthropic(  # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key="my_api_key",
    )
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        temperature=0,
        system="Your task is to take the text provided and rewrite it into a clear, grammatically correct version while preserving the original meaning as closely as possible. Correct any spelling mistakes, punctuation errors, verb tense issues, word choice problems, and other grammatical mistakes.",
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": "I can haz cheeseburger?"}],
            }
        ],
    )
    print(message.content)

    ```


  
**TypeScript**

```TypeScript  theme={null}
    import Anthropic from "@anthropic-ai/sdk";

    const anthropic = new Anthropic({
      apiKey: "my_api_key", // defaults to process.env["ANTHROPIC_API_KEY"]
    });

    const msg = await anthropic.messages.create({
      model: "claude-sonnet-4-5",
      max_tokens: 1000,
      temperature: 0,
      system: "Your task is to take the text provided and rewrite it into a clear, grammatically correct version while preserving the original meaning as closely as possible. Correct any spelling mistakes, punctuation errors, verb tense issues, word choice problems, and other grammatical mistakes.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "I can haz cheeseburger?"
            }
          ]
        }
      ]
    });
    console.log(msg);

    ```


  
**AWS Bedrock Python**

```Python  theme={null}
    from anthropic import AnthropicBedrock

    # See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
    # for authentication options
    client = AnthropicBedrock()

    message = client.messages.create(
        model="anthropic.claude-sonnet-4-5-20250929-v1:0",
        max_tokens=1000,
        temperature=0,
        system="Your task is to take the text provided and rewrite it into a clear, grammatically correct version while preserving the original meaning as closely as possible. Correct any spelling mistakes, punctuation errors, verb tense issues, word choice problems, and other grammatical mistakes.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I can haz cheeseburger?"
                    }
                ]
            }
        ]
    )
    print(message.content)

    ```


  
**AWS Bedrock TypeScript**

```TypeScript  theme={null}
    import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";

    // See https://docs.claude.com/claude/reference/claude-on-amazon-bedrock
    // for authentication options
    const client = new AnthropicBedrock();

    const msg = await client.messages.create({
    model: "anthropic.claude-sonnet-4-5-20250929-v1:0",
    max_tokens: 1000,
    temperature: 0,
    system: "Your task is to take the text provided and rewrite it into a clear, grammatically correct version while preserving the original meaning as closely as possible. Correct any spelling mistakes, punctuation errors, verb tense issues, word choice problems, and other grammatical mistakes.",
    messages: [
    {
    "role": "user",
    "content": [
    {
    "type": "text",
    "text": "I can haz cheeseburger?"
    }
    ]
    }
    ]
    });
    console.log(msg);

    ```


  
**Vertex AI Python**

```Python  theme={null}
    from anthropic import AnthropicVertex

    client = AnthropicVertex()

    message = client.messages.create(
        model="claude-sonnet-4@20250514",
        max_tokens=1000,
        temperature=0,
        system="Your task is to take the text provided and rewrite it into a clear, grammatically correct version while preserving the original meaning as closely as possible. Correct any spelling mistakes, punctuation errors, verb tense issues, word choice problems, and other grammatical mistakes.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I can haz cheeseburger?"
                    }
                ]
            }
        ]
    )
    print(message.content)

    ```


  
**Vertex AI TypeScript**

```TypeScript  theme={null}
    import { AnthropicVertex } from '@anthropic-ai/vertex-sdk';

    // Reads from the `CLOUD_ML_REGION` & `ANTHROPIC_VERTEX_PROJECT_ID` environment variables.
    // Additionally goes through the standard `google-auth-library` flow.
    const client = new AnthropicVertex();

    const msg = await client.messages.create({
      model: "claude-sonnet-4@20250514",
      max_tokens: 1000,
      temperature: 0,
      system: "Your task is to take the text provided and rewrite it into a clear, grammatically correct version while preserving the original meaning as closely as possible. Correct any spelling mistakes, punctuation errors, verb tense issues, word choice problems, and other grammatical mistakes.",
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "I can haz cheeseburger?"
            }
          ]
        }
      ]
    });
    console.log(msg);

    ```



---

**Source:** [Official Documentation](https://docs.claude.com/en/resources/prompt-library/grammar-genie)
