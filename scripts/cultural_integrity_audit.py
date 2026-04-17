import json
import csv
import datetime
import os
import re

# Config
GLOSSARY_PATH = '/Users/petrhlavacek/Programming/Shopify AI BU1/config/goalkeeper_glossary.json'
TRANSLATION_FILES = [
    'products_translations.json',
    'collections_translations.json',
    'pages_translations.json',
    'links_translations.json'
]
OUTPUT_PATH = f'/Users/petrhlavacek/Programming/Shopify AI BU1/reports/cultural_integrity_audit_{datetime.datetime.now().strftime("%Y%m%d")}.csv'
PRIORITY_LOCALES = ['de', 'hu', 'pl']
ALL_LOCALES = ['de', 'hu', 'pl', 'sk', 'ro', 'hr', 'es', 'it', 'fr', 'bg', 'en']

def load_glossary():
    with open(GLOSSARY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_translations(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return data.get('translatableResources', {}).get('nodes', [])
        except json.JSONDecodeError:
            return []

def audit():
    glossary = load_glossary()
    report = []
    
    # Prepare regex for technical terms check
    # For DE specifically mentioned in the prompt:
    # "Schaumstoff" -> "Haftschaum" (also forbidden)
    # "Schaum" -> "Haftschaum"
    # "Schnitt NC" or "Negative Cut" -> "NC-Schnitt"
    
    for file_name in TRANSLATION_FILES:
        nodes = load_translations(file_name)
        for node in nodes:
            resource_id = node['resourceId']
            
            for locale in ALL_LOCALES:
                translations = node.get(locale, [])
                if not translations:
                    continue
                
                # For sampled locales, we could limit the check, but let's just run it for all since it's fast.
                
                for trans in translations:
                    key = trans['key']
                    value = trans['value']
                    if not value or not isinstance(value, str):
                        continue
                    
                    # 1. Check Forbidden Terms
                    forbidden = glossary.get('forbidden_terms', {}).get(locale, {})
                    for term, reason in forbidden.items():
                        if re.search(r'\b' + re.escape(term) + r'\b', value, re.IGNORECASE):
                            report.append([resource_id, value, value.replace(term, "[FIXME]"), f"Zakázaný termín '{term}' ({locale}): {reason}"])
                    
                    # 2. Technical Correctness (specific rules from prompt + glossary)
                    if locale == 'de':
                        # Haftschaum check
                        if re.search(r'\bSchaum\b', value, re.IGNORECASE) and 'Haftschaum' not in value:
                            report.append([resource_id, value, value.replace('Schaum', 'Haftschaum').replace('schaum', 'haftschaum'), "Glosář: foam_latex -> Haftschaum (nalezeno 'Schaum')"])
                        
                        # NC-Schnitt check
                        if ('Negative Cut' in value or 'negativer Schnitt' in value or 'Schnitt NC' in value) and 'NC-Schnitt' not in value:
                             report.append([resource_id, value, value.replace('Negative Cut', 'NC-Schnitt').replace('negativer Schnitt', 'NC-Schnitt').replace('Schnitt NC', 'NC-Schnitt'), "Glosář: negative_cut -> NC-Schnitt"])

                    # 3. Check for technical terms from glossary that should be used
                    # (This checks if the source term is present but translated differently than glossary)
                    # We look at the source content to see what it's supposed to be.
                    source_content = node.get('translatableContent', [])
                    for source_item in source_content:
                        if source_item['key'] == key:
                            source_val = source_item['value']
                            if not source_val: continue
                            
                            for term_id, langs in glossary.get('terms', {}).items():
                                cs_term = langs.get('cs')
                                if not cs_term: continue
                                
                                if re.search(r'\b' + re.escape(cs_term) + r'\b', source_val, re.IGNORECASE):
                                    expected = langs.get(locale)
                                    if expected and expected.lower() not in value.lower():
                                        # Term found in source but expected translation not in value
                                        # This might have many false positives if synonyms are allowed, 
                                        # but glossary says "primary reference for all translations to ensure professional authority".
                                        report.append([resource_id, f"SRC({locale}): {value}", expected, f"Glosář: {term_id} -> {expected} (Source contains '{cs_term}')"])

    # Remove duplicates from report
    unique_report = []
    seen = set()
    for row in report:
        row_tuple = tuple(row)
        if row_tuple not in seen:
            unique_report.append(row)
            seen.add(row_tuple)

    # Save report
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Resource ID', 'Původní hodnota', 'Navrhovaná hodnota', 'Důvod'])
        writer.writerows(unique_report)
    print(f"Report saved to {OUTPUT_PATH}")

if __name__ == '__main__':
    audit()
