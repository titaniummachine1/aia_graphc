"""Serve-latch parity bot: the compiler's take on the sim's ServeAimHint latch.

Session-9b8af82 model (aia_comp-sim/src/tennis/world.rs): at ServeSetup
entry the world latches the server's live Vector31 IF it lies inside the
legal diagonal serve box, else falls back to the box center; the serve
strike uses the latch, never the live Toss-phase stance output.

This bot expresses the same latch in source code: it reads the
"Legal Serve Target" sensor vector, splits it into components, and holds
them in cross-tick vars. During serve phase it outputs the LIVE target
components (so the world's latch sees an in-box candidate and honors it);
outside serve phase it holds the latched values.

Pipeline: BOT_SOURCE -> ast_fe.compile_source -> graphc-rs -> save.
Run: python examples/demo_serve_latch.py
Output: examples/graphc_serve_latch.txt (game save).
Replay: copy into %USERPROFILE%\\AppData\\LocalLow\\Unicorn One\\AIComp\\
Saves\\Tennis\\graphc_serve_latch.txt, then in the sim repo run
`cargo run --release --bin tennis_tournament -- --home graphc_serve_latch
--away "" --seed 7 --points 4` and compare faults/double_faults against
the non-latching demo (graphc_demo_tennis).
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
    # Live legal-serve-target components (the in-box candidate).
    tgt = api.tennis_get_vector3("Legal Serve Target")
    tx = api.vec_split(tgt, 0)
    tz = api.vec_split(tgt, 2)
    # Previous-tick latch (cross-tick RAM).
    prev_x = api.var("serve_x")
    prev_z = api.var("serve_z")
    # Serve phase covers ServeSetup (where the world latches) + Toss.
    serving = api.tennis_get_bool("Is Serve Phase")
    if serving:
        aim_x = tx
        aim_z = tz
    else:
        aim_x = prev_x
        aim_z = prev_z
    api.set_var("serve_x", aim_x)
    api.set_var("serve_z", aim_z)
    swing = api.tennis_get_bool("Ball In Swing Range")
    api.tennis_move(aim_x, aim_z, swing, 2.0)
'''


def build(target=("tennis", "v0.14"), out: str | None = None) -> str:
    here = Path(__file__).parent
    out = out or str(here / "graphc_serve_latch.txt")
    desc = compile_source(BOT_SOURCE, target)
    desc["bot_name"] = "graphc_serve_latch"
    desc_path = str(here / "graphc_serve_latch.desc.json")
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
