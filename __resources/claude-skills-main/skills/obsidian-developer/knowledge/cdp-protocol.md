# Chrome DevTools Protocol (CDP) for Obsidian

## Overview
Obsidian runs on Electron, which allows automation via the Chrome DevTools Protocol. The MCP server wraps `Runtime.evaluate` to execute code within the Obsidian window context.

## Execution Context
Code sent to `obsidian_eval` runs in the context of the main window (Renderer process).
- **Global Object**: `window` (and `app` is a property of `window`).
- **Isolation**: The MCP server wraps your code in a closure to prevent access to Node.js primitives (`require`, `process`) for security.

## Handling Return Values
CDP `Runtime.evaluate` can return results in two ways:

1.  **By Value (`returnByValue: true`)**
    - The object is JSON-serialized and sent back over the WebSocket.
    - **Use for**: Primitives (strings, numbers, booleans), simple arrays, and POJOs (Plain Old JavaScript Objects).
    - **Limit**: Circular references will throw errors. Large objects may impact performance.

2.  **By Reference (`returnByValue: false`)**
    - Returns a `RemoteObject` ID (pointer).
    - **Use for**: Complex Obsidian objects (`TFile`, `App`, DOM Elements) that cannot be serialized.
    - **MCP Behavior**: The current `obsidian_eval` tool defaults to `returnByValue: true` for convenience. If you need to manipulate a complex object, do it *inside* the JavaScript expression and return a simplified result.

    **Bad (Circular Error):**
    ```javascript
    // TFile contains circular references to parent folders
    app.workspace.getActiveFile()
    ```

    **Good (Serializable):**
    ```javascript
    const f = app.workspace.getActiveFile();
    ({ path: f.path, name: f.name, stat: f.stat })
    ```

## `awaitPromise`
The MCP tool sets `awaitPromise: true`.
- If your expression returns a Promise, CDP waits for it to resolve.
- You can use top-level `await` inside the string if you wrap it or if the runtime supports it, but the safest pattern is to return the promise chain.

**Example:**
```javascript
// This works because awaitPromise is true
app.vault.read(app.workspace.getActiveFile())
```

## Console Logs
`Runtime.consoleAPICalled` events capture `console.log` from the Obsidian app.
- This is useful for debugging plugins or scripts running inside Obsidian.
- The `obsidian_read_console` tool fetches these buffered logs.
