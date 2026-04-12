---
name: godmode-databases
description: Query SQLite, PostgreSQL, MySQL, and Redis via GODMODE MCP. Execute SQL with parameterized args, list tables, and perform Redis operations (GET/SET/HGET/LPUSH/etc). Tools — sqlite_query, sqlite_tables, postgres_query, mysql_query, redis_ops.
allowed-tools: Read, Bash
---

# Godmode Databases

Database tools via GODMODE MCP.

## Tools

| Tool | Args | Description |
|------|------|-------------|
| `sqlite_query` | `database`, `query`, `params?` | Execute SQLite query |
| `sqlite_tables` | `database` | List all tables |
| `postgres_query` | `connection_string`, `query`, `params?` | PostgreSQL query |
| `mysql_query` | `host`, `user`, `password`, `database`, `query` | MySQL query |
| `redis_ops` | `operation`, `key`, `value?`, `field?` | Redis: GET, SET, DEL, KEYS, HGET, HSET, LPUSH, RPUSH, LRANGE, EXPIRE, TTL, EXISTS, INCR, DECR |
