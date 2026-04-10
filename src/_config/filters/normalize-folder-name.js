/**
 * Normalize a string for use in folder paths and URLs.
 * - Convert to lowercase
 * - Replace spaces and slashes with dashes
 * - Remove quotes and special characters
 *
 * e.g. "Poetry/Songs" → "poetry-songs"
 *      "Short Stories" → "short-stories"
 */
export default function normalizeFolderName(name) {
  if (!name) return 'uncategorized';
  return String(name)
    .toLowerCase()
    .replace(/[\s/]+/g, '-')  // spaces and slashes → dashes
    .replace(/['"]/g, '');     // remove quotes
}
