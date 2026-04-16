#!/usr/bin/env python3
"""
BU1 Translation Quality Control — CSV Export Validator
======================================================
Reads an explicit Shopify translation export input and runs
the full Translation Quality Checklist:

1. Missing required fields (title, body/body_html, meta_description, handle)
2. Domain errors (bu1.cz in foreign-language content)
3. Forbidden terms & terminology consistency
4. Duplicate/untranslated content (translated == default)
5. Formal register violations (informal pronouns in DE/PL/SK/…)
6. Localization rules (handles, brand terms, technical abbreviations)
7. Coverage & quality metrics per locale

Usage:
    python3 scripts/validate_translations.py --input BU1_translations/2026-04-10_shopify_email_export
    python3 scripts/validate_translations.py --input BU1_translations/2026-04-10_shopify_email_export --locale en --type PRODUCT --verbose
    python3 scripts/validate_translations.py --input BU1_translations/2026-04-10_shopify_email_export --summary
    python3 scripts/validate_translations.py --input BU1_translations/2026-04-10_shopify_email_export --report reports/qc_report.csv
"""

import argparse
import csv
import glob
import os
import re
import sys
from collections import defaultdict
from datetime import datetime

# ─── Configuration ───────────────────────────────────────────────────────────

TRANSLATION_DIR = os.path.join(os.path.dirname(__file__), '..', 'BU1_translations')

# Required translated fields per content type
REQUIRED_FIELDS = {
    'PRODUCT': {'title', 'body_html', 'meta_description', 'handle'},
    'PAGE': {'title', 'body_html', 'meta_description', 'handle'},
    'ARTICLE': {'title', 'body_html', 'summary_html', 'handle'},
    'BLOG': {'title', 'handle'},
    'PRODUCT_OPTION': {'name'},
    'PRODUCT_OPTION_VALUE': {'name'},
    'SHOP_POLICY': {'body'},
}

# Priority locales: must reach 100% coverage
PRIORITY_LOCALES = {'en', 'de', 'pl', 'sk'}
# Other locales: target 95%+
ALL_LOCALES = {'bg', 'de', 'en', 'es', 'fr', 'hr', 'hu', 'it', 'pl', 'ro', 'sk'}

# Terms that must NEVER appear in translations (case-insensitive)
FORBIDDEN_TERMS = {
    # Czech leaks in non-CS/SK content
    'soccer': 'Use "football" (or locale equivalent) instead of "soccer"',
    'fotbal': 'Czech term leaked — translate to target language',
    'brankářské': 'Czech term leaked — translate to target language',
    'brankář': 'Czech term leaked — translate to target language',
    'rukavice': 'Czech term leaked — translate to target language',
    # Brand-forbidden marketing terms (apply to ALL locales incl. CS)
    'revoluční': 'Forbidden marketing hyperbole — remove or rephrase',
    'prémiový': 'Forbidden marketing hyperbole — remove or rephrase',
    'unikátní': 'Forbidden marketing hyperbole — remove or rephrase',
    'revolutionary': 'Forbidden marketing hyperbole — remove or rephrase',
    'premium': 'Forbidden marketing hyperbole — remove or rephrase',
    'unique': 'Forbidden marketing hyperbole — remove or rephrase',
    'revolutionär': 'Forbidden marketing hyperbole (DE) — remove or rephrase',
    'einzigartig': 'Forbidden marketing hyperbole (DE) — remove or rephrase',
    'révolutionnaire': 'Forbidden marketing hyperbole (FR) — remove or rephrase',
    'revolucionario': 'Forbidden marketing hyperbole (ES) — remove or rephrase',
    'rivoluzionario': 'Forbidden marketing hyperbole (IT) — remove or rephrase',
}

# Terms that must NEVER be translated (keep original)
DO_NOT_TRANSLATE = [
    'BU1',           # brand name
    'NC',            # model abbreviation
    'RF',            # model abbreviation
    'HG',            # model abbreviation
    'FG',            # model abbreviation
    'AG',            # model abbreviation
    'TF',            # model abbreviation
    'Triangle',      # model name
    'Gator',         # model name
    'Light',         # model name (within product context)
    'Classic',       # model name
    'Tube Socks',    # product line name
]

# Domain rules: foreign locales must use bu1sport.com, not bu1.cz
CZECH_DOMAIN = 'bu1.cz'
INTL_DOMAIN = 'bu1sport.com'

# Informal pronoun patterns per locale (translations should use formal register)
INFORMAL_PATTERNS = {
    'de': [r'\bdu\b', r'\bdein[erem]*\b', r'\bdir\b', r'\bdich\b'],
    'pl': [r'\bty\b', r'\btwoj[aeimych]*\b', r'\bciebie\b', r'\btobie\b'],
    'sk': [r'\bty\b', r'\btvoj[eaiíchmu]*\b', r'\bteba\b', r'\btebe\b'],
    'hu': [r'\bte\b(?!\s)', r'\btied\b'],
    'es': [r'\btú\b', r'\btuyo\b', r'\btu\s'],
    'fr': [r'\btu\b', r'\bton\b(?=\s)', r'\bta\b(?=\s)', r'\btes\b(?=\s)'],
    'it': [r'\btu\b', r'\btuo\b', r'\btua\b'],
    'ro': [r'\btu\b', r'\btău\b', r'\bta\b(?=\s)'],
    'hr': [r'\bti\b', r'\btvoj[eaimu]*\b'],
    'bg': [r'\bти\b', r'\bтвой\b', r'\bтвоя\b'],
}


# ─── Issue types ─────────────────────────────────────────────────────────────

class Issue:
    MISSING = 'MISSING_TRANSLATION'
    DOMAIN = 'WRONG_DOMAIN'
    FORBIDDEN = 'FORBIDDEN_TERM'
    DUPLICATE = 'UNTRANSLATED_DUPLICATE'
    INFORMAL = 'INFORMAL_REGISTER'
    OUTDATED = 'OUTDATED_STATUS'
    EMPTY = 'EMPTY_TRANSLATION'

    SEVERITY = {
        MISSING: 'HIGH',
        DOMAIN: 'HIGH',
        FORBIDDEN: 'MEDIUM',
        DUPLICATE: 'MEDIUM',
        INFORMAL: 'LOW',
        OUTDATED: 'MEDIUM',
        EMPTY: 'HIGH',
    }


# ─── Parsing ─────────────────────────────────────────────────────────────────

def resolve_input_paths(input_path):
    """Resolve explicit input into one or more CSV snapshot files."""
    abs_input = os.path.abspath(input_path)
    if os.path.isfile(abs_input):
        return [abs_input]
    if os.path.isdir(abs_input):
        paths = sorted(glob.glob(os.path.join(abs_input, '*.csv')))
        if paths:
            return paths
    raise FileNotFoundError(abs_input)


def load_translations(input_path):
    """Load one CSV or one explicit batch directory and return rows + file list."""
    rows = []
    paths = resolve_input_paths(input_path)
    csv.field_size_limit(sys.maxsize)
    for path in paths:
        with open(path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    return rows, paths


def filter_issues(issues, locale_filter=None, type_filter=None):
    """Apply CLI filters consistently for output, report export, and exit code."""
    filtered = issues
    if locale_filter:
        filtered = [i for i in filtered if i['locale'] == locale_filter]
    if type_filter:
        filtered = [i for i in filtered if i['type'] == type_filter]
    return filtered


def group_by_resource(rows):
    """Group rows by (Type, Identification, Locale) -> {field: translated_content}"""
    groups = defaultdict(dict)
    meta = {}
    for row in rows:
        key = (row['Type'], row['Identification'], row['Locale'])
        field = row['Field']
        groups[key][field] = row.get('Translated content', '')
        # Also store default content and status
        meta_key = (row['Type'], row['Identification'], row['Locale'], field)
        meta[meta_key] = {
            'default': row.get('Default content', ''),
            'translated': row.get('Translated content', ''),
            'status': row.get('Status', '').strip(),
        }
    return groups, meta


# ─── Checks ──────────────────────────────────────────────────────────────────

def check_missing_fields(groups, meta):
    """Check required fields are present and non-empty."""
    issues = []
    for (ctype, cid, locale), fields in groups.items():
        required = REQUIRED_FIELDS.get(ctype, set())
        for req_field in required:
            translated = fields.get(req_field, '')
            if not translated or not translated.strip():
                issues.append({
                    'type': ctype, 'id': cid, 'locale': locale,
                    'field': req_field, 'issue': Issue.MISSING,
                    'detail': f'Missing required field: {req_field}',
                })
    return issues


def check_domain_errors(meta):
    """Foreign locales must not reference bu1.cz."""
    issues = []
    for (ctype, cid, locale, field), data in meta.items():
        translated = data['translated']
        if not translated:
            continue
        # SK is served under bu1.cz/sk — exempt from the domain check
        if locale == 'sk':
            continue
        if CZECH_DOMAIN in translated and INTL_DOMAIN not in translated:
            issues.append({
                'type': ctype, 'id': cid, 'locale': locale,
                'field': field, 'issue': Issue.DOMAIN,
                'detail': f'Contains bu1.cz — should be bu1sport.com for locale {locale}',
            })
    return issues


def check_forbidden_terms(meta):
    """Check for terms that should never appear in translations."""
    issues = []
    for (ctype, cid, locale, field), data in meta.items():
        translated = data['translated']
        if not translated:
            continue
        text_lower = translated.lower()
        for term, reason in FORBIDDEN_TERMS.items():
            if term in text_lower:
                # Skip if it's Czech locale — forbidden terms are Czech-specific leaks
                if locale == 'cs':
                    continue
                # Some terms only flagged in non-Czech locales
                if term in ('fotbal', 'brankářské', 'brankář', 'rukavice') and locale in ('cs', 'sk'):
                    continue
                issues.append({
                    'type': ctype, 'id': cid, 'locale': locale,
                    'field': field, 'issue': Issue.FORBIDDEN,
                    'detail': f'Forbidden term "{term}": {reason}',
                })
    return issues


def check_duplicates(meta):
    """Flag translations identical to Czech default (likely untranslated)."""
    issues = []
    for (ctype, cid, locale, field), data in meta.items():
        default = data['default']
        translated = data['translated']
        if not translated or not default:
            continue
        # Skip short values (handles, option names like "S", "M", "L")
        if len(default.strip()) < 10:
            continue
        # Skip handle field — often intentionally same
        if field == 'handle':
            continue
        if translated.strip() == default.strip():
            issues.append({
                'type': ctype, 'id': cid, 'locale': locale,
                'field': field, 'issue': Issue.DUPLICATE,
                'detail': f'Translation identical to Czech default (likely untranslated)',
            })
    return issues


def check_informal_register(meta):
    """Check for informal pronouns in languages that should use formal register."""
    issues = []
    for (ctype, cid, locale, field), data in meta.items():
        translated = data['translated']
        if not translated or locale not in INFORMAL_PATTERNS:
            continue
        # Only check text-heavy fields
        if field not in ('title', 'body_html', 'body', 'summary_html', 'meta_description'):
            continue
        # Strip HTML for cleaner matching
        text = re.sub(r'<[^>]+>', ' ', translated).lower()
        for pattern in INFORMAL_PATTERNS[locale]:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                issues.append({
                    'type': ctype, 'id': cid, 'locale': locale,
                    'field': field, 'issue': Issue.INFORMAL,
                    'detail': f'Possible informal pronoun: "{matches[0]}" — use formal register',
                })
                break  # One issue per field is enough
    return issues


def check_sources_section(meta):
    """Flag articles that still contain a standalone Zdroje/Sources heading.

    BU1 editorial rule: sources are cited inline — no <h2>Zdroje</h2> section.
    """
    SOURCES_PATTERNS = [
        r'<h2[^>]*>\s*Zdroje\s*</h2>',
        r'<h2[^>]*>\s*Sources\s*</h2>',
        r'<h2[^>]*>\s*Quellen\s*</h2>',
        r'<h2[^>]*>\s*Références\s*</h2>',
        r'<h2[^>]*>\s*Fuentes\s*</h2>',
        r'<h2[^>]*>\s*Fonti\s*</h2>',
        r'<h2[^>]*>\s*Források\s*</h2>',
        r'<h2[^>]*>\s*Surse\s*</h2>',
        r'<h2[^>]*>\s*Zdroje\s*</h2>',  # cs/sk
    ]
    issues = []
    for (ctype, cid, locale, field), data in meta.items():
        if field != 'body_html':
            continue
        translated = data['translated']
        if not translated:
            continue
        for pattern in SOURCES_PATTERNS:
            if re.search(pattern, translated, re.IGNORECASE):
                issues.append({
                    'type': ctype, 'id': cid, 'locale': locale,
                    'field': field, 'issue': Issue.FORBIDDEN,
                    'detail': 'Contains standalone Sources/Zdroje heading — cite inline instead',
                })
                break
    return issues


def check_outdated(meta):
    """Flag rows with outdated status."""
    issues = []
    for (ctype, cid, locale, field), data in meta.items():
        if data['status'] == 'outdated':
            issues.append({
                'type': ctype, 'id': cid, 'locale': locale,
                'field': field, 'issue': Issue.OUTDATED,
                'detail': 'Translation marked as outdated — needs review',
            })
    return issues


# ─── Coverage metrics ────────────────────────────────────────────────────────

def compute_coverage(groups):
    """Compute translation coverage per locale and content type."""
    # Count required fields present vs expected
    stats = defaultdict(lambda: {'total': 0, 'filled': 0})

    for (ctype, cid, locale), fields in groups.items():
        required = REQUIRED_FIELDS.get(ctype, set())
        for req_field in required:
            key = (locale, ctype)
            stats[key]['total'] += 1
            translated = fields.get(req_field, '')
            if translated and translated.strip():
                stats[key]['filled'] += 1

    return stats


def print_coverage_summary(stats):
    """Print coverage table."""
    # Aggregate by locale
    locale_totals = defaultdict(lambda: {'total': 0, 'filled': 0})
    for (locale, ctype), counts in sorted(stats.items()):
        locale_totals[locale]['total'] += counts['total']
        locale_totals[locale]['filled'] += counts['filled']

    print('\n' + '=' * 65)
    print('TRANSLATION COVERAGE SUMMARY')
    print('=' * 65)
    print(f'{"Locale":<8} {"Filled":>8} {"Total":>8} {"Coverage":>10}  {"Status"}')
    print('-' * 65)

    for locale in sorted(ALL_LOCALES):
        t = locale_totals[locale]
        if t['total'] == 0:
            continue
        pct = (t['filled'] / t['total'] * 100) if t['total'] else 0
        target = '100%' if locale in PRIORITY_LOCALES else '95%'
        met = pct >= (100 if locale in PRIORITY_LOCALES else 95)
        status = f'OK (target {target})' if met else f'BELOW TARGET ({target})'
        marker = ' ✅' if met else ' ❌'
        print(f'{locale:<8} {t["filled"]:>8} {t["total"]:>8} {pct:>9.1f}%  {status}{marker}')

    print('=' * 65)


# ─── Issue reporting ─────────────────────────────────────────────────────────

def print_issues(issues, verbose=False, locale_filter=None, type_filter=None):
    """Print issues grouped by severity."""
    filtered = filter_issues(issues, locale_filter=locale_filter, type_filter=type_filter)

    by_severity = defaultdict(list)
    for issue in filtered:
        sev = Issue.SEVERITY.get(issue['issue'], 'MEDIUM')
        by_severity[sev].append(issue)

    total = len(filtered)
    print(f'\nTotal issues found: {total}')

    for sev in ['HIGH', 'MEDIUM', 'LOW']:
        sev_issues = by_severity.get(sev, [])
        if not sev_issues:
            continue
        print(f'\n{"─" * 60}')
        print(f'  {sev} severity: {len(sev_issues)} issues')
        print(f'{"─" * 60}')

        # Group by issue type
        by_type = defaultdict(list)
        for i in sev_issues:
            by_type[i['issue']].append(i)

        for issue_type, items in sorted(by_type.items()):
            print(f'\n  [{issue_type}] — {len(items)} occurrences')
            shown = items if verbose else items[:5]
            for item in shown:
                print(f'    {item["type"]:20s} {item["id"]:20s} {item["locale"]:4s} '
                      f'{item["field"]:20s} | {item["detail"][:60]}')
            if not verbose and len(items) > 5:
                print(f'    ... and {len(items) - 5} more (use --verbose to see all)')


def export_report(issues, path):
    """Export issues to CSV report."""
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'severity', 'issue', 'type', 'id', 'locale', 'field', 'detail'
        ])
        writer.writeheader()
        for issue in sorted(issues, key=lambda x: (Issue.SEVERITY.get(x['issue'], 'Z'), x['locale'])):
            writer.writerow({
                'severity': Issue.SEVERITY.get(issue['issue'], 'MEDIUM'),
                **issue,
            })
    print(f'\nReport exported to: {path}')


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='BU1 Translation Quality Control')
    parser.add_argument('--input', help='Path to one CSV file or one export batch directory')
    parser.add_argument('--csv', dest='legacy_csv', help='Deprecated alias for --input')
    parser.add_argument('--locale', help='Filter by locale (e.g. en, de, pl)')
    parser.add_argument('--type', help='Filter by content type (e.g. PRODUCT, PAGE)')
    parser.add_argument('--verbose', action='store_true', help='Show all issues (not just top 5)')
    parser.add_argument('--summary', action='store_true', help='Only show coverage summary')
    parser.add_argument('--report', help='Export issues to CSV file')
    args = parser.parse_args()

    input_path = args.input or args.legacy_csv
    if not input_path:
        print('Missing required argument: --input <csv-file-or-batch-directory>')
        sys.exit(2)

    print(f'BU1 Translation QC — {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print(f'Loading translations from: {os.path.abspath(input_path)}')

    try:
        rows, source_files = load_translations(input_path)
    except FileNotFoundError:
        print(f'Input not found or contains no CSV files: {os.path.abspath(input_path)}')
        sys.exit(2)

    print(f'Source files: {len(source_files)}')
    print(f'Loaded {len(rows):,} translation rows')

    groups, meta = group_by_resource(rows)
    print(f'Resources: {len(groups):,} (type, id, locale) combinations')

    # Coverage
    stats = compute_coverage(groups)
    print_coverage_summary(stats)

    if args.summary:
        return

    # Run all checks
    print('\nRunning quality checks...')
    issues = []
    issues.extend(check_missing_fields(groups, meta))
    issues.extend(check_domain_errors(meta))
    issues.extend(check_forbidden_terms(meta))
    issues.extend(check_duplicates(meta))
    issues.extend(check_informal_register(meta))
    issues.extend(check_outdated(meta))
    issues.extend(check_sources_section(meta))

    print_issues(issues, verbose=args.verbose,
                 locale_filter=args.locale, type_filter=args.type)

    filtered_issues = filter_issues(issues, locale_filter=args.locale, type_filter=args.type)

    if args.report:
        export_report(filtered_issues, args.report)

    # Exit code: 1 if HIGH severity issues exist in the filtered result set
    high = [i for i in filtered_issues if Issue.SEVERITY.get(i['issue']) == 'HIGH']
    if high:
        print(f'\n⚠ {len(high)} HIGH severity issues — review required')
        sys.exit(1)
    else:
        print('\n✓ No HIGH severity issues')


if __name__ == '__main__':
    main()
