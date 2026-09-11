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
    NAME = <num> (module level)   a module variable the bot WRITES becomes
                                  cross-tick state automatically (writes =>
                                  dynamic latch, never written => inlined
                                  constant); no annotation, no api.var
    api.array("name", n)          packed array handle (RAM)
    api.set_array_cell(buf, i, v) static cell write
    api.get_array_cell(buf, i)    static cell read
    api.get_array_cell_dynamic(buf, idx)  dynamic cell read (select-chain)
    api.plot("channel", expr)     TimePlot debug sink (all targets;
                                  observable in game, sim, pure VM)
    api.move(x, z)                soccer controller (target soccer)
    api.soccer_get_bool/float/vector3/transform(label)   sensors (soccer)
    api.position_of(t)            transform -> position vector
    api.tennis_get_bool/float/vector3/transform(label)   sensors (tennis)
    api.tennis_move(x, z, swing=None, shot=None, sprint=None)  (tennis)
    api.tennis_move_vec(v, swing=None, shot=None, sprint=None) (tennis)
    api.tennis_aim(x, z)          strike-aim request for the next move
                                  (autoswitch — walk wire untouched; one
                                  per tick, paired with a controller)
    api.tennis_auto_swing(shot, mode='Prefer Charge')  game swing node
                                  -> bool (wire into move's swing)
    api.split_vector(v, i)        vector component -> float (i: 0=x,1=y,2=z)
    api.make_vector(x, y, z)      3 floats -> vector (feeds tennis_move_vec)
    api.var("name") / set_var     explicit latch (legacy; prefer module vars)

Bounded control flow (unrolled/inlined at compile time — the game runs
the flat graph, so per-tick cost stays static and reported):
    for i in range(a[, b[, s]])   literal-int trips, unrolled. Pure
                                  accumulation; break/continue allowed.
    while cond:                   unrolled to MAX_WHILE_TRIPS (64) with an
                                  overflow canary plot (!!while_overflow).
    def f(...): ... f(...)        direct/indirect self-call inlines to
                                  MAX_REC_DEPTH (32) with an overflow canary
                                  (!!recursion_overflow). Single tail return;
                                  bodies must be sink-free (hoist set_var /
                                  plot / move out of loops and recursion).

Expressions: numbers, names, + - * / % **, single comparisons, unary -,
`not`. Every value carries a TYPE (float/bool/vector/transform/array) and
every connection is checked: bool into arithmetic, vector into a float
slot, transform into vec_split, float where bool is needed — all fail HERE
with a pointing error, never a silently miswired game node. You never name
a node, port, or wire: write values, the compiler connects them.
api.* calls inside if branches are not yet supported (assignments only) —
the whitelist fails loudly, never silently.

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
import sys

_BIN = {ast.Add: "AddFloats", ast.Sub: "SubtractFloats",
        ast.Mult: "MultiplyFloats", ast.Div: "DivideFloats",
        ast.Mod: "Modulo", ast.Pow: "Power"}
#: Sensors the game leaves stale/garbage outside narrow windows (pinned
#: from native timeplots + reference-bot avoidance, NOT from the dropdown
#: tables — the tables cannot tell you a sensor lies).
_STALE_SENSORS = {
    # Game truth 2026-09-11: only sane right after your own hit while
    # positioning for the opponent's bounced reply; garbage otherwise.
    # titanium54 never reads it. Prefer predicted_bounce (the ball's own
    # predicted landing) for walking.
    "Estimated Opponent Shot Location":
        "stale outside the post-own-hit receive window — prefer "
        "predicted_bounce (Vector3 ball bounce position)",
}


def _warn_stale_sensor(label: str) -> None:
    """Loud-but-not-fatal: the bot compiles, the author has been told."""
    note = _STALE_SENSORS.get(label)
    if note is not None:
        print(f"graphc warning: {label!r} {note}", file=sys.stderr)


#: Terse api.* spellings and their canonical self-documenting forms.
#: Both compile to identical graphs; errors and docs name the full form.
_FULL_NAMES = {
    "arr_set": "set_array_cell",
    "arr_get": "get_array_cell",
    "arr_get_dyn": "get_array_cell_dynamic",
    "vec_split": "split_vector",
    "vec_make": "make_vector",
    "pos_of": "position_of",
}

#: api.* calls whose effect is a side effect (controller / latch / sink):
#: ambiguous inside an if branch, always loud. Everything else (sensors,
#: split_vector, position_of, var, array reads, make_vector, auto_swing)
#: is a pure value and is allowed in branches.
_BRANCH_SINK_FNS = {
    "set_var", "set_array_cell", "move", "tennis_move", "tennis_move_vec",
    "tennis_aim", "plot",
}
_CMP = {ast.Lt: "<", ast.Gt: ">", ast.LtE: "<=", ast.GtE: ">=",
        ast.Eq: "==", ast.NotEq: "!="}

_TENNIS_KINDS = {"tennis_get_bool": "bool", "tennis_get_float": "float",
                 "tennis_get_vector3": "vector3",
                 "tennis_get_transform": "transform"}
_SOCCER_KINDS = {"soccer_get_bool": "bool", "soccer_get_float": "float",
                 "soccer_get_vector3": "vector3",
                 "soccer_get_transform": "transform"}

#: Target-bound author modules: import AIA_Comp_Libry.tennis.v014 as t.
#: The (game, version) path must match the compile target or it fails loudly
#: (version pinning). Supported forms:
#:   import AIA_Comp_Libry.tennis.v014 as t   (+ t.sensor())
#:   from AIA_Comp_Libry.tennis.v014 import sensor (+ sensor())
#:   from AIA_Comp_Libry.tennis import v014      (+ v014.sensor())
LIBRY = "AIA_Comp_Libry"


# --- bounded-loop / recursion caps (flat graph out: static per-tick cost)
MAX_FOR_TRIPS = 4096
MAX_WHILE_TRIPS = 64
MAX_REC_DEPTH = 32
# Total-op guard against degenerate unrolls (nested loops x recursion).
MAX_UNROLL_OPS = 100_000
# Lowering-chain guard: longest demand chain (desc ops) the sim's
# recursive lowerer must walk. Measured 2026-09-11 (Windows 1MB main
# thread): chains <= 641 lower fine, 1540 kills the process with
# STATUS_STACK_OVERFLOW (uncaught — no loud error possible downstream).
# 800 keeps margin both ways. Deep chains mean "use latches across ticks".
# (The principled sim-side fix is an explicit heap work-stack in the
# lowerer instead of call-stack recursion; until then this is the net.)
MAX_CHAIN_DEPTH = 800


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
        # Per-tick idiot-proofing (reset per compile — NEVER carried across
        # ticks, and never silently resolved):
        # _set_vars/_arrays/_controller/_set_cells catch double-writes whose
        # in-game order would be ambiguous (if the bot misbehaves, it is the
        # author's bug, and it fails HERE, not in the game).
        self._set_vars: set[str] = set()
        self._set_cells: set[tuple[int, int]] = set()
        self._arrays: set[str] = set()
        self._controller: str | None = None
        # Auto cross-tick state: module-level names the bot reassigns.
        # Reads emit GetVariable, the single end-of-tick value emits
        # SetVariable — plain Python variables, no api.var/set_var.
        self._state_names: set[str] = set()
        self._state_dirty: set[str] = set()
        # Split drive (tennis): tennis_aim records the strike-aim request
        # for the next tennis_move (autoswitch — walk wire untouched);
        # one aim per tick, and never without its controller.
        self._aim_pending: bool = False
        # Bounded control flow (for/while/recursion unroll inline — flat graph
        # out, static cost): _loop_stack frames gate assignments under
        # break/continue/while-exit; _cond_stack holds enclosing if-conditions
        # (op id, polarity) for exact exit/overflow accounting; _rec_over
        # collects per-function overflow sites for end-of-compile canaries.
        self._loop_stack: list = []
        self._cond_stack: list = []
        self._rec_over: dict = {}
        self._helper_depth: int = 0
        self._rec_depth: int = 0
        self._rec_left: int = MAX_REC_DEPTH
        # Pending one-sided arm returns per inline frame: (cond, polarity,
        # value). The next tail return combines them (nesting rebuilds full
        # paths); end-of-body with pendings but no tail return is loud.
        self._fn_pend: list = []
        # Static-dead value per inline frame: a return on a statically-taken
        # path (guard clause) ends the block — the rest is Python-unreachable
        # and skipped, not traced.
        self._static_ret: list = []
        # Trace-time static domain (SCCP-lite: ints with abs < 2**24,
        # bools): exact Python-int semantics, f32-exact range, used ONLY to
        # prune branches (if/while arm selection, recursion base cases).
        # Values ALWAYS lower through the normal float ops — never folded —
        # so game bit-identity is untouched. Anything float-flavored,
        # dynamic, or out of range is simply absent (Unknown) and takes the
        # dynamic path.
        self._static: dict = {}
        # SSA op id -> value type (float/bool/vector/transform/array).
        # Every connection is checked against this; illegal node wiring is
        # a compile error here, never a silent game misbehavior.
        self._types: dict[int, str] = {}

    def _desc(self, v: float) -> int:
        key = ("const", float(v))
        if key not in self._cse:
            self._cse[key] = len(self.ops)
            self.ops.append({"op": "const", "value": float(v)})
        op_id = self._cse[key]
        self._types[op_id] = "float"
        return op_id

    def _emit(self, op: dict) -> int:
        key = tuple(sorted((k, str(v)) for k, v in op.items() if k != "op"))
        key = (op["op"],) + key
        if key not in self._cse:
            self._cse[key] = len(self.ops)
            self.ops.append(op)
        return self._cse[key]

    def _set_type(self, op_id: int, typ: str) -> int:
        prev = self._types.get(op_id)
        if prev is not None and prev != typ:
            raise SyntaxError(
                f"internal type conflict for op {op_id}: {prev} vs {typ}")
        self._types[op_id] = typ
        return op_id

    def _typeof(self, op_id: int) -> str:
        return self._types.get(op_id, "float")

    def _need(self, op_id: int, want: str, where: str) -> int:
        got = self._typeof(op_id)
        if got != want:
            raise SyntaxError(
                f"{where} needs {want}, got {got} (op {op_id}) — "
                f"illegal node connection blocked: convert explicitly "
                f"(e.g. vec_split a vector, compare floats for a bool)")
        return op_id


def _expr(ctx: _Ctx, node: ast.expr) -> int:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            # Dedicated const op (NOT _desc-shared): the type tag on a
            # shared float const would flip with emission order, making
            # `x + True` pass or fail depending on surrounding code.
            op_id = ctx._emit(
                {"op": "const", "value": 1.0 if node.value else 0.0})
            ctx._types[op_id] = "bool"
            _tag_static(ctx, op_id, node.value)
            return op_id
        if not isinstance(node.value, (int, float)):
            raise SyntaxError(f"only numeric constants, got {node.value!r}")
        op_id = ctx._desc(float(node.value))
        if isinstance(node.value, int):
            _tag_static(ctx, op_id, node.value)
        elif float(node.value).is_integer():
            # Integral float literal (1.0, 2.0): exactly the integer, so
            # it joins the static domain (n <= 1.0 prunes like n <= 1).
            _tag_static(ctx, op_id, int(node.value))
        return op_id
    if isinstance(node, ast.Name):
        if node.id not in ctx._env:
            # Module-level variable the bot mutates: first read pulls the
            # persisted latch (GetVariable). Plain Python state, no api.var.
            if node.id in ctx._state_names:
                op = ctx._set_type(ctx._emit(
                    {"op": "var_get", "name": node.id}), "float")
                ctx._env[node.id] = op
                return op
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
        a = _expr(ctx, node.left)
        b = _expr(ctx, node.right)
        ctx._need(a, "float", f"{fn} left operand")
        ctx._need(b, "float", f"{fn} right operand")
        op_id = ctx._set_type(ctx._emit(
            {"op": "bin", "fn": fn, "a": a, "b": b}), "float")
        # Static ints for branch pruning (values still lower as floats).
        sa, sb = ctx._static.get(a), ctx._static.get(b)
        if isinstance(sa, int) and not isinstance(sa, bool) and \
                isinstance(sb, int) and not isinstance(sb, bool):
            try:
                if isinstance(node.op, ast.Add):
                    _tag_static(ctx, op_id, sa + sb)
                elif isinstance(node.op, ast.Sub):
                    _tag_static(ctx, op_id, sa - sb)
                elif isinstance(node.op, ast.Mult):
                    _tag_static(ctx, op_id, sa * sb)
                elif isinstance(node.op, ast.Mod) and sb != 0:
                    _tag_static(ctx, op_id, sa % sb)
            except (OverflowError, ValueError):
                pass
        return op_id
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            v = _const_number(node.operand)
            if v is not None:
                op_id = ctx._desc(-v)
                if float(v).is_integer():
                    _tag_static(ctx, op_id, int(-v))
                return op_id
            b = _expr(ctx, node.operand)
            ctx._need(b, "float", "unary minus operand")
            op_id = ctx._set_type(ctx._emit(
                {"op": "bin", "fn": "SubtractFloats",
                 "a": ctx._desc(0.0), "b": b}), "float")
            sb = ctx._static.get(b)
            if isinstance(sb, int) and not isinstance(sb, bool):
                _tag_static(ctx, op_id, -sb)
            return op_id
        if isinstance(node.op, ast.Not):
            b = _expr(ctx, node.operand)
            ctx._need(b, "bool", "not operand")
            op_id = ctx._set_type(
                ctx._emit({"op": "not", "b": b}), "bool")
            sb = ctx._static.get(b)
            if isinstance(sb, bool):
                _tag_static(ctx, op_id, not sb)
            return op_id
        raise SyntaxError(f"unsupported unary {type(node.op).__name__}")
    if isinstance(node, ast.Compare):
        if len(node.ops) != 1:
            raise SyntaxError("chained comparisons unsupported")
        cmp = _CMP.get(type(node.ops[0]))
        if cmp is None:
            raise SyntaxError(f"unsupported comparison {type(node.ops[0]).__name__}")
        a = _expr(ctx, node.left)
        b = _expr(ctx, node.comparators[0])
        ctx._need(a, "float", f"comparison ({cmp}) left operand")
        ctx._need(b, "float", f"comparison ({cmp}) right operand")
        sa, sb = ctx._static.get(a), ctx._static.get(b)
        if cmp == "!=":
            eq = ctx._set_type(ctx._emit(
                {"op": "bin", "fn": "CompareFloats",
                 "a": a, "b": b, "cmp": "=="}), "bool")
            op_id = ctx._set_type(
                ctx._emit({"op": "not", "b": eq}), "bool")
            if isinstance(sa, int) and not isinstance(sa, bool) and \
                    isinstance(sb, int) and not isinstance(sb, bool):
                _tag_static(ctx, op_id, sa != sb)
            return op_id
        op_id = ctx._set_type(ctx._emit(
            {"op": "bin", "fn": "CompareFloats",
             "a": a, "b": b, "cmp": cmp}), "bool")
        if isinstance(sa, int) and not isinstance(sa, bool) and \
                isinstance(sb, int) and not isinstance(sb, bool):
            _tag_static(ctx, op_id, {
                "==": sa == sb, "<": sa < sb, ">": sa > sb,
                "<=": sa <= sb, ">=": sa >= sb}[cmp])
        return op_id
    if isinstance(node, ast.Call):
        try:
            return _api_call(ctx, node)
        except SyntaxError as e:
            if "whitelist" not in str(e):
                raise
            return _project_call(ctx, node)
    if isinstance(node, ast.BoolOp):
        raise SyntaxError(
            f"'and/or' is not compilable — nest if statements: "
            f"{ast.unparse(node)[:60]!r}")
    if isinstance(node, ast.IfExp):
        raise SyntaxError(
            f"x-if-c-else is not compilable — use if/else assignments: "
            f"{ast.unparse(node)[:60]!r}")
    if isinstance(node, ast.Subscript):
        raise SyntaxError(
            f"subscripts are not compilable — arrays use api.get_array_cell: "
            f"{ast.unparse(node)[:60]!r}")
    if isinstance(node, ast.NamedExpr):
        raise SyntaxError(
            f"walrus is not compilable — assign first: "
            f"{ast.unparse(node)[:60]!r}")
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
        # Recursive re-entry: inline to a depth budget. Exhausted levels
        # wire 0.0 and record a reached-gated overflow site (canaried at
        # end of compile — never silent). Bodies stay single-tail-return:
        # both arms trace, the select picks, the budget bounds the tree.
        if ctx._rec_left <= 0:
            ctx._rec_over.setdefault(qual, []).append(_path_float(ctx))
            return ctx._desc(0.0)
        return _inline_call(ctx, qual, node, ctx._rec_left - 1)
    return _inline_call(ctx, qual, node, ctx._rec_left)


def _combine_pendings(ctx: _Ctx, qual, v: int) -> int:
    """Fold pending one-sided arm returns around a tail value (nesting
    rebuilds full paths: earlier paths take precedence)."""
    for (c, pol, pv) in ctx._fn_pend:
        if ctx._typeof(pv) != ctx._typeof(v):
            where = f" in {qual!r}" if qual else ""
            raise SyntaxError(
                f"return paths{where} mix {ctx._typeof(pv)} and "
                f"{ctx._typeof(v)} — helpers return one float")
        v = ctx._set_type(ctx._emit(
            {"op": "select", "c": c if pol else _bnot(ctx, c),
             "t": pv, "f": v}), ctx._typeof(pv))
    ctx._fn_pend = []
    return v


def _inline_call(ctx: _Ctx, qual, node: ast.Call, rec_left: int) -> int:
    """Trace a helper body with params bound (one inline frame)."""
    _check_unroll_budget(ctx, f"inline of {qual!r}")
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
    saved_left = ctx._rec_left
    saved_pend = ctx._fn_pend
    ctx._fn_pend = []
    ctx._static_ret.append(None)
    added = qual not in ctx._active
    if added:
        ctx._active.add(qual)
    recursive = not added
    ctx._helper_depth += 1
    if recursive:
        ctx._rec_depth += 1
    ctx._rec_left = rec_left
    try:
        # Evaluate ALL args in the caller env FIRST, then bind params:
        # binding one-by-one would clobber caller locals that later args
        # still read (gcd(b, a % b) bound a before reading caller-a).
        arg_vals = []
        for i, p in enumerate(params):
            if p == "api" and not (
                    i < len(node.args)
                    and isinstance(node.args[i], ast.Name)
                    and node.args[i].id == "api"
                    and "api" not in ctx._env):
                raise SyntaxError(
                    "parameter 'api' shadows the game-API namespace — "
                    "rename it (api.* calls work inside helpers without "
                    "passing api)")
            if i < len(node.args):
                a = node.args[i]
                if isinstance(a, ast.Name) and a.id == "api" \
                        and "api" not in ctx._env:
                    arg_vals.append(_API_MARKER)
                else:
                    arg_vals.append(_expr(ctx, a))
            else:
                d = fdef.args.defaults[i - (len(params) - len(fdef.args.defaults))]
                arg_vals.append(_expr(ctx, d))
        for p, v in zip(params, arg_vals):
            ctx._env[p] = v
        ret = None
        returned = False
        for s in fdef.body:
            if ctx._static_ret[-1] is not None:
                continue  # static path returned: rest is dead, skip
            if returned:
                raise SyntaxError(
                    f"unreachable statement after return in {qual!r} — "
                    "remove it (every path already returned)")
            if isinstance(s, ast.Return):
                if ret is not None:
                    raise SyntaxError(f"multiple return in {qual!r}")
                v = _expr(ctx, s.value) if s.value is not None \
                    else ctx._desc(0.0)
                v = _combine_pendings(ctx, qual, v)
                ret = v
                returned = True
            else:
                try:
                    _stmt(ctx, s)
                except _FnReturn as r:
                    # Top-level if with returns in both arms: every path
                    # returned — combine pendings and take the merged value.
                    if ret is not None:
                        raise SyntaxError(
                            f"unreachable return in {qual!r} — every path "
                            "already returned; restructure to nested "
                            "if/else")
                    ret = _combine_pendings(ctx, qual, r.value)
                    returned = True
        if ctx._fn_pend and ret is None and ctx._static_ret[-1] is None:
            raise SyntaxError(
                f"not all paths return in {qual!r} — add a tail return "
                "(paths that fall off the end have no value)")
        if ret is None:
            if ctx._static_ret[-1] is not None:
                ret = ctx._static_ret[-1]
            else:
                raise SyntaxError(f"function {qual!r} has no return")
        return ret
    finally:
        if added:
            ctx._active.remove(qual)
        ctx._helper_depth -= 1
        if recursive:
            ctx._rec_depth -= 1
        ctx._rec_left = saved_left
        ctx._fn_pend = saved_pend
        ctx._static_ret.pop()
        ctx._env = saved_env


def _targetmod_call(ctx: _Ctx, node: ast.Call, game: str, ver: str,
                    fn: str) -> int:
    """AIA_Comp_Libry.tennis.v014.ball_incoming() -> the tennis_get op.

    Unversioned game paths resolve to latest; anything that does not match
    the compile target fails loudly, so a bot can never silently mean a
    different game version than it runs on.
    """
    from .desc import LATEST_TARGETS
    if game not in LATEST_TARGETS:
        raise SyntaxError(
            f"unknown API game {LIBRY}.{game} — known: "
            f"{sorted(LATEST_TARGETS)}")
    if ver == "latest":
        ver = _norm_ver(LATEST_TARGETS[game])
    if game != ctx.target[0] or ver != _norm_ver(ctx.target[1]):
        raise SyntaxError(
            f"API module {LIBRY}.{game}.{ver} does not match compile target "
            f"{ctx.target}")
    game_c = game
    if fn in ("move", "move_vec", "aim", "auto_swing"):
        if fn in ("aim", "auto_swing"):
            if game_c != "tennis":
                raise SyntaxError(f"api.{fn} is not valid for target {ctx.target}")
            real = {"aim": "tennis_aim",
                    "auto_swing": "tennis_auto_swing"}[fn]
        else:
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
    typ = "vector" if kind == "vector3" else kind
    if game_c == "tennis":
        from .desc import tennis_sensor_index
        idx, lab = tennis_sensor_index(kind, label, ctx.target[1])
        _warn_stale_sensor(lab)
        return ctx._set_type(ctx._emit(
            {"op": "tennis_get", "kind": kind,
             "index": idx, "label": lab}), typ)
    from .desc import soccer_sensor_index
    idx, lab = soccer_sensor_index(kind, label)
    return ctx._set_type(ctx._emit(
        {"op": "soccer_get", "kind": kind,
         "index": idx, "label": lab}), typ)


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
    # Self-documenting full spellings are canonical; terse aliases still
    # work (normalized here, so errors and docs always name the full form).
    fn = _FULL_NAMES.get(fn, fn)
    # Pure reads (sensors, split_vector, position_of, var, array reads,
    # make_vector, auto_swing) are safe inside if branches: both arms
    # evaluate every tick anyway, so emitting the op unconditionally is
    # exactly what the graph does. Only SIDE-EFFECT sinks are ambiguous in
    # a branch (double writes / double controllers), and those stay loud.
    if ctx._in_branch and fn in _BRANCH_SINK_FNS:
        raise SyntaxError(
            f"api.{fn} inside an if branch is ambiguous in-game (it would "
            "run on the branch's arm only) — hoist it out of the branch")
    if ctx._in_branch and fn == "array":
        raise SyntaxError(
            "api.array declaration inside an if branch — declare memory at "
            "the top of the tick")
    args = node.args
    if fn == "var":
        (name,) = args
        return ctx._set_type(ctx._emit(
            {"op": "var_get", "name": ast.literal_eval(name)}), "float")
    if fn == "set_var":
        _sink_guard(ctx, 'api.set_var')
        name, v = args
        sname = ast.literal_eval(name)
        if sname in ctx._set_vars:
            raise SyntaxError(
                f"api.set_var({sname!r}) twice in one tick — the in-game "
                "write order would be ambiguous; merge into one call")
        ctx._set_vars.add(sname)
        vv = _expr(ctx, v)
        ctx._need(vv, "float", f"api.set_var({sname!r}) value")
        ctx.ops.append({"op": "var_set", "name": sname, "v": vv})
        return ctx._desc(0.0)
    if fn == "array":
        _sink_guard(ctx, 'api.array')
        name, cells = args
        aname = ast.literal_eval(name)
        if aname in ctx._arrays:
            raise SyntaxError(
                f"api.array({aname!r}) twice in one tick — declare once, "
                "share the handle")
        ctx._arrays.add(aname)
        op_id = len(ctx.ops)
        ctx.ops.append({"op": "array", "name": aname,
                        "cells": ast.literal_eval(cells)})
        ctx._types[op_id] = "array"
        return op_id
    if fn == "set_array_cell":
        _sink_guard(ctx, 'api.set_array_cell')
        arr, i, v = args
        aa = _expr(ctx, arr)
        ctx._need(aa, "array", "api.set_array_cell buffer")
        vv = _expr(ctx, v)
        ctx._need(vv, "float", "api.set_array_cell value")
        cell = (aa, ast.literal_eval(i))
        if cell in ctx._set_cells:
            raise SyntaxError(
                f"api.set_array_cell(cell {cell[1]}) twice in one tick — the "
                "in-game write order would be ambiguous; merge into one call")
        ctx._set_cells.add(cell)
        ctx.ops.append({"op": "array_set_static", "arr": aa,
                        "i": ast.literal_eval(i), "v": vv})
        return ctx._desc(0.0)
    if fn == "get_array_cell":
        arr, i = args
        aa = _expr(ctx, arr)
        ctx._need(aa, "array", "api.get_array_cell buffer")
        return ctx._set_type(ctx._emit(
            {"op": "array_get_static", "arr": aa,
             "i": ast.literal_eval(i)}), "float")
    if fn == "get_array_cell_dynamic":
        arr, i = args
        aa = _expr(ctx, arr)
        ctx._need(aa, "array", "api.get_array_cell_dynamic buffer")
        ii = _expr(ctx, i)
        ctx._need(ii, "float", "api.get_array_cell_dynamic index")
        return ctx._set_type(ctx._emit(
            {"op": "array_get_dynamic", "arr": aa, "i": ii}), "float")
    if fn == "move":
        _sink_guard(ctx, 'api.move')
        if ctx.target[0] != "soccer":
            raise SyntaxError(f"api.move is not valid for target {ctx.target}")
        _claim_controller(ctx, "move")
        x, z = args
        xx, zz = _expr(ctx, x), _expr(ctx, z)
        ctx._need(xx, "float", "api.move x")
        ctx._need(zz, "float", "api.move z")
        ctx.ops.append({"op": "soccer_move", "x": xx, "z": zz})
        return ctx._desc(0.0)
    if fn == "plot":
        _sink_guard(ctx, 'api.plot')
        # Debug sink: no game attached, valid on every target including
        # universal. Channel is save metadata (string literal); the value
        # is any float. Repeatable — each call is one TimePlot node.
        if len(args) != 2:
            raise SyntaxError(
                f"api.plot needs (channel, value), got {ast.unparse(node)[:60]!r}")
        name, v = args
        try:
            sname = ast.literal_eval(name)
        except Exception:
            raise SyntaxError(
                "api.plot channel must be a string literal — "
                f"got {ast.unparse(name)[:60]!r} (channels live in the "
                "save, they cannot be computed per tick)")
        if not isinstance(sname, str) or not sname:
            raise SyntaxError(
                f"api.plot channel must be a non-empty str, got {sname!r}")
        vv = _expr(ctx, v)
        ctx._need(vv, "float", f"api.plot({sname!r}) value")
        ctx.ops.append({"op": "plot", "name": sname, "v": vv})
        return ctx._desc(0.0)
    if fn in _TENNIS_KINDS:
        if ctx.target[0] != "tennis":
            raise SyntaxError(
                f"api.{fn} is not valid for target {ctx.target}")
        (label,) = args
        kind = _TENNIS_KINDS[fn]
        from .desc import tennis_sensor_index
        idx, lab = tennis_sensor_index(kind, ast.literal_eval(label))
        _warn_stale_sensor(lab)
        typ = "vector" if kind == "vector3" else kind
        return ctx._set_type(ctx._emit(
            {"op": "tennis_get", "kind": kind,
             "index": idx, "label": lab}), typ)
    if fn in _SOCCER_KINDS:
        if ctx.target[0] != "soccer":
            raise SyntaxError(
                f"api.{fn} is not valid for target {ctx.target}")
        (label,) = args
        kind = _SOCCER_KINDS[fn]
        from .desc import soccer_sensor_index
        try:
            idx, lab = soccer_sensor_index(kind, ast.literal_eval(label))
        except (KeyError, ValueError, SyntaxError) as e:
            raise SyntaxError(
                f"api.{fn} needs a valid {kind} dropdown label — {e}")
        typ = "vector" if kind == "vector3" else (
            "transform" if kind == "transform" else kind)
        return ctx._set_type(ctx._emit(
            {"op": "soccer_get", "kind": kind,
             "index": idx, "label": lab}), typ)
    if fn == "position_of":
        (v,) = args
        vv = _expr(ctx, v)
        ctx._need(vv, "transform",
                  "api.position_of source (transforms are opaque — RelativePosition "
                  "reads the world position out of them)")
        return ctx._set_type(ctx._emit(
            {"op": "transform_pos", "v": vv}), "vector")
    if fn == "tennis_move":
        _sink_guard(ctx, 'api.tennis_move')
        if ctx.target[0] != "tennis":
            raise SyntaxError(
                f"api.tennis_move is not valid for target {ctx.target}")
        if not 2 <= len(args) <= 5:
            raise SyntaxError(
                "api.tennis_move(x, z, swing=None, shot=None, sprint=None)")
        _claim_controller(ctx, "tennis_move")
        x, z = _expr(ctx, args[0]), _expr(ctx, args[1])
        ctx._need(x, "float", "api.tennis_move x")
        ctx._need(z, "float", "api.tennis_move z")
        opt = [_opt_arg(ctx, a) for a in args[2:]]
        _check_move_opts(ctx, "api.tennis_move", opt)
        ctx.ops.append({
            "op": "tennis_move", "x": x, "z": z,
            "swing": opt[0] if len(opt) > 0 else None,
            "shot": opt[1] if len(opt) > 1 else None,
            "sprint": opt[2] if len(opt) > 2 else None,
        })
        return ctx._desc(0.0)
    if fn == "tennis_move_vec":
        _sink_guard(ctx, 'api.tennis_move_vec')
        if ctx.target[0] != "tennis":
            raise SyntaxError(
                f"api.tennis_move_vec is not valid for target {ctx.target}")
        if not 1 <= len(args) <= 4:
            raise SyntaxError(
                "api.tennis_move_vec(v, swing=None, shot=None, sprint=None)")
        _claim_controller(ctx, "tennis_move_vec")
        vv = _expr(ctx, args[0])
        if ctx._typeof(vv) == "transform":
            raise SyntaxError(
                "api.tennis_move_vec needs a vector, got transform — "
                "use a vector3 sensor (e.g. t.center_of_half()) or "
                "api.make_vector(x, y, z), not a transform (Self/Opponent/Ball)")
        ctx._need(vv, "vector", "api.tennis_move_vec v")
        opt = [_opt_arg(ctx, a) for a in args[1:]]
        _check_move_opts(ctx, "api.tennis_move_vec", opt)
        ctx.ops.append({
            "op": "tennis_move_vec", "v": vv,
            "swing": opt[0] if len(opt) > 0 else None,
            "shot": opt[1] if len(opt) > 1 else None,
            "sprint": opt[2] if len(opt) > 2 else None,
        })
        return ctx._desc(0.0)
    if fn == "tennis_aim":
        _sink_guard(ctx, 'api.tennis_aim')
        if ctx.target[0] != "tennis":
            raise SyntaxError(
                f"api.tennis_aim is not valid for target {ctx.target}")
        if len(args) != 2:
            raise SyntaxError("api.tennis_aim(x, z)")
        if ctx._aim_pending:
            raise SyntaxError(
                "api.tennis_aim twice in one tick — merge into one call")
        ctx._aim_pending = True
        x, z = _expr(ctx, args[0]), _expr(ctx, args[1])
        ctx._need(x, "float", "api.tennis_aim x")
        ctx._need(z, "float", "api.tennis_aim z")
        ctx.ops.append({"op": "tennis_aim", "x": x, "z": z})
        return ctx._desc(0.0)
    if fn == "tennis_auto_swing":
        if ctx.target[0] != "tennis":
            raise SyntaxError(
                f"api.tennis_auto_swing is not valid for target {ctx.target}")
        if not 1 <= len(args) <= 2:
            raise SyntaxError(
                "api.tennis_auto_swing(shot, mode='Prefer Charge')")
        vv = _expr(ctx, args[0])
        ctx._need(vv, "float", "api.tennis_auto_swing shot")
        mode = "Prefer Charge"
        if len(args) > 1:
            mode = ast.literal_eval(args[1])
            if mode not in ("Normal Only", "Prefer Charge", "Random"):
                raise SyntaxError(
                    f"api.tennis_auto_swing mode {mode!r} — "
                    "Normal Only | Prefer Charge | Random")
        return ctx._set_type(ctx._emit(
            {"op": "tennis_auto_swing", "shot": vv, "mode": mode}), "bool")
    if fn == "split_vector":
        v, i = args
        idx = ast.literal_eval(i)
        if idx not in (0, 1, 2):
            raise SyntaxError(
                f"api.split_vector component must be 0/1/2, got {idx!r}")
        vv = _expr(ctx, v)
        if ctx._typeof(vv) == "transform":
            raise SyntaxError(
                "api.split_vector needs a vector, got transform — transforms "
                "(Self/Opponent/Ball) are opaque; use a vector3 sensor "
                "(e.g. ball_position, legal_serve_target, center_of_half)")
        ctx._need(vv, "vector", "api.split_vector source")
        return ctx._set_type(ctx._emit(
            {"op": "vec_split", "v": vv, "i": idx}), "float")
    if fn == "make_vector":
        x, y, z = args
        xx, yy, zz = _expr(ctx, x), _expr(ctx, y), _expr(ctx, z)
        ctx._need(xx, "float", "api.vec_make x")
        ctx._need(yy, "float", "api.vec_make y")
        ctx._need(zz, "float", "api.vec_make z")
        return ctx._set_type(ctx._emit(
            {"op": "vec_make", "x": xx, "y": yy, "z": zz}), "vector")
    raise SyntaxError(f"unknown api function {fn!r}")


def _opt_arg(ctx: _Ctx, a: ast.expr | None) -> int | None:
    if a is None or (isinstance(a, ast.Constant) and a.value is None):
        return None
    return _expr(ctx, a)


def _check_move_opts(ctx: _Ctx, where: str, opt: list[int | None]) -> None:
    # swing: bool, shot: float, sprint: bool.
    wants = (("swing", "bool"), ("shot", "float"), ("sprint", "bool"))
    for (name, want), got_id in zip(wants, opt):
        if got_id is None:
            continue
        got = ctx._typeof(got_id)
        if got != want:
            raise SyntaxError(
                f"{where} {name} needs {want}, got {got} (op {got_id}) — "
                f"illegal controller connection blocked")


def _claim_controller(ctx: _Ctx, what: str) -> None:
    if ctx._controller is not None:
        raise SyntaxError(
            f"two controllers in one tick ({ctx._controller} + {what}) — "
            "the in-game winner would be ambiguous; merge into one call "
            "with if/else assignments")
    ctx._controller = what


# f32-exact integer range: static pruning is sound only where the game
# evaluates the identical integers (comparisons of exactly-represented
# values match Python-int comparisons one for one).
_STATIC_INT_MAX = 2 ** 24


def _tag_static(ctx: _Ctx, op_id: int, value) -> None:
    """Record a trace-time static (small int or bool) for branch pruning."""
    if isinstance(value, bool):
        ctx._static[op_id] = value
    elif isinstance(value, int) and abs(value) < _STATIC_INT_MAX:
        ctx._static[op_id] = value


# --- bounded loops + recursion (compile-time unroll/inline) ---------------
#
# The game has no loop or call-stack nodes, so control flow is compiled
# away: for/while bodies are traced once per trip (straight-line SSA),
# self-calls inline to a depth budget. The emitted graph is flat, which
# keeps the per-tick transition cost static and exactly reported.
# Overflow past a cap is never silent: while/recursion carry an
# auto-plotted `!!` canary (nonzero = exceeded, check the TimePlot).


class _LoopJump(Exception):
    """break/continue inside a loop body (re-raised through if-merges)."""

    def __init__(self, kind: str, uncond: bool):
        super().__init__(kind)
        self.kind = kind
        self.uncond = uncond


class _FnReturn(Exception):
    """return inside a helper if-arm: value propagates, arms merge."""

    def __init__(self, value: int):
        super().__init__("return")
        self.value = value


class _LoopFrame:
    def __init__(self) -> None:
        self.exited: int = -1
        self.skipped: int = -1
        # may_gate: some path may deactivate iterations (while, or a
        # conditional break/continue seen) — assignments must select-gate.
        # dirty: a flag op was actually updated (gating is provably exact
        # before the first update, so plain loops emit zero extra nodes).
        self.may_gate: bool = False
        self.dirty: bool = False


def _fbin(ctx: _Ctx, fn: str, a: int, b: int) -> int:
    return ctx._set_type(ctx._emit(
        {"op": "bin", "fn": fn, "a": a, "b": b}), "float")


def _fcmp(ctx: _Ctx, a: int, b: int, cmp: str) -> int:
    return ctx._set_type(ctx._emit(
        {"op": "bin", "fn": "CompareFloats", "a": a, "b": b,
         "cmp": cmp}), "bool")


def _bnot(ctx: _Ctx, b: int) -> int:
    return ctx._set_type(ctx._emit({"op": "not", "b": b}), "bool")


def _fsel(ctx: _Ctx, c: int, t: int, f: int) -> int:
    return ctx._set_type(ctx._emit(
        {"op": "select", "c": c, "t": t, "f": f}), "float")


def _b2f(ctx: _Ctx, c: int) -> int:
    """bool -> 0.0/1.0 float (float select: proven node shape)."""
    return _fsel(ctx, c, ctx._desc(1.0), ctx._desc(0.0))


def _f2b(ctx: _Ctx, f: int) -> int:
    """nonzero float -> bool."""
    return _bnot(ctx, _fcmp(ctx, f, ctx._desc(0.0), "=="))


def _active_float(ctx: _Ctx) -> int:
    """Product of every loop frame's live factors (1.0 = fully active)."""
    f = None
    one = ctx._desc(1.0)
    for fr in ctx._loop_stack:
        for flag in (fr.exited, fr.skipped):
            term = _fbin(ctx, "SubtractFloats", one, flag)
            f = term if f is None else _fbin(ctx, "MultiplyFloats", f, term)
    return f if f is not None else one


def _path_float(ctx: _Ctx) -> int:
    """Active factor ANDed with every enclosing if-condition (as float)."""
    f = _active_float(ctx)
    for (c, pol) in ctx._cond_stack:
        cf = _b2f(ctx, c) if pol else _b2f(ctx, _bnot(ctx, c))
        f = _fbin(ctx, "MultiplyFloats", f, cf)
    return f


def _path_taken(ctx: _Ctx) -> int:
    """Current path as bool (for break/continue/overflow accounting)."""
    return _f2b(ctx, _path_float(ctx))


def _gate_assign(ctx: _Ctx, name: str, new: int) -> int:
    """Select-gate a loop-body assignment to the currently-active path."""
    if not ctx._loop_stack:
        return new
    if not any(fr.may_gate for fr in ctx._loop_stack):
        return new
    if all(not fr.dirty for fr in ctx._loop_stack):
        return new
    prev = ctx._env.get(name)
    if prev is None:
        raise SyntaxError(
            f"{name!r} is first assigned under a possibly-inactive path "
            "(break/continue/while-exit) — initialize it before the loop")
    t = ctx._typeof(new)
    if t not in ("float", "bool"):
        raise SyntaxError(
            f"only float/bool accumulators survive break/continue/while "
            f"— {name!r} is {t} (compute it after the loop)")
    if ctx._typeof(prev) != t:
        raise SyntaxError(
            f"{name!r} changes type across loop paths ({ctx._typeof(prev)} "
            f"vs {t}) — keep one type")
    return ctx._set_type(ctx._emit(
        {"op": "select", "c": _f2b(ctx, _active_float(ctx)),
         "t": new, "f": prev}), t)


def _sink_guard(ctx: _Ctx, what: str) -> None:
    """Per-tick sinks execute once per node per tick — inside a loop body
    or a recursive body they would execute N times (ambiguous order in
    game). Hoist: assign a local in the loop, sink it after."""
    if ctx._loop_stack:
        raise SyntaxError(
            f"{what} inside a loop body would execute once per trip "
            "(ambiguous in-game order) — assign a local in the loop, "
            f"{what} after it")
    if ctx._rec_depth:
        raise SyntaxError(
            f"{what} inside a recursive function would execute once per "
            f"inline level — hoist it out (compute a value, {what} "
            "at the call site)")


def _check_unroll_budget(ctx: _Ctx, what: str) -> None:
    if len(ctx.ops) > MAX_UNROLL_OPS:
        raise SyntaxError(
            f"{what} unrolled past {MAX_UNROLL_OPS} ops — shrink the "
            "trip count / recursion depth (the game loads every node)")


def _chain_depth(ctx: _Ctx) -> int:
    """Longest demand chain over current ops (linear forward pass; refs
    always point backward by SSA construction)."""
    from .desc import _refs
    n = len(ctx.ops)
    depth = [0] * n
    for i, o in enumerate(ctx.ops):
        refs = [v for _, v in _refs(o) if isinstance(v, int) and 0 <= v < i]
        if refs:
            depth[i] = 1 + max(depth[r] for r in refs)
    return max(depth, default=0)


def _check_chain_depth(ctx: _Ctx) -> None:
    d = _chain_depth(ctx)
    if d > MAX_CHAIN_DEPTH:
        raise SyntaxError(
            f"demand chain depth {d} exceeds {MAX_CHAIN_DEPTH} — the sim's "
            "recursive lowerer would overflow its stack (measured kill "
            "past ~1400 on a 1MB thread; no loud error possible there). "
            "Split the work: fewer trips per loop, shallower bodies, or "
            "latches across ticks (one step per tick, ~constant depth)")


def _loop_jump(ctx: _Ctx, kind: str) -> None:
    """break/continue: update this loop's flag, then unwind the iteration."""
    if not ctx._loop_stack:
        raise SyntaxError(f"{kind} outside a loop is not compilable")
    frame = ctx._loop_stack[-1]
    taken = _path_taken(ctx)
    one = ctx._desc(1.0)
    if kind == "break":
        frame.exited = _fsel(ctx, taken, one, frame.exited)
    else:
        frame.skipped = _fsel(ctx, taken, one, frame.skipped)
    frame.dirty = True
    uncond = not ctx._cond_stack
    if not uncond:
        frame.may_gate = True
    raise _LoopJump(kind, uncond)


def _drive_loop(ctx: _Ctx, s, loopvar: str | None, trips: list,
                implicit_cond: ast.expr | None, canary: str | None) -> None:
    """Trace a loop body once per trip (SSA accumulation across trips).

    loopvar=None for while (hidden counter). implicit_cond (while only)
    is re-traced every trip as an internal `if not cond: break`.
    canary (while only) names the overflow plot (emitted iff the cap may
    have been hit — always, since trips are dynamic).
    """
    frame = _LoopFrame()
    frame.exited = ctx._desc(0.0)
    if implicit_cond is not None:
        frame.may_gate = True
    ctx._loop_stack.append(frame)
    if implicit_cond is not None:
        # Zero-trip while: body and canary vanish (nothing can overflow).
        probe = _expr(ctx, implicit_cond)
        ctx._need(probe, "bool",
                  "while condition (comparisons and bool sensors "
                  "give bool; floats/vectors cannot branch)")
        if ctx._static.get(probe) is False:
            ctx._loop_stack.pop()
            return
    try:
        for v in trips:
            _check_unroll_budget(ctx, f"loop at line {s.lineno}")
            frame.skipped = ctx._desc(0.0)
            if loopvar is not None:
                loop_op = ctx._desc(float(v))
                _tag_static(ctx, loop_op, v)
                ctx._env[loopvar] = loop_op
            if implicit_cond is not None:
                c = _expr(ctx, implicit_cond)
                ctx._need(c, "bool",
                          "while condition (comparisons and bool sensors "
                          "give bool; floats/vectors cannot branch)")
                # Internal `if not cond: break` (top of trip: cond stack
                # holds only outer ifs, so the jump is unconditional iff
                # this loop body is not inside a branch).
                taken = _f2b(ctx, _fbin(
                    ctx, "MultiplyFloats", _path_float(ctx),
                    _b2f(ctx, _bnot(ctx, c))))
                frame.exited = _fsel(ctx, taken, ctx._desc(1.0),
                                     frame.exited)
                frame.dirty = True
            try:
                for stmt in s.body:
                    _stmt(ctx, stmt)
            except _LoopJump as j:
                if j.kind == "break" and j.uncond and \
                        implicit_cond is None:
                    break  # remaining trips provably dead
                # conditional jump (or any jump in while): later trips
                # stay gated, keep unrolling
                continue
    finally:
        ctx._loop_stack.pop()
    if canary is not None:
        c = _expr(ctx, implicit_cond)
        ctx._need(c, "bool", "while condition")
        over = _fbin(ctx, "MultiplyFloats", _active_float(ctx),
                     _b2f(ctx, c))
        ctx.ops.append({"op": "plot", "name": canary, "v": over})


def _range_trips(node: ast.Call) -> list:
    """Literal range(...) args -> trip list (loud on anything dynamic)."""
    if node.keywords:
        raise SyntaxError(
            f"range() takes no keywords — got {ast.unparse(node)[:60]!r}")
    if len(node.args) not in (1, 2, 3):
        raise SyntaxError(
            f"range() needs 1-3 literal ints — got {ast.unparse(node)[:60]!r}")
    vals = []
    for a in node.args:
        if isinstance(a, ast.UnaryOp) and isinstance(a.op, ast.USub) and \
                isinstance(a.operand, ast.Constant) and \
                isinstance(a.operand.value, int) and \
                not isinstance(a.operand.value, bool):
            vals.append(-a.operand.value)
        elif isinstance(a, ast.Constant) and isinstance(a.value, int) and \
                not isinstance(a.value, bool):
            vals.append(a.value)
        else:
            raise SyntaxError(
                f"range() needs literal ints — got {ast.unparse(a)[:40]!r} "
                "(trip count must be static: the game runs a flat graph)")
    start, stop, step = (0, vals[0], 1) if len(vals) == 1 else (
        (*vals, 1) if len(vals) == 2 else tuple(vals))
    if step == 0:
        raise SyntaxError("range() step must not be 0")
    return list(range(start, stop, step))


def _mark_state(ctx: _Ctx, name: str) -> None:
    """A module-level (persistent) variable was assigned this tick."""
    if name not in ctx._state_names:
        return
    if ctx._loop_stack or ctx._rec_depth or ctx._helper_depth:
        raise SyntaxError(
            f"{name!r} is persistent state (a module variable) — assign it "
            "at the top level of tick, not inside a loop, recursion, or a "
            "helper (in-game write order would be ambiguous)")
    ctx._state_dirty.add(name)


def _stmt(ctx: _Ctx, s: ast.stmt) -> None:
    if isinstance(s, ast.Global):
        # `global x` is declarative in Python; module variables here are
        # already persistent, so it is accepted and ignored.
        return
    if isinstance(s, ast.Assign):
        if len(s.targets) != 1 or not isinstance(s.targets[0], ast.Name):
            raise SyntaxError("only single-name assignments")
        if s.targets[0].id == "api":
            raise SyntaxError(
                "cannot assign to 'api' — it is the game-API namespace")
        _mark_state(ctx, s.targets[0].id)
        ctx._env[s.targets[0].id] = _gate_assign(
            ctx, s.targets[0].id, _expr(ctx, s.value))
    elif isinstance(s, ast.AugAssign):
        if not isinstance(s.target, ast.Name):
            raise SyntaxError("augmented assign to non-name")
        name = s.target.id
        if name == "api":
            raise SyntaxError(
                "cannot assign to 'api' — it is the game-API namespace")
        _mark_state(ctx, name)
        if name not in ctx._env:
            raise SyntaxError(f"name {name!r} used before assignment")
        fn = _BIN.get(type(s.op))
        if fn is None:
            raise SyntaxError(f"unsupported operator {type(s.op).__name__}")
        ctx._need(ctx._env[name], "float",
                  f"augmented assign to {name!r} (left side)")
        rhs = _expr(ctx, s.value)
        ctx._need(rhs, "float",
                  f"augmented assign to {name!r} (right side)")
        ctx._env[name] = _gate_assign(ctx, name, ctx._set_type(ctx._emit(
            {"op": "bin", "fn": fn, "a": ctx._env[name], "b": rhs}), "float"))
    elif isinstance(s, ast.If):
        cond = _expr(ctx, s.test)
        ctx._need(cond, "bool",
                  "if condition (comparisons and bool sensors give bool; "
                  "floats/vectors cannot branch)")
        taken = ctx._static.get(cond)
        if isinstance(taken, bool):
            # Statically known arm: trace it alone (no merge, no select).
            # Untaken-arm names stay unbound — using one later fails loudly,
            # which is correct (that path never executes). This is what
            # bounds branching recursion over literal args.
            # A return on the static path ends the block: the rest is
            # Python-unreachable (guard-clause style). Empty cond-stack =
            # whole remaining body dead (record + skip); nested = record a
            # pending path return like a dynamic one-sided return.
            try:
                _block(ctx, s.body if taken else s.orelse)
            except _FnReturn as r:
                v = _combine_pendings(ctx, None, r.value)
                if ctx._cond_stack:
                    ctx._fn_pend.append((_path_taken(ctx), True, v))
                elif ctx._static_ret:
                    ctx._static_ret[-1] = v
            return
        env_saved = dict(ctx._env)
        ctx._in_branch = True
        ctx._cond_stack.append((cond, True))
        t_ret = None
        try:
            _block(ctx, s.body)
        except _LoopJump:
            pass  # flags updated; env captured below, tracing continues
        except _FnReturn as r:
            t_ret = r.value
        finally:
            env_true = dict(ctx._env)
            ctx._cond_stack.pop()
        ctx._env = env_saved
        ctx._cond_stack.append((cond, False))
        f_ret = None
        try:
            _block(ctx, s.orelse)
        except _LoopJump:
            pass
        except _FnReturn as r:
            f_ret = r.value
        finally:
            env_false = dict(ctx._env)
            ctx._cond_stack.pop()
        ctx._in_branch = False
        # SSA phi: every name differing between branches merges via select.
        # Arms must share a type — mixing float and bool across branches
        # would miswire the select node, so it fails here.
        for name in set(env_true) | set(env_false):
            t = env_true.get(name, env_saved.get(name))
            f = env_false.get(name, env_saved.get(name))
            # Branch-local name (assigned on one path only, no prior
            # value): not a phi — leave it unbound so a later read fails
            # loudly as path-dependent, instead of mis-typing it as float.
            if t is None or f is None:
                continue
            if t != f:
                tt, ff = ctx._typeof(t), ctx._typeof(f)
                if tt != ff:
                    raise SyntaxError(
                        f"if/else arms for {name!r} mix {tt} and {ff} — "
                        f"both branches must produce the same type")
                ctx._env[name] = ctx._set_type(ctx._emit(
                    {"op": "select", "c": cond, "t": t, "f": f}), tt)
        # A conditional jump inside an arm updates flags and merges envs
        # here; tracing CONTINUES past the if with the rest gating on the
        # flags. (Unconditional jumps never reach here — they only occur
        # with an empty cond-stack, i.e. at body top level, where they
        # unwind straight to the loop driver. break in one arm + continue
        # in the other is fine: arm conditions are exclusive, so exactly
        # one flag fires per tick.)
        # Returns merge the same way values do: both arms -> select and
        # propagate; one arm -> record a pending path return for the next
        # tail return to combine (full path rebuilt by nesting).
        if t_ret is not None and f_ret is not None:
            tt, ff = ctx._typeof(t_ret), ctx._typeof(f_ret)
            if tt != ff:
                raise SyntaxError(
                    f"return arms mix {tt} and {ff} — both must produce "
                    "the same type (helpers return one float)")
            raise _FnReturn(ctx._set_type(ctx._emit(
                {"op": "select", "c": cond, "t": t_ret,
                 "f": f_ret}), tt))
        if t_ret is not None:
            ctx._fn_pend.append((cond, True, t_ret))
        elif f_ret is not None:
            ctx._fn_pend.append((cond, False, f_ret))
    elif isinstance(s, ast.For):
        if not isinstance(s.target, ast.Name):
            raise SyntaxError(
                "for-target must be a single name — "
                f"got {ast.unparse(s.target)[:40]!r}")
        if not (isinstance(s.iter, ast.Call)
                and isinstance(s.iter.func, ast.Name)
                and s.iter.func.id == "range"):
            raise SyntaxError(
                "only for <name> in range(...) with literal ints is "
                f"compilable — got {ast.unparse(s.iter)[:60]!r} (trip "
                "count must be static: the game runs a flat graph)")
        if s.orelse:
            raise SyntaxError(
                "for/else is not compilable yet — restructure with a "
                "flag variable (the unrolled loop always completes, so "
                "else would need exit-tracking)")
        trips = _range_trips(s.iter)
        if len(trips) > MAX_FOR_TRIPS:
            raise SyntaxError(
                f"for-range has {len(trips)} trips (cap {MAX_FOR_TRIPS}) "
                "— chunk it (fewer trips per loop, state in latches "
                "across ticks)")
        _drive_loop(ctx, s, s.target.id, trips, None, None)
    elif isinstance(s, ast.While):
        if s.orelse:
            raise SyntaxError(
                "while/else is not compilable yet — restructure with a "
                "flag variable")
        _drive_loop(ctx, s, None, list(range(MAX_WHILE_TRIPS)), s.test,
                    f"!!while_overflow:L{s.lineno}")
    elif isinstance(s, ast.Break):
        _loop_jump(ctx, "break")
    elif isinstance(s, ast.Continue):
        _loop_jump(ctx, "continue")
    elif isinstance(s, ast.Expr):
        _expr(ctx, s.value)
    elif isinstance(s, ast.Return):
        if ctx._helper_depth == 0:
            raise SyntaxError(
                "return is only allowed inside helper functions "
                "(tick is void)")
        if ctx._loop_stack:
            raise SyntaxError(
                "return inside a loop body — restructure (compute in "
                "the loop, break out, single tail return after it)")
        v = _expr(ctx, s.value) if s.value is not None else ctx._desc(0.0)
        raise _FnReturn(v)
    else:
        raise SyntaxError(
            f"unsupported statement {type(s).__name__} — loops are "
            "for i in range(...) / while cond (bounded, unrolled); "
            "express cross-tick state with api.set_var")


def _block(ctx: _Ctx, stmts: list[ast.stmt]) -> None:
    for s in stmts:
        _stmt(ctx, s)


def compile_source(source: str, target: tuple[str, str], opt: int = 1) -> dict:
    """Parse plain Python source -> description dict (for graphc-rs).

    Helpers are allowed: the bot function is `tick` when defined, else the
    single top-level function (same rule as compile_project).
    opt: 0 = raw ops, 1 = transition-shaving passes (DCE, select-fold).
    """
    return _assemble({"": ast.parse(source)}, [""], target, opt, {""})


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
    real_mods = {""}
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
                    real_mods.add(a.name)
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
                real_mods.add(s.module or "")
                if fp not in seen_files:
                    seen_files.add(fp)
                    modules[s.module or ""] = _load_module(fp)
                    order.append(s.module or "")
    return _assemble(modules, order, target, opt, real_mods)


def _const_number(node: ast.expr) -> float | None:
    """Numeric literal value (incl. unary minus), else None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        v = _const_number(node.operand)
        return None if v is None else -v
    return None


def _assemble(modules: dict[str, ast.Module], order: list[str],
              target: tuple[str, str], opt: int = 1,
              real_mods: set[str] | None = None) -> dict:
    real_mods = real_mods if real_mods is not None else set(order)
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
                if s.name == "api":
                    raise SyntaxError(
                        "cannot name a function 'api' — it is the "
                        "game-API namespace")
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
                    elif a.name == LIBRY or a.name.startswith(LIBRY + "."):
                        # import AIA_Comp_Libry.tennis as t -> latest
                        parts = a.name.split(".")
                        if len(parts) != 2 or not a.asname:
                            raise SyntaxError(
                                f"import {a.name!r}: use "
                                "import AIA_Comp_Libry.<game> as t "
                                "(latest) or the full "
                                "AIA_Comp_Libry.<game>.<version> path")
                        _alias(a.asname, f"@{parts[1].lower()}/latest",
                               "libry")
                    else:
                        # Project file (validated by the crawl): alias the
                        # dotted path for mod.attr resolution. Single
                        # scripts cannot import project files.
                        if a.name not in real_mods:
                            raise SyntaxError(
                                f"import {a.name!r} is not a project file "
                                "(whitelist: api, AIA_Comp_Libry, project "
                                "files — use compile_project for multi-file)")
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
                    # from AIA_Comp_Libry.tennis import v014  (module alias)
                    # from AIA_Comp_Libry.tennis import sensor (latest sensor)
                    parts = (s.module or "").split(".")
                    if len(parts) > 3 or parts[0] != LIBRY:
                        raise SyntaxError(
                            f"import {s.module!r}: use the full "
                            "AIA_Comp_Libry.<game>.<version> path")
                    from .desc import LATEST_TARGETS
                    for a in s.names:
                        if a.name == "*":
                            raise SyntaxError(
                                "star imports are not compilable")
                        if len(parts) == 1:
                            # from AIA_Comp_Libry import tennis (latest)
                            _alias(a.asname or a.name,
                                   f"@{a.name.lower()}/latest",
                                   "libry-from-import")
                        elif len(parts) == 3:
                            game, ver = parts[1].lower(), _norm_ver(parts[2])
                            _alias(a.asname or a.name, f"@{game}/{ver}.{a.name}",
                                   "libry-from-import")
                        elif _norm_ver(a.name) in (
                                _norm_ver(v) for v in LATEST_TARGETS.values()) \
                                or a.name.lower() in LATEST_TARGETS:
                            # version module alias
                            _alias(a.asname or a.name,
                                   f"@{parts[1].lower()}/{_norm_ver(a.name)}",
                                   "libry-from-import")
                        else:
                            # unversioned sensor: latest, pinned at call time
                            _alias(a.asname or a.name,
                                   f"@{parts[1].lower()}/latest.{a.name}",
                                   "libry-from-import")
                elif s.module == "api" or (s.module or "").startswith("api."):
                    for a in s.names:
                        if a.name == "*":
                            raise SyntaxError(
                                "from api import * is not compilable")
                        _alias(a.asname or a.name, "api." + a.name,
                               "from-import")
                else:
                    if (s.module or "") not in real_mods:
                        raise SyntaxError(
                            f"from {s.module!r} import is not a project file "
                            "(whitelist: api, AIA_Comp_Libry, project files)")
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
    # Same name + same value in two files is fine; same name with a
    # DIFFERENT value fails loudly (silent first-wins would mean something
    # other than what one of the files says).
    seen_consts: dict[str, float] = {}
    for mod in order:
        for s in modules[mod].body:
            if isinstance(s, ast.Assign) and len(s.targets) == 1 and \
                    isinstance(s.targets[0], ast.Name):
                v = _const_number(s.value)
                if v is None:
                    continue
                nm = s.targets[0].id
                if nm == "api":
                    raise SyntaxError(
                        "cannot name a constant 'api' — it is the "
                        "game-API namespace")
                if nm in seen_consts and seen_consts[nm] != v:
                    raise SyntaxError(
                        f"constant {nm!r} has conflicting values "
                        f"({seen_consts[nm]} vs {v}) across project files")
                seen_consts[nm] = v
                if nm not in ctx._env:
                    ctx._env[nm] = ctx._desc(v)
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
    fdef = ctx._functions[(bmod, bname)]
    bargs = fdef.args.args
    if len(bargs) != 1 or bargs[0].arg != "api" or fdef.args.vararg \
            or fdef.args.kwarg:
        raise SyntaxError("bot function tick takes exactly (api)")
    # Auto cross-tick state, the one simple rule: a module-level numeric
    # name the bot WRITES becomes a latch; one it only reads stays an
    # inlined constant. No annotation, no api.var/set_var, no static
    # analysis — "written => dynamic, never written => constant".
    assigned_in_bot = {
        n.id for n in ast.walk(fdef)
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)
    }
    for name in sorted(assigned_in_bot & set(seen_consts)):
        if seen_consts[name] != 0:
            raise SyntaxError(
                f"persistent state {name!r} must start at 0 (game variables "
                f"start at 0) — set {name} in tick instead of initializing "
                f"it to {seen_consts[name]}")
        ctx._env.pop(name, None)
        ctx._state_names.add(name)
    saved = dict(ctx._env)
    state_writes: dict[str, int] = {}
    try:
        # Materialize every state name up front (GetVariable). This gives
        # each one a previous-tick base so a branch-local write merges into
        # `select(cond, new, previous)` instead of being dropped; unused
        # reads are dead code and DCE removes them.
        for name in sorted(ctx._state_names):
            ctx._env[name] = ctx._set_type(
                ctx._emit({"op": "var_get", "name": name}), "float")
        _block(ctx, fdef.body)
        for name in ctx._state_dirty:
            if name in ctx._env:
                state_writes[name] = ctx._env[name]
    finally:
        ctx._active.remove((bmod, bname))
        ctx._env = saved
    # One SetVariable per written state name, with the value the tick
    # finished on (branch merges already became selects).
    for name in sorted(state_writes):
        ctx.ops.append({"op": "var_set", "name": name,
                        "v": state_writes[name]})
    if ctx._aim_pending and ctx._controller is None:
        raise SyntaxError(
            "api.tennis_aim without a controller — the aim only steers a "
            "strike; pair it with t.move(...) in the same tick")
    # Recursion overflow canaries: one plot per recursive function that hit
    # the depth budget (value = reached exhaustion count, 0 = clean).
    for qual, sites in ctx._rec_over.items():
        total = sites[0]
        for st in sites[1:]:
            total = _fbin(ctx, "AddFloats", total, st)
        qname = f"{qual[0]}.{qual[1]}" if qual[0] else qual[1]
        ctx.ops.append({"op": "plot", "name": "!!recursion_overflow:" + qname,
                        "v": total})
    _check_chain_depth(ctx)
    from .desc import optimize_ops
    return {
        "schema": "graphc-desc-v1",
        "target": {"game": target[0], "version": target[1]},
        "bot_name": bname,
        "ops": optimize_ops(ctx.ops, opt),
    }