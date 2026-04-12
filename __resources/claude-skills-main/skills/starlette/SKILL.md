---
name: starlette
description: >
  Starlette 1.0 ASGI framework reference with working code examples for every feature.
  Use this skill whenever writing Starlette applications, building ASGI middleware,
  working with FastAPI internals, or writing async Python web services. Also trigger
  when the user mentions Starlette, ASGI, or needs help with routing, WebSockets,
  middleware, lifespan handlers, or test clients in the Starlette ecosystem — even
  if they don't name Starlette explicitly but are clearly working with it (e.g.,
  importing from starlette.*, using TestClient with httpx, or writing ASGI scope/
  receive/send functions). Covers the 1.0 API exclusively — all deprecated 0.x
  patterns have been removed.
---

# Starlette 1.0 — Skill Reference

Starlette 1.0 shipped March 22, 2026. It is the lightweight ASGI framework behind FastAPI, the Python MCP SDK, and most of the modern async Python web stack. The only hard dependency is `anyio`.

```shell
pip install starlette
pip install uvicorn                # ASGI server
pip install starlette[full]        # httpx, jinja2, python-multipart, itsdangerous, pyyaml
```

## What changed in 1.0

The 1.0 release removed all previously deprecated APIs and locked in the modern patterns from 0.x. If you're upgrading or referencing old tutorials, these are the breaks:

1. **`on_startup` / `on_shutdown` removed.** Use `lifespan` — an async context manager passed to `Starlette(lifespan=...)`. Setup goes before `yield`, teardown goes after.
2. **Decorator-style route/middleware registration removed.** Pass `routes=` and `middleware=` as explicit lists to the `Starlette` constructor. No more `@app.route(...)`.
3. **Old `TemplateResponse(name, context)` signature removed.** The new signature is `TemplateResponse(request, name, context=...)` — request is the first positional arg.
4. **`SessionMiddleware` now tracks access.** `request.session.is_loaded` and `request.session.is_modified` are available for conditional persistence logic.
5. **Typed state generic extended to WebSocket.** `WebSocket[AppState]` gives typed access to `websocket.state` the same way `Request[AppState]` does.

## Feature index

The full feature reference with code examples lives in `references/features.md`. It covers 20 sections:

| # | Section | What it covers |
|---|---------|---------------|
| 1 | Application | `Starlette` class, combining routes/middleware/lifespan |
| 2 | Routing | `Route`, `Mount`, `WebSocketRoute`, path params, converters |
| 3 | Requests | Method, URL, headers, query params, body, form, uploads, streaming |
| 4 | Responses | Plain, HTML, JSON, Redirect, Streaming, File, custom |
| 5 | WebSockets | Accept, send, receive, close, iteration, typed state |
| 6 | Endpoints | Class-based HTTP and WebSocket endpoints |
| 7 | Lifespan | Async context manager pattern (replaced startup/shutdown) |
| 8 | Middleware | CORS, Sessions, TrustedHost, HTTPS redirect, GZip, BaseHTTPMiddleware, pure ASGI |
| 9 | Exception Handling | `HTTPException`, custom handlers |
| 10 | Background Tasks | Attaching work to responses |
| 11 | Static Files | `StaticFiles`, `html=True` mode |
| 12 | Templates | Jinja2, new `TemplateResponse` signature |
| 13 | Authentication | `AuthenticationMiddleware`, custom backends, `requires`, scopes |
| 14 | Configuration | `Config`, `environ`, `.env` files |
| 15 | Test Client | `TestClient` (httpx-based), async testing |
| 16 | Schema Generation | OpenAPI extraction |
| 17 | Thread Pool | `run_in_threadpool` for sync functions |
| 18 | Data Structures | `State`, `URL`, `Headers`, `QueryParams`, `MutableHeaders` |
| 19 | ASGI Types | Raw `Scope`, `Receive`, `Send` |
| 20 | Complete App | Full working application tying everything together |

When answering a question about a specific feature, read the corresponding section from `references/features.md` rather than guessing. The code examples there are verified against the 1.0 release.

## Quick patterns

### Minimal app

```python
from contextlib import asynccontextmanager
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route

@asynccontextmanager
async def lifespan(app):
    print("Starting up")
    yield
    print("Shutting down")

def homepage(request):
    return PlainTextResponse("Hello, world!")

app = Starlette(routes=[Route("/", homepage)], lifespan=lifespan)
```

### Route with path parameters

```python
from starlette.routing import Route
from starlette.responses import JSONResponse

async def get_item(request):
    item_id = request.path_params["item_id"]
    return JSONResponse({"item_id": item_id})

routes = [Route("/items/{item_id:int}", get_item)]
```

### Middleware stack

```python
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"]),
    Middleware(SessionMiddleware, secret_key="your-secret"),
]

app = Starlette(routes=routes, middleware=middleware, lifespan=lifespan)
```

### WebSocket

```python
from starlette.routing import WebSocketRoute

async def ws_echo(websocket):
    await websocket.accept()
    async for message in websocket.iter_text():
        await websocket.send_text(f"Echo: {message}")

routes = [WebSocketRoute("/ws", ws_echo)]
```

### Testing

```python
from starlette.testclient import TestClient

client = TestClient(app)
response = client.get("/")
assert response.status_code == 200
assert response.text == "Hello, world!"
```

## Common mistakes to catch

- Using `@app.route()` or `@app.middleware()` decorators — removed in 1.0.
- Using `on_startup`/`on_shutdown` lists — removed in 1.0, use `lifespan`.
- Old `TemplateResponse("index.html", {"request": request})` — first arg is now `request`.
- Forgetting `await websocket.accept()` before sending.
- Passing `debug=True` in production — it serves tracebacks to clients.
