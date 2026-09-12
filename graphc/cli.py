"""`python -m graphc` — the one-command front door.

    python -m graphc mybot/entry.py -o mybot.txt --install

does the whole pipeline in one shot: Python source -> description IR ->
`graphc-rs` backend -> game save, and (with `--install`) copies it into the
game's Saves folder so it is loadable by name immediately.

This exists so a bot author never has to know about `graphc-rs`, temp desc
files, or the backend's location: the backend is auto-discovered next to this
checkout (or via `GRAPHC_BACKEND`).

Usage:
    python -m graphc <entry.py|project_dir> [options]

Options:
    -o, --out PATH      save output (default: <entry stem>.txt)
    --target G:V        game:version (default tennis:v15f; e.g. soccer:v0.12)
    -O, --optimize M    raw|o0|o1|o2 (default: o0 for source, o2 for saves)
    --desc PATH         also write the intermediate description JSON
    --install           copy the save into the game Saves dir
    --backend PATH      graphc-rs path (else GRAPHC_BACKEND / target/release)
    -q, --quiet         only print the final save path
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def find_backend(explicit: str | None) -> str:
    if explicit:
        return explicit
    env = os.environ.get("GRAPHC_BACKEND")
    if env:
        return env
    for cand in (
        os.path.join(ROOT, "target", "release", "graphc-rs.exe"),
        os.path.join(ROOT, "target", "release", "graphc-rs"),
        os.path.join(ROOT, "target", "debug", "graphc-rs.exe"),
        os.path.join(ROOT, "target", "debug", "graphc-rs"),
    ):
        if os.path.isfile(cand):
            return cand
    return "graphc-rs"  # rely on PATH


def saves_dir(game: str) -> str:
    base = os.path.join(os.path.expanduser("~"), "AppData", "LocalLow",
                        "Unicorn One", "AIComp", "Saves")
    return os.path.join(base, "Tennis" if game == "tennis" else "Soccer")


def parse_target(raw: str) -> tuple[str, str]:
    if ":" in raw:
        game, _, ver = raw.partition(":")
        return game.strip(), ver.strip()
    # bare game name -> its default pinned version
    defaults = {"tennis": "v15f", "soccer": "v0.12"}
    if raw in defaults:
        return raw, defaults[raw]
    if raw == "universal":
        return "universal", "v1"
    raise SystemExit(f"target must be game:version (e.g. tennis:v15f), got {raw!r}")


def resolve_entry(path: str) -> str:
    if os.path.isdir(path):
        cand = os.path.join(path, "entry.py")
        if not os.path.isfile(cand):
            raise SystemExit(f"no entry.py in {path}")
        return cand
    return path


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(prog="graphc", add_help=True,
                                 description="compile a Python bot into a game save")
    ap.add_argument("entry", help="entry .py or a project dir containing entry.py")
    ap.add_argument("-o", "--out", default=None, help="save output path")
    ap.add_argument("--target", default="tennis:v15f",
                    help="game:version (default tennis:v15f)")
    ap.add_argument("-O", "--optimize", default=None,
                    help="raw|o0|o1|o2 (default o0)")
    ap.add_argument("--desc", default=None, help="also write the description JSON")
    ap.add_argument("--install", action="store_true",
                    help="copy the save into the game Saves dir")
    ap.add_argument("--backend", default=None, help="graphc-rs path")
    ap.add_argument("-q", "--quiet", action="store_true")
    a = ap.parse_args(argv)

    entry = resolve_entry(a.entry)
    if not os.path.isfile(entry):
        raise SystemExit(f"no such entry file: {entry}")
    target = parse_target(a.target)
    optimize = a.optimize or "o0"
    out = a.out or (os.path.splitext(os.path.basename(entry))[0] + ".txt")

    from .ast_fe import compile_project

    desc = compile_project(entry, target, optimize)

    backend = find_backend(a.backend)
    if os.path.sep in backend and not os.path.isfile(backend):
        raise SystemExit(f"backend not found: {backend}")

    if a.desc:
        with open(a.desc, "w", encoding="utf-8") as f:
            json.dump(desc, f)
        if not a.quiet:
            print(f"desc  {a.desc}")

    # Backend takes a desc file (or a save for compaction). Use a temp desc.
    fd, tmp = tempfile.mkstemp(suffix=".desc.json")
    os.close(fd)
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(desc, f)
        cmd = [backend, tmp, out]
        if a.optimize:
            cmd.append(a.optimize)
        proc = subprocess.run(cmd, capture_output=True, text=True)
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass

    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout)
        return proc.returncode

    if not a.quiet:
        print(f"save  {os.path.abspath(out)}")
        report = (proc.stderr or proc.stdout).strip()
        if report:
            print(f"build {report}")
        # Measured v15f ceiling 2026-09-12: 12288-trip loop (24589
        # traversals / size 36889 / 37 MB) plays, 16384-trip (32781 /
        # 49177 / 50 MB) dies on load. Loud but non-fatal: the compiler
        # stays out of the way, the author owns the risk past this line.
        trans = None
        for line in ((proc.stderr or "") + "\n" + (proc.stdout or "")).splitlines()[::-1]:
            try:
                trans = json.loads(line).get("per_tick_transitions")
                break
            except Exception:
                continue
        if isinstance(trans, int) and trans > 26000:
            print(f"graphc warning: {trans} connection traversals per tick "
                  f"is past the proven-danger line (~26k traversals / "
                  f"~40 MB size v15f) — expect load-crash territory; "
                  f"verify in game before shipping",
                  file=sys.stderr)

    if a.install:
        dest_dir = saves_dir(target[0])
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, os.path.basename(out))
        with open(out, "rb") as src, open(dest, "wb") as dst:
            dst.write(src.read())
        if not a.quiet:
            print(f"installed -> {dest}")
            print(f"  load it in the node editor as \"{os.path.splitext(os.path.basename(out))[0]}\"")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
