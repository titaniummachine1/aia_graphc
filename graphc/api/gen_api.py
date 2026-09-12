"""Generate per-(game,version) author API stubs from the fork's tables.

Reads AIGamePyLibrary DROPDOWN_OPTIONS (the sensor ABI ground truth) and
emits graphc/api/<game>_<version>.py: one typed function per sensor label
(mangled to snake_case) plus the game controller. The compiler resolves
`from tennis_v014 import ball_incoming` to the same ops as the equivalent
api.* call, so stubs and compiler agree by construction (same source).

Usage: GRAPHC_PYLIB pointed at the fork; python graphc/api/gen_api.py
"""
from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

PYLIB = os.environ.get(
    "GRAPHC_PYLIB", r"C:\gitProjects\AIA_tennis\AIGamePyLibrary")
if PYLIB not in sys.path:
    sys.path.insert(0, PYLIB)

from AIGamePyLibrary.data import DROPDOWN_OPTIONS  # noqa: E402
from descriptions import (  # noqa: E402
    SOCCER_MOVE_DOC,
    TENNIS_AIM_DOC,
    TENNIS_AUTO_SWING_DOC,
    TENNIS_MOVE_DOC,
    TENNIS_MOVE_VEC_DOC,
    describe,
)

TARGETS = {
    ("tennis", "v0.14", "v014"): {
        "bool": "TennisGetBool",
        "float": "TennisGetFloat",
        "vector3": "TennisGetVector3",
        "transform": "TennisGetTransform",
    },
    # v15f assumed node-identical to v0.14 (user directive 2026-09-11:
    # measure later). It is also the tennis LATEST.
    ("tennis", "v15f", "v15f"): {
        "bool": "TennisGetBool",
        "float": "TennisGetFloat",
        "vector3": "TennisGetVector3",
        "transform": "TennisGetTransform",
    },
    ("soccer", "v0.12", "v012"): {
        "bool": "SoccerGetBool",
        "float": "SoccerGetFloat",
        "vector3": "SoccerGetVector3",
        "transform": "SoccerGetTransform",
    },
}

#: Game -> latest version module (unversioned imports resolve here).
LATEST = {"tennis": "v15f", "soccer": "v012"}

ASSUMED = {("tennis", "v15f"): "v0.14"}

#: Measured renames the fork table does not know yet: stub name ->
#: (kind, fork label it resolves to). Same dropdown index (order
#: preserved), so the game reads the identical sensor — the new name only
#: matches upstream docs + real-bot saves (titanium54).
#: "Center Of Legal Serve Area" == legacy "Legal Serve Target" (upstream
#: README: both players read the same world point from it).
EXTRA_ALIASES = {
    ("tennis", "v15f"): {
        "center_of_legal_serve_area": ("vector3", "Legal Serve Target"),
    },
}


def mangle(label: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")
    if re.match(r"^[0-9]", s):
        s = "n_" + s
    return s or "sensor"


def build(game: str, version: str, ver: str, kinds: dict) -> str:
    table: dict[str, tuple[str, str]] = {}
    for kind, node in kinds.items():
        for label in DROPDOWN_OPTIONS[node]:
            name = mangle(label)
            if name in table:
                name = f"{kind}_{name}"
            if name in table:
                raise ValueError(f"mangle collision on {label!r} ({game})")
            table[name] = (kind, label)
    for name, (kind, label) in EXTRA_ALIASES.get((game, version), {}).items():
        if name in table:
            raise ValueError(f"alias collision on {name!r} ({game} {version})")
        table[name] = (kind, label)
    is_tennis = game == "tennis"
    mod = f"AIA_Comp_Libry.{game}.{ver}"
    assumed = ASSUMED.get((game, ver))
    lines = [
        f'"""Author API for target ({game!r}, {version!r}) — GENERATED, do not edit.',
        "",
        "Simple to use (humans + LLMs): import this module, call its",
        "functions as plain values, and pass them to move()/move_vec().",
        "You NEVER wire nodes, ports, or connections — the compiler assigns",
        "every value a type (float/bool/vector/transform), checks every",
        "connection, and emits the game save. Illegal wiring (bool into",
        "arithmetic, vector into a float slot, transform into vec_split,",
        "float where bool is needed) fails at compile time, loudly.",
        "",
        "Types: float = number, bool = true/false, vector = 3D point",
        "(split with api.vec_split or feed move_vec), transform = placed",
        "object (opaque: Self/Opponent/Ball — pick a vector3 sensor instead).",
        "",
    ]
    if assumed:
        lines += [
            f"Assumed node-identical to {assumed} until measured.",
            "",
        ]
    lines += [
        "Import this in bot projects instead of raw api.* strings:",
        f"    import {mod} as t",
        "The compiler maps these to the same ops as the api.* calls.",
        '"""',
        "from __future__ import annotations",
        "",
        f"TARGET = ({game!r}, {version!r})",
        "",
        "class Vector3:",
        '    """Opaque 3D point: split via api.vec_split(v, 0/1/2) or feed',
        "    t.move_vec(v). Never arithmetic directly.\"\"\"",
        "",
        "class Transform:",
        '    """Opaque placed object (Self/Opponent/Ball): cannot split or',
        '    do math on it; use a vector3 sensor instead."""',
        "",
        "_SENSORS = {",
    ]
    for name in sorted(table):
        kind, label = table[name]
        lines.append(f"    {name!r}: ({kind!r}, {label!r}),")
    lines += ["}", ""]
    ctrls = ["move", "move_vec"] if is_tennis else ["move"]
    lines.append(
        f"__all__ = [{', '.join(repr(n) for n in sorted(table) + ctrls)}]")
    lines.append("")
    for name in sorted(table):
        kind, label = table[name]
        ret = {"bool": "bool", "float": "float", "vector3": "Vector3",
               "transform": "Transform"}.get(kind, "float")
        node = {"bool": "GetBool", "float": "GetFloat",
                "vector3": "GetVector3", "transform": "GetTransform"}[kind]
        lines += [
            f"def {name}() -> {ret}:",
            f'    """{describe(game, kind, label)}',
            "",
            f"    Returns: {kind} (game node "
            f"{'Tennis' if is_tennis else 'Soccer'}{node}).",
            f"    Game label: {label!r}.",
            '    Connections are automatic: use the return value directly; '
            "    illegal uses fail at compile time.\"\"\"",
            "    raise RuntimeError('author stub: compile with graphc')",
            "",
        ]
    if is_tennis:
        lines += [
            "def move(x: float, z: float, swing: bool | None = None, "
            "shot: float | None = None, sprint: bool | None = None) -> None:",
            f'    """{TENNIS_MOVE_DOC}',
            "",
            "    Args: x (float court x), z (float court z), swing "
            "(bool|None charge/hit), shot (float|None Shot:* id), sprint "
            "(bool|None). Exactly one controller call per tick.",
            '    Connections are automatic; type mismatches fail loudly."""',
            "    raise RuntimeError('author stub: compile with graphc')",
            "",
            "def move_vec(v: Vector3, swing: bool | None = None, "
            "shot: float | None = None, sprint: bool | None = None) -> None:",
            f'    """{TENNIS_MOVE_VEC_DOC}',
            "",
            "    Args: v (vector from vec_make or a vector3 sensor).",
            '    Connections are automatic; transform input fails loudly."""',
            "    raise RuntimeError('author stub: compile with graphc')",
            "",
            "def aim(x: float, z: float) -> None:",
            f'    """{TENNIS_AIM_DOC}',
            "",
            "    Args: x (float court x), z (float court z).",
            '    Connections are automatic; type mismatches fail loudly."""',
            "    raise RuntimeError('author stub: compile with graphc')",
            "",
            "def auto_swing(shot: float, "
            "mode: str | None = None) -> bool:",
            f'    """{TENNIS_AUTO_SWING_DOC}',
            "",
            "    Args: shot (float Shot:* id), mode (str|None swing mode).",
            '    Connections are automatic; type mismatches fail loudly."""',
            "    raise RuntimeError('author stub: compile with graphc')",
            "",
        ]
    else:
        lines += [
            "def move(x: float, z: float) -> None:",
            f'    """{SOCCER_MOVE_DOC}',
            "",
            "    Args: x (float), z (float). Exactly one call per tick.",
            '    Connections are automatic; type mismatches fail loudly."""',
            "    raise RuntimeError('author stub: compile with graphc')",
            "",
        ]
    lines.append("")
    return "\n".join(lines), table


def main() -> None:
    pkg = os.path.join(HERE, "AIA_Comp_Libry")
    seen_games: dict[str, str] = {}
    for (game, version, ver), kinds in TARGETS.items():
        src, table = build(game, version, ver, kinds)
        gdir = os.path.join(pkg, game)
        os.makedirs(gdir, exist_ok=True)
        if not os.path.exists(os.path.join(pkg, "__init__.py")):
            with open(os.path.join(pkg, "__init__.py"), "w",
                      encoding="utf-8", newline="\n") as f:
                f.write('"""AIA_Comp_Libry author API (generated stubs)."""\n')
        dst = os.path.join(gdir, ver + ".py")
        with open(dst, "w", encoding="utf-8", newline="\n") as f:
            f.write(src)
        print(f"AIA_Comp_Libry.{game}.{ver}: {len(table)} sensors")
        seen_games[game] = LATEST[game]
    for game, latest in seen_games.items():
        init = os.path.join(pkg, game, "__init__.py")
        with open(init, "w", encoding="utf-8", newline="\n") as f:
            f.write(
                '"""AIA_Comp_Libry author API (generated stubs)."""\n'
                f'"""Unversioned {game} resolves to latest ({latest})."""\n'
                f"from .{latest} import *  # noqa: F401,F403\n")


if __name__ == "__main__":
    main()
