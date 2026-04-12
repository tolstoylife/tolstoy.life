---
name: dead-letter-queue
description: Design dead letter queues for failed message processing. Handle poison messages, implement retry policies, and build alerting for DLQ accumulation across RabbitMQ, SQS, and Kafka.
---

# dead letter queue

Design dead letter queues for failed message processing. Handle poison messages, implement retry policies, and build alerting for DLQ accumulation across RabbitMQ, SQS, and Kafka.

## When to Use

- Designing or implementing dead letter queue in your application
- Reviewing existing implementation for best practices
- Troubleshooting issues related to dead letter queue

## Workflow

1. **Assess** — Understand the current architecture and requirements
2. **Design** — Choose the right pattern for the use case
3. **Implement** — Write the code with proper error handling
4. **Test** — Verify behavior under normal and failure conditions
5. **Monitor** — Set up metrics and alerting for production
