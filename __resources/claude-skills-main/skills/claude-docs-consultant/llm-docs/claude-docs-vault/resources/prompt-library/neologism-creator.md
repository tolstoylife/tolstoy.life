---
created: 2025-11-05
modified: 2025-11-05
title: "Neologism creator"
url: https://docs.claude.com/en/resources/prompt-library/neologism-creator
category: resources
subcategory: prompt-library
description: "Invent new words and provide their definitions based on user-provided concepts or ideas."
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

# Neologism creator

Invent new words and provide their definitions based on user-provided concepts or ideas.

> Copy this prompt into our developer [Console](https://console.anthropic.com/dashboard) to try it for yourself!

|      | Content                                                                                                                               |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------- |
| User | Can you help me create a new word for the act of pretending to understand something in order to avoid looking ignorant or uninformed? |

## Example output

How about the neologism "fauxprehension" to describe this concept?

Fauxprehension (fəʊprɪˈhɛnʃ(ə)n) - noun\
Definition: The act of feigning understanding or comprehension of a topic, concept, or situation in order to avoid appearing ignorant, uninformed, or out of the loop. It is the pretense of knowledge or grasp of a subject matter, often employed in social or professional settings to maintain one's image or status.

Etymology: The word "fauxprehension" is a blend of "faux," which comes from the French word meaning false or fake, and "comprehension," which means the action or capability of understanding something.

***

## API request



**Python**

```Python  theme={null}
    import anthropic

    client = anthropic.Anthropic(
      # defaults to os.environ.get("ANTHROPIC_API_KEY")
      api_key="my_api_key",
    )
    message = client.messages.create(
      model="claude-sonnet-4-5",
      max_tokens=1000,
      temperature=1,
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Can you help me create a new word for the act of pretending to understand something in order to avoid looking ignorant or uninformed?"
            }
          ]
        }
      ]
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
      temperature: 1,
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Can you help me create a new word for the act of pretending to understand something in order to avoid looking ignorant or uninformed?"
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
        temperature=1,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Can you help me create a new word for the act of pretending to understand something in order to avoid looking ignorant or uninformed?"
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
      temperature: 1,
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Can you help me create a new word for the act of pretending to understand something in order to avoid looking ignorant or uninformed?"
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
        temperature=1,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Can you help me create a new word for the act of pretending to understand something in order to avoid looking ignorant or uninformed?"
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
      temperature: 1,
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Can you help me create a new word for the act of pretending to understand something in order to avoid looking ignorant or uninformed?"
            }
          ]
        }
      ]
    });
    console.log(msg);

    ```



---

**Source:** [Official Documentation](https://docs.claude.com/en/resources/prompt-library/neologism-creator)
