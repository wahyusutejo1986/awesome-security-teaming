"""Validate catalog data without network calls or external packages."""
import re
import sys
from urllib.parse import urlparse
from catalog import load, taxonomy

REQUIRED = {'id','name','description','teams','capabilities','primary_use','repository','homepage','license','deployment','integrations','attack_techniques','maintenance','enterprise_readiness','verification','last_verified','notes','source_dataset'}

def validate():
    errors=[]
    items=load()
    tax=taxonomy()
    if not isinstance(items,list): return ['Catalog must be a JSON array']
    seen=set()
    for index,t in enumerate(items,1):
        where=f'item {index}'
        if not isinstance(t,dict): errors.append(f'{where}: not an object');continue
        missing=REQUIRED-set(t)
        if missing: errors.append(f'{where}: missing {sorted(missing)}');continue
        ident=t['id'];where=ident
        if not isinstance(ident,str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',ident): errors.append(f'{where}: invalid id')
        if ident in seen: errors.append(f'{where}: duplicate id')
        seen.add(ident)
        for key in ('name','description','primary_use','license','notes','source_dataset'):
            if not isinstance(t[key],str): errors.append(f'{where}: {key} must be string')
        for key in ('teams','capabilities','deployment','integrations','attack_techniques'):
            if not isinstance(t[key],list) or any(not isinstance(v,str) for v in t[key]): errors.append(f'{where}: {key} must be list of strings')
        for key in ('teams','capabilities'):
            if isinstance(t[key],list):
                if not t[key]: errors.append(f'{where}: {key} must not be empty')
                if len(t[key])!=len(set(t[key])): errors.append(f'{where}: duplicate {key}')
                for v in t[key]:
                    if v not in tax[key]: errors.append(f'{where}: invalid {key} value {v}')
        for key in ('maintenance','enterprise_readiness','verification'):
            if t[key] not in tax[key]: errors.append(f'{where}: invalid {key} value')
        for key in ('repository','homepage'):
            v=t[key]
            if v is not None and (not isinstance(v,str) or urlparse(v).scheme!='https' or not urlparse(v).netloc): errors.append(f'{where}: invalid {key} HTTPS URL')
        date=t['last_verified']
        if date is not None and (not isinstance(date,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',date)): errors.append(f'{where}: last_verified must be YYYY-MM-DD or null')
        if t['verification']=='verified' and not date: errors.append(f'{where}: verified requires last_verified')
        if t['enterprise_readiness']!='not-assessed' and t['verification']!='verified': errors.append(f'{where}: readiness requires verification')
    return errors

if __name__=='__main__':
    issues=validate()
    if issues:
        print('\n'.join('ERROR: '+e for e in issues));sys.exit(1)
    print(f'OK: {len(load())} tools validated')
