// Pattern: Extract Theme Variables
// Description: Dumps all CSS variables starting with -- from the body styles.
// Usage: Run via obsidian_eval

(() => {
  const styles = getComputedStyle(document.body);
  const variables = {};

  // Iterate through all properties
  for (let i = 0; i < styles.length; i++) {
    const prop = styles[i];
    if (prop.startsWith('--')) {
      variables[prop] = styles.getPropertyValue(prop).trim();
    }
  }

  return variables;
})();
