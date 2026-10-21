"""Regenerate catalog Markdown deterministically."""
import argparse
import sys
from catalog import ROOT,load,table

parser=argparse.ArgumentParser()
parser.add_argument('--check',action='store_true',help='Fail if generated Markdown is stale')
args=parser.parse_args()
items=load()
changes=[]
for team in ('red','blue','purple'):
    subset=[t for t in items if team in t['teams']]
    content=f'# {team.title()} Team Tools\n\n> Imported entries are unverified until reviewed. Repository URLs are candidate links.\n\n{len(subset)} entries\n\n'+table(subset)+'\n'
    path=ROOT/'docs'/f'{team}-team.md'
    if not path.exists() or path.read_text(encoding='utf-8')!=content:
        changes.append(str(path.relative_to(ROOT)))
        if not args.check: path.write_text(content,encoding='utf-8')
readme=ROOT/'README.md'
old=readme.read_text(encoding='utf-8')
start='<!-- CATALOG:START -->';end='<!-- CATALOG:END -->'
if old.count(start)!=1 or old.count(end)!=1: raise SystemExit('README catalog markers missing or duplicated')
summary=f'**{len(items)} tools** currently listed. All imported entries are unverified.\n\n'+table(items)
new=old.split(start)[0]+start+'\n\n'+summary+'\n\n'+end+old.split(end,1)[1]
if new!=old:
    changes.append('README.md')
    if not args.check: readme.write_text(new,encoding='utf-8')
if args.check and changes:
    print('Generated files stale: '+', '.join(changes));sys.exit(1)
print('Generated files up to date' if not changes else 'Updated: '+', '.join(changes))
