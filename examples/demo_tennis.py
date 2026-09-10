"""Demo: plain-Python tennis bot compiled via AST -> description -> graphc-rs.

Run: python examples/demo_tennis.py
Output: examples/graphc_demo_tennis.txt (game save, replayed by the sim CI)

Serve-latch shape (the compiler's take on the sim's §4B diagnosis): aim is
select-merged between the serve target and a neutral court position, keyed
on the serve-phase sensor.
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
    serving = api.tennis_get_bool("Is Self Actively Serving")
    serve_no = api.tennis_get_float("Serve Number")
    if serving:
        aim_x = -1.6
        # Second serve aims shorter.
        aim_z = 10.5 - serve_no * 0.5
    else:
        aim_x = 0.0
        aim_z = 11.0
    swing = api.tennis_get_bool("Ball In Swing Range")
    api.tennis_move(aim_x, aim_z, swing, 2.0)
'''


def build(target=("tennis", "v0.14"), out: str | None = None) -> str:
    here = Path(__file__).parent
    out = out or str(here / "graphc_demo_tennis.txt")
    desc = compile_source(BOT_SOURCE, target)
    desc["bot_name"] = "graphc_demo_tennis"
    desc_path = str(here / "graphc_demo_tennis.desc.json")
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
