"""graphc AST frontend: parse plain Python bot code -> description IR.

You write normal Python; we parse it with the built-in `ast` module and
compile the syntax tree into the description IR (graphc-desc-v1), which the
Rust backend (graphc-rs) optimizes and emits as a game save.

Supported (v1):
    x = <expr>                    assignments (locals = per-tick values)
    x += <expr>                   augmented ops
    if <cond>: ... else: ...      REAL if: cond evaluated first, both
                                  branches compiled, assigned names merged
                                  with select (SSA phi)
    api.move(x, z)                soccer controller (target soccer)
    api.var("name")               cross-tick read (latch)
    api.set_var("name", expr)     cross-tick write
    buf = api.array("name", n)    packed array handle
    api.arr_set(buf, i, v)        static cell write
    api.arr_get(buf, i)           static cell read
    api.arr_get_dyn(buf, idx)     dynamic cell read (select-chain decode)

Expressions: numbers, names, + - * / % **, single comparisons, unary -,
`not`. Anything else = compile error with the offending snippet. api.* calls
inside if branches are not yet supported (assignments only) — the whitelist
fails loudly, never silently.
"""
from __future__ import annotations

import ast

_BIN = {ast.Add: "AddFloats", ast.Sub: "SubtractFloats",
        ast.Mult: "MultiplyFloats", ast.Div: "DivideFloats",
        ast.Mod: "Modulo", ast.Pow: "Power"}
_CMP = {ast.Lt: "<", ast.Gt: ">", ast.LtE: "<=", ast.GtE: ">=",
        ast.Eq: "==", ast.NotEq: "!="}


class _Ctx:
    def __init__(self, target):
        self.target = target
        self.ops: list[dict] = []
        self._env: dict[str, int] = {}
        self._cse: dict = {}
        self._in_branch = False

    def _desc(self, v: float) -> int:
        key = ("const", float(v))
        if key not in self._cse:
            self._cse[key] = len(self.ops)
            self.ops.append({"op": "const", "value": float(v)})
        return self._cse[key]

    def _emit(self, op: dict) -> int:
        key = tuple(sorted((k, str(v)) for k, v in op.items() if k != "op"))
        key = (op["op"],) + key
        if key not in self._cse:
            self._cse[key] = len(self.ops)
            self.ops.append(op)
        return self._cse[key]


def _expr(ctx: _Ctx, node: ast.expr) -> int:
    if isinstance(node, ast.Constant):
        if not isinstance(node.value, (int, float)):
            raise SyntaxError(f"only numeric constants, got {node.value!r}")
        return ctx._desc(float(node.value))
    if isinstance(node, ast.Name):
        if node.id not in ctx._env:
            raise SyntaxError(f"name {node.id!r} used before assignment")
        return ctx._env[node.id]
    if isinstance(node, ast.BinOp):
        fn = _BIN.get(type(node.op))
        if fn is None:
            raise SyntaxError(f"unsupported operator {type(node.op).__name__}")
        return ctx._emit({"op": "bin", "fn": fn, "a": _expr(ctx, node.left),
                          "b": _expr(ctx, node.right)})
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return ctx._emit({"op": "bin", "fn": "SubtractFloats",
                              "a": ctx._desc(0.0), "b": _expr(ctx, node.operand)})
        if isinstance(node.op, ast.Not):
            return ctx._emit({"op": "not", "b": _expr(ctx, node.operand)})
        raise SyntaxError(f"unsupported unary {type(node.op).__name__}")
    if isinstance(node, ast.Compare):
        if len(node.ops) != 1:
            raise SyntaxError("chained comparisons unsupported")
        cmp = _CMP.get(type(node.ops[0]))
        if cmp is None:
            raise SyntaxError(f"unsupported comparison {type(node.ops[0]).__name__}")
        return ctx._emit({"op": "bin", "fn": "CompareFloats",
                          "a": _expr(ctx, node.left),
                          "b": _expr(ctx, node.comparators[0]), "cmp": cmp})
    if isinstance(node, ast.Call):
        return _api_call(ctx, node)
    raise SyntaxError(f"unsupported expression: {ast.unparse(node)[:80]!r}")


def _api_call(ctx: _Ctx, node: ast.Call) -> int:
    if not isinstance(node.func, ast.Name) or not node.func.id.startswith("api."):
        raise SyntaxError(
            f"untraceable call {ast.unparse(node)[:60]!r} — only api.* calls "
            "are supported (the game-API whitelist)")
    if ctx._in_branch:
        raise SyntaxError(
            "api.* calls inside if branches not supported yet — only "
            "assignments merge; hoist the call")
    fn = node.func.id[4:]
    args = node.args
    if fn == "var":
        (name,) = args
        return ctx._emit({"op": "var_get", "name": ast.literal_eval(name)})
    if fn == "set_var":
        name, v = args
        ctx.ops.append({"op": "var_set", "name": ast.literal_eval(name),
                        "v": _expr(ctx, v)})
        return ctx._desc(0.0)
    if fn == "array":
        name, cells = args
        op_id = len(ctx.ops)
        ctx.ops.append({"op": "array", "name": ast.literal_eval(name),
                        "cells": ast.literal_eval(cells)})
        return op_id
    if fn == "arr_set":
        arr, i, v = args
        ctx.ops.append({"op": "array_set_static", "arr": _expr(ctx, arr),
                        "i": ast.literal_eval(i), "v": _expr(ctx, v)})
        return ctx._desc(0.0)
    if fn == "arr_get":
        arr, i = args
        return ctx._emit({"op": "array_get_static", "arr": _expr(ctx, arr),
                          "i": ast.literal_eval(i)})
    if fn == "arr_get_dyn":
        arr, i = args
        return ctx._emit({"op": "array_get_dynamic", "arr": _expr(ctx, arr),
                          "i": _expr(ctx, i)})
    raise SyntaxError(f"unknown api function {fn!r}")


def _stmt(ctx: _Ctx, s: ast.stmt) -> None:
    if isinstance(s, ast.Assign):
        if len(s.targets) != 1 or not isinstance(s.targets[0], ast.Name):
            raise SyntaxError("only single-name assignments")
        ctx._env[s.targets[0].id] = _expr(ctx, s.value)
    elif isinstance(s, ast.AugAssign):
        if not isinstance(s.target, ast.Name):
            raise SyntaxError("augmented assign to non-name")
        name = s.target.id
        if name not in ctx._env:
            raise SyntaxError(f"name {name!r} used before assignment")
        fn = _BIN.get(type(s.op))
        if fn is None:
            raise SyntaxError(f"unsupported operator {type(s.op).__name__}")
        ctx._env[name] = ctx._emit({"op": "bin", "fn": fn, "a": ctx._env[name],
                                    "b": _expr(ctx, s.value)})
    elif isinstance(s, ast.If):
        cond = _expr(ctx, s.test)
        env_saved = dict(ctx._env)
        ctx._in_branch = True
        _block(ctx, s.body)
        env_true = dict(ctx._env)
        ctx._env = env_saved
        _block(ctx, s.orelse)
        env_false = dict(ctx._env)
        ctx._in_branch = False
        # SSA phi: every name differing between branches merges via select
        for name in set(env_true) | set(env_false):
            t = env_true.get(name, env_saved.get(name))
            f = env_false.get(name, env_saved.get(name))
            if t != f:
                ctx._env[name] = ctx._emit({"op": "select", "c": cond,
                                            "t": t, "f": f})
    elif isinstance(s, ast.Expr):
        _expr(ctx, s.value)
    else:
        raise SyntaxError(
            f"unsupported statement {type(s).__name__} — dynamic while/for/"
            "imports are not compilable; express state across ticks with "
            "api.set_var")


def _block(ctx: _Ctx, stmts: list[ast.stmt]) -> None:
    for s in stmts:
        _stmt(ctx, s)


def compile_source(source: str, target: tuple[str, str]) -> dict:
    """Parse plain Python source -> description dict (for graphc-rs)."""
    tree = ast.parse(source)
    fns = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    if len(fns) != 1:
        raise SyntaxError("exactly one bot function expected")
    ctx = _Ctx(target)
    _block(ctx, fns[0].body)
    return {
        "schema": "graphc-desc-v1",
        "target": {"game": target[0], "version": target[1]},
        "bot_name": fns[0].name,
        "ops": ctx.ops,
    }