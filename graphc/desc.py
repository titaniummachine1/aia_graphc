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


def tennis_sensor_index(kind: str, label: str) -> tuple[int, str]:
    """Dropdown label -> builder-order index (what graph JSON modifiers mean)."""
    from AIGamePyLibrary.data import DROPDOWN_OPTIONS

    node = _TENNIS_GET_NODES.get(kind)
    if node is None:
        raise KeyError(f"unknown tennis sensor kind {kind!r}")
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