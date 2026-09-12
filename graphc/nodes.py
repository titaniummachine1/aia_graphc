"""Node + IR reference for authors and LLMs (single source of truth).

You NEVER wire nodes, ports, or connections by hand. You write plain Python
with the AIA_Comp_Libry API (``import AIA_Comp_Libry.tennis.v15f as t``);
the compiler assigns every value a TYPE, checks every connection, and emits
the game save. An illegal connection (bool into arithmetic, vector into a
float slot, transform into split_vector, ...) fails HERE with a pointing
error — never a silently wrong bot.

Value types (author-visible):
  float     — a number (positions, speeds, charges, shot ids, math results)
  bool      — a true/false sensor or comparison (serve phase, in-range, <, ==)
  vector    — an opaque 3D point (aim targets, ball velocity). Only splits
               into floats via api.split_vector(v, 0/1/2) or feeds move_vec.
  transform — an opaque placed object (Self, Opponent, Ball). NOT splittable;
              pick a vector3 sensor instead.
  array     — an api.array handle (RAM). Only set_array_cell /
              get_array_cell use it.

Game nodes emitted by the backend (what the save contains):
"""
from __future__ import annotations

VALUE_TYPES = ("float", "bool", "vector", "transform", "array")

#: kind -> {inputs: [(port, type)], output: type|None, desc}.
#: Port names match the save JSON; polarity != 0 marks the output port.
NODE_DOCS: dict[str, dict] = {
    "Float": {
        "inputs": [],
        "output": "float",
        "desc": "Constant number (modifier holds the value).",
    },
    "AddFloats": {
        "inputs": [("Float1", "float"), ("Float2", "float")],
        "output": "float",
        "desc": "a + b.",
    },
    "SubtractFloats": {
        "inputs": [("Float1", "float"), ("Float2", "float")],
        "output": "float",
        "desc": "a - b (also unary minus as 0 - x).",
    },
    "MultiplyFloats": {
        "inputs": [("Float1", "float"), ("Float2", "float")],
        "output": "float",
        "desc": "a * b.",
    },
    "DivideFloats": {
        "inputs": [("Float1", "float"), ("Float2", "float")],
        "output": "float",
        "desc": "a / b.",
    },
    "Modulo": {
        "inputs": [("Float1", "float"), ("Float2", "float")],
        "output": "float",
        "desc": "a % b.",
    },
    "Power": {
        "inputs": [("Float1", "float"), ("Float2", "float")],
        "output": "float",
        "desc": "a ** b.",
    },
    "CompareFloats": {
        "inputs": [("Float1", "float"), ("Float2", "float")],
        "output": "bool",
        "desc": "Compare a vs b; modifier is the dropdown INDEX "
        "(0 ==, 1 <, 2 >, 3 <=, 4 >=).",
    },
    "Not": {
        "inputs": [("Bool1", "bool")],
        "output": "bool",
        "desc": "Logical not.",
    },
    "ConditionalSetFloatV2": {
        "inputs": [("Bool1", "bool"), ("Float1", "float"), ("Float2", "float")],
        "output": "float",
        "desc": "Per-tick select: Bool1 picks Float1 (true) or Float2 "
        "(false). Both arms evaluate every tick; unwired false holds "
        "the previous tick. Also backs if/else SSA merges.",
    },
    "GetVariable": {
        "inputs": [],
        "output": "float",
        "desc": "Cross-tick read (modifier names the latch).",
    },
    "SetVariable": {
        "inputs": [("Any1", "float")],
        "output": None,
        "desc": "Cross-tick write (modifier names the latch). Sink.",
    },
    "String": {
        "inputs": [],
        "output": "string",
        "desc": "Static text constant (modifier holds it). Only feeds "
        "TimePlot channel names — strings never enter arithmetic.",
    },
    "TimePlot": {
        "inputs": [("String1", "string"), ("Float1", "float")],
        "output": None,
        "desc": "Debug sink: records Float1 per tick under the String1 "
        "channel. Authors call api.plot(channel, value). Sink, repeatable; "
        "the channel is readable in game (TimePlot export), sim, pure VM.",
    },
    "ConstructVector3": {
        "inputs": [("Float1", "float"), ("Float2", "float"), ("Float3", "float")],
        "output": "vector",
        "desc": "Build a vector from 3 floats (x, y, z).",
    },
    "Vector3Split": {
        "inputs": [("Vector31", "vector")],
        "output": "float",
        "desc": "Split one component out of a vector (Float1=x, "
        "Float2=y, Float3=z). One node shared per source vector.",
    },
    "SoccerController1": {
        "inputs": [("Vector31", "vector"), ("Bool1", "bool"), ("Bool2", "bool")],
        "output": None,
        "desc": "Soccer drive target. Authors call api.move(x, z) — "
        "the compiler builds the vector. Sink, one per tick.",
    },
    "TennisGetBool": {
        "inputs": [],
        "output": "bool",
        "desc": "Tennis bool sensor (modifier = dropdown index).",
    },
    "TennisGetFloat": {
        "inputs": [],
        "output": "float",
        "desc": "Tennis float sensor (modifier = dropdown index).",
    },
    "TennisGetVector3": {
        "inputs": [],
        "output": "vector",
        "desc": "Tennis vector3 sensor (modifier = dropdown index).",
    },
    "TennisGetTransform": {
        "inputs": [],
        "output": "transform",
        "desc": "Tennis transform sensor (modifier = dropdown index). "
        "Opaque — cannot feed split_vector or arithmetic.",
    },
    "TennisController": {
        "inputs": [
            ("Vector31", "vector"),
            ("Bool1", "bool"),
            ("Float1", "float"),
            ("Bool2", "bool"),
        ],
        "output": None,
        "desc": "Tennis drive+strike: Vector31 aim, Bool1 swing/charge, "
        "Float1 shot id, Bool2 sprint. Authors call "
        "t.move(x, z, swing, shot, sprint) or t.move_vec(v, ...), which "
        "route the request through TennisAutoAim + TennisAutoMove below "
        "(the native assist chain). Sink, one per tick.",
    },
    "TennisAutoAim": {
        "inputs": [("Vector31", "vector")],
        "output": "vector",
        "desc": "Game aim assist: corrects the request the way it does "
        "for native bots. Emitted automatically by t.move/t.move_vec; "
        "authors never wire it by hand.",
    },
    "TennisAutoMove": {
        "inputs": [("Vector31", "vector"), ("Vector32", "vector")],
        "output": "vector",
        "desc": "Game movement gate: Vector31 move target, Vector32 "
        "assisted aim; output drives the controller. Emitted "
        "automatically by t.move/t.move_vec.",
    },
    "SoccerGetBool": {
        "inputs": [],
        "output": "bool",
        "desc": "Soccer bool sensor (modifier = dropdown index).",
    },
    "SoccerGetFloat": {
        "inputs": [],
        "output": "float",
        "desc": "Soccer float sensor (modifier = dropdown index).",
    },
    "SoccerGetVector3": {
        "inputs": [],
        "output": "vector",
        "desc": "Soccer vector3 sensor (modifier = dropdown index).",
    },
    "SoccerGetTransform": {
        "inputs": [],
        "output": "transform",
        "desc": "Soccer transform sensor (modifier = dropdown index). "
        "Opaque — feed api.position_of for the world position vector.",
    },
    "RelativePosition": {
        "inputs": [("Transform1", "transform")],
        "output": "vector",
        "desc": "World position vector out of a transform (modifier 13 = "
        "World). Authors call api.position_of(t), then split_vector for x/y/z.",
    },
}

#: Description-IR op -> {args: [(field, type)], returns: type|None, desc}.
#: This is what the Python frontend emits; the backend lowers it to NODES.
IR_OPS: dict[str, dict] = {
    "const": {
        "args": [],
        "returns": "float",
        "desc": "Numeric literal.",
    },
    "var_get": {
        "args": [],
        "returns": "float",
        "desc": "api.var(name): cross-tick float latch read.",
    },
    "var_set": {
        "args": [("v", "float")],
        "returns": None,
        "desc": "api.set_var(name, v): cross-tick float latch write. "
        "Once per name per tick.",
    },
    "bin": {
        "args": [("a", "float"), ("b", "float")],
        "returns": "float|bool",
        "desc": "Arithmetic (float->float) or CompareFloats (float->bool).",
    },
    "not": {
        "args": [("b", "bool")],
        "returns": "bool",
        "desc": "not b.",
    },
    "select": {
        "args": [("c", "bool"), ("t", "float|bool|vector"),
                 ("f", "float|bool|vector")],
        "returns": "float|bool|vector",
        "desc": "if/else merge: both arms same type as result (float ->
                 ConditionalSetFloatV2, bool -> ConditionalSetBool, vector
                 -> ConditionalSetVector3).",
    },
    "array": {
        "args": [],
        "returns": "array",
        "desc": 'api.array(name, cells): packed RAM handle.',
    },
    "array_set_static": {
        "args": [("arr", "array"), ("v", "float")],
        "returns": None,
        "desc": "api.set_array_cell(buf, i, v): static cell write.",
    },
    "array_get_static": {
        "args": [("arr", "array")],
        "returns": "float",
        "desc": "api.get_array_cell(buf, i): static cell read.",
    },
    "array_get_dynamic": {
        "args": [("arr", "array"), ("i", "float")],
        "returns": "float",
        "desc": "api.get_array_cell_dynamic(buf, idx): decoded cell read.",
    },
    "soccer_move": {
        "args": [("x", "float"), ("z", "float")],
        "returns": None,
        "desc": "api.move(x, z).",
    },
    "plot": {
        "args": [("v", "float")],
        "returns": None,
        "desc": "api.plot(channel, v): TimePlot debug sink. The channel "
        "name is a static string (save metadata, not an op ref). DCE root "
        "on every target.",
    },
    "tennis_get": {
        "args": [],
        "returns": "bool|float|vector|transform",
        "desc": "Sensor read; kind fixed per label.",
    },
    "tennis_move": {
        "args": [
            ("x", "float"),
            ("z", "float"),
            ("swing", "bool|None"),
            ("shot", "float|None"),
            ("sprint", "bool|None"),
        ],
        "returns": None,
        "desc": "t.move(x, z, swing, shot, sprint).",
    },
    "vec_split": {
        "args": [("v", "vector")],
        "returns": "float",
        "desc": "api.split_vector(v, 0/1/2): vector component -> float.",
    },
    "vec_make": {
        "args": [("x", "float"), ("y", "float"), ("z", "float")],
        "returns": "vector",
        "desc": "api.make_vector(x, y, z): 3 floats -> vector.",
    },
    "tennis_move_vec": {
        "args": [
            ("v", "vector"),
            ("swing", "bool|None"),
            ("shot", "float|None"),
            ("sprint", "bool|None"),
        ],
        "returns": None,
        "desc": "t.move_vec(v, ...): vector-driven controller.",
    },
    "tennis_aim": {
        "args": [("x", "float"), ("z", "float")],
        "returns": None,
        "desc": "t.aim(x, z): strike-aim request for the next move "
        "(autoswitch — walk wire untouched). One per tick, paired.",
    },
    "tennis_auto_swing": {
        "args": [("shot", "float")],
        "returns": "bool",
        "desc": "t.auto_swing(shot, mode): game swing node (Prefer "
        "Charge default) — wire the bool into move's swing.",
    },
    "tennis_aim": {
        "args": [("x", "float"), ("z", "float")],
        "returns": None,
        "desc": "api.tennis_aim / t.aim(x, z): strike-aim request for the "
        "next move (autoswitch — walk wire untouched). One per tick, "
        "paired with a controller.",
    },
    "tennis_auto_swing": {
        "args": [("shot", "float")],
        "returns": "bool",
        "desc": "api.tennis_auto_swing / t.auto_swing(shot, mode): game "
        "swing node (Prefer Charge default) — wire the bool into move.",
    },
    "soccer_get": {
        "args": [],
        "returns": "bool|float|vector|transform",
        "desc": "Soccer sensor read (backend lowering pending).",
    },
    "transform_pos": {
        "args": [("v", "transform")],
        "returns": "vector",
        "desc": "api.position_of(t): RelativePosition(World) — transform to "
        "world position vector.",
    },
}

__all__ = ["VALUE_TYPES", "NODE_DOCS", "IR_OPS"]
