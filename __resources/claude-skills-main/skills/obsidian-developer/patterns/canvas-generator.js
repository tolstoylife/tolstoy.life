// Pattern: Canvas Generator
// Description: Generate canvas files from vault data structures
// Usage: Run via obsidian_eval or adapt for SDK

/**
 * Generate a concept map canvas from a note's links
 * @param {string} sourcePath - Path to the source note
 * @param {string} outputPath - Path for the output canvas
 */
async function createConceptMap(sourcePath, outputPath) {
    const sourceFile = app.vault.getAbstractFileByPath(sourcePath);
    if (!sourceFile) throw new Error(`Source not found: ${sourcePath}`);

    const cache = app.metadataCache.getFileCache(sourceFile);
    const links = cache?.links || [];

    // Center node
    const nodes = [{
        id: 'source',
        type: 'file',
        file: sourcePath,
        x: 0,
        y: 0,
        width: 400,
        height: 300
    }];

    const edges = [];
    const radius = 500;
    const angleStep = (2 * Math.PI) / Math.max(links.length, 1);

    links.forEach((link, i) => {
        const angle = i * angleStep;
        const x = radius * Math.cos(angle);
        const y = radius * Math.sin(angle);

        const nodeId = `link-${i}`;
        const targetPath = app.metadataCache.getFirstLinkpathDest(link.link, sourcePath)?.path;

        nodes.push({
            id: nodeId,
            type: targetPath ? 'file' : 'text',
            file: targetPath,
            text: targetPath ? undefined : `[[${link.link}]]`,
            x: x,
            y: y,
            width: 300,
            height: 200
        });

        edges.push({
            id: `edge-${i}`,
            fromNode: 'source',
            fromSide: x > 0 ? 'right' : 'left',
            toNode: nodeId,
            toSide: x > 0 ? 'left' : 'right'
        });
    });

    await app.vault.create(outputPath, JSON.stringify({ nodes, edges }, null, 2));
    return { nodes: nodes.length, edges: edges.length };
}

/**
 * Generate a hierarchical canvas from folder structure
 * @param {string} folderPath - Root folder to visualize
 * @param {string} outputPath - Path for the output canvas
 * @param {Object} options - Layout options
 */
async function createFolderHierarchy(folderPath, outputPath, options = {}) {
    const { nodeWidth = 250, nodeHeight = 100, levelGap = 200, siblingGap = 50 } = options;

    const folder = app.vault.getAbstractFileByPath(folderPath);
    if (!folder || folder.children === undefined) {
        throw new Error(`Folder not found: ${folderPath}`);
    }

    const nodes = [];
    const edges = [];
    let nodeIndex = 0;

    function processFolder(f, level, position) {
        const nodeId = `node-${nodeIndex++}`;
        const x = position * (nodeWidth + siblingGap);
        const y = level * levelGap;

        nodes.push({
            id: nodeId,
            type: 'text',
            text: `📁 **${f.name}**`,
            x: x,
            y: y,
            width: nodeWidth,
            height: nodeHeight
        });

        const children = f.children || [];
        const folders = children.filter(c => c.children !== undefined);
        const files = children.filter(c => c.children === undefined && c.extension === 'md');

        // Add file nodes
        files.slice(0, 5).forEach((file, i) => {
            const fileId = `node-${nodeIndex++}`;
            nodes.push({
                id: fileId,
                type: 'file',
                file: file.path,
                x: x + (i - 2) * (nodeWidth * 0.6),
                y: y + levelGap * 0.6,
                width: nodeWidth * 0.8,
                height: nodeHeight
            });
            edges.push({
                id: `edge-${nodeId}-${fileId}`,
                fromNode: nodeId,
                fromSide: 'bottom',
                toNode: fileId,
                toSide: 'top',
                color: '4' // Green
            });
        });

        // Recursively process subfolders
        folders.forEach((subfolder, i) => {
            const childPos = position + (i - folders.length / 2) * 2;
            const childId = processFolder(subfolder, level + 1.5, childPos);
            edges.push({
                id: `edge-${nodeId}-${childId}`,
                fromNode: nodeId,
                fromSide: 'bottom',
                toNode: childId,
                toSide: 'top'
            });
        });

        return nodeId;
    }

    processFolder(folder, 0, 0);

    await app.vault.create(outputPath, JSON.stringify({ nodes, edges }, null, 2));
    return { nodes: nodes.length, edges: edges.length };
}

/**
 * Generate a canvas from Dataview query results
 * @param {string} query - Dataview query (e.g., 'FROM #topic')
 * @param {string} outputPath - Path for the output canvas
 * @param {Object} options - Layout options
 */
async function createFromDataview(query, outputPath, options = {}) {
    const { layout = 'grid', columns = 4, nodeWidth = 300, nodeHeight = 200, gap = 50 } = options;

    const dv = app.plugins.plugins.dataview?.api;
    if (!dv) throw new Error('Dataview plugin not enabled');

    const pages = dv.pages(query);
    if (!pages || pages.length === 0) {
        throw new Error(`No results for query: ${query}`);
    }

    const nodes = [];
    const edges = [];

    pages.forEach((page, i) => {
        let x, y;

        if (layout === 'grid') {
            const row = Math.floor(i / columns);
            const col = i % columns;
            x = col * (nodeWidth + gap);
            y = row * (nodeHeight + gap);
        } else if (layout === 'radial') {
            const angle = (2 * Math.PI * i) / pages.length;
            const radius = 400 + Math.floor(i / 8) * 300;
            x = radius * Math.cos(angle);
            y = radius * Math.sin(angle);
        }

        nodes.push({
            id: `dv-${i}`,
            type: 'file',
            file: page.file.path,
            x: x,
            y: y,
            width: nodeWidth,
            height: nodeHeight
        });
    });

    await app.vault.create(outputPath, JSON.stringify({ nodes, edges }, null, 2));
    return { nodes: nodes.length, query };
}

/**
 * Generate SAQ study canvas with concepts
 * @param {string} saqFolder - Folder containing SAQs
 * @param {string} outputPath - Path for the output canvas
 */
async function createSAQStudyMap(saqFolder, outputPath) {
    const files = app.vault.getFiles()
        .filter(f => f.path.startsWith(saqFolder) && f.extension === 'md');

    const nodes = [];
    const edges = [];
    const conceptMap = new Map(); // Track concept positions

    // Add SAQ nodes
    files.slice(0, 20).forEach((file, i) => {
        const cache = app.metadataCache.getFileCache(file);
        const fm = cache?.frontmatter || {};

        const row = Math.floor(i / 5);
        const col = i % 5;

        const nodeId = `saq-${i}`;
        nodes.push({
            id: nodeId,
            type: 'file',
            file: file.path,
            x: col * 350,
            y: row * 400,
            width: 300,
            height: 200
        });

        // Process concepts
        const concepts = fm.concept_direct || fm.related?.concepts || [];
        concepts.forEach((concept, ci) => {
            const conceptName = concept.replace(/\[\[|\]\]/g, '');
            let conceptId;

            if (!conceptMap.has(conceptName)) {
                conceptId = `concept-${conceptMap.size}`;
                conceptMap.set(conceptName, {
                    id: conceptId,
                    x: -500 - (conceptMap.size % 3) * 200,
                    y: Math.floor(conceptMap.size / 3) * 150
                });

                nodes.push({
                    id: conceptId,
                    type: 'text',
                    text: `## ${conceptName}`,
                    x: conceptMap.get(conceptName).x,
                    y: conceptMap.get(conceptName).y,
                    width: 180,
                    height: 100,
                    color: '5' // Cyan
                });
            } else {
                conceptId = conceptMap.get(conceptName).id;
            }

            edges.push({
                id: `edge-${nodeId}-${conceptId}`,
                fromNode: nodeId,
                fromSide: 'left',
                toNode: conceptId,
                toSide: 'right',
                color: '4' // Green
            });
        });
    });

    await app.vault.create(outputPath, JSON.stringify({ nodes, edges }, null, 2));
    return {
        saqs: files.length,
        concepts: conceptMap.size,
        nodes: nodes.length,
        edges: edges.length
    };
}

/**
 * Create a timeline canvas from dated notes
 * @param {string} folderPath - Folder to scan
 * @param {string} outputPath - Path for the output canvas
 * @param {string} dateField - Frontmatter field containing date
 */
async function createTimeline(folderPath, outputPath, dateField = 'date') {
    const files = app.vault.getFiles()
        .filter(f => f.path.startsWith(folderPath) && f.extension === 'md');

    const dated = [];
    for (const file of files) {
        const cache = app.metadataCache.getFileCache(file);
        const fm = cache?.frontmatter || {};
        if (fm[dateField]) {
            dated.push({
                file: file.path,
                date: new Date(fm[dateField]),
                title: fm.title || file.basename
            });
        }
    }

    dated.sort((a, b) => a.date - b.date);

    const nodes = [];
    const edges = [];
    const dayWidth = 400;

    dated.forEach((item, i) => {
        const nodeId = `timeline-${i}`;
        nodes.push({
            id: nodeId,
            type: 'file',
            file: item.file,
            x: i * dayWidth,
            y: 0,
            width: 350,
            height: 250
        });

        if (i > 0) {
            edges.push({
                id: `edge-timeline-${i}`,
                fromNode: `timeline-${i - 1}`,
                fromSide: 'right',
                toNode: nodeId,
                toSide: 'left',
                color: '2' // Orange
            });
        }
    });

    await app.vault.create(outputPath, JSON.stringify({ nodes, edges }, null, 2));
    return { events: dated.length };
}

// Export for use
return {
    createConceptMap,
    createFolderHierarchy,
    createFromDataview,
    createSAQStudyMap,
    createTimeline
};
