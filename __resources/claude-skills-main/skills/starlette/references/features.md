# Starlette 1.0 Complete Feature Reference

A comprehensive guide to all features in Starlette 1.0 (released March 22, 2026) with working code examples.

## Table of Contents

1. [What Changed in 1.0](#what-changed-in-10)
2. [Installation & Dependencies](#installation--dependencies)
3. [Application Structure](#application-structure)
4. [Routing](#routing)
5. [Requests](#requests)
6. [Responses](#responses)
7. [Cookies](#cookies)
8. [WebSockets](#websockets)
9. [Endpoints](#endpoints)
10. [Lifespan](#lifespan)
11. [Middleware](#middleware)
12. [Exception Handling](#exception-handling)
13. [Background Tasks](#background-tasks)
14. [Static Files](#static-files)
15. [Templates](#templates)
16. [Authentication](#authentication)
17. [Configuration](#configuration)
18. [Testing](#testing)
19. [OpenAPI Schemas](#openapi-schemas)
20. [Performance & Threading](#performance--threading)
21. [Data Structures](#data-structures)
22. [Complete Application Example](#complete-application-example)

---

## What Changed in 1.0

Starlette 1.0 introduces major API changes focused on clarity and type safety:

### Breaking Changes

**`on_startup` and `on_shutdown` removed**
- These decorators are deprecated in favor of the lifespan context manager
- Use `lifespan` parameter in `Starlette()` instead

```python
# OLD (no longer works)
@app.on_startup
async def startup():
    pass

# NEW
@asynccontextmanager
async def lifespan(app):
    # Startup code here
    yield
    # Shutdown code here

app = Starlette(lifespan=lifespan)
```

**SessionMiddleware state tracking**
- State is now automatically tracked in `scope["state"]` (typed as a TypedDict for safety)
- Access via `request.state.user` instead of `request.session["user"]` for non-cookie storage

**Type-safe request/response handling**
- Routes can be annotated with `Request[YourStateType]` and `WebSocket[YourStateType]`
- Enables IDE autocomplete and type checking for custom state attributes

---

## Installation & Dependencies

```bash
pip install starlette==1.0.0
```

Core dependencies:
- **Python** ≥ 3.8
- **anyio** (async I/O library)
- **httpx** (for TestClient)

Optional dependencies:
```bash
# For Jinja2 templates
pip install jinja2

# For sessions
pip install itsdangerous

# For form parsing
pip install python-multipart

# For static file serving
# (included with Starlette)

# For OpenAPI schemas
pip install pydantic

# For full async support
pip install asyncio-context-manager  # if on Python < 3.11
```

---

## Application Structure

### Basic Application

```python
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import PlainTextResponse

async def homepage(request):
    return PlainTextResponse("Hello, world!")

app = Starlette(routes=[
    Route("/", homepage),
])
```

### State Management (TypedDict Pattern)

```python
from typing import TypedDict
from starlette.applications import Starlette
from starlette.requests import Request
from contextlib import asynccontextmanager

class State(TypedDict):
    db_pool: object
    config: dict

@asynccontextmanager
async def lifespan(app):
    # Startup
    state = State(db_pool=create_db_pool(), config=load_config())
    app.state.db_pool = state["db_pool"]
    app.state.config = state["config"]
    
    yield
    
    # Shutdown
    await app.state.db_pool.close()

app = Starlette(lifespan=lifespan)

# In endpoints
async def endpoint(request: Request[State]):
    pool = request.app.state.db_pool
    config = request.app.state.config
```

---

## Routing

### Built-in Route Types

```python
from starlette.routing import Route, WebSocketRoute, Mount, Host, Router
from starlette.applications import Starlette

# HTTP Routes
Route("/users/{user_id}", endpoint, methods=["GET", "POST"], name="user_detail")

# WebSocket Routes
WebSocketRoute("/ws", endpoint)

# Mount applications or routers
Mount("/api", router)
Mount("/static", app=StaticFiles(directory="static"))

# Host-based routing
Host("example.com", app=app1),
Host("api.example.com", app=app2),
```

### Path Converters

```python
from starlette.routing import Route
from starlette.responses import JSONResponse

# Built-in convertors
# str: matches any string (default)
# int: matches positive integers
# float: matches floating-point numbers
# uuid: matches UUID4 strings
# path: matches any string including slashes

async def get_item(request):
    item_id = request.path_params["item_id"]
    return JSONResponse({"item_id": item_id})

routes = [
    Route("/items/{item_id:int}", get_item),      # /items/123
    Route("/items/{item_id:str}", get_item),      # /items/abc
    Route("/files/{file_path:path}", get_item),   # /files/dir/subdir/file.txt
]
```

### Custom Path Convertors

```python
from starlette.routing import Convertor

class DateConvertor(Convertor):
    regex = r'\d{4}-\d{2}-\d{2}'
    
    def convert(self, value):
        import datetime
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()
    
    def to_string(self, value):
        return value.strftime('%Y-%m-%d')

routes = [
    Route("/events/{event_date:date}", endpoint),  # /events/2026-03-23
]
```

### Dynamic Routing

```python
from starlette.applications import Starlette
from starlette.routing import Route, Mount, Router

# Create routers dynamically
api_router = Router(routes=[
    Route("/users", list_users),
    Route("/users/{user_id}", get_user),
])

app = Starlette(routes=[
    Mount("/api/v1", api_router),
    Mount("/api/v2", other_router),
])
```

---

## Requests

### Reading Body Data

```python
from starlette.requests import Request

async def endpoint(request: Request):
    # Raw bytes
    body = await request.body()
    
    # JSON
    json_data = await request.json()
    
    # Form data (application/x-www-form-urlencoded or multipart/form-data)
    form_data = await request.form()
    
    # Streaming (large files)
    async for chunk in request.stream():
        process_chunk(chunk)
```

### Request Properties

```python
async def endpoint(request: Request):
    method = request.method                # "GET", "POST", etc.
    url = request.url                      # Full URL as URL object
    base_url = request.base_url            # Base URL
    path = request.url.path                # "/api/users"
    query_params = request.query_params    # ImmutableMultiDict
    headers = request.headers              # ImmutableMultiDict
    cookies = request.cookies              # dict
    client_host, client_port = request.client
    content_length = request.headers.get("content-length")
    is_secure = request.url.scheme == "https"
    
    # Path parameters
    user_id = request.path_params["user_id"]
    
    # Scope (raw ASGI)
    scope = request.scope                  # Full ASGI scope dict
```

### Streaming Requests

```python
async def upload_large_file(request: Request):
    async for chunk in request.stream():
        # Process each chunk (default size: 64KB)
        process_chunk(chunk)
    
    # Or with custom chunk size
    async for chunk in request.stream(chunk_size=1024 * 1024):
        write_to_storage(chunk)
```

### File Uploads

```python
from starlette.datastructures import UploadFile

async def upload(request: Request):
    form = await request.form()
    
    # Single file
    file: UploadFile = form["file"]
    contents = await file.read()
    filename = file.filename
    content_type = file.content_type
    
    # Multiple files
    files: list[UploadFile] = form.getlist("files")
    for file in files:
        await process_file(file)
```

---

## Responses

### Response Types

```python
from starlette.responses import (
    Response,
    PlainTextResponse,
    HTMLResponse,
    JSONResponse,
    StreamingResponse,
    FileResponse,
    RedirectResponse,
)

# Plain text
return PlainTextResponse("Hello, world!")

# HTML
return HTMLResponse("<h1>Hello</h1>")

# JSON
return JSONResponse({"message": "Hello"})

# Redirect
return RedirectResponse(url="/home", status_code=302)

# File download
return FileResponse("path/to/file.pdf")

# Streaming
async def generate():
    for i in range(10):
        yield f"data: {i}\n"

return StreamingResponse(generate(), media_type="text/event-stream")

# Custom response
response = Response("Custom", status_code=201, media_type="text/plain")
```

### Setting Response Headers and Cookies

```python
from starlette.responses import JSONResponse

response = JSONResponse({"message": "Hello"})

# Headers
response.headers["X-Custom-Header"] = "value"
response.headers["Cache-Control"] = "max-age=3600"

# Cookies
response.set_cookie(
    "session_id",
    value="abc123",
    max_age=86400,           # 1 day
    path="/",
    domain=None,             # Current domain only
    secure=True,             # HTTPS only
    httponly=True,           # No JavaScript access
    samesite="lax",          # CSRF protection
)

return response
```

---

## Cookies

### Setting and Deleting Cookies

```python
from starlette.responses import Response

async def set_cookie(request):
    response = Response("Cookie set")
    response.set_cookie(
        "user_id",
        value="12345",
        max_age=604800,        # 1 week
        expires=None,          # Alternative to max_age
        path="/",
        domain=None,
        secure=True,
        httponly=True,
        samesite="strict",
    )
    return response

async def delete_cookie(request):
    response = Response("Cookie deleted")
    response.delete_cookie("user_id", path="/")
    return response

async def read_cookie(request):
    session_id = request.cookies.get("session_id")
    return JSONResponse({"session_id": session_id})
```

### Signed Cookies (Tamper-proof)

```python
from starlette.responses import Response
from itsdangerous import SignatureExpired, BadSignature

async def set_signed_cookie(request):
    response = Response("Signed cookie set")
    response.set_cookie(
        "secure_data",
        value="secret123",
        max_age=3600,
        secure=True,
        httponly=True,
    )
    return response
```

---

## WebSockets

### Basic WebSocket Handler

```python
from starlette.websockets import WebSocket

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except Exception as e:
        await websocket.close(code=1000, reason=str(e))
```

### WebSocket Operations

```python
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Receive text
    text = await websocket.receive_text()
    
    # Receive bytes
    bytes_data = await websocket.receive_bytes()
    
    # Receive JSON
    json_data = await websocket.receive_json()
    
    # Send text
    await websocket.send_text("Hello")
    
    # Send bytes
    await websocket.send_bytes(b"Hello")
    
    # Send JSON
    await websocket.send_json({"message": "Hello"})
    
    # Close connection
    await websocket.close(code=1000, reason="Normal closure")
```

### Iterating Over Messages

```python
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Iterate over text messages
    async for text in websocket.iter_text():
        await websocket.send_text(f"Echo: {text}")
    
    # Iterate over JSON messages
    async for json_data in websocket.iter_json():
        await websocket.send_json({"received": json_data})
```

### Rejecting WebSocket Connections

```python
async def websocket_endpoint(websocket: WebSocket):
    # Check authorization
    token = websocket.query_params.get("token")
    if not is_valid_token(token):
        await websocket.close(code=1008, reason="Invalid token")
        return
    
    await websocket.accept()
    # ... handle connection
```

### Broadcasting to Multiple Clients

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message: {data}")
    except Exception:
        manager.disconnect(websocket)
```

---

## Endpoints

### Class-Based HTTP Endpoints

```python
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

class UserEndpoint(HTTPEndpoint):
    async def get(self, request):
        user_id = request.path_params["user_id"]
        return JSONResponse({"user_id": user_id})
    
    async def post(self, request):
        data = await request.json()
        # Create user
        return JSONResponse({"created": True}, status_code=201)
    
    async def put(self, request):
        data = await request.json()
        # Update user
        return JSONResponse({"updated": True})
    
    async def delete(self, request):
        # Delete user
        return JSONResponse({"deleted": True}, status_code=204)

# Route registration
routes = [
    Route("/users/{user_id}", UserEndpoint),
]
```

### Class-Based WebSocket Endpoints

```python
from starlette.endpoints import WebSocketEndpoint

class ChatEndpoint(WebSocketEndpoint):
    encoding = "text"  # or "bytes" or "json"
    
    async def on_receive(self, websocket, data):
        await websocket.send_text(f"Echo: {data}")
    
    async def on_connect(self, websocket):
        await websocket.accept()
        print("Client connected")
    
    async def on_disconnect(self, websocket):
        print("Client disconnected")

# Route registration
routes = [
    WebSocketRoute("/chat", ChatEndpoint),
]
```

---

## Lifespan

### Context Manager Pattern

```python
from contextlib import asynccontextmanager
from starlette.applications import Starlette
from typing import TypedDict

class AppState(TypedDict):
    db: object
    cache: object

@asynccontextmanager
async def lifespan(app):
    # Startup
    db = await create_database_connection()
    cache = await create_cache_connection()
    
    app.state.db = db
    app.state.cache = cache
    
    print("Application started")
    
    yield  # Application runs here
    
    # Shutdown
    await db.close()
    await cache.close()
    
    print("Application shutdown")

app = Starlette(lifespan=lifespan)
```

### Type-Safe State Access

```python
from typing import TypedDict
from starlette.requests import Request

class AppState(TypedDict):
    db: DatabaseConnection
    config: dict
    logger: Logger

async def endpoint(request: Request[AppState]):
    db = request.app.state.db      # Type-safe access
    config = request.app.state.config
    logger = request.app.state.logger
    
    # IDE autocomplete and type checking work here
```

### Lifespan Events in Mount/Router

```python
from starlette.routing import Mount, Router

@asynccontextmanager
async def api_lifespan(app):
    print("API startup")
    yield
    print("API shutdown")

api_router = Router(
    routes=[...],
    on_startup=[],  # Deprecated, use lifespan
)

mounted = Mount("/api", api_router)
```

---

## Middleware

### CORS Middleware

```python
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware

app = Starlette()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com", "https://app.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],
    max_age=600,
)
```

### Session Middleware

```python
from starlette.middleware.sessions import SessionMiddleware

app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# In endpoint
async def login(request):
    request.session["user_id"] = 123
    return JSONResponse({"status": "logged in"})

async def get_user(request):
    user_id = request.session.get("user_id")
    return JSONResponse({"user_id": user_id})
```

### HTTPS Redirect Middleware

```python
from starlette.middleware.https import HTTPSRedirectMiddleware

app.add_middleware(HTTPSRedirectMiddleware)
# All HTTP requests redirect to HTTPS
```

### Trusted Host Middleware

```python
from starlette.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"],
)
```

### GZip Middleware

```python
from starlette.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
# Responses >= 1000 bytes are gzipped
```

### Custom Pure ASGI Middleware

```python
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from starlette.datastructures import MutableHeaders

async def custom_middleware(app: ASGIApp, scope: Scope, receive: Receive, send: Send) -> None:
    if scope["type"] == "http":
        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(raw=message["headers"])
                headers["X-Custom-Header"] = "value"
            await send(message)
        
        await app(scope, receive, send_wrapper)
    else:
        await app(scope, receive, send)

app = Starlette(middleware=[Middleware(custom_middleware)])
```

### BaseHTTPMiddleware Pattern

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        import time
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        return response

app.add_middleware(TimingMiddleware)
```

### Middleware Ordering

```python
# Add in reverse order (last added = innermost)
app.add_middleware(GZipMiddleware)              # Applied third
app.add_middleware(CORSMiddleware, ...)         # Applied second
app.add_middleware(SessionMiddleware, ...)      # Applied first
# Routes are at the center
```

---

## Exception Handling

### HTTPException

```python
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

async def endpoint(request):
    if not is_authenticated(request):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if not has_permission(request):
        raise HTTPException(status_code=403, detail="Forbidden")
    
    if resource_not_found():
        raise HTTPException(status_code=404, detail="Not found")
    
    return JSONResponse({"status": "ok"})
```

### Custom Exception Handlers

```python
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse

class CustomException(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message

async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        {"error_code": exc.code, "detail": exc.message},
        status_code=400,
    )

app = Starlette(
    exception_handlers={
        CustomException: custom_exception_handler,
    }
)

# In endpoint
async def endpoint(request):
    if invalid_data():
        raise CustomException("INVALID_DATA", "The provided data is invalid")
    return JSONResponse({"status": "ok"})
```

### WebSocket Exception Handling

```python
from starlette.exceptions import WebSocketException

async def websocket_endpoint(websocket: WebSocket):
    try:
        token = websocket.query_params.get("token")
        if not validate_token(token):
            raise WebSocketException(code=1008, reason="Invalid token")
        
        await websocket.accept()
        
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    
    except WebSocketException as e:
        await websocket.close(code=e.code, reason=e.reason)
    except Exception as e:
        await websocket.close(code=1011, reason="Internal error")
```

### Global Exception Handler

```python
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse

async def exception_handler(request: Request, exc: Exception):
    # Log exception
    import traceback
    traceback.print_exc()
    
    return JSONResponse(
        {"detail": "Internal server error"},
        status_code=500,
    )

app = Starlette(
    exception_handlers={Exception: exception_handler}
)
```

---

## Background Tasks

### Single Background Task

```python
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse

def send_email(email: str, message: str):
    # Simulate email sending
    import time
    time.sleep(2)
    print(f"Email sent to {email}: {message}")

async def endpoint(request):
    task = BackgroundTask(send_email, "user@example.com", "Hello")
    return JSONResponse(
        {"status": "processing"},
        background=task
    )
```

### Multiple Background Tasks

```python
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse

def log_message(message: str):
    print(f"Log: {message}")

def send_notification(message: str):
    print(f"Notification: {message}")

async def endpoint(request):
    tasks = BackgroundTasks()
    tasks.add_task(log_message, "User action")
    tasks.add_task(send_notification, "Action completed")
    
    return JSONResponse(
        {"status": "success"},
        background=tasks
    )
```

### Async Background Tasks

```python
async def async_send_email(email: str):
    # Async operation
    await asyncio.sleep(2)
    print(f"Email sent to {email}")

async def endpoint(request):
    tasks = BackgroundTasks()
    tasks.add_task(async_send_email, "user@example.com")
    return JSONResponse({"status": "ok"}, background=tasks)
```

---

## Static Files

### Serving Static Files

```python
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

app = Starlette(routes=[
    Mount("/static", app=StaticFiles(directory="static"), name="static"),
])

# Directory structure:
# static/
#   css/
#     style.css
#   js/
#     app.js
#   images/
#     logo.png
```

### URL Reversal for Static Files

```python
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import HTMLResponse

async def homepage(request):
    # Generate URL for static file
    static_url = request.url_for("static", path="css/style.css")
    
    html = f"""
    <html>
        <link rel="stylesheet" href="{static_url}">
    </html>
    """
    return HTMLResponse(html)

app = Starlette(routes=[
    Route("/", homepage),
    Mount("/static", app=StaticFiles(directory="static"), name="static"),
])
```

### StaticFiles with HTML5 History API

```python
from starlette.staticfiles import StaticFiles

# Single page application
app = StaticFiles(
    directory="static",
    html=True,  # Serve index.html for missing routes
    check_dir=True,
)
```

---

## Templates

### Jinja2 Templates

```python
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

async def homepage(request):
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "title": "Home"}
    )

app = Starlette(routes=[
    Route("/", homepage),
])

# templates/home.html
# <h1>{{ title }}</h1>
```

### Custom Filters

```python
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

# Add custom filter
templates.env.filters["uppercase"] = lambda s: s.upper()

# In template: {{ name|uppercase }}
```

### Custom Context Processors

```python
from datetime import datetime
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

# Add globals
templates.env.globals["year"] = datetime.now().year

# In template: <footer>&copy; {{ year }}</footer>
```

### Template Inheritance

```python
# templates/base.html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Default{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

# templates/page.html
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
<h1>Page Content</h1>
{% endblock %}
```

---

## Authentication

### Basic Authentication Middleware

```python
from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, AuthCredentials
)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request
import base64

class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return AuthCredentials([]), SimpleUser("anonymous")
        
        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != "basic":
                return AuthCredentials([]), SimpleUser("anonymous")
            
            decoded = base64.b64decode(credentials).decode("utf-8")
            username, password = decoded.split(":", 1)
            
            if validate_credentials(username, password):
                return AuthCredentials(["authenticated"]), SimpleUser(username)
            else:
                raise AuthenticationError("Invalid credentials")
        except Exception:
            raise AuthenticationError("Invalid auth header")

app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
```

### Token Authentication

```python
from starlette.authentication import AuthenticationBackend, AuthCredentials, SimpleUser, AuthenticationError

class TokenAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return AuthCredentials([]), SimpleUser("anonymous")
        
        auth = request.headers["Authorization"]
        try:
            scheme, token = auth.split()
            if scheme.lower() != "bearer":
                return AuthCredentials([]), SimpleUser("anonymous")
            
            user_id = validate_token(token)
            if user_id:
                return AuthCredentials(["authenticated"]), SimpleUser(user_id)
            else:
                raise AuthenticationError("Invalid token")
        except Exception:
            raise AuthenticationError("Invalid auth header")

app.add_middleware(AuthenticationMiddleware, backend=TokenAuthBackend())
```

### @requires Decorator

```python
from starlette.authentication import requires
from starlette.responses import JSONResponse

@requires("authenticated")
async def protected_endpoint(request):
    return JSONResponse({"user": request.user.username})

# Accessing the user
async def endpoint(request):
    if request.user.is_authenticated:
        return JSONResponse({"user": request.user.username})
    else:
        return JSONResponse({"error": "Not authenticated"}, status_code=401)
```

---

## Configuration

### Configuration Class

```python
from starlette.config import Config

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config("DATABASE_URL")
SECRET_KEY = config("SECRET_KEY")
```

### Environment Variables

```bash
# .env
DEBUG=true
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=your-secret-key-here
```

### Secret Values

```python
from starlette.datastructures import Secret

SECRET_KEY = Secret(config("SECRET_KEY"))

# Secret values are masked in logs and repr
print(repr(SECRET_KEY))  # Secret('***')
```

### Pydantic Settings (Alternative)

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    database_url: str
    secret_key: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## Testing

### TestClient Basic Usage

```python
from starlette.testclient import TestClient
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def homepage(request):
    return JSONResponse({"message": "Hello"})

app = Starlette(routes=[
    Route("/", homepage),
])

client = TestClient(app)
response = client.get("/")
assert response.status_code == 200
assert response.json() == {"message": "Hello"}
```

### Testing with Lifespan

```python
from starlette.testclient import TestClient
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    # Startup
    app.state.db = setup_test_db()
    yield
    # Shutdown
    teardown_test_db(app.state.db)

client = TestClient(app, base_url="http://testserver")
# Lifespan runs automatically with TestClient
response = client.get("/")
```

### WebSocket Testing

```python
from starlette.testclient import TestClient

client = TestClient(app)

with client.websocket_connect("/ws") as websocket:
    data = websocket.receive_text()
    assert data == "Hello"
    
    websocket.send_text("Hello back")
    data = websocket.receive_text()
    assert data == "Echo: Hello back"
```

### Async Testing with httpx

```python
import httpx
import asyncio
from starlette.applications import Starlette

app = Starlette()

async def test_app():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200

asyncio.run(test_app())
```

### Testing Form Data

```python
client = TestClient(app)

response = client.post(
    "/upload",
    data={"field": "value"},
    files={"file": ("filename.txt", b"file content")},
)

assert response.status_code == 200
```

---

## OpenAPI Schemas

### Schema Generation

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.schemas import SchemaGenerator

schemas = SchemaGenerator(
    title="My API",
    version="1.0.0",
    description="API documentation",
)

async def list_items(request):
    """
    Get all items.
    
    responses:
      200:
        description: List of items
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
    """
    return JSONResponse([{"id": 1, "name": "Item 1"}])

routes = [
    Route("/items", list_items),
    Route("/schema", lambda request: schemas.OpenAPIResponse(request)),
]

app = Starlette(routes=routes)
```

### Pydantic Models in Schemas

```python
from pydantic import BaseModel
from starlette.responses import JSONResponse

class Item(BaseModel):
    id: int
    name: str
    price: float

async def create_item(request):
    """
    Create a new item.
    
    responses:
      201:
        description: Created item
        content:
          application/json:
            schema: Item
    """
    data = await request.json()
    item = Item(**data)
    return JSONResponse(item.dict(), status_code=201)
```

---

## Performance & Threading

### Thread Pool Configuration

```python
from starlette.applications import Starlette
import concurrent.futures

# Custom thread pool
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

async def cpu_heavy(request):
    # Run sync code in thread pool
    result = await asyncio.get_event_loop().run_in_executor(
        executor, heavy_computation
    )
    return JSONResponse({"result": result})

def heavy_computation():
    # CPU-intensive work
    total = sum(i**2 for i in range(1_000_000))
    return total
```

### Async Endpoints

```python
async def async_endpoint(request):
    # All async operations
    data = await fetch_data()
    processed = await process_data(data)
    return JSONResponse(processed)

async def fetch_data():
    # Async I/O
    await asyncio.sleep(0.1)
    return {"data": "example"}

async def process_data(data):
    await asyncio.sleep(0.1)
    return data
```

### Sync Endpoints (Auto Thread Pool)

```python
def sync_endpoint(request):
    # Sync code automatically runs in thread pool
    data = fetch_data_sync()
    return JSONResponse(data)

def fetch_data_sync():
    import time
    time.sleep(0.1)
    return {"data": "example"}
```

---

## Data Structures

### URL Object

```python
from starlette.datastructures import URL

url = request.url
print(url.scheme)          # "https"
print(url.netloc)          # "example.com:8000"
print(url.path)            # "/api/users"
print(url.query)           # "page=2&limit=10"
print(url.fragment)        # "section"

# Build URL
new_url = url.replace(query="page=3")
```

### Headers

```python
from starlette.datastructures import Headers, MutableHeaders

# Immutable (from request)
headers = request.headers
content_type = headers["content-type"]
accept_all = headers.getlist("accept")

# Mutable (for response)
response_headers = MutableHeaders()
response_headers["X-Custom"] = "value"
response_headers.add_vary_header("Accept-Encoding")
```

### QueryParams

```python
from starlette.datastructures import QueryParams

params = request.query_params
page = params.get("page", "1")
tags = params.getlist("tags")

# Immutable
print(params["search"])
```

### Secret

```python
from starlette.datastructures import Secret

api_key = Secret("sk_live_abc123")
print(repr(api_key))  # Secret('***')
print(str(api_key))   # Won't work directly for security

# To use the value
actual_value = str(api_key)
```

### State

```python
from starlette.datastructures import State

# Create state
state = State()
state.user_id = 123
state.settings = {"debug": True}

# Access
user_id = state.user_id
settings = state.settings
```

---

## Complete Application Example

```python
from contextlib import asynccontextmanager
from typing import TypedDict

from starlette.applications import Starlette
from starlette.authentication import (
    AuthenticationBackend, AuthCredentials, SimpleUser, AuthenticationError
)
from starlette.background import BackgroundTasks
from starlette.datastructures import Secret
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocket

# Type-safe state
class AppState(TypedDict):
    db: object
    cache: object

# Authentication
class TokenAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return AuthCredentials([]), SimpleUser("anonymous")
        
        auth = request.headers["Authorization"]
        try:
            scheme, token = auth.split()
            if scheme.lower() != "bearer":
                return AuthCredentials([]), SimpleUser("anonymous")
            
            # Validate token
            if token == "valid_token":
                return AuthCredentials(["authenticated"]), SimpleUser("user123")
            else:
                raise AuthenticationError("Invalid token")
        except Exception:
            raise AuthenticationError("Invalid auth header")

# Lifespan
@asynccontextmanager
async def lifespan(app):
    # Startup
    print("Starting up...")
    app.state.db = {"connection": "mock_db"}
    app.state.cache = {"connection": "mock_cache"}
    
    yield
    
    # Shutdown
    print("Shutting down...")

# Routes
async def homepage(request: Request[AppState]):
    return JSONResponse({"message": "Welcome"})

async def list_items(request: Request[AppState]):
    return JSONResponse([
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"},
    ])

class ItemEndpoint(HTTPEndpoint):
    async def get(self, request: Request[AppState]):
        item_id = request.path_params["item_id"]
        # Get from database
        return JSONResponse({"id": item_id, "name": "Item"})
    
    async def put(self, request: Request[AppState]):
        item_id = request.path_params["item_id"]
        data = await request.json()
        # Update in database
        return JSONResponse({"id": item_id, "updated": True})
    
    async def delete(self, request: Request[AppState]):
        item_id = request.path_params["item_id"]
        # Delete from database
        return JSONResponse(status_code=204)

async def create_item(request: Request[AppState]):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    data = await request.json()
    
    # Background task
    tasks = BackgroundTasks()
    tasks.add_task(send_notification, f"New item: {data['name']}")
    
    return JSONResponse(
        {"id": 3, "name": data["name"], "created": True},
        status_code=201,
        background=tasks
    )

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except Exception:
        await websocket.close(code=1000)

def send_notification(message: str):
    print(f"Notification: {message}")

# Routes
routes = [
    Route("/", homepage),
    Route("/items", list_items, methods=["GET"]),
    Route("/items", create_item, methods=["POST"]),
    Route("/items/{item_id}", ItemEndpoint),
    Route("/ws", websocket_endpoint, name="websocket"),
]

# Create app
app = Starlette(
    routes=routes,
    lifespan=lifespan,
)

# Middleware
app.add_middleware(AuthenticationMiddleware, backend=TokenAuthBackend())
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (optional)
# app = Mount("/static", app=StaticFiles(directory="static"))

# Usage
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

---

## Summary

Starlette 1.0 provides a modern, type-safe foundation for building ASGI applications:

- **Lifespan**: Use context managers instead of on_startup/on_shutdown
- **Type Safety**: Leverage TypedDict for state and Request[State] annotations
- **Middleware**: Choose between pure ASGI or BaseHTTPMiddleware depending on needs
- **WebSockets**: Full support with connection management and broadcasting patterns
- **Testing**: TestClient and async httpx support for comprehensive testing
- **Performance**: Automatic thread pool for sync endpoints, full async support available

For production applications, pair Starlette with Uvicorn for ASGI serving and add monitoring, logging, and error tracking as needed.
