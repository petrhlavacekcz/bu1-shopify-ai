# BU1 Translation Export Batches

Shopify translation exports arrive by e-mail and can be split into multiple CSV attachments.

## Storage Rule

- Keep each e-mail export in its own dated directory.
- Do not mix CSV files from different export dates in the same directory.
- Treat one dated directory as one validation snapshot.

## Current Batch

- `2026-04-10_shopify_email_export/`
  Contains the four CSV attachments downloaded from the Shopify e-mail export on April 10, 2026.

## Validator Usage

```bash
python3 scripts/validate_translations.py --input BU1_translations/2026-04-10_shopify_email_export
python3 scripts/validate_translations.py --input BU1_translations/2026-04-10_shopify_email_export --locale en --type PRODUCT
python3 scripts/validate_translations.py --input BU1_translations/2026-04-10_shopify_email_export --report reports/qc_20260410.csv
```
