// Pattern: Execute Dataview Query (JS)
// Description: Runs a DataviewJS query if the plugin is available.
// Usage: Modify the 'query' variable below.

(async () => {
  if (!app.plugins.enabledPlugins.has("dataview")) {
    return { error: "Dataview plugin is not enabled" };
  }

  // Access the Dataview API
  const dv = app.plugins.plugins.dataview.api;

  try {
    // Example: Get all files with tag #task
    // Note: Dataview API returns DataArrays which need to be converted to standard JS arrays
    // for JSON serialization over CDP.

    const result = await dv.query('TABLE file.mtime as "Modified" FROM #task LIMIT 10');

    if (result.successful) {
      return {
        type: "table",
        headers: result.value.headers,
        values: result.value.values
      };
    } else {
      return { error: result.error };
    }
  } catch (e) {
    return { error: e.toString() };
  }
})();
