// Pattern: Audit Plugin Usage
// Description: Lists all enabled plugins, their versions, and descriptions.
// Usage: Run via obsidian_eval

(() => {
  const plugins = app.plugins.manifests;
  const enabled = Array.from(app.plugins.enabledPlugins);

  return enabled.map(id => {
    const manifest = plugins[id] || {};
    return {
      id: id,
      name: manifest.name || id,
      version: manifest.version || 'unknown',
      author: manifest.author || 'unknown',
      description: manifest.description || ''
    };
  });
})();
