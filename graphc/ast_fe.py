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
    api.move(x, z)                soccer controller (target soccer)
    api.tennis_get_bool/float/vector3/transform(label)   sensors (tennis)
    api.tennis_move(x, z, swing=None, shot=None, sprint=None)  (tennis)
    api.tennis_move_vec(v, swing=None, shot=None, sprint=None) (tennis)
    api.vec_split(v, i)           vector component -> float (i: 0=x,1=y,2=z)
    api.vec_make(x, y, z)         3 floats -> vector (feeds tennis_move_vec)

Expressions: numbers, names, + - * / % **, single comparisons, unary -,
`not`. Anything else = compile error with the offending snippet. api.* calls
inside if branches are not yet supported (assignments only) — the whitelist
fails loudly, never silently.

Multi-file projects: compile_project(entry_path, target) resolves local
imports (import mod / from mod import name — sibling .py files, packages via
mod/__init__.py) and inlines every project function at its call sites, so an
organized codebase compiles to the same graph as one flat script. Only the
api.* surface + project-defined names are visible; any other import or
global fails loudly (whitelist). Exactly one bot function per project: tick
if defined, else the single top-level function.
"""
from __future__ import annotations

import ast
import os

_BIN = {ast.Add: "AddFloats", ast.Sub: "SubtractFloats",
        ast.Mult: "MultiplyFloats", ast.Div: "DivideFloats",
        ast.Mod: "Modulo", ast.Pow: "Power"}
_CMP = {ast.Lt: "<", ast.Gt: ">", ast.LtE: "<=", ast.GtE: ">=",
        ast.Eq: "==", ast.NotEq: "!="}

_TENNIS_KINDS = {"tennis_get_bool": "bool", "tennis_get_float": "float",
                 "tennis_get_vector3": "vector3",
                 "tennis_get_transform": "transform"}

#: Target-bound author modules: import AIA_Comp_Libry.tennis.v014 as t.
#: The (game, version) path must match the compile target or it fails loudly
#: (version pinning). Supported forms:
#:   import AIA_Comp_Libry.tennis.v014 as t   (+ t.sensor())
#:   from AIA_Comp_Libry.tennis.v014 import sensor (+ sensor())
#:   from AIA_Comp_Libry.tennis import v014      (+ v014.sensor())
LIBRY = "AIA_Comp_Libry"


def _norm_ver(v: str) -> str:
    return "".join(c for c in v.lower() if c.isalnum())


def _libry_key(dotted: str) -> tuple[str, str] | None:
    """AIA_Comp_Libry.<game>.<ver> -> (game, ver-normalized), else None."""
    parts = dotted.split(".")
    if len(parts) == 3 and parts[0] == LIBRY:
        return parts[1].lower(), _norm_ver(parts[2])
    return None


def _target_sensors(game: str, ver: str) -> dict:
    import importlib
    try:
        mod = importlib.import_module(
            f".api.{LIBRY}.{game}.{ver}", package=__package__)
    except ImportError:
        raise SyntaxError(
            f"unknown API module {LIBRY}.{game}.{ver} — regenerate the stubs")
    return mod._SENSORS

# Env marker for the api namespace passed as a helper argument: attribute
# calls (api.*) bypass the env, bare value-use fails loudly in _expr.
_API_MARKER = -1


class _Ctx:
    def __init__(self, target):
        from .desc import check_target
        check_target(target)
        self.target = target
        self.ops: list[dict] = []
        self._env: dict[str, int] = {}
        self._cse: dict = {}
        self._in_branch = False
        # Project scope: (module, name) -> FunctionDef, local name -> module
        # prefix ("" = current module, "api" = builtin game-API namespace).
        self._functions: dict = {}
        self._imports: dict[str, str] = {}
        self._active: set = set()

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
        v = ctx._env[node.id]
        if v == _API_MARKER:
            raise SyntaxError(
                "the api namespace is not a value — call api.* functions")
        return v
    if isinstance(node, ast.BinOp):
        fn = _BIN.get(type(node.op))
        if fn is None:
            raise SyntaxError(f"unsupported operator {type(node.op).__name__}")
        return ctx._emit({"op": "bin", "fn": fn, "a": _expr(ctx, node.left),
                          "b": _expr(ctx, node.right)})
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            v = _const_number(node.operand)
            if v is not None:
                return ctx._desc(-v)
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
        try:
            return _api_call(ctx, node)
        except SyntaxError as e:
            if "whitelist" not in str(e):
                raise
            return _project_call(ctx, node)
    raise SyntaxError(f"unsupported expression: {ast.unparse(node)[:80]!r}")


def _project_call(ctx: _Ctx, node: ast.Call) -> int:
    """Inline a project-defined function call (helper, not api.*)."""
    func = node.func
    mod: str | None = None
    name: str | None = None
    if isinstance(func, ast.Name):
        target = ctx._imports.get(func.id)
        if target and target.startswith("api."):
            # from api import move -> rewrite to api.move(...)
            node = ast.Call(
                func=ast.Attribute(value=ast.Name(id="api"),
                                   attr=target[4:]),
                args=node.args, keywords=node.keywords)
            return _api_call(ctx, node)
        if target and target.startswith("@"):
            # from AIA_Comp_Libry.tennis.v014 import ball_incoming
            game, _, rest = target[1:].partition("/")
            ver, _, tfn = rest.partition(".")
            return _targetmod_call(ctx, node, game, ver, tfn)
        if target and "." in target:
            mod, _, name = target.partition(".")
        else:
            name = func.id
    elif (isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name)
            and func.value.id in ctx._imports):
        mod = ctx._imports[func.value.id] or None
        name = func.attr
        if mod and mod.startswith("@"):
            # t.sensor() where t is import AIA_Comp_Libry.tennis.v014 as t
            game, _, rest = mod[1:].partition("/")
            ver, _, _ = rest.partition(".")
            return _targetmod_call(ctx, node, game, ver, name)
    if name is None:
        raise SyntaxError(
            f"untraceable call {ast.unparse(node)[:60]!r} — only api.* calls "
            "and project-defined functions are supported (whitelist)")
    if mod is not None:
        quals = [(mod, name)]
    else:
        quals = [(m, name) for (m, n) in ctx._functions if n == name]
    if len(quals) != 1:
        raise SyntaxError(
            f"untraceable call {ast.unparse(node)[:60]!r} — only api.* calls "
            "are supported (the game-API whitelist)")
    qual = quals[0]
    if qual in ctx._active:
        raise SyntaxError(f"recursive call to {qual!r} is not compilable")
    fdef = ctx._functions[qual]
    params = [a.arg for a in fdef.args.args]
    if fdef.args.vararg or fdef.args.kwarg:
        raise SyntaxError(f"*{fdef.args.vararg and 'args' or 'kwargs'} in "
                          f"{qual!r} is not compilable")
    if len(node.args) > len(params) or node.keywords:
        raise SyntaxError(f"bad call arity/keywords for {qual!r}")
    if len(node.args) < len(params):
        missing = len(params) - len(node.args)
        defaults = fdef.args.defaults
        if len(defaults) < missing:
            raise SyntaxError(f"missing arguments for {qual!r}")
    saved_env = dict(ctx._env)
    ctx._active.add(qual)
    try:
        for i, p in enumerate(params):
            if i < len(node.args):
                a = node.args[i]
                if isinstance(a, ast.Name) and a.id == "api" \
                        and "api" not in ctx._env:
                    ctx._env[p] = _API_MARKER
                else:
                    ctx._env[p] = _expr(ctx, a)
            else:
                d = fdef.args.defaults[i - (len(params) - len(fdef.args.defaults))]
                ctx._env[p] = _expr(ctx, d)
        ret = None
        for s in fdef.body:
            if isinstance(s, ast.Return):
                if ret is not None:
                    raise SyntaxError(f"multiple return in {qual!r}")
                ret = _expr(ctx, s.value) if s.value is not None else ctx._desc(0.0)
            else:
                _stmt(ctx, s)
        if ret is None:
            raise SyntaxError(f"function {qual!r} has no return")
        return ret
    finally:
        ctx._active.remove(qual)
        ctx._env = saved_env


def _targetmod_call(ctx: _Ctx, node: ast.Call, game: str, ver: str,
                    fn: str) -> int:
    """AIA_Comp_Libry.tennis.v014.ball_incoming() -> the tennis_get op."""
    if game != ctx.target[0] or ver != _norm_ver(ctx.target[1]):
        raise SyntaxError(
            f"API module {LIBRY}.{game}.{ver} does not match compile target "
            f"{ctx.target}")
    game_c = game
    if fn in ("move", "move_vec"):
        try:
            real = {"tennis": {"move": "tennis_move",
                               "move_vec": "tennis_move_vec"},
                    "soccer": {"move": "move"}}[game_c][fn]
        except KeyError:
            raise SyntaxError(f"api.{fn} is not valid for target {ctx.target}")
        return _api_call(ctx, ast.Call(
            func=ast.Attribute(value=ast.Name(id="api"), attr=real),
            args=node.args, keywords=node.keywords))
    sensors = _target_sensors(game, ver)
    if fn not in sensors:
        raise SyntaxError(
            f"unknown {LIBRY}.{game}.{ver}.{fn} — regenerate the api stubs")
    kind, label = sensors[fn]
    if game_c == "tennis":
        from .desc import tennis_sensor_index
        idx, lab = tennis_sensor_index(kind, label)
        return ctx._emit({"op": "tennis_get", "kind": kind,
                          "index": idx, "label": lab})
    from .desc import soccer_sensor_index
    idx, lab = soccer_sensor_index(kind, label)
    return ctx._emit({"op": "soccer_get", "kind": kind,
                      "index": idx, "label": lab})


def _api_call(ctx: _Ctx, node: ast.Call) -> int:
    func = node.func
    if (isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name)):
        base = func.value.id
        alias = ctx._imports.get(base, base if base == "api" else None)
        if alias is None or (base != "api" and alias == base):
            raise SyntaxError(
                f"untraceable call {ast.unparse(node)[:60]!r} — only api.* "
                "calls are supported (the game-API whitelist)")
        if alias == "api" or base == "api":
            fn = func.attr
        elif alias.startswith("@"):
            # "@game/ver" (module alias; fn takes func.attr) or
            # "@game/ver.fn" (from-imported sensor).
            game, _, rest = alias[1:].partition("/")
            ver, _, fn = rest.partition(".")
            return _targetmod_call(ctx, node, game, ver, fn or func.attr)
        else:
            raise SyntaxError(
                f"untraceable call {ast.unparse(node)[:60]!r} — only api.* "
                "calls are supported (the game-API whitelist)")
    elif isinstance(func, ast.Name) and func.id.startswith("api."):
        fn = func.id[4:]
    else:
        raise SyntaxError(
            f"untraceable call {ast.unparse(node)[:60]!r} — only api.* calls "
            "are supported (the game-API whitelist)")
    if ctx._in_branch:
        raise SyntaxError(
            "api.* calls inside if branches not supported yet — only "
            "assignments merge; hoist the call")
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
    if fn == "move":
        if ctx.target[0] != "soccer":
            raise SyntaxError(f"api.move is not valid for target {ctx.target}")
        x, z = args
        ctx.ops.append({"op": "soccer_move", "x": _expr(ctx, x),
                        "z": _expr(ctx, z)})
        return ctx._desc(0.0)
    if fn in _TENNIS_KINDS:
        if ctx.target[0] != "tennis":
            raise SyntaxError(
                f"api.{fn} is not valid for target {ctx.target}")
        (label,) = args
        kind = _TENNIS_KINDS[fn]
        from .desc import tennis_sensor_index
        idx, lab = tennis_sensor_index(kind, ast.literal_eval(label))
        return ctx._emit({"op": "tennis_get", "kind": kind,
                          "index": idx, "label": lab})
    if fn == "tennis_move":
        if ctx.target[0] != "tennis":
            raise SyntaxError(
                f"api.tennis_move is not valid for target {ctx.target}")
        if not 2 <= len(args) <= 5:
            raise SyntaxError(
                "api.tennis_move(x, z, swing=None, shot=None, sprint=None)")
        opt = [None if a is None or (isinstance(a, ast.Constant)
                                     and a.value is None) else _expr(ctx, a)
               for a in args[2:]]
        x, z = _expr(ctx, args[0]), _expr(ctx, args[1])
        ctx.ops.append({
            "op": "tennis_move", "x": x, "z": z,
            "swing": opt[0] if len(opt) > 0 else None,
            "shot": opt[1] if len(opt) > 1 else None,
            "sprint": opt[2] if len(opt) > 2 else None,
        })
        return ctx._desc(0.0)
    if fn == "tennis_move_vec":
        if ctx.target[0] != "tennis":
            raise SyntaxError(
                f"api.tennis_move_vec is not valid for target {ctx.target}")
        if not 1 <= len(args) <= 4:
            raise SyntaxError(
                "api.tennis_move_vec(v, swing=None, shot=None, sprint=None)")
        opt = [None if a is None or (isinstance(a, ast.Constant)
                                     and a.value is None) else _expr(ctx, a)
               for a in args[1:]]
        ctx.ops.append({
            "op": "tennis_move_vec", "v": _expr(ctx, args[0]),
            "swing": opt[0] if len(opt) > 0 else None,
            "shot": opt[1] if len(opt) > 1 else None,
            "sprint": opt[2] if len(opt) > 2 else None,
        })
        return ctx._desc(0.0)
    if fn == "vec_split":
        v, i = args
        idx = ast.literal_eval(i)
        if idx not in (0, 1, 2):
            raise SyntaxError(
                f"api.vec_split component must be 0/1/2, got {idx!r}")
        return ctx._emit({"op": "vec_split", "v": _expr(ctx, v), "i": idx})
    if fn == "vec_make":
        x, y, z = args
        return ctx._emit({"op": "vec_make", "x": _expr(ctx, x),
                          "y": _expr(ctx, y), "z": _expr(ctx, z)})
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
    elif isinstance(s, ast.Return):
        raise SyntaxError(
            "return is only allowed inside helper functions (tick is void)")
    else:
        raise SyntaxError(
            f"unsupported statement {type(s).__name__} — dynamic while/for "
            "are not compilable; express state across ticks with "
            "api.set_var")


def _block(ctx: _Ctx, stmts: list[ast.stmt]) -> None:
    for s in stmts:
        _stmt(ctx, s)


def compile_source(source: str, target: tuple[str, str], opt: int = 1) -> dict:
    """Parse plain Python source -> description dict (for graphc-rs).

    Helpers are allowed: the bot function is `tick` when defined, else the
    single top-level function (same rule as compile_project).
    opt: 0 = raw ops, 1 = transition-shaving passes (DCE, select-fold).
    """
    return _assemble({"": ast.parse(source)}, [""], target, opt)


def _load_module(path: str) -> ast.Module:
    with open(path, encoding="utf-8") as f:
        return ast.parse(f.read(), filename=path)


def _resolve_file(base_dir: str, dotted: str) -> str:
    """Sibling module file for `dotted` (mod.py or mod/__init__.py)."""
    parts = dotted.split(".")
    cand = os.path.join(base_dir, *parts) + ".py"
    if os.path.isfile(cand):
        return cand
    cand = os.path.join(base_dir, *parts, "__init__.py")
    if os.path.isfile(cand):
        return cand
    raise SyntaxError(f"import {dotted!r} is not a project file (whitelist)")


def compile_project(entry: str, target: tuple[str, str], opt: int = 1) -> dict:
    """Compile a whole project: entry .py + its local imports.

    Every project function is inlined at its call sites, so the output is
    identical to a hand-flattened single script (verify by diffing descs).
    The bot function is `tick` when defined, else the single top-level
    function. `import api` / `from api import x` address the builtin
    game-API namespace; every other import must resolve to a project file.
    opt: 0 = raw ops, 1 = transition-shaving passes (DCE, select-fold).
    """
    entry = os.path.abspath(entry)
    base_dir = os.path.dirname(entry)
    modules: dict[str, ast.Module] = {"": _load_module(entry)}
    order = [""]
    # Fixed-point import crawl (cycles fail loudly at the end).
    seen_files = {entry}
    i = 0
    while i < len(order):
        mod = order[i]
        i += 1
        tree = modules[mod]
        for s in tree.body:
            if isinstance(s, ast.Import):
                for a in s.names:
                    if a.name == "api" or a.name == LIBRY or \
                            a.name.startswith(LIBRY + "."):
                        continue
                    fp = _resolve_file(base_dir, a.name)
                    key = a.asname or a.name
                    if fp not in seen_files:
                        seen_files.add(fp)
                        modules[key] = _load_module(fp)
                        order.append(key)
            elif isinstance(s, ast.ImportFrom):
                if s.module == "api" or (s.module or "").startswith("api.") \
                        or (s.module or "") == LIBRY \
                        or (s.module or "").startswith(LIBRY + ".") \
                        or _libry_key(s.module or ""):
                    continue
                if s.level:
                    raise SyntaxError("relative imports are not compilable")
                fp = _resolve_file(base_dir, s.module or "")
                if fp not in seen_files:
                    seen_files.add(fp)
                    modules[s.module or ""] = _load_module(fp)
                    order.append(s.module or "")
    return _assemble(modules, order, target, opt)


def _const_number(node: ast.expr) -> float | None:
    """Numeric literal value (incl. unary minus), else None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        v = _const_number(node.operand)
        return None if v is None else -v
    return None


def _assemble(modules: dict[str, ast.Module], order: list[str],
              target: tuple[str, str], opt: int = 1) -> dict:
    ctx = _Ctx(target)
    # Register functions + import aliases per module.

    def _alias(key: str, val: str, where: str) -> None:
        if key in ctx._imports and ctx._imports[key] != val:
            raise SyntaxError(
                f"conflicting import alias {key!r} ({where})")
        ctx._imports[key] = val

    for mod in order:
        tree = modules[mod]
        for s in tree.body:
            if isinstance(s, ast.FunctionDef):
                if (mod, s.name) in ctx._functions:
                    raise SyntaxError(f"duplicate function {s.name!r}")
                ctx._functions[(mod, s.name)] = s
            elif isinstance(s, ast.Import):
                for a in s.names:
                    if a.name == "api":
                        _alias("api", "", "api")
                    elif _libry_key(a.name):
                        if not a.asname:
                            raise SyntaxError(
                                f"import {a.name!r} needs 'as' "
                                "(e.g. import AIA_Comp_Libry.tennis.v014 as t)")
                        game, ver = _libry_key(a.name)
                        _alias(a.asname, f"@{game}/{ver}", "libry")
                    else:
                        _alias(a.asname or a.name, a.name, "import")
            elif isinstance(s, ast.ImportFrom):
                if _libry_key(s.module or ""):
                    game, ver = _libry_key(s.module or "")
                    for a in s.names:
                        if a.name == "*":
                            raise SyntaxError(
                                "star imports are not compilable")
                        _alias(a.asname or a.name, f"@{game}/{ver}.{a.name}",
                               "libry-from-import")
                elif (s.module or "") == LIBRY or \
                        (s.module or "").startswith(LIBRY + "."):
                    # from AIA_Comp_Libry.tennis import v014
                    parts = (s.module or "").split(".")
                    if len(parts) != 2 or parts[0] != LIBRY:
                        raise SyntaxError(
                            f"import {s.module!r}: use the full "
                            "AIA_Comp_Libry.<game>.<version> path")
                    for a in s.names:
                        if a.name == "*":
                            raise SyntaxError(
                                "star imports are not compilable")
                        _alias(a.asname or a.name,
                               f"@{parts[1].lower()}/{_norm_ver(a.name)}",
                               "libry-from-import")
                elif s.module == "api" or (s.module or "").startswith("api."):
                    for a in s.names:
                        if a.name == "*":
                            raise SyntaxError(
                                "from api import * is not compilable")
                        _alias(a.asname or a.name, "api." + a.name,
                               "from-import")
                else:
                    for a in s.names:
                        if a.name == "*":
                            raise SyntaxError(
                                "star imports are not compilable")
                        _alias(a.asname or a.name,
                               (s.module or "") + "." + a.name,
                               "from-import")
            elif isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant):
                pass  # docstring
            elif isinstance(s, ast.Assign) and len(s.targets) == 1 and \
                    isinstance(s.targets[0], ast.Name) and \
                    _const_number(s.value) is not None:
                pass  # numeric module constant (bound below)
            else:
                raise SyntaxError(
                    f"top-level {type(s).__name__} is not compilable — only "
                    "functions, imports and numeric constants live at "
                    "project top level")
    # Numeric module constants (tuning tables living at top level).
    for mod in order:
        for s in modules[mod].body:
            if isinstance(s, ast.Assign) and len(s.targets) == 1 and \
                    isinstance(s.targets[0], ast.Name):
                v = _const_number(s.value)
                if v is not None and s.targets[0].id not in ctx._env:
                    ctx._env[s.targets[0].id] = ctx._desc(v)
    bots = [(m, n) for (m, n) in ctx._functions if n == "tick"]
    if not bots:
        singles = {}
        for (m, n) in ctx._functions:
            singles.setdefault(n, []).append(m)
        once = [n for n, ms in singles.items() if len(ms) == 1]
        if len(once) != 1:
            raise SyntaxError(
                "exactly one bot function expected (name it tick)")
        bots = [(singles[once[0]][0], once[0])]
    if len(bots) != 1:
        raise SyntaxError("multiple tick functions across project files")
    (bmod, bname) = bots[0]
    ctx._active.add((bmod, bname))
    saved = dict(ctx._env)
    try:
        fdef = ctx._functions[(bmod, bname)]
        bargs = fdef.args.args
        if len(bargs) != 1 or bargs[0].arg != "api" or fdef.args.vararg \
                or fdef.args.kwarg:
            raise SyntaxError("bot function tick takes exactly (api)")
        _block(ctx, fdef.body)
    finally:
        ctx._active.remove((bmod, bname))
        ctx._env = saved
    from .desc import optimize_ops
    return {
        "schema": "graphc-desc-v1",
        "target": {"game": target[0], "version": target[1]},
        "bot_name": bname,
        "ops": optimize_ops(ctx.ops, opt),
    }