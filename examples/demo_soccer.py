"""Demo bot compiled with graphc: counter latch + packed array roundtrip.

Pipeline: plain-Python bot source -> AST frontend (graphc.ast_fe) ->
description IR -> graphc-rs backend -> game save. Replayable in the
aia_comp-sim VM (graphc_poc_demo_replays).

Output: examples/graphc_demo_soccer.txt (game save).
Run: python examples/demo_soccer.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from graphc.ast_fe import compile_source  # noqa: E402

BOT_SOURCE = '''
def bot(api):
    cnt = api.var("cnt")
    nxt = cnt + 1
    api.set_var("cnt", nxt)
    buf = api.array("buf", 6)
    api.arr_set(buf, 3, 7.5)
    api.arr_set(buf, 4, 8.5)
    api.arr_set(buf, 5, 9.5)
    val = api.arr_get_dyn(buf, 3 + cnt % 3)
    flag = 1.0
    if cnt > 12:
        flag = 2.0
    api.move(val + flag, nxt)
'''


def build(target=("soccer", "v0.12"), out: str | None = None) -> str:
    here = Path(__file__).parent
    out = out or str(here / "graphc_demo_soccer.txt")
    desc = compile_source(BOT_SOURCE, target)
    desc["bot_name"] = "graphc_demo"
    desc_path = str(here / "graphc_demo.desc.json")
    with open(desc_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(desc, f, separators=(",", ":"))
    repo = Path(__file__).parent.parent
    exe = os.environ.get(
        "GRAPHC_BACKEND", str(repo / "target" / "release" / "graphc-rs.exe"))
    if not os.path.exists(exe):
        subprocess.run(["cargo", "build", "--release", "-q"], cwd=repo, check=True)
    proc = subprocess.run([exe, desc_path, out], check=True,
                          capture_output=True, text=True)
    print(proc.stdout.strip())
    return out


if __name__ == "__main__":
    build()
