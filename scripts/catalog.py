"""Shared standard-library-only catalog utilities."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def load():
    return json.loads((ROOT / 'data/tools.json').read_text(encoding='utf-8'))

def taxonomy():
    return json.loads((ROOT / 'data/taxonomy.json').read_text(encoding='utf-8'))

def link(tool):
    if tool['repository']:
        return f"[{tool['name']}]({tool['repository']})"
    return tool['name']

def table(tools):
    rows = ['| Tool | Capability | Verification | Readiness |', '|---|---|---|---|']
    for t in sorted(tools, key=lambda x: x['name'].casefold()):
        rows.append(f"| {link(t)} | {', '.join(t['capabilities'])} | {t['verification']} | {t['enterprise_readiness']} |")
    return '\n'.join(rows)
