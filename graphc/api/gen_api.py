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

TARGETS = {
    ("tennis", "v0.14", "v014"): {
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
    is_tennis = game == "tennis"
    mod = f"AIA_Comp_Libry.{game}.{ver}"
    lines = [
        f'"""Author API for target ({game!r}, {version!r}) — GENERATED, do not edit.',
        "",
        "Import this in bot projects instead of raw api.* strings:",
        f"    import {mod} as t",
        "The compiler maps these to the same ops as the api.* calls.",
        '"""',
        "from __future__ import annotations",
        "",
        f"TARGET = ({game!r}, {version!r})",
        "",
        "_SENSORS = {",
    ]
    for name in sorted(table):
        kind, label = table[name]
        lines.append(f"    {name!r}: ({kind!r}, {label!r}),")
    lines += ["}", ""]
    for name in sorted(table):
        kind, label = table[name]
        ret = {"bool": "bool", "float": "float"}.get(kind, "object")
        lines += [
            f"def {name}() -> {ret}:",
            f'    """Sensor {label!r} ({kind}). Compile-time only."""',
            "    raise RuntimeError('author stub: compile with graphc')",
            "",
        ]
    if is_tennis:
        lines += [
            "def move(x: float, z: float, swing=None, shot=None, "
            "sprint=None) -> None:",
            '    """Tennis controller. Compile-time only."""',
            "    raise RuntimeError('author stub: compile with graphc')",
            "",
            "def move_vec(v, swing=None, shot=None, sprint=None) -> None:",
            '    """Tennis vector controller. Compile-time only."""',
            "    raise RuntimeError('author stub: compile with graphc')",
            "",
        ]
    else:
        lines += [
            "def move(x: float, z: float) -> None:",
            '    """Soccer controller. Compile-time only."""',
            "    raise RuntimeError('author stub: compile with graphc')",
            "",
        ]
    lines.append("")
    return "\n".join(lines), table


def main() -> None:
    pkg = os.path.join(HERE, "AIA_Comp_Libry")
    for (game, version, ver), kinds in TARGETS.items():
        src, table = build(game, version, ver, kinds)
        gdir = os.path.join(pkg, game)
        os.makedirs(gdir, exist_ok=True)
        for init in (os.path.join(pkg, "__init__.py"),
                     os.path.join(gdir, "__init__.py")):
            if not os.path.exists(init):
                with open(init, "w", encoding="utf-8", newline="\n") as f:
                    f.write('"""AIA_Comp_Libry author API (generated stubs)."""\n')
        dst = os.path.join(gdir, ver + ".py")
        with open(dst, "w", encoding="utf-8", newline="\n") as f:
            f.write(src)
        print(f"AIA_Comp_Libry.{game}.{ver}: {len(table)} sensors")


if __name__ == "__main__":
    main()
