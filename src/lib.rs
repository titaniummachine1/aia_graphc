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
    #[serde(rename = "vec_split")]
    VecSplit { v: usize, i: usize },
    #[serde(rename = "vec_make")]
    VecMake { x: usize, y: usize, z: usize },
    #[serde(rename = "tennis_move_vec")]
    TennisMoveVec {
        v: usize,
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

impl std::fmt::Debug for CompileReport {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "CompileReport {{ nodes: {}, connections: {} }}",
            self.nodes, self.connections
        )
    }
}

/// Pinned (game, version) targets with a game-API surface. ("universal",
/// any version) is the raw-emission fallback: game-API ops are rejected,
/// pure value/memory ops still emit. Anything else is an error — version
/// strings are never silently accepted (tennis v0.12 vs v0.14 differ).
fn check_target(game: &str, version: &str) -> Result<(), String> {
    match (game, version) {
        ("soccer", "v0.12") | ("tennis", "v0.14") => Ok(()),
        ("universal", _) => Ok(()),
        _ => Err(format!(
            "unknown target (\"{game}\", \"{version}\") — supported: \
             (\"soccer\", \"v0.12\"), (\"tennis\", \"v0.14\"), \
             (\"universal\", <version>) raw-only"
        )),
    }
}

fn require_game(desc_game: &str, want: &str, op: &str) -> Result<(), String> {
    if desc_game == want {
        Ok(())
    } else {
        Err(format!("{op} is not valid for target game \"{desc_game}\""))
    }
}

/// Compile a description into save JSON + cost report.
pub fn compile(desc: &Description) -> Result<(serde_json::Value, CompileReport), String> {
    if desc.schema != "graphc-desc-v1" {
        return Err(format!("unknown schema {}", desc.schema));
    }
    check_target(&desc.target.game, &desc.target.version)?;
    let game = desc.target.game.as_str();
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
    // vec_split source ssa id -> shared Vector3Split node
    let mut vec_splits: HashMap<usize, usize> = HashMap::new();

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
                    // Dropdown index "0" == equality (never the raw "=="
                    // string — the sim parses the modifier as i32).
                    let cond = em.node("CompareFloats", "0".into());
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
                require_game(game, "soccer", "soccer_move")?;
                let vec = em.node("ConstructVector3", String::new());
                wire_val(&mut em, &vals, *x, vec, "Float1");
                wire_val(&mut em, &vals, *z, vec, "Float3");
                let n = em.node("SoccerController1", String::new());
                em.edge(vec, "Vector31", n, "Vector31");
                vals.push(Val::Const(0.0)); // placeholder: op id alignment
            }
            Op::TennisGet { kind, index, .. } => {
                require_game(game, "tennis", "tennis_get")?;
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
                require_game(game, "tennis", "tennis_move")?;
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
            Op::VecSplit { v, i } => {
                if *i > 2 {
                    return Err(format!("vec_split component must be 0/1/2, got {i}"));
                }
                let split = match vec_splits.get(v) {
                    Some(&n) => n,
                    None => {
                        let (src, sport) = match vals.get(*v) {
                            Some(Val::Node(n, p)) => (*n, *p),
                            Some(Val::Const(_)) => {
                                return Err("vec_split of a constant float — source must be a vector".into());
                            }
                            None => return Err(format!("vec_split of unknown op id {v}")),
                        };
                        let split = em.node("Vector3Split", String::new());
                        em.edge(src, sport, split, "Vector31");
                        vec_splits.insert(*v, split);
                        split
                    }
                };
                vals.push(Val::Node(split, comp_out(*i)));
            }
            Op::VecMake { x, y, z } => {
                let vec = em.node("ConstructVector3", String::new());
                wire_val(&mut em, &vals, *x, vec, "Float1");
                wire_val(&mut em, &vals, *y, vec, "Float2");
                wire_val(&mut em, &vals, *z, vec, "Float3");
                vals.push(Val::Node(vec, "Vector31"));
            }
            Op::TennisMoveVec { v, swing, shot, sprint } => {
                require_game(game, "tennis", "tennis_move_vec")?;
                let n = em.node("TennisController", String::new());
                match vals.get(*v) {
                    Some(Val::Node(src, sport)) => em.edge(*src, sport, n, "Vector31"),
                    Some(Val::Const(_)) => {
                        return Err("tennis_move_vec of a constant float — source must be a vector".into());
                    }
                    None => return Err(format!("tennis_move_vec of unknown op id {v}")),
                }
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

// ---------- layered layout (editor visualization) ----------
//
// The game tolerates zero rects (it stacks everything at the origin —
// titanium54's 5383 nodes all sit at 0,0), but a compiler should show its
// work: data flows left-to-right (outputs exit right, inputs enter left),
// so layer = longest path from sources, x grows with depth, y spreads per
// layer with a barycenter crossing-reduction pass. Same column pitch as
// AIGamePyLibrary's autoLayout so our graphs look native next to pylibry's.
const LAYER_X0: f64 = 1263.0;
const LAYER_Y0: f64 = -278.0;
/// Editor grid pitch in canvas px (Float 8x2 grid = 256x64).
const GRID: f64 = 32.0;
/// Clear gaps between facing node edges, in px.
const LAYER_HGAP: f64 = 96.0;
const LAYER_VGAP: f64 = 64.0;
/// Node sizes (w, h) in px, grid unit = 32px, pivot = top-left (user
/// 2026-09-11, editor-measured). Rules, not a table:
/// - default (0-1 inputs, 1 output): 8x2 like the Float constant;
/// - 2+ inputs: height steps to Multiply's 4 (base rule);
/// - game getters: 12 wide (Vector3 getter: 14); controller 8x5;
/// - ConditionalSetFloatV2 8x9 and CompareFloats 8x5 are explicit
///   (dropdown rows), not input-count derived.
fn node_size(kind: &str, n_inputs: usize) -> (f64, f64) {
    match kind {
        "TennisGetVector3" | "SoccerGetVector3" => (448.0, 64.0),
        k if k.contains("Get")
            && (k.starts_with("Tennis") || k.starts_with("Soccer")) =>
        {
            (384.0, 64.0)
        }
        "TennisController" | "SoccerController1" => (256.0, 160.0),
        "ConditionalSetFloatV2" => (256.0, 288.0),
        "CompareFloats" => (256.0, 160.0),
        _ if n_inputs >= 2 => (256.0, 128.0),
        _ => (256.0, 64.0),
    }
}

fn snap_grid(v: f64) -> f64 {
    (v / GRID).round() * GRID
}

fn layout_positions(
    kinds: &[(String, usize)],
    conns: &[(usize, &'static str, usize, &'static str)],
) -> Vec<(f64, f64)> {
    let n = kinds.len();
    let size = |i: usize| node_size(&kinds[i].0, kinds[i].1);
    let mut succ = vec![Vec::<usize>::new(); n];
    let mut pred = vec![Vec::<usize>::new(); n];
    let mut indeg = vec![0usize; n];
    for (s, _, d, _) in conns {
        succ[*s].push(*d);
        pred[*d].push(*s);
        indeg[*d] += 1;
    }
    // Longest-path layers (Kahn). Compiler output is a DAG (cross-tick
    // links are name-based, not edges); cyclic leftovers go rightmost.
    let mut level = vec![0usize; n];
    let mut done = vec![false; n];
    let mut queue: Vec<usize> = (0..n).filter(|&i| indeg[i] == 0).collect();
    let mut qi = 0;
    while qi < queue.len() {
        let u = queue[qi];
        qi += 1;
        done[u] = true;
        for &v in &succ[u] {
            if level[v] < level[u] + 1 {
                level[v] = level[u] + 1;
            }
            indeg[v] -= 1;
            if indeg[v] == 0 {
                queue.push(v);
            }
        }
    }
    let maxl = level.iter().copied().max().unwrap_or(0);
    for i in 0..n {
        if !done[i] {
            level[i] = maxl + 1;
        }
    }
    let nlayers = level.iter().copied().max().unwrap_or(0) + 1;
    let mut layers = vec![Vec::<usize>::new(); nlayers];
    for i in 0..n {
        layers[level[i]].push(i);
    }
    // Barycenter sweeps: order each layer by mean neighbor position to cut
    // edge crossings. Stable + deterministic (ties keep emission order).
    let mut pos_in_layer = vec![0usize; n];
    for layer in layers.iter() {
        for (p, &i) in layer.iter().enumerate() {
            pos_in_layer[i] = p;
        }
    }
    for _ in 0..2 {
        for li in (0..nlayers.saturating_sub(1)).rev() {
            let mut keyed: Vec<(f64, usize, usize)> = layers[li]
                .iter()
                .enumerate()
                .map(|(p, &i)| {
                    let ns: Vec<usize> = succ[i]
                        .iter()
                        .filter(|&&v| level[v] == li + 1)
                        .map(|&v| pos_in_layer[v])
                        .collect();
                    let b = if ns.is_empty() {
                        p as f64
                    } else {
                        ns.iter().sum::<usize>() as f64 / ns.len() as f64
                    };
                    (b, p, i)
                })
                .collect();
            keyed.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap().then(a.1.cmp(&b.1)));
            layers[li] = keyed.iter().map(|&(_, _, i)| i).collect();
            for (p, &i) in layers[li].iter().enumerate() {
                pos_in_layer[i] = p;
            }
        }
        for li in 1..nlayers {
            let mut keyed: Vec<(f64, usize, usize)> = layers[li]
                .iter()
                .enumerate()
                .map(|(p, &i)| {
                    let ns: Vec<usize> = pred[i]
                        .iter()
                        .filter(|&&v| level[v] == li - 1)
                        .map(|&v| pos_in_layer[v])
                        .collect();
                    let b = if ns.is_empty() {
                        p as f64
                    } else {
                        ns.iter().sum::<usize>() as f64 / ns.len() as f64
                    };
                    (b, p, i)
                })
                .collect();
            keyed.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap().then(a.1.cmp(&b.1)));
            layers[li] = keyed.iter().map(|&(_, _, i)| i).collect();
            for (p, &i) in layers[li].iter().enumerate() {
                pos_in_layer[i] = p;
            }
        }
    }
    let mut out = vec![(0.0, 0.0); n];
    // Width-aware pitch from top-left pivots: next column starts after the
    // widest node of this one + gap, so nothing overlaps horizontally.
    // Columns are vertically centered blocks; every coordinate snaps to
    // the editor grid.
    let mut layer_x = vec![0.0; nlayers];
    layer_x[0] = snap_grid(LAYER_X0);
    for li in 1..nlayers {
        let w = layers[li - 1]
            .iter()
            .map(|&i| size(i).0)
            .fold(0.0f64, f64::max);
        layer_x[li] = snap_grid(layer_x[li - 1] + w + LAYER_HGAP);
    }
    for (li, layer) in layers.iter().enumerate() {
        let total: f64 = layer
            .iter()
            .map(|&i| size(i).1)
            .sum::<f64>()
            + LAYER_VGAP * (layer.len().saturating_sub(1) as f64);
        let mut y = LAYER_Y0 - total / 2.0;
        for &i in layer {
            let h = size(i).1;
            out[i] = (layer_x[li], snap_grid(y));
            y += h + LAYER_VGAP;
        }
    }
    out
}

fn placed_rect(x: f64, y: f64) -> serde_json::Value {
    let mut r = zero_rect();
    r["position"] = serde_json::json!({"x": x, "y": y, "z": 0.0});
    r["anchoredPosition"] = serde_json::json!({"x": x, "y": y});
    r
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
    let kinds: Vec<(String, usize)> = em
        .nodes
        .iter()
        .map(|(k, _, ports)| {
            (k.clone(), ports.iter().filter(|(_, pol)| *pol == 0).count())
        })
        .collect();
    let layout = layout_positions(&kinds, &em.conns);
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
            "serializableRectTransform": placed_rect(layout[i].0, layout[i].1),
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

// ---------- golden-desc unit tests ----------
//
// Every bug from the last session was e2e-only (cargo check green, sim
// replay red). These tests compile small descriptions in-process and assert
// on the emitted save JSON: vals/op-id alignment, per-port-instance sid
// resolution, CompareFloats dropdown indices, and target gating. They run
// with plain `cargo test` — no sim checkout needed.

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::Value;
    use std::collections::HashSet;

    fn test_desc(game: &str, version: &str, ops: Vec<Op>) -> Description {
        Description {
            schema: "graphc-desc-v1".into(),
            target: Target {
                game: game.into(),
                version: version.into(),
            },
            bot_name: "test".into(),
            ops,
        }
    }

    fn const_op(v: f32) -> Op {
        Op::Const { value: v }
    }

    fn kind_nodes<'v>(save: &'v Value, kind: &str) -> Vec<&'v Value> {
        save["serializableNodes"]
            .as_array()
            .unwrap()
            .iter()
            .filter(|n| n["id"] == kind)
            .collect()
    }

    fn node_modifier(n: &Value) -> &str {
        n["modifier"].as_str().unwrap()
    }

    /// Port sids of one node split by direction (out = polarity != 0).
    fn node_port_sids(n: &Value, out: bool) -> Vec<String> {
        n["serializablePorts"]
            .as_array()
            .unwrap()
            .iter()
            .filter(|p| (p["polarity"].as_i64().unwrap() != 0) == out)
            .map(|p| p["sID"].as_str().unwrap().to_string())
            .collect()
    }

    fn modifier_of_port_owner(save: &Value, sid: &str) -> String {
        for n in save["serializableNodes"].as_array().unwrap() {
            for p in n["serializablePorts"].as_array().unwrap() {
                if p["sID"] == sid {
                    return node_modifier(n).to_string();
                }
            }
        }
        panic!("no port with sid {sid}");
    }

    fn kind_of_port_owner(save: &Value, sid: &str) -> String {
        for n in save["serializableNodes"].as_array().unwrap() {
            for p in n["serializablePorts"].as_array().unwrap() {
                if p["sID"] == sid {
                    return n["id"].as_str().unwrap().to_string();
                }
            }
        }
        panic!("no port with sid {sid}");
    }

    /// (node kind, modifier) of the nodes feeding a node's input ports.
    fn input_sources(save: &Value, node: &Value) -> Vec<(String, String)> {
        let inputs: HashSet<String> =
            node_port_sids(node, false).into_iter().collect();
        let mut out = vec![];
        for c in save["serializableConnections"].as_array().unwrap() {
            let p1 = c["port1SID"].as_str().unwrap();
            if inputs.contains(p1) {
                let p0 = c["port0SID"].as_str().unwrap();
                out.push((
                    kind_of_port_owner(save, p0),
                    modifier_of_port_owner(save, p0),
                ));
            }
        }
        out.sort();
        out
    }

    /// Modifiers of the Float nodes feeding a node's input ports.
    fn float_source_modifiers(save: &Value, node: &Value) -> Vec<String> {
        let mut out: Vec<String> = input_sources(save, node)
            .into_iter()
            .filter(|(k, _)| k == "Float")
            .map(|(_, m)| m)
            .collect();
        out.sort();
        out
    }

    /// Mini soccer-demo shape: counter latch + array decode + select, with
    /// effectful (placeholder) ops interleaved between value ids.
    fn soccer_demo_ops() -> Vec<Op> {
        vec![
            Op::VarGet { name: "cnt".into() },                        // 0
            const_op(1.0),                                            // 1
            Op::Bin { r#fn: "AddFloats".into(), a: 0, b: 1, cmp: None }, // 2
            Op::VarSet { name: "cnt".into(), v: 2 },                  // 3
            Op::Array { name: "buf".into(), cells: 6 },               // 4
            const_op(7.5),                                            // 5
            const_op(8.5),                                            // 6
            const_op(9.5),                                            // 7
            Op::ArraySetStatic { arr: 4, i: 3, v: 5 },                // 8
            Op::ArraySetStatic { arr: 4, i: 4, v: 6 },                // 9
            Op::ArraySetStatic { arr: 4, i: 5, v: 7 },                // 10
            const_op(3.0),                                            // 11
            Op::Bin { r#fn: "Modulo".into(), a: 0, b: 11, cmp: None }, // 12
            Op::Bin { r#fn: "AddFloats".into(), a: 11, b: 12, cmp: None }, // 13
            Op::ArrayGetDynamic { arr: 4, i: 13 },                    // 14
            const_op(12.0),                                           // 15
            Op::Bin { r#fn: "CompareFloats".into(), a: 0, b: 15,      // 16
                      cmp: Some(">".into()) },
            const_op(2.0),                                            // 17
            Op::Select { c: 16, t: 17, f: 1 },                        // 18
            Op::Bin { r#fn: "AddFloats".into(), a: 14, b: 18, cmp: None }, // 19
            Op::SoccerMove { x: 19, z: 2 },                           // 20
        ]
    }

    #[test]
    fn vals_stay_aligned_across_placeholder_ops() {
        // Bug class: non-value ops (var_set/array_set/soccer_move, ...)
        // must push placeholder vals or every later op id wires one slot
        // off. The final add must see the array decode + the select.
        let (save, _) = compile(
            &test_desc("soccer", "v0.12", soccer_demo_ops()),
        )
        .expect("soccer demo shape compiles");
        let adds = kind_nodes(&save, "AddFloats");
        // adds: cnt+1 (id 2), idx base (id 13), final (id 19)
        assert_eq!(adds.len(), 3, "three AddFloats nodes expected");
        let final_add = adds
            .iter()
            .find(|n| {
                let srcs = float_source_modifiers(&save, n);
                // final add has NO direct Float sources (both inputs are
                // computed: array-decode select chain + select node)
                srcs.is_empty()
            })
            .expect("final add wires two computed values");
        let inputs: HashSet<String> =
            node_port_sids(final_add, false).into_iter().collect();
        let mut feeders = vec![];
        for c in save["serializableConnections"].as_array().unwrap() {
            let p1 = c["port1SID"].as_str().unwrap();
            if inputs.contains(p1) {
                feeders.push(kind_of_port_owner(
                    &save,
                    c["port0SID"].as_str().unwrap(),
                ));
            }
        }
        feeders.sort();
        assert_eq!(feeders, vec!["ConditionalSetFloatV2", "ConditionalSetFloatV2"]);
        // cnt+1 add wires the latched var + const 1, not shifted neighbors.
        let first_add = adds
            .iter()
            .find(|n| {
                input_sources(&save, n)
                    == vec![
                        ("Float".to_string(), "1".to_string()),
                        ("GetVariable".to_string(), "cnt".to_string()),
                    ]
            })
            .expect("cnt+1 add must wire GetVariable(cnt) + const 1.0");
        let _ = first_add;
    }

    #[test]
    fn connection_endpoints_respect_polarity() {
        // Bug class: duplicate port names within a node (AddFloats in/out
        // both named "Float1") collapsed in one HashMap and edges resolved
        // to the wrong port instance. Every source endpoint must be an
        // output port, every destination an input port.
        let (save, _) = compile(
            &test_desc("soccer", "v0.12", soccer_demo_ops()),
        )
        .expect("soccer demo shape compiles");
        let mut out_sids = HashSet::new();
        let mut in_sids = HashSet::new();
        for n in save["serializableNodes"].as_array().unwrap() {
            for p in n["serializablePorts"].as_array().unwrap() {
                let sid = p["sID"].as_str().unwrap().to_string();
                if p["polarity"].as_i64().unwrap() != 0 {
                    out_sids.insert(sid);
                } else {
                    in_sids.insert(sid);
                }
            }
        }
        assert!(out_sids.is_disjoint(&in_sids), "port sids are per-instance");
        for c in save["serializableConnections"].as_array().unwrap() {
            let p0 = c["port0SID"].as_str().unwrap();
            let p1 = c["port1SID"].as_str().unwrap();
            assert!(out_sids.contains(p0), "source {p0} is an output port");
            assert!(in_sids.contains(p1), "dest {p1} is an input port");
        }
    }

    #[test]
    fn compare_modifier_is_dropdown_index() {
        // Bug class: raw "==" string in the modifier made the sim parse
        // every comparison as equality. The IR carries operator strings;
        // the save must carry Unity dropdown indices.
        let mut ops = vec![const_op(3.0), const_op(4.0)];
        for cmp in ["==", "<", ">", "<=", ">="] {
            ops.push(Op::Bin {
                r#fn: "CompareFloats".into(),
                a: 0,
                b: 1,
                cmp: Some(cmp.into()),
            });
        }
        ops.push(Op::SoccerMove { x: 0, z: 1 });
        let (save, _) = compile(&test_desc("soccer", "v0.12", ops))
            .expect("compares compile");
        let mut mods: Vec<String> = kind_nodes(&save, "CompareFloats")
            .iter()
            .map(|n| node_modifier(n).to_string())
            .collect();
        mods.sort();
        assert_eq!(mods, vec!["0", "1", "2", "3", "4"]);
        // Dynamic array reads compare index equality ("0"); the demo's own
        // compare is ">" ("2"). Everything in the save is a dropdown index.
        let (save2, _) = compile(
            &test_desc("soccer", "v0.12", soccer_demo_ops()),
        )
        .expect("soccer demo shape compiles");
        for n in kind_nodes(&save2, "CompareFloats") {
            assert!(
                ["0", "1", "2", "3", "4"].contains(&node_modifier(n)),
                "only dropdown indices in saves, got {:?}",
                node_modifier(n)
            );
        }
    }

    #[test]
    fn vec_split_shares_one_split_node() {
        // Two components of the same vector share one Vector3Split; the
        // controller sees split outputs, not the raw sensor.
        let ops = vec![
            Op::TennisGet { kind: "vector3".into(), index: 8,       // 0
                            label: "Legal Serve Target".into() },
            Op::VecSplit { v: 0, i: 0 },                            // 1
            Op::VecSplit { v: 0, i: 2 },                            // 2
            Op::TennisMove { x: 1, z: 2, swing: None,                // 3
                             shot: None, sprint: None },
        ];
        let (save, report) = compile(&test_desc("tennis", "v0.14", ops))
            .expect("vec_split compiles");
        assert_eq!(kind_nodes(&save, "Vector3Split").len(), 1);
        let splits = kind_nodes(&save, "Vector3Split");
        let split = splits[0];
        let split_outs: HashSet<String> =
            node_port_sids(split, true).into_iter().collect();
        let mut fed_from_split = 0;
        for c in save["serializableConnections"].as_array().unwrap() {
            let p0 = c["port0SID"].as_str().unwrap();
            if split_outs.contains(p0) {
                fed_from_split += 1;
            }
        }
        assert_eq!(fed_from_split, 2, "both components flow from the split");
        // Split input is the TennisGetVector3 output.
        let split_ins: HashSet<String> =
            node_port_sids(split, false).into_iter().collect();
        assert_eq!(split_ins.len(), 1);
        for c in save["serializableConnections"].as_array().unwrap() {
            if split_ins.contains(c["port1SID"].as_str().unwrap()) {
                assert_eq!(
                    kind_of_port_owner(&save, c["port0SID"].as_str().unwrap()),
                    "TennisGetVector3"
                );
            }
        }
        let _ = report;
    }

    #[test]
    fn layout_flows_left_to_right_without_overlap() {
        // Sources left, controller rightmost, grid-snapped, no rect overlap
        // (top-left pivots, measured sizes).
        let ops = vec![
            Op::TennisGet { kind: "bool".into(), index: 5,          // 0
                            label: "Is Self Actively Serving".into() },
            const_op(11.0),                                          // 1
            Op::TennisMove { x: 1, z: 1, swing: Some(0),            // 2
                             shot: None, sprint: None },
        ];
        let (save, _) = compile(&test_desc("tennis", "v0.14", ops))
            .expect("layout bot compiles");
        let rect = |kind: &str, n_in: usize| -> Vec<(f64, f64, f64, f64)> {
            kind_nodes(&save, kind)
                .iter()
                .map(|n| {
                    let p = &n["serializableRectTransform"]["position"];
                    let (w, h) = node_size(kind, n_in);
                    (p["x"].as_f64().unwrap(), p["y"].as_f64().unwrap(), w, h)
                })
                .collect()
        };
        let sensors = rect("TennisGetBool", 0);
        let ctrls = rect("TennisController", 4);
        assert_eq!(sensors.len(), 1);
        assert_eq!(ctrls.len(), 1);
        assert!(ctrls[0].0 > sensors[0].0, "controller sits right of sensor");
        let mut all = sensors;
        all.extend(rect("Float", 0));
        all.extend(ctrls);
        for (x, y, _, _) in &all {
            assert_eq!((x / GRID).round() * GRID, *x, "x snaps to grid");
            assert_eq!((y / GRID).round() * GRID, *y, "y snaps to grid");
        }
        for i in 0..all.len() {
            for j in (i + 1)..all.len() {
                let (ax, ay, aw, ah) = all[i];
                let (bx, by, bw, bh) = all[j];
                let overlap = ax < bx + bw && bx < ax + aw
                    && ay < by + bh && by < ay + ah;
                assert!(!overlap, "nodes {i} and {j} overlap");
            }
        }
    }

    #[test]
    fn vec_make_and_move_vec_wire_vector() {
        // vec_make builds one ConstructVector3 from 3 floats; the
        // tennis_move_vec controller takes its Vector31, not x/z floats.
        let ops = vec![
            const_op(1.0),                                            // 0
            const_op(0.0),                                            // 1
            const_op(3.0),                                            // 2
            Op::VecMake { x: 0, y: 1, z: 2 },                        // 3
            Op::TennisMoveVec { v: 3, swing: None,                    // 4
                                shot: None, sprint: None },
        ];
        let (save, _) = compile(&test_desc("tennis", "v0.14", ops))
            .expect("vec_make compiles");
        let makes = kind_nodes(&save, "ConstructVector3");
        assert_eq!(makes.len(), 1);
        assert_eq!(
            float_source_modifiers(&save, makes[0]),
            vec!["0", "1", "3"]
        );
        let ctrls = kind_nodes(&save, "TennisController");
        assert_eq!(ctrls.len(), 1);
        let vec_ins: HashSet<String> = node_port_sids(ctrls[0], false)
            .into_iter()
            .collect();
        let make_outs: HashSet<String> = node_port_sids(makes[0], true)
            .into_iter()
            .collect();
        let linked = save["serializableConnections"]
            .as_array()
            .unwrap()
            .iter()
            .any(|c| {
                make_outs.contains(c["port0SID"].as_str().unwrap())
                    && vec_ins.contains(c["port1SID"].as_str().unwrap())
            });
        assert!(linked, "controller Vector31 comes from the vec_make node");
    }

    #[test]
    fn vec_errors_are_loud() {
        for bad in vec![
            vec![
                const_op(1.0),
                Op::VecSplit { v: 0, i: 0 },
            ],
            vec![
                const_op(1.0),
                Op::VecSplit { v: 99, i: 0 },
            ],
        ] {
            assert!(
                compile(&test_desc("tennis", "v0.14", bad)).is_err(),
                "vec_split of const/unknown id must fail"
            );
        }
        assert!(
            compile(&test_desc(
                "tennis",
                "v0.14",
                vec![
                    Op::TennisGet { kind: "vector3".into(), index: 8,
                                    label: "t".into() },
                    Op::VecSplit { v: 0, i: 3 },
                ]
            ))
            .is_err(),
            "component index 3 must fail"
        );
    }

    #[test]
    fn target_gating_rejects_unknown_loudly() {
        let soccer = soccer_demo_ops();
        assert!(compile(&test_desc("soccer", "v0.12", soccer.clone())).is_ok());
        for (game, ver) in [
            ("tennis", "v0.12"),
            ("soccer", "v0.14"),
            ("chess", "v1.0"),
            ("tennis", "v9.99"),
        ] {
            let err = compile(&test_desc(game, ver, soccer.clone()))
                .expect_err(&format!("{game} {ver} must be rejected"));
            assert!(err.contains("unknown target"), "loud error, got: {err}");
        }
        // Universal compiles raw value graphs but rejects game API.
        assert!(
            compile(&test_desc(
                "universal",
                "v9.99",
                vec![
                    const_op(1.0),
                    const_op(2.0),
                    Op::Bin { r#fn: "AddFloats".into(), a: 0, b: 1, cmp: None },
                ]
            ))
            .is_ok()
        );
        for op in [
            Op::SoccerMove { x: 0, z: 0 },
            Op::TennisMove { x: 0, z: 0, swing: None, shot: None, sprint: None },
            Op::TennisGet { kind: "bool".into(), index: 0, label: "t".into() },
        ] {
            assert!(
                compile(&test_desc("universal", "v9.99", vec![const_op(0.0), op]))
                    .is_err(),
                "universal must reject game API"
            );
        }
        // Cross-game misuse fails loudly too.
        assert!(
            compile(&test_desc(
                "soccer",
                "v0.12",
                vec![
                    const_op(0.0),
                    Op::TennisMove { x: 0, z: 0, swing: None,
                                     shot: None, sprint: None },
                ]
            ))
            .is_err()
        );
        // Unknown schema fails loudly.
        let mut bad = test_desc("soccer", "v0.12", vec![]);
        bad.schema = "graphc-desc-v0".into();
        assert!(compile(&bad).is_err());
    }
}