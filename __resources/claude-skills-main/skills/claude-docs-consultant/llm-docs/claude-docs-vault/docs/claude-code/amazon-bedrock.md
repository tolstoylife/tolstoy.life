---
created: 2025-11-05
modified: 2025-11-05
title: "Claude Code on Amazon Bedrock"
url: https://docs.claude.com/en/docs/claude-code/amazon-bedrock
category: docs
subcategory: claude-code
description: "Learn about configuring Claude Code through Amazon Bedrock, including setup, IAM configuration, and troubleshooting."
tags:
  - docs
  - claude-code
related:
  - '[[analytics]]'
  - '[[checkpointing]]'
  - '[[claude-code-on-the-web]]'
  - '[[cli-reference]]'
  - '[[common-workflows]]'
---

# Claude Code on Amazon Bedrock

Learn about configuring Claude Code through Amazon Bedrock, including setup, IAM configuration, and troubleshooting.

## Prerequisites

Before configuring Claude Code with Bedrock, ensure you have:

* An AWS account with Bedrock access enabled
* Access to desired Claude models (e.g., Claude Sonnet 4.5) in Bedrock
* AWS CLI installed and configured (optional - only needed if you don't have another mechanism for getting credentials)
* Appropriate IAM permissions

## Setup

### 1. Submit use case details

First-time users of Anthropic models are required to submit use case details before invoking a model. This is done once per account.

1. Ensure you have the right IAM permissions (see more on that below)
2. Navigate to the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/)
3. Select **Chat/Text playground**
4. Choose any Anthropic model and you will be prompted to fill out the use case form

### 2. Configure AWS credentials

Claude Code uses the default AWS SDK credential chain. Set up your credentials using one of these methods:

**Option A: AWS CLI configuration**

```bash  theme={null}
aws configure
```

**Option B: Environment variables (access key)**

```bash  theme={null}
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**Option C: Environment variables (SSO profile)**

```bash  theme={null}
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**Option D: Bedrock API keys**

```bash  theme={null}
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Bedrock API keys provide a simpler authentication method without needing full AWS credentials. [Learn more about Bedrock API keys](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### Advanced credential configuration

Claude Code supports automatic credential refresh for AWS SSO and corporate identity providers. Add these settings to your Claude Code settings file (see [[settings|Settings]] for file locations).

When Claude Code detects that your AWS credentials are expired (either locally based on their timestamp or when Bedrock returns a credential error), it will automatically run your configured `awsAuthRefresh` and/or `awsCredentialExport` commands to obtain new credentials before retrying the request.

##### Example configuration

```json  theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### Configuration settings explained

**`awsAuthRefresh`**: Use this for commands that modify the `.aws` directory (e.g., updating credentials, SSO cache, or config files). Output is shown to the user (but user input is not supported), making it suitable for browser-based authentication flows where the CLI displays a code to enter in the browser.

**`awsCredentialExport`**: Only use this if you cannot modify `.aws` and must directly return credentials. Output is captured silently (not shown to the user). The command must output JSON in this format:

```json  theme={null}
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value"
  }
}
```

### 3. Configure Claude Code

Set the following environment variables to enable Bedrock:

```bash  theme={null}

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/amazon-bedrock)
