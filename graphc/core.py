"""graphc core: symbolic tracing over AIGamePyLibrary node emission.

Every traced operation emits at most one node; constants fold at trace
time; identical operations are CSE'd (node reuse = fewer per-tick
transitions). The cost report counts nodes + connections — the per-tick
traversal metric the game pays on every tick.
"""
from __future__ import annotations

import os
import sys

# AIGamePyLibrary is the game-save emitter (node JSON writer). Until it is
# published as a package, point GRAPHC_PYLIB at its checkout.
PYLIB = os.environ.get(
    "GRAPHC_PYLIB",
    r"C:\gitProjects\AIA_tennis\AIGamePyLibrary",
)
if PYLIB not in sys.path:
    sys.path.insert(0, PYLIB)

from AIGamePyLibrary import AddNode, ConnectPorts, SaveData  # noqa: E402


class Sym:
    """Traced value: node output port or folded constant."""

    __slots__ = ("ctx", "node", "port", "const")

    def __init__(self, ctx, node, port, const=None):
        self.ctx = ctx
        self.node = node
        self.port = port
        self.const = const

    def _binop(self, name, other, swap=False):
        a = self.ctx._as_node_sym(self)
        b = self.ctx._as_node_sym(other)
        if swap:
            a, b = b, a
        return self.ctx.op2(name, a, b)

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

    def _cmp(self, other, op: str, swap=False):
        a = self.ctx._as_node_sym(self)
        b = self.ctx._as_node_sym(other)
        if swap:
            a, b = b, a
        return self.ctx.op2("CompareFloats", a, b, out_port="Bool1",
                            value=op)

    def __lt__(self, o): return self._cmp(o, "<")

    def __gt__(self, o): return self._cmp(o, ">")

    def __le__(self, o): return self._cmp(o, "<=")

    def __ge__(self, o): return self._cmp(o, ">=")

    def __eq__(self, o): return self._cmp(o, "==")

    def __ne__(self, o): return self.ctx.not_(self._cmp(o, "=="))


class GraphCtx:
    """Tracing context for one target (game, version).

    Targets are explicit and version-pinned: sensor/controller helpers only
    exist for known (game, version) pairs; "universal" emits raw nodes for
    unknown games. There is no implicit default target.
    """

    def __init__(self, target: tuple[str, str]):
        self.target = target
        self.cse: dict = {}
        self.nodes = 0
        self.conns = 0
        self._arrays: list = []

    # --- node plumbing ----------------------------------------------------
    def new_node(self, name, value=""):
        self.nodes += 1
        return AddNode(name, value)

    def connect(self, src_sym: Sym, dst_node, dst_port):
        self.conns += 1
        ConnectPorts((src_sym.port, dst_port), src_sym.node, dst_node)

    def _as_node_sym(self, v) -> Sym:
        if isinstance(v, Sym):
            return v if v.node is not None else self.const(float(v.const))
        return self.const(float(v))

    def const(self, v: float) -> Sym:
        key = ("const", float(v))
        sym = self.cse.get(key)
        if sym is None:
            text = str(int(v)) if float(v).is_integer() else repr(float(v))
            sym = self.sym(self.new_node("Float", text), "Float1")
            self.cse[key] = sym
        return sym

    def sym(self, node, port) -> Sym:
        return Sym(self, node, port)

    def op2(self, name, a: Sym, b: Sym, out_port="Float1",
            value: str = "") -> Sym:
        key = (name, value, id(a.node), id(b.node), out_port)
        sym = self.cse.get(key)
        if sym is not None:
            return sym
        n = self.new_node(name, value)
        self.connect(a, n, "Float1")
        self.connect(b, n, "Float2")
        sym = self.sym(n, out_port)
        self.cse[key] = sym
        return sym

    def not_(self, b: Sym) -> Sym:
        n = self.new_node("Not")
        self.connect(b, n, "Bool1")
        return self.sym(n, "Bool1")

    # --- memory: named latches ---------------------------------------------
    def var_get(self, name: str) -> Sym:
        key = ("getvar", name)
        sym = self.cse.get(key)
        if sym is None:
            sym = self.sym(self.new_node("GetVariable", name), "Any1")
            self.cse[key] = sym
        return sym

    def var_set(self, name: str, value) -> None:
        n = self.new_node("SetVariable", name)
        self.connect(self._as_node_sym(value), n, "Any1")

    # --- control flow --------------------------------------------------------
    def select(self, cond, t, f) -> Sym:
        """if/else as a node; both arms evaluate every tick (game semantics).
        The unwired-false variant is the game's native previous-tick HOLD."""
        c = self._as_node_sym(cond)
        tn = self._as_node_sym(t)
        fn = self._as_node_sym(f)
        n = self.new_node("ConditionalSetFloatV2")
        self.connect(c, n, "Bool1")
        self.connect(tn, n, "Float1")
        self.connect(fn, n, "Float2")
        return self.sym(n, "Float1")

    # --- game surface (version-pinned; grows with targets.py) ---------------
    def soccer_move(self, x, z) -> None:
        """Controller 1 move target; second arg is the pitch-plane Z axis
        (the game's move vector reads X/Z)."""
        if self.target[0] != "soccer":
            raise TypeError(f"soccer_move is not valid for target {self.target}")
        n = self.new_node("SoccerController1")
        vec = self.new_node("ConstructVector3")
        self.connect(self._as_node_sym(x), vec, "Float1")
        self.connect(self._as_node_sym(z), vec, "Float3")
        self.connect(self.sym(vec, "Vector31"), n, "Vector31")

    # --- arrays -------------------------------------------------------------
    def array(self, name: str, cells: int) -> PackedArray:
        arr = PackedArray(self, name, cells)
        self._arrays.append(arr)
        return arr


class PackedArray:
    """Fixed-capacity array packed into Vector3 variables (3 cells each).

    Static writes to the SAME vector in one tick are MERGED into a single
    split+construct+store (the compiler handles read-modify-write; the user
    never thinks about components). Dynamic read: select-chain over cells —
    charged honestly in the cost report.
    """

    def __init__(self, ctx: GraphCtx, name: str, cells: int):
        self.ctx = ctx
        self.name = name
        self.cells = cells
        self.n_vecs = (cells + 2) // 3
        self._splits: dict[int, object] = {}
        self._pending_map: dict[int, dict[int, object]] = {}  # vec -> comp -> val

    def _var(self, k: int) -> Sym:
        return self.ctx.var_get(f"{self.name}_v{k}")

    def _split(self, k: int) -> object:
        if k not in self._splits:
            s = self.ctx.new_node("Vector3Split")
            self.ctx.connect(self._var(k), s, "Vector31")
            self._splits[k] = s
        return self._splits[k]

    def set_static(self, i: int, value) -> None:
        k, comp = divmod(int(i), 3)
        self._pending_map.setdefault(k, {})[comp] = value

    def _flush(self, k: int) -> None:
        """Emit the merged write for vector k (split + construct + store)."""
        ctx = self.ctx
        comps = self._pending_map.pop(k, None)
        if not comps:
            return
        split = self._split(k)
        vec = ctx.new_node("ConstructVector3")
        for comp, out_port, in_port in ((0, "Float1", "Float1"),
                                        (1, "Float2", "Float2"),
                                        (2, "Float3", "Float3")):
            if comp in comps:
                ctx.connect(ctx._as_node_sym(comps[comp]), vec, in_port)
            else:
                ctx.connect(ctx.sym(split, out_port), vec, in_port)
        store = ctx.new_node("SetVariable", f"{self.name}_v{k}")
        ctx.connect(ctx.sym(vec, "Vector31"), store, "Any1")

    def flush(self) -> None:
        """Emit all pending merged writes (call once per tick's stores)."""
        for k in sorted(set(self._pending_map) | set(range(self.n_vecs))):
            if k in self._pending_map:
                self._flush(k)

    def get_static(self, i: int) -> Sym:
        k, comp = divmod(int(i), 3)
        self._flush(k)  # reads observe this tick's pending writes (RMW order)
        return self.ctx.sym(self._split(k), f"Float{comp + 1}")

    def get_dynamic(self, idx) -> Sym:
        for k in range(self.n_vecs):
            self._flush(k)
        acc = self.get_static(0)
        for k in range(1, self.cells):
            cond = self.ctx.op2("CompareFloats", self.ctx._as_node_sym(idx),
                                self.ctx._as_node_sym(float(k)),
                                out_port="Bool1", value="==")
            cell = self.ctx.sym(self._split(k // 3), f"Float{(k % 3) + 1}")
            acc = self.ctx.select(cond, cell, acc)
        return acc


def compile_graph(target: tuple[str, str], builder, out_path: str | None = None,
                  bot_name: str = "graphc_bot") -> dict:
    """Trace `builder(ctx)` once for (game, version), save, report cost.

    out_path=None writes directly into the game's save folder:
    %USERPROFILE%\\AppData\\LocalLow\\Unicorn One\\AIComp\\Saves\\<Game>\\
    <bot_name>.txt — the writer never sees node internals.
    """
    ctx = GraphCtx(target)
    builder(ctx)
    for v in ctx._arrays:
        v.flush()
    if out_path is None:
        game, _version = target
        base = Path(os.path.expanduser("~"),
                    "AppData", "LocalLow", "Unicorn One", "AIComp",
                    "Saves", game.capitalize())
        base.mkdir(parents=True, exist_ok=True)
        out_path = str(base / f"{bot_name}.txt")
    SaveData(out_path, "single")
    report = {
        "target": target,
        "nodes": ctx.nodes,
        "connections": ctx.conns,
        "per_tick_transitions": ctx.nodes + ctx.conns,
        "path": out_path,
    }
    print(f"graphc: {out_path} -> "
          f"{report['nodes']} nodes / {report['per_tick_transitions']} "
          f"per-tick transitions")
    return report