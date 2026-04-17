#!/usr/bin/env node
/**
 * upload_blog_articles.mjs
 *
 * Handles three scenarios automatically:
 *   • New article     → articleCreate (isPublished: false — always a draft)
 *   • Existing draft  → articleUpdate (keeps isPublished: false)
 *   • Existing public → articleUpdate (keeps isPublished: true — never unpublishes)
 *   + Translations    → translationsRegister for all matching translation files
 *
 * Usage:
 *   node scripts/upload_blog_articles.mjs                   # all files in drafts/blog/
 *   node scripts/upload_blog_articles.mjs <file1> [file2]   # specific source files only
 *
 * Prerequisites:
 *   shopify store auth --store bu1rebuild.myshopify.com \
 *     --scopes write_content,write_translations,read_content,read_translations
 *
 * Author field: always "Petr Hlavacek"
 */

import { execSync, execFileSync } from 'child_process';
import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs';
import { tmpdir } from 'os';
import { join, dirname, basename } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname  = dirname(__filename);
const BASE       = join(__dirname, '..');
const STORE      = 'bu1rebuild.myshopify.com';
const BLOG_ID    = 'gid://shopify/Blog/82163826771';
const AUTHOR     = 'Petr Hlavacek';

// ─── YAML frontmatter parser ──────────────────────────────────────────────────
// Handles:  key: value   key: "value"   key: 'value'   key: [a, b, c]
// Skips:    # comments   indented lines   list items (- ...)
function parseMd(filePath) {
  const raw = readFileSync(filePath, 'utf-8');
  const end = raw.indexOf('\n---\n', 4);
  if (end === -1) throw new Error(`No closing --- in ${filePath}`);

  const yaml = raw.slice(4, end);
  const body = raw.slice(end + 5).trim();
  const f    = {};

  for (const line of yaml.split('\n')) {
    if (!line || line.startsWith('#') || line.startsWith(' ') || line.startsWith('\t') || line.startsWith('-')) continue;

    let m = line.match(/^([\w]+):\s+"(.*?)"\s*$/);   // key: "value"
    if (m) { f[m[1]] = m[2]; continue; }

    m = line.match(/^([\w]+):\s+'(.*?)'\s*$/);        // key: 'value'
    if (m) { f[m[1]] = m[2]; continue; }

    m = line.match(/^([\w]+):\s+\[(.+?)\]\s*$/);      // key: [a, b]
    if (m) { f[m[1]] = m[2].split(',').map(s => s.trim().replace(/^['"]|['"]$/g, '')); continue; }

    m = line.match(/^([\w]+):\s+(.+?)\s*$/);          // key: plain
    if (m) { f[m[1]] = m[2]; continue; }
  }

  return { fields: f, body };
}

// ─── Source file discovery ─────────────────────────────────────────────────────
function findSourceFiles() {
  const dir = join(BASE, 'drafts/blog');
  return readdirSync(dir)
    .filter(f => /^\d{4}-\d{2}-\d{2}-.+\.md$/.test(f))
    .filter(f => statSync(join(dir, f)).isFile())
    .sort()
    .map(f => join(dir, f));
}

function findTranslationFiles() {
  const dir = join(BASE, 'drafts/blog/translations');
  return readdirSync(dir)
    .filter(f => f.endsWith('.md'))
    .sort()
    .map(f => parseMd(join(dir, f)));
}

function validateImageStrategy(sourceFiles) {
  const validator = join(BASE, 'scripts/validate_blog_images.py');
  console.log('\n🔎 Validating image strategy...');
  try {
    execFileSync('python3', [validator, ...sourceFiles], { stdio: 'inherit' });
  } catch (err) {
    console.error('\n❌ Image validation failed. Fix draft image planning before upload.');
    throw err;
  }
}

// ─── Shopify CLI executor ─────────────────────────────────────────────────────
// NOTE: shopify store execute --json returns data directly (no { data: {} } wrapper)
function shopifyExec(query, variables = null, allowMutations = false) {
  const id    = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  const qFile = join(tmpdir(), `bu1-q-${id}.graphql`);
  writeFileSync(qFile, query);

  let cmd = `shopify store execute --store ${STORE} --query-file "${qFile}" --json`;

  if (variables) {
    const vFile = join(tmpdir(), `bu1-v-${id}.json`);
    writeFileSync(vFile, JSON.stringify(variables, null, 2));
    cmd += ` --variable-file "${vFile}"`;
  }
  if (allowMutations) cmd += ' --allow-mutations';

  try {
    const out = execSync(cmd, { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] });
    return JSON.parse(out);
  } catch (err) {
    console.error('\n❌ CLI error:', err.stderr || err.message);
    throw err;
  }
}

// ─── Lookup existing article ──────────────────────────────────────────────────
// NOTE: We do NOT read isPublished here — articleUpdate omits it entirely,
// so Shopify preserves whatever status is currently on the article.
function lookupArticle(handle) {
  const QUERY = `
    query LookupArticle($query: String!) {
      articles(first: 1, query: $query) {
        edges { node { id handle title } }
      }
    }
  `;
  const res   = shopifyExec(QUERY, { query: `handle:${handle}` });
  const edges = res?.articles?.edges ?? [];
  return edges.length ? edges[0].node : null;
}

// ─── Build article input fields ────────────────────────────────────────────────
function buildArticleInput({ fields, body }) {
  const summaryMatch = body.match(/<p>([\s\S]*?)<\/p>/);
  return {
    title:   fields.title,
    handle:  fields.handle,
    body:    body,
    summary: summaryMatch ? `<p>${summaryMatch[1]}</p>` : '',
    tags:    Array.isArray(fields.tags) ? fields.tags : (fields.tags ? [fields.tags] : []),
    metafields: [
      { namespace: 'global', key: 'title_tag',       type: 'single_line_text_field',  value: fields.seo_title       || fields.title },
      { namespace: 'global', key: 'description_tag', type: 'multi_line_text_field',   value: fields.seo_description || '' },
    ],
  };
}

// ─── Create new article (always draft) ────────────────────────────────────────
function createArticle(draft) {
  const MUTATION = `
    mutation ArticleCreate($article: ArticleCreateInput!) {
      articleCreate(article: $article) {
        article { id handle isPublished }
        userErrors { code field message }
      }
    }
  `;
  const variables = {
    article: {
      blogId:      BLOG_ID,
      author:      { name: AUTHOR },
      isPublished: false,           // new articles always start as draft
      ...buildArticleInput(draft),
    },
  };

  console.log(`\n📝 Creating (draft): ${draft.fields.handle}`);
  const res    = shopifyExec(MUTATION, variables, true);
  const errors = res?.articleCreate?.userErrors ?? [];
  if (errors.length) {
    console.error('   userErrors:', JSON.stringify(errors, null, 2));
    throw new Error(`articleCreate failed for ${draft.fields.handle}`);
  }
  const art = res.articleCreate.article;
  console.log(`   ✅ ${art.id}  isPublished=${art.isPublished}`);
  return art;
}

// ─── Update existing article (isPublished intentionally omitted → Shopify preserves it) ───
function updateArticle(existingId, draft) {
  const MUTATION = `
    mutation ArticleUpdate($id: ID!, $article: ArticleUpdateInput!) {
      articleUpdate(id: $id, article: $article) {
        article { id handle isPublished }
        userErrors { code field message }
      }
    }
  `;
  // isPublished is NOT included → Shopify keeps whatever status the article already has.
  // Published stays published. Draft stays draft. No accidental unpublishing.
  const variables = {
    id:      existingId,
    article: buildArticleInput(draft),
  };

  console.log(`\n✏️  Updating: ${draft.fields.handle}`);
  const res    = shopifyExec(MUTATION, variables, true);
  const errors = res?.articleUpdate?.userErrors ?? [];
  if (errors.length) {
    console.error('   userErrors:', JSON.stringify(errors, null, 2));
    throw new Error(`articleUpdate failed for ${draft.fields.handle}`);
  }
  const art = res.articleUpdate.article;
  console.log(`   ✅ ${art.id}  isPublished=${art.isPublished}`);
  return art;
}

// ─── Create or update (auto-detect) ──────────────────────────────────────────
// Returns { article, action: 'created' | 'updated' }
function syncArticle(draft) {
  const existing = lookupArticle(draft.fields.handle);
  if (existing) {
    return { article: updateArticle(existing.id, draft), action: 'updated' };
  }
  return { article: createArticle(draft), action: 'created' };
}

// ─── Fetch translatable digests ───────────────────────────────────────────────
function getDigests(articleId) {
  const QUERY = `
    query TranslatableContent($resourceId: ID!) {
      translatableResource(resourceId: $resourceId) {
        translatableContent { key digest }
      }
    }
  `;
  const res   = shopifyExec(QUERY, { resourceId: articleId });
  const items = res?.translatableResource?.translatableContent ?? [];
  const map   = {};
  for (const { key, digest } of items) map[key] = digest;
  console.log(`   Digests: ${Object.keys(map).join(', ')}`);
  return map;
}

// ─── Register translations ────────────────────────────────────────────────────
function registerTranslations(articleId, digests, translationDrafts) {
  const MUTATION = `
    mutation TranslationsRegister($resourceId: ID!, $translations: [TranslationInput!]!) {
      translationsRegister(resourceId: $resourceId, translations: $translations) {
        translations { key locale }
        userErrors { field message }
      }
    }
  `;

  const translations = [];
  for (const { fields, body } of translationDrafts) {
    const locale = fields.locale;
    const candidates = [
      { key: 'title',            value: fields.title },
      { key: 'body_html',        value: body },
      { key: 'handle',           value: fields.handle },
      { key: 'meta_title',       value: fields.seo_title },
      { key: 'meta_description', value: fields.seo_description },
      { key: 'summary_html',     value: fields.summary_html },
    ];
    for (const { key, value } of candidates) {
      if (!value || !digests[key]) continue;
      translations.push({ locale, key, value, translatableContentDigest: digests[key] });
    }
  }

  if (!translations.length) {
    console.log('   ⚠️  No translation entries to register');
    return 0;
  }

  console.log(`   Registering ${translations.length} entries across ${translationDrafts.length} locales...`);
  const res    = shopifyExec(MUTATION, { resourceId: articleId, translations }, true);
  const errors = res?.translationsRegister?.userErrors ?? [];
  const done   = res?.translationsRegister?.translations ?? [];

  if (errors.length) {
    console.error('   ⚠️  Translation errors (first 5):', JSON.stringify(errors.slice(0, 5), null, 2));
  }
  console.log(`   ✅ Registered ${done.length} translation entries`);
  return done.length;
}

// ─── Main ─────────────────────────────────────────────────────────────────────
function main() {
  console.log('═'.repeat(60));
  console.log(' BU1 Blog Article Upload');
  console.log(`  Store  : ${STORE}`);
  console.log(`  Blog   : ${BLOG_ID}`);
  console.log(`  Author : ${AUTHOR}`);
  console.log('═'.repeat(60));

  // Resolve source files: CLI args override auto-discovery
  const cliArgs = process.argv.slice(2).filter(a => a.endsWith('.md'));
  const sourceFiles = cliArgs.length
    ? cliArgs.map(a => (a.startsWith('/') ? a : join(BASE, a)))
    : findSourceFiles();

  if (!sourceFiles.length) {
    console.log('\nNo source files found in drafts/blog/');
    return;
  }

  validateImageStrategy(sourceFiles);

  // Load all translation files once
  const allTrans = findTranslationFiles();
  console.log(`\nSource files : ${sourceFiles.length}`);
  console.log(`Translations : ${allTrans.length} files`);

  let created = 0, updated = 0, totalTrans = 0;

  for (const filePath of sourceFiles) {
    const draft  = parseMd(filePath);
    const handle = draft.fields.handle;
    console.log(`\n${'─'.repeat(60)}`);

    // 1. Sync article (create or update, preserve publish status)
    const { article, action } = syncArticle(draft);
    if (action === 'created') created++; else updated++;

    // 2. Get digests
    const digests = getDigests(article.id);

    // 3. Match + register translations
    const matching = allTrans.filter(t => t.fields.source_handle === handle);
    console.log(`   Translations found: ${matching.length} locales`);
    totalTrans += registerTranslations(article.id, digests, matching);
  }

  console.log(`\n${'═'.repeat(60)}`);
  console.log(` ✅ Done. Created: ${created}  Updated: ${updated}  Translations: ${totalTrans} entries`);
  console.log('═'.repeat(60));
}

main();
