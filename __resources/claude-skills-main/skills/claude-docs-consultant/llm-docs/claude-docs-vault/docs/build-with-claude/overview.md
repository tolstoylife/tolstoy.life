---
created: 2025-11-05
modified: 2025-11-05
title: "Features overview"
url: https://docs.claude.com/en/docs/build-with-claude/overview
category: docs
subcategory: build-with-claude
description: "Explore Claude's advanced features and capabilities."
tags:
  - docs
  - build-with-claude
related:
  - '[[batch-processing]]'
  - '[[citations]]'
  - '[[context-editing]]'
  - '[[context-windows]]'
  - '[[embeddings]]'
---

# Features overview

Explore Claude's advanced features and capabilities.

export const PlatformAvailability = ({claudeApi = false, claudeApiBeta = false, bedrock = false, bedrockBeta = false, vertexAi = false, vertexAiBeta = false}) => {
  const platforms = [];
  if (claudeApi || claudeApiBeta) {
    platforms.push(claudeApiBeta ? 'Claude API (Beta)' : 'Claude API');
  }
  if (bedrock || bedrockBeta) {
    platforms.push(bedrockBeta ? 'Amazon Bedrock (Beta)' : 'Amazon Bedrock');
  }
  if (vertexAi || vertexAiBeta) {
    platforms.push(vertexAiBeta ? "Google Cloud's Vertex AI (Beta)" : "Google Cloud's Vertex AI");
  }
  return <>
      {platforms.map((platform, index) => <span key={index}>
          {platform}
          {index < platforms.length - 1 && <><br /><br /></>}
        </span>)}
    </>;
};

## Core capabilities

These features enhance Claude's fundamental abilities for processing, analyzing, and generating content across various formats and use cases.

| Feature                                                                                       | Description                                                                                                                                                                                                               | Availability                                                    |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [[context-windows#1m-token-context-window|1M token context window]] | An extended context window that allows you to process much larger documents, maintain longer conversations, and work with more extensive codebases.                                                                       | <PlatformAvailability claudeApiBeta bedrockBeta vertexAiBeta /> |
| [[overview|Agent Skills]]                               | Extend Claude's capabilities with Skills. Use pre-built Skills (PowerPoint, Excel, Word, PDF) or create custom Skills with instructions and scripts. Skills use progressive disclosure to efficiently manage context.     | <PlatformAvailability claudeApiBeta />                          |
| [[batch-processing|Batch processing]]                               | Process large volumes of requests asynchronously for cost savings. Send batches with a large number of queries per batch. Batch API calls costs 50% less than standard API calls.                                         | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [[citations|Citations]]                                             | Ground Claude's responses in source documents. With Citations, Claude can provide detailed references to the exact sentences and passages it uses to generate responses, leading to more verifiable, trustworthy outputs. | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [[context-editing|Context editing]]                                 | Automatically manage conversation context with configurable strategies. Supports clearing tool results when approaching token limits and managing thinking blocks in extended thinking conversations.                     | <PlatformAvailability claudeApiBeta bedrockBeta vertexAiBeta /> |
| [[extended-thinking|Extended thinking]]                             | Enhanced reasoning capabilities for complex tasks, providing transparency into Claude's step-by-step thought process before delivering its final answer.                                                                  | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [[files|Files API]]                                                 | Upload and manage files to use with Claude without re-uploading content with each request. Supports PDFs, images, and text files.                                                                                         | <PlatformAvailability claudeApiBeta />                          |
| [[pdf-support|PDF support]]                                         | Process and analyze text and visual content from PDF documents.                                                                                                                                                           | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [[prompt-caching|Prompt caching (5m)]]                              | Provide Claude with more background knowledge and example outputs to reduce costs and latency.                                                                                                                            | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [[prompt-caching#1-hour-cache-duration|Prompt caching (1hr)]]       | Extended 1-hour cache duration for less frequently accessed but important context, complementing the standard 5-minute cache.                                                                                             | <PlatformAvailability claudeApi />                              |
| [[search-results|Search results]]                                   | Enable natural citations for RAG applications by providing search results with proper source attribution. Achieve web search-quality citations for custom knowledge bases and tools.                                      | <PlatformAvailability claudeApi vertexAi />                     |
| [[messages-count-tokens|Token counting]]                                               | Token counting enables you to determine the number of tokens in a message before sending it to Claude, helping you make informed decisions about your prompts and usage.                                                  | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [[overview|Tool use]]                                       | Enable Claude to interact with external tools and APIs to perform a wider variety of tasks. For a list of supported tools, see [the Tools table](#tools).                                                                 | <PlatformAvailability claudeApi bedrock vertexAi />             |

## Tools

These features enable Claude to interact with external systems, execute code, and perform automated tasks through various tool interfaces.

| Feature                                                                                       | Description                                                                                                                                                        | Availability                                                    |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------- |
| [[bash-tool|Bash]]                                          | Execute bash commands and scripts to interact with the system shell and perform command-line operations.                                                           | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [[code-execution-tool|Code execution]]                      | Run Python code in a sandboxed environment for advanced data analysis.                                                                                             | <PlatformAvailability claudeApiBeta />                          |
| [[computer-use-tool|Computer use]]                          | Control computer interfaces by taking screenshots and issuing mouse and keyboard commands.                                                                         | <PlatformAvailability claudeApiBeta bedrockBeta vertexAiBeta /> |
| [[fine-grained-tool-streaming|Fine-grained tool streaming]] | Stream tool use parameters without buffering/JSON validation, reducing latency for receiving large parameters.                                                     | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [[mcp-connector|MCP connector]]                                      | Connect to remote [MCP](https://docs.claude.com/en/docs/agents-and-tools/mcp) servers directly from the Messages API without a separate MCP client.                                       | <PlatformAvailability claudeApiBeta />                          |
| [[memory-tool|Memory]]                                      | Enable Claude to store and retrieve information across conversations. Build knowledge bases over time, maintain project context, and learn from past interactions. | <PlatformAvailability claudeApiBeta bedrockBeta vertexAiBeta /> |
| [[text-editor-tool|Text editor]]                            | Create and edit text files with a built-in text editor interface for file manipulation tasks.                                                                      | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [[web-fetch-tool|Web fetch]]                                | Retrieve full content from specified web pages and PDF documents for in-depth analysis.                                                                            | <PlatformAvailability claudeApiBeta />                          |
| [[web-search-tool|Web search]]                              | Augment Claude's comprehensive knowledge with current, real-world data from across the web.                                                                        | <PlatformAvailability claudeApi vertexAi />                     |

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/build-with-claude/overview)
