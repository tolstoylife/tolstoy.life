---
created: 2025-11-05
modified: 2025-11-05
title: "Git gud"
url: https://docs.claude.com/en/resources/prompt-library/git-gu
category: resources
subcategory: prompt-library
description: "Generate appropriate Git commands based on user-described version control actions."
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

# Git gud

Generate appropriate Git commands based on user-described version control actions.

> Copy this prompt into our developer [Console](https://console.anthropic.com/dashboard) to try it for yourself!

| Role | Content                                                                                                                       |
| ---- | ----------------------------------------------------------------------------------------------------------------------------- |
| User | I have made some changes to my local files and I want to save them in my local Git repository. What Git command should I use? |

## Example Output

To save the changes you've made to your local files in your local Git repository, you should use the following Git commands:

1. `git add .` or `git add <file>`

   * This command stages the changes you've made, preparing them to be committed. The `.` adds all changes in the current directory and its subdirectories. If you only want to stage specific files, replace `.` with the file name or path.

2. `git commit -m "Your commit message"`

   * This command commits the staged changes to your local Git repository. The `-m` flag allows you to provide a commit message describing the changes you've made. Replace `"Your commit message"` with a brief, descriptive summary of your changes.

For example, if you've made changes to a file named `example.txt`, you would run:

```
git add example.txt
git commit -m "Update example.txt with new content"

```

These commands will save your changes in your local Git repository, creating a new commit with the provided message. You can later push these changes to a remote repository or continue working on your local branch.

Remember to run these commands from within your Git repository directory in your terminal or command prompt.

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
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I have made some changes to my local files and I want to save them in my local Git repository. What Git command should I use?",
                    }
                ],
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
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "I have made some changes to my local files and I want to save them in my local Git repository. What Git command should I use?"
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
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I have made some changes to my local files and I want to save them in my local Git repository. What Git command should I use?"
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
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "I have made some changes to my local files and I want to save them in my local Git repository. What Git command should I use?"
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
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I have made some changes to my local files and I want to save them in my local Git repository. What Git command should I use?"
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
      messages: [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "I have made some changes to my local files and I want to save them in my local Git repository. What Git command should I use?"
            }
          ]
        }
      ]
    });
    console.log(msg);

    ```



---

**Source:** [Official Documentation](https://docs.claude.com/en/resources/prompt-library/git-gu)
