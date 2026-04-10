#!/usr/bin/env node

/**
 * generate-md.js
 *
 * Fetches structured metadata from Supabase and writes YAML frontmatter into
 * .md files under src/works/ and src/wiki/. The prose body below the frontmatter
 * is never touched.
 *
 * Usage:
 *   node scripts/generate-md.js           # fetch from Supabase, update all files
 *   node scripts/generate-md.js --dry-run # preview changes without writing
 *   node scripts/generate-md.js --id anna-karenina  # single record only
 *
 * Environment variables (required):
 *   SUPABASE_URL          e.g. https://xxxx.supabase.co
 *   SUPABASE_SERVICE_KEY  service role key (not the anon key — needs read access)
 *
 * .md file zones:
 *   ---
 *   # GENERATED — do not edit above this line
 *   id: anna-karenina
 *   ...
 *   ---
 *
 *   <!-- PROSE — edit freely in Obsidian -->
 *
 *   Prose body with [[wikilinks]] here.
 *
 * The script replaces only the frontmatter block. Prose is preserved.
 * For new files (no existing .md), a stub prose section is created.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

// ── JSONB sub-object key order ────────────────────────────────────────────────
// Postgres JSONB does not preserve insertion order. These maps define the
// canonical field order for each nested object type, matching the schema.

const KEY_ORDER = {
  titleAlternative: ['title', 'type', 'language'],

  authoringLocation: [
    'country', 'region', 'city', 'estate', 'building', 'room', 'coordinates',
    'dateFrom', 'dateFromOldStyle', 'dateFromApproximate',
    'dateTo', 'dateToOldStyle', 'dateToApproximate',
    'notes',
  ],

  coordinates: ['lat', 'lng'],

  manuscript: [
    'draftId', 'draftNumber', 'draftLabel',
    'dateCreated', 'dateCreatedOldStyle', 'dateCreatedApproximate', 'timeCreated',
    'numberOfFolios', 'condition',
    'currentRepository', 'repositoryCity', 'repositoryCountry', 'repositoryCallNumber',
    'scans', 'writingMaterials',
  ],

  transcription: [
    'sourceManuscriptId', 'transcriberId', 'transcriberName', 'relationToAuthor',
    'dateTranscribed', 'dateTranscribedOldStyle', 'dateTranscribedApproximate', 'timeTranscribed',
    'currentRepository', 'repositoryCity', 'repositoryCountry', 'repositoryCallNumber',
    'scans', 'notes',
  ],

  scan: ['url', 'sourceInstitution', 'license', 'credit', 'dateAccessed'],

  writingMaterials: ['pen', 'ink', 'paper', 'notes'],

  ban: [
    'banningAuthority', 'authorityType', 'jurisdiction', 'scope',
    'banDate', 'banDateOldStyle', 'banDateApproximate',
    'banLiftedDate', 'banLiftedDateOldStyle', 'banLiftedDateApproximate',
    'notes',
  ],

  relatedWork: ['id', 'relationshipType'],

  relatedArticle: ['id', 'relationshipType'],

  fieldSourceEntry: ['sourceId', 'volume', 'page', 'quote', 'notes'],
};

/**
 * Re-order the keys of a plain object according to a reference key list.
 * Unknown keys (not in the list) are appended at the end in their original order.
 */
function reorder(obj, keyList) {
  if (!obj || typeof obj !== 'object' || Array.isArray(obj)) return obj;
  const out = {};
  for (const k of keyList) {
    if (k in obj) out[k] = obj[k];
  }
  for (const k of Object.keys(obj)) {
    if (!(k in out)) out[k] = obj[k];
  }
  return out;
}

/**
 * Recursively normalise key order in all known JSONB sub-objects within a works row.
 */
function normaliseJsonbKeyOrder(row) {
  const r = { ...row };

  if (Array.isArray(r.titleAlternatives)) {
    r.titleAlternatives = r.titleAlternatives.map(o => reorder(o, KEY_ORDER.titleAlternative));
  }

  if (Array.isArray(r.authoringLocations)) {
    r.authoringLocations = r.authoringLocations.map(loc => {
      const l = reorder(loc, KEY_ORDER.authoringLocation);
      if (l.coordinates) l.coordinates = reorder(l.coordinates, KEY_ORDER.coordinates);
      return l;
    });
  }

  if (Array.isArray(r.manuscripts)) {
    r.manuscripts = r.manuscripts.map(ms => {
      const m = reorder(ms, KEY_ORDER.manuscript);
      if (Array.isArray(m.scans)) m.scans = m.scans.map(s => reorder(s, KEY_ORDER.scan));
      if (m.writingMaterials) m.writingMaterials = reorder(m.writingMaterials, KEY_ORDER.writingMaterials);
      return m;
    });
  }

  if (Array.isArray(r.transcriptions)) {
    r.transcriptions = r.transcriptions.map(tr => {
      const t = reorder(tr, KEY_ORDER.transcription);
      if (Array.isArray(t.scans)) t.scans = t.scans.map(s => reorder(s, KEY_ORDER.scan));
      return t;
    });
  }

  if (Array.isArray(r.bans)) {
    r.bans = r.bans.map(b => reorder(b, KEY_ORDER.ban));
  }

  if (Array.isArray(r.relatedWorks)) {
    r.relatedWorks = r.relatedWorks.map(w => reorder(w, KEY_ORDER.relatedWork));
  }

  // fieldSources: each value is an array of source entries
  if (r.fieldSources && typeof r.fieldSources === 'object') {
    const fs = {};
    for (const [field, entries] of Object.entries(r.fieldSources)) {
      fs[field] = Array.isArray(entries)
        ? entries.map(e => reorder(e, KEY_ORDER.fieldSourceEntry))
        : entries;
    }
    r.fieldSources = fs;
  }

  return r;
}

// ── Config ────────────────────────────────────────────────────────────────────

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_KEY;

const WORKS_SRC_DIR = path.join(ROOT, 'src', 'works');
const WIKI_SRC_DIR  = path.join(ROOT, 'src', 'wiki');

// Tables to pull from Supabase.
// Each entry maps a Supabase table to a local directory and a filename strategy.
const SOURCES = [
  {
    table: 'works',
    dir: WORKS_SRC_DIR,
    // Each work is nested: main_category / subcategory / work_id / title.md
    // Folder names are normalized: spaces and slashes become dashes, lowercase
    // e.g. "Poetry/Songs" → "poetry-songs", "Short Stories" → "short-stories"
    // e.g. src/works/fiction/novels/anna-karenina/Anna Karenina.md
    filename: (row) => {
      const main = normalizeFolderName(row.main_category);
      const sub = normalizeFolderName(row.subcategory);
      return `${main}/${sub}/${row.id}/${row.title_en || row.id}.md`;
    },
  },
  {
    table: 'wiki_articles',
    dir: WIKI_SRC_DIR,
    filename: (row) => `${row.title_en || row.id}.md`,
  },
];

// ── CLI flags ─────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
const DRY_RUN = args.includes('--dry-run');
const SINGLE_ID = (() => {
  const idx = args.indexOf('--id');
  return idx !== -1 ? args[idx + 1] : null;
})();

// ── Helpers ───────────────────────────────────────────────────────────────────

/**
 * Convert a snake_case Supabase row object to camelCase keys for YAML frontmatter.
 * e.g. title_en → titleEn, date_first_published → dateFirstPublished
 */
function snakeToCamel(str) {
  return str.replace(/_([a-z])/g, (_, c) => c.toUpperCase());
}

/**
 * Normalize category/subcategory names for use in folder paths.
 * Convert to lowercase, replace spaces and slashes with dashes.
 * e.g. "Poetry/Songs" → "poetry-songs", "Short Stories" → "short-stories"
 */
function normalizeFolderName(name) {
  if (!name) return 'uncategorized';
  return name
    .toLowerCase()
    .replace(/[\s/]+/g, '-')  // spaces and slashes → dashes
    .replace(/['"]/g, '');     // remove quotes
}

function rowToCamelCase(row) {
  const out = {};
  for (const [key, val] of Object.entries(row)) {
    out[snakeToCamel(key)] = val;
  }
  return out;
}

/**
 * Serialize a JS value to a YAML string fragment.
 * Handles strings, numbers, booleans, null, arrays, and plain objects.
 * Not a full YAML serialiser — covers the schema field types used in this project.
 */
function toYaml(value, indent = 0) {
  const pad = ' '.repeat(indent);

  if (value === null || value === undefined) return '""';
  if (typeof value === 'boolean') return String(value);
  if (typeof value === 'number') return String(value);

  if (typeof value === 'string') {
    // Multi-line strings use block scalar
    if (value.includes('\n')) {
      const lines = value.trimEnd().split('\n');
      return '|\n' + lines.map(l => pad + '  ' + l).join('\n');
    }
    // Strings needing quotes: empty, contain special YAML chars, or look like numbers/booleans
    if (
      value === '' ||
      /[:{}[\],&*#?|<>=!%@`]/.test(value) ||
      /^(true|false|null|~|\d)/.test(value)
    ) {
      return JSON.stringify(value); // safe double-quoted string
    }
    return value;
  }

  if (Array.isArray(value)) {
    if (value.length === 0) return '[]';
    return '\n' + value.map(item => {
      if (typeof item === 'object' && item !== null) {
        const inner = Object.entries(item)
          .map(([k, v]) => `${pad}    ${k}: ${toYaml(v, indent + 4)}`)
          .join('\n');
        return `${pad}  -\n${inner}`;
      }
      return `${pad}  - ${toYaml(item, indent + 2)}`;
    }).join('\n');
  }

  if (typeof value === 'object') {
    const lines = Object.entries(value)
      .map(([k, v]) => `${pad}  ${k}: ${toYaml(v, indent + 2)}`);
    return '\n' + lines.join('\n');
  }

  return String(value);
}

/**
 * Build the Eleventy-specific frontmatter fields that layouts and meta partials
 * depend on (title, description, titleRu). These are derived from schema fields
 * and placed at the top of the frontmatter block so Eleventy always finds them.
 *
 * Kept in a clearly labelled section so it's obvious they come from the schema
 * and should not be hand-edited — edit the source fields in Supabase instead.
 */
function eleventyFields(row, table) {
  if (table === 'works') {
    return [
      '# ELEVENTY — derived from schema, do not edit',
      `title: ${toYaml(row.titleEn || '')}`,
      `description: ${toYaml(row.synopsis || row.titleEn || '')}`,
      ...(row.titleRu ? [`titleRu: ${toYaml(row.titleRu)}`] : []),
    ];
  }
  if (table === 'wiki_articles') {
    return [
      '# ELEVENTY — derived from schema, do not edit',
      `title: ${toYaml(row.titleEn || '')}`,
      `description: ${toYaml(row.description || '')}`,
      ...(row.titleRu ? [`titleRu: ${toYaml(row.titleRu)}`] : []),
    ];
  }
  return [];
}

// Fields emitted in the ELEVENTY block — must not be repeated in the GENERATED block.
// titleEn and titleRu are represented as title/titleRu in the Eleventy block,
// description is carried through directly. All would cause YAML duplicate key errors.
const ELEVENTY_ONLY_FIELDS = new Set(['titleRu', 'description']);

/**
 * Serialize a full camelCase row object to a YAML frontmatter block string.
 * Returns the block including the opening and closing --- delimiters.
 *
 * Fields duplicated in both the Eleventy block and the schema (titleEn, titleRu,
 * description) are emitted only once — in the Eleventy block — to avoid the
 * YAML duplicate key error Eleventy throws.
 */
function buildFrontmatter(row, table) {
  const lines = ['---'];
  const eleventy = eleventyFields(row, table);
  if (eleventy.length) {
    lines.push(...eleventy, '');
  }
  lines.push('# GENERATED — do not edit below this line');
  for (const [key, val] of Object.entries(row)) {
    // Skip fields already present in the Eleventy block
    if (ELEVENTY_ONLY_FIELDS.has(key)) continue;
    lines.push(`${key}: ${toYaml(val)}`);
  }
  lines.push('---');
  return lines.join('\n');
}

/**
 * Given existing file content (or null for new files), extract the prose body.
 * Handles three cases:
 *   1. File has the PROSE zone marker — return everything after it.
 *   2. File has frontmatter but no zone marker (legacy) — return the prose body as-is.
 *   3. File doesn't exist — return a stub.
 */
function extractProse(existingContent, titleEn) {
  if (!existingContent) {
    // New file — create a stub prose section
    return `<!-- PROSE — edit freely in Obsidian -->\n\n`;
  }

  // Case 1: has zone marker
  const markerMatch = existingContent.match(/<!--\s*PROSE[^>]*-->/);
  if (markerMatch) {
    const markerIndex = existingContent.indexOf(markerMatch[0]);
    return existingContent.slice(markerIndex);
  }

  // Case 2: legacy file — extract everything after the closing frontmatter ---
  // Match the second occurrence of --- on its own line
  const fmMatch = existingContent.match(/^---\n[\s\S]*?\n---\n([\s\S]*)$/m);
  if (fmMatch) {
    const legacyProse = fmMatch[1].trimStart();
    return `<!-- PROSE — edit freely in Obsidian -->\n\n${legacyProse}`;
  }

  // Fallback: no frontmatter found — treat whole file as prose
  return `<!-- PROSE — edit freely in Obsidian -->\n\n${existingContent.trimStart()}`;
}

/**
 * Transform a camelCase works row into the nested structure the schema expects.
 *
 * Two things to handle:
 *   1. Re-nest flat identifier_* columns back into identifiers: { wikidata, gutenberg, ... }
 *   2. Strip DB-internal fields (createdAt, updatedAt) — these are not schema fields
 *      and should not appear in the .md frontmatter.
 */
function transformWorksRow(row) {
  const out = {};

  // Fields to drop entirely from frontmatter
  const DROP = new Set(['createdAt', 'updatedAt']);

  // Prefix that marks identifier columns
  const ID_PREFIX = 'identifier';

  const identifiers = {};

  for (const [key, val] of Object.entries(row)) {
    if (DROP.has(key)) continue;

    if (key.startsWith(ID_PREFIX) && key !== ID_PREFIX) {
      // e.g. identifierWikidata → wikidata
      //      identifierJubileeEditionVolumes → jubileeEdition.volumes (handled below)
      const subKey = key.slice(ID_PREFIX.length);
      const camelSub = subKey.charAt(0).toLowerCase() + subKey.slice(1);

      // jubileeEdition fields: identifierJubileeEditionVolumes, identifierJubileeEditionNotes
      if (camelSub.startsWith('jubileeEdition')) {
        if (!identifiers.jubileeEdition) identifiers.jubileeEdition = {};
        const jubKey = camelSub.slice('jubileeEdition'.length);
        identifiers.jubileeEdition[jubKey.charAt(0).toLowerCase() + jubKey.slice(1)] = val;
      } else {
        identifiers[camelSub] = val;
      }
    } else {
      out[key] = val;
    }
  }

  // Insert identifiers block in the correct schema position (after notes, before fieldSources)
  // We do this by rebuilding the object in schema order
  const ordered = {};
  const BEFORE_IDENTIFIERS = [
    'id','recordStatus','titleEn','titleRu','titleAlternatives',
    'mainCategory','subcategory','genre','language','completionStatus','publishedDuringLifetime','publishedInRussiaDuringLifetime',
    'dateWritingStarted','dateWritingStartedOldStyle','dateWritingStartedApproximate','timeWritingStarted',
    'dateWritingCompleted','dateWritingCompletedOldStyle','dateWritingCompletedApproximate','timeWritingCompleted',
    'dateFirstPublished','dateFirstPublishedOldStyle','dateFirstPublishedApproximate',
    'firstPublishedVenue','firstPublishedVenueType',
    'dateFirstPublishedInRussia','dateFirstPublishedInRussiaOldStyle','dateFirstPublishedInRussiaApproximate',
    'firstPublishedInRussiaVenue','firstPublishedInRussiaVenueType',
    'authoringLocations','manuscripts','transcriptions',
    'dedicatedToEn','dedicatedToRu','epigraph','epigraphLanguage','epigraphAuthor','epigraphSource',
    'themes','subjectHeadings','synopsis',
    'bans','samizdatCirculation','excommunicationRelated',
    'censoredVersionExists','censoredVersionNotes','censorshipNotes',
    'wordCount','wordCountEdition','relatedWorks','notes',
  ];

  for (const k of BEFORE_IDENTIFIERS) {
    if (k in out) ordered[k] = out[k];
  }
  ordered.identifiers = identifiers;
  if ('fieldSources' in out) ordered.fieldSources = out.fieldSources;

  // Any remaining keys not in the explicit list (future schema additions)
  for (const k of Object.keys(out)) {
    if (!(k in ordered)) ordered[k] = out[k];
  }

  return normaliseJsonbKeyOrder(ordered);
}

/**
 * Transform a camelCase wiki_articles row into the nested structure the schema expects.
 * Re-nests flat identifier_* columns into identifiers: { wikidata, viaf, ... }
 * Strips DB-internal fields (createdAt, updatedAt).
 * Enforces canonical field order.
 */
function transformWikiRow(row) {
  const out = {};
  const DROP = new Set(['createdAt', 'updatedAt']);
  const ID_PREFIX = 'identifier';
  const identifiers = {};

  for (const [key, val] of Object.entries(row)) {
    if (DROP.has(key)) continue;
    if (key.startsWith(ID_PREFIX) && key !== ID_PREFIX) {
      const subKey = key.slice(ID_PREFIX.length);
      identifiers[subKey.charAt(0).toLowerCase() + subKey.slice(1)] = val;
    } else {
      out[key] = val;
    }
  }

  // Strip fields that don't apply to this entity type — they'd only add noise
  const PERSON_ONLY = new Set(['birthDate','birthDateOldStyle','birthDateApproximate','deathDate','deathDateOldStyle','deathDateApproximate','birthPlace','nationality','roles','relationToTolstoy']);
  const EVENT_ONLY  = new Set(['eventDate','eventDateOldStyle','eventDateApproximate','eventDateEnd','eventDateEndOldStyle','eventDateEndApproximate','eventLocation']);
  const PLACE_ONLY  = new Set(['country','region','city','coordinates']);

  const type = out.type;
  for (const key of Object.keys(out)) {
    if (type === 'person' && (EVENT_ONLY.has(key) || PLACE_ONLY.has(key))) delete out[key];
    if (type === 'event'  && (PERSON_ONLY.has(key) || PLACE_ONLY.has(key))) delete out[key];
    if (type === 'place'  && (PERSON_ONLY.has(key) || EVENT_ONLY.has(key))) delete out[key];
    // Also drop empty JSONB objects (e.g. coordinates: {} on non-place records)
    if (out[key] && typeof out[key] === 'object' && !Array.isArray(out[key]) && Object.keys(out[key]).length === 0) delete out[key];
  }

  // Canonical field order matching the wiki schema
  const ORDERED_KEYS = [
    'id', 'recordStatus', 'titleEn', 'titleRu', 'type', 'description',
    // person
    'birthDate', 'birthDateOldStyle', 'birthDateApproximate',
    'deathDate', 'deathDateOldStyle', 'deathDateApproximate',
    'birthPlace', 'nationality', 'roles', 'relationToTolstoy',
    // event
    'eventDate', 'eventDateOldStyle', 'eventDateApproximate',
    'eventDateEnd', 'eventDateEndOldStyle', 'eventDateEndApproximate',
    'eventLocation',
    // place
    'country', 'region', 'city', 'coordinates',
    // shared
    'relatedWorks', 'relatedArticles', 'themes',
  ];

  const ordered = {};
  for (const k of ORDERED_KEYS) {
    if (k in out) ordered[k] = out[k];
  }
  ordered.identifiers = identifiers;
  if ('fieldSources' in out) ordered.fieldSources = out.fieldSources;
  // Any future keys not in the explicit list
  for (const k of Object.keys(out)) {
    if (!(k in ordered)) ordered[k] = out[k];
  }

  // Normalise JSONB key order for shared sub-objects
  if (Array.isArray(ordered.relatedWorks)) {
    ordered.relatedWorks = ordered.relatedWorks.map(w => reorder(w, KEY_ORDER.relatedWork));
  }
  if (Array.isArray(ordered.relatedArticles)) {
    ordered.relatedArticles = ordered.relatedArticles.map(a => reorder(a, KEY_ORDER.relatedArticle));
  }
  if (ordered.coordinates && typeof ordered.coordinates === 'object') {
    ordered.coordinates = reorder(ordered.coordinates, KEY_ORDER.coordinates);
  }
  if (ordered.fieldSources && typeof ordered.fieldSources === 'object') {
    const fs = {};
    for (const [field, entries] of Object.entries(ordered.fieldSources)) {
      fs[field] = Array.isArray(entries)
        ? entries.map(e => reorder(e, KEY_ORDER.fieldSourceEntry))
        : entries;
    }
    ordered.fieldSources = fs;
  }

  return ordered;
}

/**
 * Build the full .md file content from a Supabase row and existing file (if any).
 */
function buildFileContent(camelRow, existingContent, table) {
  const frontmatter = buildFrontmatter(camelRow, table);
  const prose = extractProse(existingContent, camelRow.titleEn);
  return `${frontmatter}\n\n${prose}`;
}

// ── Supabase fetch ────────────────────────────────────────────────────────────

async function fetchTable(table, singleId = null) {
  if (!SUPABASE_URL || !SUPABASE_KEY) {
    throw new Error(
      'Missing environment variables. Set SUPABASE_URL and SUPABASE_SERVICE_KEY.'
    );
  }

  let url = `${SUPABASE_URL}/rest/v1/${table}?select=*`;
  if (singleId) {
    url += `&id=eq.${encodeURIComponent(singleId)}`;
  }

  const res = await fetch(url, {
    headers: {
      apikey: SUPABASE_KEY,
      Authorization: `Bearer ${SUPABASE_KEY}`,
      'Content-Type': 'application/json',
    },
  });

  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Supabase fetch failed for table "${table}": ${res.status} ${body}`);
  }

  return res.json();
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function processSource({ table, dir, filename }) {
  let rows;
  try {
    rows = await fetchTable(table, SINGLE_ID);
  } catch (err) {
    // If the table doesn't exist yet, skip gracefully
    if (
      err.message.includes('42P01') ||
      err.message.includes('does not exist') ||
      err.message.includes('PGRST205') ||
      err.message.includes('404')
    ) {
      console.warn(`  ⚠  Table "${table}" not found in Supabase — skipping.`);
      return { created: 0, updated: 0, skipped: 1 };
    }
    throw err;
  }

  if (rows.length === 0) {
    console.log(`  No rows found in "${table}".`);
    return { created: 0, updated: 0, skipped: 0 };
  }

  let created = 0;
  let updated = 0;

  for (const row of rows) {
    let camelRow = rowToCamelCase(row);
    if (table === 'works') camelRow = transformWorksRow(camelRow);
    if (table === 'wiki_articles') camelRow = transformWikiRow(camelRow);
    const fname = filename(row);
    const filepath = path.join(dir, fname);

    let existingContent = null;
    let isNew = false;

    if (fs.existsSync(filepath)) {
      existingContent = fs.readFileSync(filepath, 'utf8');
    } else {
      isNew = true;
    }

    const newContent = buildFileContent(camelRow, existingContent, table);

    // Skip if content is unchanged (avoids unnecessary file writes + git noise)
    if (existingContent && newContent === existingContent) {
      continue;
    }

    const label = isNew ? 'CREATE' : 'UPDATE';
    console.log(`  [${label}] ${path.relative(ROOT, filepath)}`);

    if (!DRY_RUN) {
      fs.mkdirSync(dir, { recursive: true });
      fs.writeFileSync(filepath, newContent, 'utf8');
    }

    isNew ? created++ : updated++;
  }

  return { created, updated, skipped: 0 };
}

async function main() {
  console.log(`\n🗄  generate-md.js${DRY_RUN ? ' (dry run)' : ''}${SINGLE_ID ? ` — id: ${SINGLE_ID}` : ''}\n`);

  let totalCreated = 0;
  let totalUpdated = 0;

  for (const source of SOURCES) {
    console.log(`Pulling from "${source.table}" → ${path.relative(ROOT, source.dir)}/`);
    const { created, updated } = await processSource(source);
    totalCreated += created;
    totalUpdated += updated;
  }

  console.log(`\n✓ Done. ${totalCreated} created, ${totalUpdated} updated.\n`);
  if (DRY_RUN) {
    console.log('  (dry run — no files were written)\n');
  }
}

main().catch(err => {
  console.error('\n✗ Error:', err.message);
  process.exit(1);
});
