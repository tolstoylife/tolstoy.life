---
created: 2025-11-05
modified: 2025-11-05
title: "Delete a File"
url: https://docs.claude.com/en/api/files-delete
category: api
description: "Make a file inaccessible through the API"
tags:
  - api
related:
  - '[[get-api-key]]'
  - '[[list-api-keys]]'
  - '[[update-api-key]]'
  - '[[get-claude-code-usage-report]]'
  - '[[create-invite]]'
---

# Delete a File

DELETE /v1/files/{file_id}
Make a file inaccessible through the API

The Files API allows you to upload and manage files to use with the Claude API without having to re-upload content with each request. For more information about the Files API, see the [[files|developer guide for files]].

> [!note]
> The Files API is currently in beta. To use the Files API, you'll need to include the beta feature header: `anthropic-beta: files-api-2025-04-14`.
>
>   Please reach out through our [feedback form](https://forms.gle/tisHyierGwgN4DUE9) to share your experience with the Files API.

---

**Source:** [Official Documentation](https://docs.claude.com/en/api/files-delete)
