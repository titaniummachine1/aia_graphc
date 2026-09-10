//! graphc backend: description IR -> optimized game save graph.
//!
//! Pipeline (gcc/LLVM shape, scaled down):
//!   description (language-neutral JSON) -> array expansion (pack 3 cells
//!   per Vector3 var, merge same-vector static writes into one RMW) ->
//!   node emission (version-pinned port tables) -> save JSON.
//! Cost metric: per-tick node transitions (nodes + edges) — the C# overhead
//! the game pays on every tick.

use serde::Deserialize;
use std::collections::HashMap;

#[derive(Deserialize, Clone, Debug)]
pub struct Target {
    pub game: String,
    pub version: String,
}

#[derive(Deserialize, Clone, Debug)]
#[serde(tag = "op")]
pub enum Op {
    #[serde(rename = "const")]
    Const { value: f32 },
    #[serde(rename = "var_get")]
    VarGet { name: String },
    #[serde(rename = "var_set")]
    VarSet { name: String, v: usize },
    #[serde(rename = "bin")]
    Bin {
        r#fn: String,
        a: usize,
        b: usize,
        cmp: Option<String>,
    },
    #[serde(rename = "not")]
    Not { b: usize },
    #[serde(rename = "select")]
    Select { c: usize, t: usize, f: usize },
    #[serde(rename = "array")]
    Array { name: String, cells: usize },
    #[serde(rename = "array_set_static")]
    ArraySetStatic { arr: usize, i: usize, v: usize },
    #[serde(rename = "array_get_static")]
    ArrayGetStatic { arr: usize, i: usize },
    #[serde(rename = "array_get_dynamic")]
    ArrayGetDynamic { arr: usize, i: usize },
    #[serde(rename = "soccer_move")]
    SoccerMove { x: usize, z: usize },
    #[serde(rename = "tennis_get")]
    TennisGet {
        kind: String,
        index: usize,
        label: String,
    },
    #[serde(rename = "tennis_move")]
    TennisMove {
        x: usize,
        z: usize,
        swing: Option<usize>,
        shot: Option<usize>,
        sprint: Option<usize>,
    },
}

#[derive(Deserialize, Clone, Debug)]
pub struct Description {
    pub schema: String,
    pub target: Target,
    #[serde(default = "default_bot_name")]
    pub bot_name: String,
    pub ops: Vec<Op>,
}

fn default_bot_name() -> String {
    "graphc_bot".into()
}

/// SSA value after expansion.
#[derive(Clone, Copy, Debug)]
enum Val {
    Const(f32),
    Node(usize, &'static str), // node index + output port
}

/// Port tables from the game's node registry (AIGamePyLibrary `data.ports`;
/// port order AND polarity preserved — polarity != 0 marks the output port).
const PORTS: &[(&str, &[(&str, i32)])] = &[
    ("Float", &[("Float1", 1)]),
    ("AddFloats", &[("Float1", 1), ("Float2", 0), ("Float1", 0)]),
    ("SubtractFloats", &[("Float2", 0), ("Float1", 0), ("Float1", 1)]),
    ("MultiplyFloats", &[("Float1", 1), ("Float2", 0), ("Float1", 0)]),
    ("DivideFloats", &[("Float1", 1), ("Float2", 0), ("Float1", 0)]),
    ("Modulo", &[("Float1", 0), ("Float2", 0), ("Float1", 1)]),
    ("Power", &[("Float1", 0), ("Float2", 0), ("Float1", 1)]),
    ("CompareFloats", &[("Bool1", 1), ("Float1", 0), ("Float2", 0)]),
    ("Not", &[("Bool1", 1), ("Bool1", 0)]),
    (
        "ConditionalSetFloatV2",
        &[("Float1", 0), ("Float2", 0), ("Float1", 1), ("Bool1", 0)],
    ),
    ("GetVariable", &[("Any1", 1)]),
    ("SetVariable", &[("Any1", 0)]),
    (
        "ConstructVector3",
        &[("Vector31", 1), ("Float3", 0), ("Float1", 0), ("Float2", 0)],
    ),
    (
        "Vector3Split",
        &[("Vector31", 0), ("Float1", 1), ("Float2", 1), ("Float3", 1)],
    ),
    ("SoccerController1", &[("Vector31", 0), ("Bool1", 0), ("Bool2", 0)]),
    ("TennisGetBool", &[("Bool1", 1)]),
    ("TennisGetFloat", &[("Float1", 1)]),
    ("TennisGetVector3", &[("Vector31", 1)]),
    ("TennisGetTransform", &[("Transform1", 1)]),
    (
        "TennisController",
        &[("Vector31", 0), ("Bool1", 0), ("Float1", 0), ("Bool2", 0)],
    ),
];

fn ports_table(kind: &str) -> Vec<(&'static str, i32)> {
    PORTS
        .iter()
        .find(|(k, _)| *k == kind)
        .map(|(_, p)| p.to_vec())
        .unwrap_or_else(|| panic!("no port table for {kind}"))
}

fn out_port(kind: &str) -> &'static str {
    match kind {
        "CompareFloats" | "Not" | "TennisGetBool" => "Bool1",
        "GetVariable" => "Any1",
        "ConstructVector3" | "TennisGetVector3" => "Vector31",
        "TennisGetTransform" => "Transform1",
        _ => "Float1",
    }
}

fn comp_out(comp: usize) -> &'static str {
    match comp {
        0 => "Float1",
        1 => "Float2",
        _ => "Float3",
    }
}

fn fmt_float(c: f32) -> String {
    if c.fract() == 0.0 && c.abs() < 1e15 {
        format!("{}", c as i64)
    } else {
        format!("{c}")
    }
}

/// CompareFloats modifier is a Unity Operation dropdown INDEX in the save
/// (the sim eval parses it as i32; AIGamePyLibrary normalizes "==" -> "0").
/// The description IR carries the human-readable operator string.
fn cmp_modifier(cmp: &str) -> String {
    match cmp {
        "==" => "0",
        "<" => "1",
        ">" => "2",
        "<=" => "3",
        ">=" => "4",
        other => panic!("unknown comparison operator {other:?}"),
    }
    .to_string()
}

struct Emitter {
    /// (kind, modifier, ports)
    nodes: Vec<(String, String, Vec<(&'static str, i32)>)>,
    /// (src node, src port, dst node, dst port)
    conns: Vec<(usize, &'static str, usize, &'static str)>,
    consts: HashMap<u64, usize>,
}

impl Emitter {
    fn node(&mut self, kind: &str, modifier: String) -> usize {
        let ports = ports_table(kind);
        self.nodes.push((kind.to_string(), modifier, ports));
        self.nodes.len() - 1
    }

    fn edge(&mut self, src: usize, src_port: &'static str, dst: usize, dst_port: &'static str) {
        self.conns.push((src, src_port, dst, dst_port));
    }

    fn const_node(&mut self, c: f32) -> usize {
        let key = c.to_bits();
        if let Some(&n) = self.consts.get(&(key as u64)) {
            return n;
        }
        let n = self.node("Float", fmt_float(c));
        self.consts.insert(key as u64, n);
        n
    }
}

fn wire_val(em: &mut Emitter, vals: &[Val], id: usize, dst: usize, port: &'static str) {
    match vals[id] {
        Val::Node(n, p) => em.edge(n, p, dst, port),
        Val::Const(c) => {
            let n = em.const_node(c);
            em.edge(n, "Float1", dst, port);
        }
    }
}

fn wire_v(em: &mut Emitter, v: Val, dst: usize, port: &'static str) {
    match v {
        Val::Node(n, p) => em.edge(n, p, dst, port),
        Val::Const(c) => {
            let n = em.const_node(c);
            em.edge(n, "Float1", dst, port);
        }
    }
}

struct ArrayState {
    cells: usize,
    vec_names: Vec<String>,
    /// emitted split node per vec
    splits: HashMap<usize, usize>,
}

pub struct CompileReport {
    pub nodes: usize,
    pub connections: usize,
}

/// Compile a description into save JSON + cost report.
pub fn compile(desc: &Description) -> Result<(serde_json::Value, CompileReport), String> {
    if desc.schema != "graphc-desc-v1" {
        return Err(format!("unknown schema {}", desc.schema));
    }
    let mut em = Emitter {
        nodes: Vec::new(),
        conns: Vec::new(),
        consts: HashMap::new(),
    };
    let mut vals: Vec<Val> = Vec::new();
    // array decl op id -> state
    let mut arrays: HashMap<usize, ArrayState> = HashMap::new();
    // array op id -> (vec k -> comp -> ssa id) pending static writes
    let mut pending: HashMap<usize, HashMap<usize, HashMap<usize, usize>>> = HashMap::new();

    for (op_id, op) in desc.ops.iter().enumerate() {
        match op {
            Op::Const { value } => vals.push(Val::Const(*value)),
            Op::VarGet { name } => {
                let n = em.node("GetVariable", name.clone());
                vals.push(Val::Node(n, "Any1"));
            }
            Op::VarSet { name, v } => {
                let n = em.node("SetVariable", name.clone());
                wire_val(&mut em, &vals, *v, n, "Any1");
                vals.push(Val::Const(0.0)); // placeholder: op id alignment
            }
            Op::Bin { r#fn, a, b, cmp } => {
                let modifier = match cmp {
                    Some(c) => cmp_modifier(c),
                    None => String::new(),
                };
                let n = em.node(r#fn, modifier);
                wire_val(&mut em, &vals, *a, n, "Float1");
                wire_val(&mut em, &vals, *b, n, "Float2");
                vals.push(Val::Node(n, out_port(r#fn)));
            }
            Op::Not { b } => {
                let n = em.node("Not", String::new());
                wire_val(&mut em, &vals, *b, n, "Bool1");
                vals.push(Val::Node(n, "Bool1"));
            }
            Op::Select { c, t, f } => {
                let n = em.node("ConditionalSetFloatV2", String::new());
                wire_val(&mut em, &vals, *c, n, "Bool1");
                wire_val(&mut em, &vals, *t, n, "Float1");
                wire_val(&mut em, &vals, *f, n, "Float2");
                vals.push(Val::Node(n, "Float1"));
            }
            Op::Array { name, cells } => {
                let vec_names = (0..(*cells + 2) / 3)
                    .map(|k| format!("{name}_v{k}"))
                    .collect();
                arrays.insert(
                    op_id,
                    ArrayState {
                        cells: *cells,
                        vec_names,
                        splits: HashMap::new(),
                    },
                );
                vals.push(Val::Const(0.0)); // handle placeholder, never wired
            }
            Op::ArraySetStatic { arr, i, v } => {
                let (k, comp) = (*i / 3, *i % 3);
                pending
                    .entry(*arr)
                    .or_default()
                    .entry(k)
                    .or_default()
                    .insert(comp, *v);
                vals.push(Val::Const(0.0)); // placeholder: op id alignment
            }
            Op::ArrayGetStatic { arr, i } => {
                let nv = arrays[arr].vec_names.len();
                for k in 0..nv {
                    flush_vec(&mut em, *arr, k, &mut pending, &mut arrays, &vals);
                }
                let (k, comp) = (*i / 3, *i % 3);
                let split = get_split(&mut em, arrays.get_mut(arr).unwrap(), k);
                vals.push(Val::Node(split, comp_out(comp)));
            }
            Op::ArrayGetDynamic { arr, i } => {
                let nv = arrays[arr].vec_names.len();
                for k in 0..nv {
                    flush_vec(&mut em, *arr, k, &mut pending, &mut arrays, &vals);
                }
                for k in 0..nv {
                    get_split(&mut em, arrays.get_mut(arr).unwrap(), k);
                }
                let cells = arrays[arr].cells;
                let mut acc = cell_val(arrays.get(arr).unwrap(), 0);
                for k in 1..cells {
                    let cond = em.node("CompareFloats", "==".into());
                    wire_val(&mut em, &vals, *i, cond, "Float1");
                    let kc = em.const_node(k as f32);
                    em.edge(kc, "Float1", cond, "Float2");
                    let sel = em.node("ConditionalSetFloatV2", String::new());
                    em.edge(cond, "Bool1", sel, "Bool1");
                    let cell = cell_val(arrays.get(arr).unwrap(), k);
                    wire_v(&mut em, cell, sel, "Float1");
                    wire_v(&mut em, acc, sel, "Float2");
                    acc = Val::Node(sel, "Float1");
                }
                vals.push(acc);
            }
            Op::SoccerMove { x, z } => {
                let vec = em.node("ConstructVector3", String::new());
                wire_val(&mut em, &vals, *x, vec, "Float1");
                wire_val(&mut em, &vals, *z, vec, "Float3");
                let n = em.node("SoccerController1", String::new());
                em.edge(vec, "Vector31", n, "Vector31");
                vals.push(Val::Const(0.0)); // placeholder: op id alignment
            }
            Op::TennisGet { kind, index, .. } => {
                let node_kind = match kind.as_str() {
                    "bool" => "TennisGetBool",
                    "float" => "TennisGetFloat",
                    "vector3" => "TennisGetVector3",
                    "transform" => "TennisGetTransform",
                    other => return Err(format!("unknown tennis sensor kind {other:?}")),
                };
                let n = em.node(node_kind, index.to_string());
                vals.push(Val::Node(n, out_port(node_kind)));
            }
            Op::TennisMove { x, z, swing, shot, sprint } => {
                let vec = em.node("ConstructVector3", String::new());
                wire_val(&mut em, &vals, *x, vec, "Float1");
                wire_val(&mut em, &vals, *z, vec, "Float3");
                let n = em.node("TennisController", String::new());
                em.edge(vec, "Vector31", n, "Vector31");
                if let Some(s) = swing {
                    wire_val(&mut em, &vals, *s, n, "Bool1");
                }
                if let Some(s) = shot {
                    wire_val(&mut em, &vals, *s, n, "Float1");
                }
                if let Some(s) = sprint {
                    wire_val(&mut em, &vals, *s, n, "Bool2");
                }
                vals.push(Val::Const(0.0)); // placeholder: op id alignment
            }
        }
    }

    // final flush: remaining pending writes (arrays never read)
    let arr_ids: Vec<usize> = pending.keys().copied().collect();
    for arr in arr_ids {
        let nv = arrays.get(&arr).unwrap().vec_names.len();
        for k in 0..nv {
            flush_vec(&mut em, arr, k, &mut pending, &mut arrays, &vals);
        }
    }

    let report = CompileReport {
        nodes: em.nodes.len(),
        connections: em.conns.len(),
    };
    Ok((emit_save(&em), report))
}

fn get_split(em: &mut Emitter, arr: &mut ArrayState, k: usize) -> usize {
    *arr.splits.entry(k).or_insert_with(|| {
        let var = em.node("GetVariable", arr.vec_names[k].clone());
        let split = em.node("Vector3Split", String::new());
        em.edge(var, "Any1", split, "Vector31");
        split
    })
}

fn cell_val(arr: &ArrayState, cell: usize) -> Val {
    Val::Node(arr.splits[&(cell / 3)], comp_out(cell % 3))
}

/// Merge-flush all pending comp writes for one packed vector (single RMW).
fn flush_vec(
    em: &mut Emitter,
    arr: usize,
    k: usize,
    pending: &mut HashMap<usize, HashMap<usize, HashMap<usize, usize>>>,
    arrays: &mut HashMap<usize, ArrayState>,
    vals: &[Val],
) {
    let Some(mut comps) = pending.entry(arr).or_default().remove(&k) else {
        return;
    };
    let split = get_split(em, arrays.get_mut(&arr).unwrap(), k);
    let vec = em.node("ConstructVector3", String::new());
    for comp in 0..3usize {
        match comps.remove(&comp) {
            Some(ssa) => wire_val(em, vals, ssa, vec, comp_out(comp)),
            None => em.edge(split, comp_out(comp), vec, comp_out(comp)),
        }
    }
    let vec_name = arrays.get(&arr).unwrap().vec_names[k].clone();
    let store = em.node("SetVariable", vec_name);
    em.edge(vec, "Vector31", store, "Any1");
}

// ---------- save emission ----------

fn uuid(counter: &mut u64) -> String {
    *counter += 1;
    let mut z = (*counter as u64)
        .wrapping_mul(0x9E3779B97F4A7C15)
        ^ std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map(|d| d.as_nanos() as u64)
            .unwrap_or(0x1234_5678_9ABC_DEF0);
    let mut bytes = [0u8; 16];
    for b in bytes.iter_mut() {
        z ^= z << 13;
        z ^= z >> 7;
        z ^= z << 17;
        *b = (z & 0xFF) as u8;
    }
    bytes[6] = (bytes[6] & 0x0F) | 0x40;
    bytes[8] = (bytes[8] & 0x3F) | 0x80;
    format!(
        "{:02x}{:02x}{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}",
        bytes[0], bytes[1], bytes[2], bytes[3], bytes[4], bytes[5], bytes[6], bytes[7],
        bytes[8], bytes[9], bytes[10], bytes[11], bytes[12], bytes[13], bytes[14], bytes[15]
    )
}

fn zero_rect() -> serde_json::Value {
    serde_json::json!({
        "position": {"x": 0.0, "y": 0.0, "z": 0.0},
        "localPosition": {"x": 0.0, "y": 0.0, "z": 0.0},
        "anchoredPosition": {"x": 0.0, "y": 0.0},
        "anchorMin": {"x": 0.0, "y": 0.0},
        "anchorMax": {"x": 0.0, "y": 0.0},
        "sizeDelta": {"x": 0.0, "y": 0.0},
        "scale": {"x": 0.0, "y": 0.0, "z": 0.0}
    })
}

fn node_color() -> serde_json::Value {
    serde_json::json!({"r": 0.21960784494876862, "g": 0.21960784494876862, "b": 0.21960784494876862, "a": 1.0})
}

fn emit_save(em: &Emitter) -> serde_json::Value {
    let mut counter = 0u64;
    let node_sids: Vec<String> = (0..em.nodes.len()).map(|_| uuid(&mut counter)).collect();
    // One sid per port INSTANCE (registry order). Duplicate port names within
    // a node (e.g. AddFloats in/out both named "Float1") must keep distinct
    // sids or connections resolve to the wrong port.
    let port_sids: Vec<Vec<String>> = em
        .nodes
        .iter()
        .map(|(_, _, ports)| (0..ports.len()).map(|_| uuid(&mut counter)).collect())
        .collect();

    let mut nodes = Vec::new();
    for (i, (kind, modifier, ports)) in em.nodes.iter().enumerate() {
        let mut plist = Vec::new();
        for (j, (pid, pol)) in ports.iter().enumerate() {
            plist.push(serde_json::json!({
                "serializableRectTransform": zero_rect(),
                "id": pid,
                "sID": port_sids[i][j],
                "polarity": pol,
                "controlPointSerializableRectTransform": zero_rect(),
                "nodeSID": node_sids[i],
            }));
        }
        nodes.push(serde_json::json!({
            "serializableRectTransform": zero_rect(),
            "id": kind,
            "sID": node_sids[i],
            "modifier": modifier,
            "ownerFunctionSID": "",
            "serializeSizeDelta": false,
            "serializeColor": false,
            "serializableDefaultColor": node_color(),
            "defaultColor": node_color(),
            "serializablePorts": plist,
        }));
    }

    // Resolve an edge endpoint to its port sid. Names are ambiguous within a
    // node, polarity is not: a source needs the output port (polarity != 0),
    // a destination the input port (polarity == 0) — same rule the sim's
    // input_port_sid/output_port_sid and AIGamePyLibrary use.
    let find_sid = |n: usize, port: &str, out: bool| -> String {
        let (ports, sids) = (&em.nodes[n].2, &port_sids[n]);
        for (j, (pid, pol)) in ports.iter().enumerate() {
            if *pid == port && (*pol != 0) == out {
                return sids[j].clone();
            }
        }
        panic!("node {n} has no {} port named {port:?}", if out { "output" } else { "input" });
    };

    let mut conns = Vec::new();
    for (s, sp, d, dp) in &em.conns {
        conns.push(serde_json::json!({
            "sID": uuid(&mut counter),
            "port0InstanceID": 0,
            "port1InstanceID": 0,
            "port0SID": find_sid(*s, sp, true),
            "port1SID": find_sid(*d, dp, false),
        }));
    }

    serde_json::json!({
        "serializableNodes": nodes,
        "serializableConnections": conns,
    })
}