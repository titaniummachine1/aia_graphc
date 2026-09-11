import json
import os
import subprocess
import sys

sys.path.insert(0, r'C:\gitProjects\aia_graphc')
from graphc import compile_project

BACKEND = r'C:\gitProjects\aia_graphc\target\release\graphc-rs.exe'
ROOT = r'C:\gitProjects\aia_graphc\examples\bots'
OUT = r'C:\gitProjects\aia_graphc\examples'

bots = {
    'pusher': os.path.join(ROOT, 'pusher.py'),
    'open_court': os.path.join(ROOT, 'open_court.py'),
    'alternator': os.path.join(ROOT, 'alternator.py'),
    'cross_court': os.path.join(ROOT, 'project', 'entry.py'),
}

for name, path in bots.items():
    src = open(path, encoding='utf-8').read()
    nlines = len(src.splitlines())
    desc = compile_project(path, ('tennis', 'v0.14'))
    dpath = os.path.join(OUT, name + '.desc.json')
    tpath = os.path.join(OUT, name + '.txt')
    json.dump(desc, open(dpath, 'w'))
    proc = subprocess.run([BACKEND, dpath, tpath], capture_output=True, text=True)
    rep = json.loads(proc.stdout.strip() or '{}')
    print(f'=== {name} ({nlines} lines of Python) ===')
    print(f'    ops={len(desc["ops"])}  nodes={rep.get("nodes")}  '
          f'transitions={rep.get("per_tick_transitions")}')
