"""Description IR (v1) — the language-neutral bot description.

Frontends (Python tracing, later Rust tracing) record ops into this format;
the graphc Rust backend optimizes it and emits the game save. Nothing here
touches node JSON — that is the backend's job.

Op set (SSA-ish; ids are line numbers):
  {"op":"const","value":f32}
  {"op":"var_get","name":str}
  {"op":"var_set","name":str,"v":id}
  {"op":"bin","fn":AddFloats|SubtractFloats|MultiplyFloats|DivideFloats|
        Modulo|Power|CompareFloats,"a":id,"b":id,"cmp":str?}
  {"op":"not","b":id}
  {"op":"select","c":id,"t":id,"f":id}
  {"op":"array","name":str,"cells":n}            -> handle id
  {"op":"array_set_static","arr":id,"i":n,"v":id}
  {"op":"array_get_static","arr":id,"i":n}
   {"op":"array_get_dynamic","arr":id,"i":id}
   {"op":"soccer_move","x":id,"z":id}             (target soccer)
   {"op":"tennis_get","kind":bool|float|vector3|transform,
    "index":n,"label":str}                        (target tennis)
   {"op":"tennis_move","x":id,"z":id,"swing":id|null,
    "shot":id|null,"sprint":id|null}              (target tennis)
   {"op":"tennis_aim","x":id,"z":id}              aim request: AutoAim ->
    AutoMove(V32) for the NEXT tennis_move in the same tick (walk target
    stays on the move wire — the game switches strike aim without
    touching how you walk).                       (target tennis)
   {"op":"tennis_auto_swing","shot":id} -> bool   game swing node
    (Prefer Charge): hold builds charge, release strikes. (target tennis)
   {"op":"vec_split","v":id,"i":0|1|2}            vector component -> float
    (x=0, y=1, z=2; e.g. latch "Legal Serve Target" components in vars)
   {"op":"vec_make","x":id,"y":id,"z":id}         3 floats -> vector handle
   {"op":"tennis_move_vec","v":id,"swing":id|null,
    "shot":id|null,"sprint":id|null}              (target tennis)
   {"op":"soccer_get","kind":bool|float|vector3|transform,
    "index":n,"label":str}                         (target soccer)
   {"op":"transform_pos","v":id}                 RelativePosition(World):
    transform -> world position vector (api.pos_of)
   {"op":"plot","name":str,"v":id}               TimePlot debug sink
    (all targets incl. universal — observable in game, sim, pure VM)
Output description:
  {"schema":"graphc-desc-v1","target":{"game":..,"version":..},
   "bot_name":str,"ops":[...]}
"""
from __future__ import annotations

_TENNIS_GET_NODES = {
    "bool": "TennisGetBool",
    "float": "TennisGetFloat",
    "vector3": "TennisGetVector3",
    "transform": "TennisGetTransform",
}

#: Pinned (game, version) targets with a game-API surface. ("universal",
#: any version) is the raw-emission fallback: no game API, only const /
#: arithmetic / vars / arrays. Anything else fails loudly at trace time
#: AND in the backend — version strings are never silently accepted.
#: ("tennis","v15f") is accepted with v0.14-identical nodes (assumed until
#: measured — user directive 2026-09-11); it is also the tennis LATEST.
SUPPORTED_TARGETS = frozenset({("soccer", "v0.12"), ("tennis", "v0.14"),
                               ("tennis", "v15f")})

#: Game -> latest version string.
LATEST_TARGETS = {"tennis": "v15f", "soccer": "v0.12"}


def check_target(target: tuple[str, str]) -> None:
    """Reject unknown (game, version) pairs loudly.

    ("universal", <anything>) passes (raw nodes only — the game-API
    helpers reject it per-call). Everything outside SUPPORTED_TARGETS +
    universal raises TypeError listing what exists.
    """
    if (
        isinstance(target, tuple)
        and len(target) == 2
        and target[0] == "universal"
        and isinstance(target[1], str)
    ):
        return
    if target in SUPPORTED_TARGETS:
        return
    raise TypeError(
        f"unknown target {target!r} — supported: "
        f"{sorted(SUPPORTED_TARGETS)} plus (\"universal\", <version>) "
        "(raw node emission only, no game API)"
    )


def tennis_sensor_index(kind: str, label: str, version: str = "v0.14") -> tuple[int, str]:
    """Dropdown label -> builder-order index (what graph JSON modifiers mean).

    v15f resolves through the v0.14 tables (assumed node-identical until
    measured). Unknown versions fail loudly.
    """
    from AIGamePyLibrary.data import DROPDOWN_OPTIONS

    if version not in ("v0.14", "v15f"):
        raise KeyError(f"unknown tennis sensor tables for version {version!r}")
    node = _TENNIS_GET_NODES.get(kind)
    if node is None:
        raise KeyError(f"unknown tennis sensor kind {kind!r}")
    opts = DROPDOWN_OPTIONS[node]
    if label not in opts:
        raise KeyError(f"{label!r} is not a {node} sensor label; options: {opts}")
    return opts.index(label), label


_SOCCER_GET_NODES = {
    "bool": "SoccerGetBool",
    "float": "SoccerGetFloat",
    "vector3": "SoccerGetVector3",
    "transform": "SoccerGetTransform",
}


def soccer_sensor_index(kind: str, label: str) -> tuple[int, str]:
    """Soccer dropdown label -> builder-order index.

    The Rust backend lowers soccer_get like tennis_get; the sim resolves
    the numeric modifier through its own tables (same order — Team
    Player 1 == 1 on both sides), and rejects unknown labels loudly.
    """
    from AIGamePyLibrary.data import DROPDOWN_OPTIONS

    node = _SOCCER_GET_NODES.get(kind)
    if node is None:
        raise KeyError(f"unknown soccer sensor kind {kind!r}")
    opts = DROPDOWN_OPTIONS[node]
    if label not in opts:
        raise KeyError(f"{label!r} is not a {node} sensor label; options: {opts}")
    return opts.index(label), label


class Sym:
    """Traced value: description op id or folded constant."""
    __slots__ = ("ctx", "op_id", "const")

    def __init__(self, ctx, op_id=None, const=None):
        self.ctx = ctx
        self.op_id = op_id
        self.const = const

    def _binop(self, fn, other, swap=False):
        a = self.ctx._desc(self)
        b = self.ctx._desc(other)
        if swap:
            a, b = b, a
        return self.ctx._emit({"op": "bin", "fn": fn, "a": a, "b": b})

    def __add__(self, o): return self._binop("AddFloats", o)
    __radd__ = __add__

    def __sub__(self, o): return self._binop("SubtractFloats", o)

    def __rsub__(self, o): return self._binop("SubtractFloats", o, swap=True)

    def __mul__(self, o): return self._binop("MultiplyFloats", o)
    __rmul__ = __mul__

    def __truediv__(self, o): return self._binop("DivideFloats", o)

    def __rtruediv__(self, o): return self._binop("DivideFloats", o, swap=True)

    def __mod__(self, o): return self._binop("Modulo", o)

    def __rmod__(self, o): return self._binop("Modulo", o, swap=True)

    def __pow__(self, o): return self._binop("Power", o)

    def __neg__(self):
        return self.ctx.const(0.0) - self

    def _cmp(self, other, op: str):
        a = self.ctx._desc(self)
        b = self.ctx._desc(other)
        return self.ctx._emit({"op": "bin", "fn": "CompareFloats",
                               "a": a, "b": b, "cmp": op})

    def __lt__(self, o): return self._cmp(o, "<")

    def __gt__(self, o): return self._cmp(o, ">")

    def __le__(self, o): return self._cmp(o, "<=")

    def __ge__(self, o): return self._cmp(o, ">=")

    def __eq__(self, o): return self._cmp(o, "==")

    def __ne__(self, o):
        return self.ctx._emit({"op": "not", "b": self._cmp(o, "==")})


class GraphCtx:
    def __init__(self, target: tuple[str, str]):
        check_target(target)
        self.target = target
        self.ops: list[dict] = []
        self._cse: dict = {}
        self._arrays: list[PackedArray] = []

    def _desc(self, v) -> int:
        if isinstance(v, Sym):
            if v.op_id is not None:
                return v.op_id
            return self.const(float(v.const)).op_id
        return self.const(float(v)).op_id

    def const(self, v: float) -> Sym:
        key = ("const", float(v))
        op_id = self._cse.get(key)
        if op_id is None:
            op_id = len(self.ops)
            self.ops.append({"op": "const", "value": float(v)})
            self._cse[key] = op_id
        return Sym(self, op_id=op_id)

    def _emit(self, op: dict) -> Sym:
        key = tuple(sorted(op.items()))
        op_id = self._cse.get(key)
        if op_id is None:
            op_id = len(self.ops)
            self.ops.append(op)
            self._cse[key] = op_id
        return Sym(self, op_id=op_id)

    # --- memory -----------------------------------------------------------
    def var_get(self, name: str) -> Sym:
        return self._emit({"op": "var_get", "name": name})

    def var_set(self, name: str, value) -> None:
        self.ops.append({"op": "var_set", "name": name, "v": self._desc(value)})

    # --- control flow -------------------------------------------------------
    def select(self, cond, t, f) -> Sym:
        return self._emit({"op": "select", "c": self._desc(cond),
                           "t": self._desc(t), "f": self._desc(f)})

    # --- game surface (version-pinned; validated against targets) -----------
    def soccer_move(self, x, z) -> None:
        if self.target[0] != "soccer":
            raise TypeError(f"soccer_move is not valid for target {self.target}")
        self.ops.append({"op": "soccer_move", "x": self._desc(x),
                         "z": self._desc(z)})

    def _require_tennis(self) -> None:
        if self.target[0] != "tennis":
            raise TypeError(f"tennis API is not valid for target {self.target}")

    def tennis_get(self, kind: str, label: str) -> Sym:
        """Sensor read by dropdown label; the index is resolved at trace time
        against AIGamePyLibrary's DROPDOWN_OPTIONS (the builder order the
        graph JSON means). Both are recorded: index authoritative, label for
        reviewable descs."""
        self._require_tennis()
        idx, label = tennis_sensor_index(kind, label)
        return self._emit({"op": "tennis_get", "kind": kind,
                           "index": idx, "label": label})

    def tennis_move(self, x, z, swing=None, shot=None, sprint=None) -> None:
        """TennisController: Vector31 (move-to / on-hit aim from x,z),
        Bool1 swing/charge, Float1 shot type, Bool2 sprint (optional)."""
        self._require_tennis()
        self.ops.append({
            "op": "tennis_move",
            "x": self._desc(x), "z": self._desc(z),
            "swing": None if swing is None else self._desc(swing),
            "shot": None if shot is None else self._desc(shot),
            "sprint": None if sprint is None else self._desc(sprint),
        })

    def tennis_move_vec(self, v, swing=None, shot=None, sprint=None) -> None:
        """TennisController driven by a prebuilt vector (vec_make handle or
        tennis_get vector3/transform) instead of x/z floats."""
        self._require_tennis()
        self.ops.append({
            "op": "tennis_move_vec",
            "v": self._desc(v),
            "swing": None if swing is None else self._desc(swing),
            "shot": None if shot is None else self._desc(shot),
            "sprint": None if sprint is None else self._desc(sprint),
        })

    def tennis_aim(self, x, z) -> None:
        """Aim request for the NEXT tennis_move in the same tick: the
        backend routes it through TennisAutoAim into TennisAutoMove(V32)
        while the move wire keeps the walk target (autoswitch — walk
        destination unaffected, strikes land on the aim)."""
        self._require_tennis()
        self.ops.append({
            "op": "tennis_aim",
            "x": self._desc(x), "z": self._desc(z),
        })

    def tennis_auto_swing(self, shot, mode: str = "Prefer Charge") -> Sym:
        """Game swing node: returns the swing bool — hold builds charge,
        release strikes (mode: Normal Only | Prefer Charge | Random).
        Wire it into the move's swing."""
        self._require_tennis()
        return self._emit({"op": "tennis_auto_swing",
                           "shot": self._desc(shot), "mode": mode})

    # --- soccer surface -----------------------------------------------------
    def _require_soccer(self) -> None:
        if self.target[0] != "soccer":
            raise TypeError(f"soccer API is not valid for target {self.target}")

    def soccer_get(self, kind: str, label: str) -> Sym:
        """Sensor read by dropdown label (bool/float/vector3/transform);
        index resolved against the game tables, recorded alongside."""
        self._require_soccer()
        idx, label = soccer_sensor_index(kind, label)
        typ = {"vector3": "vector", "transform": "transform"}.get(kind, kind)
        return self._emit({"op": "soccer_get", "kind": kind,
                           "index": idx, "label": label})

    def transform_pos(self, v) -> Sym:
        """World position vector out of a transform (RelativePosition)."""
        return self._emit({"op": "transform_pos", "v": self._desc(v)})

    # --- vectors ------------------------------------------------------------
    def vec_split(self, v, i: int) -> Sym:
        """Vector component -> float (i: 0=x, 1=y, 2=z). The backend shares
        one Vector3Split node per source vector; each component is CSE'd."""
        if int(i) not in (0, 1, 2):
            raise ValueError(f"vec_split component must be 0/1/2, got {i!r}")
        return self._emit({"op": "vec_split", "v": self._desc(v),
                           "i": int(i)})

    def vec_make(self, x, y, z) -> Sym:
        """3 floats -> opaque vector handle (backend: ConstructVector3)."""
        return self._emit({"op": "vec_make", "x": self._desc(x),
                           "y": self._desc(y), "z": self._desc(z)})

    # --- debug sinks --------------------------------------------------------
    def plot(self, name: str, value) -> None:
        """TimePlot debug sink: {"op":"plot","name":str,"v":id}.

        Channel name is a static string (part of the save, not a value);
        the plotted value is any float. Repeatable, all targets including
        universal — the channel is observable in game (TimePlot export),
        sim, and pure VM, which makes it the compiler-verification surface.
        """
        if not isinstance(name, str) or not name:
            raise TypeError(f"plot channel must be a non-empty str, got {name!r}")
        self.ops.append({"op": "plot", "name": name, "v": self._desc(value)})

    # --- arrays -------------------------------------------------------------
    def array(self, name: str, cells: int) -> "PackedArray":
        arr = PackedArray(self, name, cells)
        self._arrays.append(arr)
        return arr

    def array_decl(self, name: str, cells: int) -> int:
        op_id = len(self.ops)
        self.ops.append({"op": "array", "name": name, "cells": cells})
        return op_id

    def finish(self) -> dict:
        for arr in self._arrays:
            arr.flush()
        return {
            "schema": "graphc-desc-v1",
            "target": {"game": self.target[0], "version": self.target[1]},
            "ops": self.ops,
        }


class PackedArray:
    """Fixed-capacity array; the backend chooses the packing (Vector3 cells,
    merged static writes). The writer never sees components."""

    def __init__(self, ctx: GraphCtx, name: str, cells: int):
        self.ctx = ctx
        self.op_id = ctx.array_decl(name, cells)
        self.cells = cells

    def set_static(self, i: int, value) -> None:
        self.ctx.ops.append({"op": "array_set_static", "arr": self.op_id,
                             "i": int(i), "v": self.ctx._desc(value)})

    def get_static(self, i: int) -> Sym:
        return self.ctx._emit({"op": "array_get_static", "arr": self.op_id,
                               "i": int(i)})

    def get_dynamic(self, idx) -> Sym:
        return self.ctx._emit({"op": "array_get_dynamic", "arr": self.op_id,
                               "i": self.ctx._desc(idx)})


def describe(target: tuple[str, str], builder) -> dict:
    """Trace `builder(ctx)` once for (game, version) -> description dict."""
    ctx = GraphCtx(target)
    builder(ctx)
    return ctx.finish()


# --- gcc-inspired peephole passes: cost = per-tick node transitions --------
_REF_KEYS = ("a", "b", "c", "t", "f", "v", "x", "z", "swing", "shot",
             "sprint", "arr", "i")
# Per-op fields that LOOK like ints but are literals, never op refs.
_LITERAL_KEYS = {
    "array_set_static": {"i"},
    "array_get_static": {"i"},
    "vec_split": {"i"},
}
# Side-effect sinks: DCE roots. Everything else must feed a sink.
_SINKS = {"var_set", "array_set_static", "soccer_move", "tennis_move",
          "tennis_move_vec", "tennis_aim", "plot"}


def _refs(op: dict):
    lit = _LITERAL_KEYS.get(op["op"], set())
    for k in _REF_KEYS:
        v = op.get(k)
        if isinstance(v, int) and k not in lit:
            yield k, v


def optimize_ops(ops: list[dict], level: int = 1) -> list[dict]:
    """Semantics-preserving transition shavers (no arithmetic folding —
    float rounding must stay bit-identical to per-tick game evaluation).

    - select-fold: select(c, t, t) -> t (both arms evaluate per tick, so a
      same-value select is pure waste).
    - DCE: drop ops unreachable from side-effect sinks (dead sensors,
      orphaned consts, folded selects).
    """
    if level < 1:
        return ops
    ops = [dict(o) for o in ops]
    changed = True
    while changed:
        changed = False
        rep = {}
        for i, o in enumerate(ops):
            if o["op"] == "select" and o["t"] == o["f"]:
                rep[i] = o["t"]
                changed = True
        if rep:
            def resolve(v):
                while isinstance(v, int) and v in rep:
                    v = rep[v]
                return v

            for o in ops:
                for k, v in _refs(o):
                    o[k] = resolve(v)
    live: set[int] = set()
    stack = [i for i, o in enumerate(ops) if o["op"] in _SINKS]
    while stack:
        i = stack.pop()
        if i in live:
            continue
        live.add(i)
        for _, v in _refs(ops[i]):
            if v not in live:
                stack.append(v)
    keep = sorted(live)
    remap = {old: new for new, old in enumerate(keep)}
    out = []
    for old in keep:
        o = dict(ops[old])
        for k, v in _refs(o):
            o[k] = remap[v]
        out.append(o)
    return out