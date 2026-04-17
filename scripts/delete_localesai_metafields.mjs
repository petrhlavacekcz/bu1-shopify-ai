/**
 * delete_localesai_metafields.mjs
 *
 * Deletes all localesAI.translations metafield values from every product.
 * These are orphaned values left behind after the Locales.AI app was uninstalled.
 * All values are empty ({}) and have no functional purpose.
 *
 * Requirements:
 *   shopify store auth --store bu1rebuild.myshopify.com \
 *     --scopes write_products,read_products
 *
 * Usage:
 *   node scripts/delete_localesai_metafields.mjs [--dry-run]
 */

import { execSync } from "child_process";

const STORE = "bu1rebuild.myshopify.com";
const DRY_RUN = process.argv.includes("--dry-run");
const PAGE_SIZE = 50;

function shopifyQuery(query, variables = {}) {
  const varFlag =
    Object.keys(variables).length > 0
      ? `--variables '${JSON.stringify(variables)}'`
      : "";
  const cmd = `shopify store execute --store ${STORE} --query '${query}' ${varFlag} 2>/dev/null`;
  try {
    const raw = execSync(cmd, { encoding: "utf8", maxBuffer: 10 * 1024 * 1024 });
    // Extract JSON from CLI output (CLI wraps it with success box)
    const match = raw.match(/\{[\s\S]*\}/);
    if (!match) throw new Error("No JSON found in output");
    return JSON.parse(match[0]);
  } catch (e) {
    throw new Error(`Query failed: ${e.message}`);
  }
}

function shopifyMutation(mutation, variables = {}) {
  const varFlag =
    Object.keys(variables).length > 0
      ? `--variables '${JSON.stringify(variables)}'`
      : "";
  const cmd = `shopify store execute --store ${STORE} --allow-mutations --query '${mutation}' ${varFlag} 2>/dev/null`;
  try {
    const raw = execSync(cmd, { encoding: "utf8", maxBuffer: 10 * 1024 * 1024 });
    const match = raw.match(/\{[\s\S]*\}/);
    if (!match) throw new Error("No JSON found in output");
    return JSON.parse(match[0]);
  } catch (e) {
    throw new Error(`Mutation failed: ${e.message}`);
  }
}

async function getAllProductIds() {
  const ids = [];
  let cursor = null;
  let hasNext = true;

  while (hasNext) {
    const afterClause = cursor ? `, after: "${cursor}"` : "";
    const data = shopifyQuery(`{
      products(first: ${PAGE_SIZE}${afterClause}) {
        nodes { id handle }
        pageInfo { hasNextPage endCursor }
      }
    }`);

    const { nodes, pageInfo } = data.products;
    ids.push(...nodes);
    hasNext = pageInfo.hasNextPage;
    cursor = pageInfo.endCursor;
    process.stdout.write(`  Fetched ${ids.length} products...\r`);
  }

  console.log(`\n  Total products: ${ids.length}`);
  return ids;
}

async function getLocalesAIMetafieldIds(productIds) {
  const metafieldInputs = [];

  // Query in batches of 10 to avoid large queries
  const batchSize = 10;
  for (let i = 0; i < productIds.length; i += batchSize) {
    const batch = productIds.slice(i, i + batchSize);
    const aliases = batch
      .map(
        (p, idx) =>
          `p${idx}: node(id: "${p.id}") {
            ... on Product {
              id
              metafields(namespace: "localesAI", first: 5) {
                nodes { id namespace key }
              }
            }
          }`
      )
      .join("\n");

    const data = shopifyQuery(`{ ${aliases} }`);

    for (const key of Object.keys(data)) {
      const product = data[key];
      if (product?.metafields?.nodes?.length > 0) {
        for (const mf of product.metafields.nodes) {
          metafieldInputs.push({
            ownerId: product.id,
            namespace: mf.namespace,
            key: mf.key,
          });
        }
      }
    }

    process.stdout.write(
      `  Checked ${Math.min(i + batchSize, productIds.length)}/${productIds.length} products...\r`
    );
  }

  console.log(`\n  Found ${metafieldInputs.length} localesAI metafields to delete`);
  return metafieldInputs;
}

async function deleteMetafields(metafieldInputs) {
  if (metafieldInputs.length === 0) {
    console.log("Nothing to delete.");
    return;
  }

  if (DRY_RUN) {
    console.log("\n[DRY RUN] Would delete:");
    metafieldInputs.slice(0, 10).forEach((mf) =>
      console.log(`  ${mf.ownerId} → ${mf.namespace}.${mf.key}`)
    );
    if (metafieldInputs.length > 10)
      console.log(`  ... and ${metafieldInputs.length - 10} more`);
    return;
  }

  // Delete in batches of 250 (Shopify limit)
  const batchSize = 250;
  let deleted = 0;

  for (let i = 0; i < metafieldInputs.length; i += batchSize) {
    const batch = metafieldInputs.slice(i, i + batchSize);
    const inputJson = JSON.stringify(batch);

    const data = shopifyMutation(
      `mutation DeleteMetafields($metafields: [MetafieldsDeleteInput!]!) {
        metafieldsDelete(metafields: $metafields) {
          deletedMetafields { ownerId namespace key }
          userErrors { field message }
        }
      }`,
      { metafields: batch }
    );

    const result = data.metafieldsDelete;
    const errors = result.userErrors || [];

    if (errors.length > 0) {
      console.error(`  Errors in batch ${i / batchSize + 1}:`, errors);
    }

    deleted += result.deletedMetafields?.length || 0;
    console.log(
      `  Deleted batch ${Math.ceil((i + 1) / batchSize)}: ${result.deletedMetafields?.length || 0} metafields`
    );
  }

  console.log(`\nDone. Total deleted: ${deleted}`);
}

// Main
console.log(`BU1 — Delete localesAI.translations metafields`);
console.log(`Store: ${STORE}`);
console.log(DRY_RUN ? "Mode: DRY RUN\n" : "Mode: LIVE — will delete\n");

console.log("Step 1: Fetching all products...");
const products = await getAllProductIds();

console.log("\nStep 2: Finding localesAI metafields...");
const toDelete = await getLocalesAIMetafieldIds(products);

console.log("\nStep 3: Deleting...");
await deleteMetafields(toDelete);
