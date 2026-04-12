// Pattern: Batch Frontmatter Operations
// Description: Update frontmatter across multiple files matching a pattern
// Usage: Run via obsidian_eval or adapt for SDK

/**
 * Batch update frontmatter for files matching a query
 * @param {string} folderPath - Folder to process (e.g., "SAQ/")
 * @param {string} key - Frontmatter key to set
 * @param {any} value - Value to set (will be JSON stringified)
 * @param {Object} options - Additional options
 */
async function batchUpdateFrontmatter(folderPath, key, value, options = {}) {
    const {
        dryRun = true,
        filter = () => true,
        extension = 'md'
    } = options;

    const files = app.vault.getFiles()
        .filter(f => f.path.startsWith(folderPath))
        .filter(f => f.extension === extension)
        .filter(filter);

    const results = {
        total: files.length,
        updated: 0,
        skipped: 0,
        errors: []
    };

    for (const file of files) {
        try {
            await app.fileManager.processFrontMatter(file, (fm) => {
                if (dryRun) {
                    console.log(`[DRY RUN] Would set ${key}=${JSON.stringify(value)} in ${file.path}`);
                    results.skipped++;
                } else {
                    fm[key] = value;
                    results.updated++;
                }
            });
        } catch (e) {
            results.errors.push({ file: file.path, error: e.message });
        }
    }

    return results;
}

/**
 * Add tags to files based on folder structure
 * @param {string} basePath - Base folder path
 */
async function tagsByFolder(basePath, options = { dryRun: true }) {
    const files = app.vault.getFiles()
        .filter(f => f.path.startsWith(basePath) && f.extension === 'md');

    for (const file of files) {
        const relativePath = file.path.replace(basePath, '');
        const folders = relativePath.split('/').slice(0, -1);
        const tags = folders.map(f => `#${f.toLowerCase().replace(/\s+/g, '-')}`);

        if (tags.length > 0) {
            await app.fileManager.processFrontMatter(file, (fm) => {
                if (options.dryRun) {
                    console.log(`[DRY RUN] Would add tags ${tags.join(', ')} to ${file.path}`);
                } else {
                    fm.tags = [...new Set([...(fm.tags || []), ...tags])];
                }
            });
        }
    }
}

/**
 * Migrate related.* fields to breadcrumbs fields
 * @param {string} folderPath - Folder to process
 */
async function migrateToBreadcrumbs(folderPath, options = { dryRun: true }) {
    const mapping = {
        'related.concepts': 'concept_direct',
        'related.prerequisites': 'concept_prerequisite',
        'related.mechanisms': 'concept_mechanism',
        'related.saqs': 'saq_direct',
        'related.los': 'lo_direct'
    };

    const files = app.vault.getFiles()
        .filter(f => f.path.startsWith(folderPath) && f.extension === 'md');

    const results = { migrated: 0, skipped: 0 };

    for (const file of files) {
        await app.fileManager.processFrontMatter(file, (fm) => {
            let changed = false;

            for (const [oldKey, newKey] of Object.entries(mapping)) {
                const [parent, child] = oldKey.split('.');
                if (fm[parent]?.[child] && !fm[newKey]) {
                    if (options.dryRun) {
                        console.log(`[DRY RUN] ${file.path}: ${oldKey} → ${newKey}`);
                    } else {
                        fm[newKey] = fm[parent][child];
                        changed = true;
                    }
                }
            }

            if (changed) results.migrated++;
            else results.skipped++;
        });
    }

    return results;
}

/**
 * Validate frontmatter against schema
 * @param {string} folderPath - Folder to validate
 * @param {Object} schema - Expected fields and types
 */
async function validateFrontmatter(folderPath, schema) {
    const files = app.vault.getFiles()
        .filter(f => f.path.startsWith(folderPath) && f.extension === 'md');

    const issues = [];

    for (const file of files) {
        const cache = app.metadataCache.getFileCache(file);
        const fm = cache?.frontmatter || {};

        for (const [field, config] of Object.entries(schema)) {
            const { required, type, validate } = config;

            if (required && !(field in fm)) {
                issues.push({ file: file.path, field, issue: 'missing' });
            } else if (field in fm) {
                const value = fm[field];
                const actualType = Array.isArray(value) ? 'array' : typeof value;

                if (type && actualType !== type) {
                    issues.push({
                        file: file.path,
                        field,
                        issue: `type mismatch: expected ${type}, got ${actualType}`
                    });
                }

                if (validate && !validate(value)) {
                    issues.push({ file: file.path, field, issue: 'validation failed' });
                }
            }
        }
    }

    return issues;
}

/**
 * Generate frontmatter report
 * @param {string} folderPath - Folder to analyze
 */
async function frontmatterReport(folderPath) {
    const files = app.vault.getFiles()
        .filter(f => f.path.startsWith(folderPath) && f.extension === 'md');

    const fieldCounts = {};
    const fieldValues = {};

    for (const file of files) {
        const cache = app.metadataCache.getFileCache(file);
        const fm = cache?.frontmatter || {};

        for (const [key, value] of Object.entries(fm)) {
            fieldCounts[key] = (fieldCounts[key] || 0) + 1;

            if (!fieldValues[key]) fieldValues[key] = new Set();
            if (typeof value === 'string' || typeof value === 'number') {
                fieldValues[key].add(value);
            } else if (Array.isArray(value)) {
                value.forEach(v => fieldValues[key].add(String(v)));
            }
        }
    }

    return {
        totalFiles: files.length,
        fields: Object.entries(fieldCounts).map(([field, count]) => ({
            field,
            count,
            coverage: `${((count / files.length) * 100).toFixed(1)}%`,
            uniqueValues: fieldValues[field]?.size || 0
        })).sort((a, b) => b.count - a.count)
    };
}

// Export for use
return {
    batchUpdateFrontmatter,
    tagsByFolder,
    migrateToBreadcrumbs,
    validateFrontmatter,
    frontmatterReport
};
