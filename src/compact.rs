//! Source-free graph compactor: shrink ANY AIComp save without changing what
//! the AI does.
//!
//! No Python and no compiler desc needed — point it at an editor-exported or
//! previously generated `.txt` and it decides what is safe to drop:
//!
//! * **Chrome** (layout rects, colors, port rects, connection metadata) and
//!   node ids are never logic — dropping them / putting nodes at 0,0 /
//!   remapping ids to dense base62 is always behavior-preserving (`o2`).
//! * **Debug sinks** (`TimePlot` / `Debug*`) are pure terminals. A producer
//!   is dropped **only if every one of its consumers is itself droppable**
//!   (backward reachability from real sinks). So a value that feeds both a
//!   `TimePlot` and a controller is kept; only debug-exclusive chains vanish.
//!   This is the safe form of pylibry `stripDebugSinks` (which the ladder
//!   flags as unsafe when applied blindly — e.g. AIA/AIA3 route debug node
//!   *outputs* into logic).
//!
//! Modes: `o0` prune truly-dead nodes (keep debug + chrome); `o1` also drop
//! debug sinks and their exclusive producers; `o2` (default for compact)
//! additionally strips chrome and remaps ids. `raw` is a no-op passthrough.

use std::collections::{HashMap, HashSet};

use serde_json::Value;

use crate::Mode;

pub struct CompactReport {
    pub nodes_before: usize,
    pub nodes_after: usize,
    pub connections_before: usize,
    pub connections_after: usize,
}

impl std::fmt::Debug for CompactReport {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "CompactReport {{ nodes {}->{}, connections {}->{} }}",
            self.nodes_before, self.nodes_after, self.connections_before, self.connections_after
        )
    }
}

fn port_is_output(p: &Value) -> bool {
    p.get("polarity")
        .and_then(Value::as_i64)
        .map(|x| x != 0)
        .unwrap_or(false)
}

/// A pure debug terminal (no side effect on the match).
fn is_debug_sink(id: &str) -> bool {
    id == "TimePlot" || id.starts_with("TimePlot") || id.starts_with("Debug")
}

/// A node that changes the match or persists state: always a DCE root.
fn is_action(id: &str) -> bool {
    id.contains("Controller")
        || id == "SetVariable"
        || id.starts_with("ArraySet")
        || id == "CreateFunction"
}

/// A node with no output ports is a terminal (sink); kept unless it is a
/// debug sink being stripped.
fn is_terminal(has_output: bool) -> bool {
    !has_output
}

/// Compact a loaded save. Returns the new save + a size report.
pub fn compact(save: &Value, mode: Mode) -> Result<(Value, CompactReport), String> {
    let nodes_in = save
        .get("serializableNodes")
        .and_then(Value::as_array)
        .ok_or_else(|| "input is not a save (missing serializableNodes)".to_string())?;
    let conns_in = save
        .get("serializableConnections")
        .and_then(Value::as_array)
        .ok_or_else(|| "input is not a save (missing serializableConnections)".to_string())?;
    if mode == Mode::Raw {
        let report = CompactReport {
            nodes_before: nodes_in.len(),
            nodes_after: nodes_in.len(),
            connections_before: conns_in.len(),
            connections_after: conns_in.len(),
        };
        return Ok((save.clone(), report));
    }

    let n = nodes_in.len();
    let mut node_ids = Vec::with_capacity(n);
    let mut has_out = vec![false; n];
    // input-port sID -> owning node
    let mut node_inputs: Vec<Vec<String>> = vec![Vec::new(); n];
    // any-port sID -> owning node
    let mut port_owner: HashMap<String, usize> = HashMap::new();

    for (i, node) in nodes_in.iter().enumerate() {
        node_ids.push(node.get("id").and_then(Value::as_str).unwrap_or("").to_string());
        if let Some(ports) = node.get("serializablePorts").and_then(Value::as_array) {
            for p in ports {
                let ps = p.get("sID").and_then(Value::as_str).unwrap_or("");
                if ps.is_empty() {
                    continue;
                }
                port_owner.insert(ps.to_string(), i);
                if port_is_output(p) {
                    has_out[i] = true;
                } else {
                    node_inputs[i].push(ps.to_string());
                }
            }
        }
    }

    // Consumer input port -> producer node, via connections (port0 = output).
    let mut input_producer: HashMap<String, usize> = HashMap::new();
    for c in conns_in {
        let (Some(p0), Some(p1)) = (
            c.get("port0SID").and_then(Value::as_str),
            c.get("port1SID").and_then(Value::as_str),
        ) else {
            continue;
        };
        if let Some(&prod) = port_owner.get(p0) {
            input_producer.insert(p1.to_string(), prod);
        }
    }

    let strip_debug = matches!(mode, Mode::O1 | Mode::O2);

    // Backward reachability from roots. Roots = actions + non-debug terminals
    // (debug terminals are only roots when we keep debug, i.e. o0).
    let mut needed = vec![false; n];
    let mut stack: Vec<usize> = Vec::new();
    for i in 0..n {
        let keep = if is_action(&node_ids[i]) {
            true
        } else if is_terminal(has_out[i]) {
            !(strip_debug && is_debug_sink(&node_ids[i]))
        } else {
            false
        };
        if keep {
            needed[i] = true;
            stack.push(i);
        }
    }
    while let Some(i) = stack.pop() {
        for in_port in &node_inputs[i] {
            if let Some(&prod) = input_producer.get(in_port) {
                if !needed[prod] {
                    needed[prod] = true;
                    stack.push(prod);
                }
            }
        }
    }

    // Any port belonging to a dropped node invalidates its connections.
    let mut dead_ports: HashSet<String> = HashSet::new();
    for (i, node) in nodes_in.iter().enumerate() {
        if needed[i] {
            continue;
        }
        if let Some(ports) = node.get("serializablePorts").and_then(Value::as_array) {
            for p in ports {
                if let Some(s) = p.get("sID").and_then(Value::as_str) {
                    dead_ports.insert(s.to_string());
                }
            }
        }
    }

    let new_nodes: Vec<Value> = nodes_in
        .iter()
        .enumerate()
        .filter(|(i, _)| needed[*i])
        .map(|(_, v)| v.clone())
        .collect();
    let new_conns: Vec<Value> = conns_in
        .iter()
        .filter(|c| {
            let p0 = c.get("port0SID").and_then(Value::as_str).unwrap_or("");
            let p1 = c.get("port1SID").and_then(Value::as_str).unwrap_or("");
            !dead_ports.contains(p0) && !dead_ports.contains(p1)
        })
        .cloned()
        .collect();

    let mut out = save.clone();
    out["serializableNodes"] = Value::Array(new_nodes);
    out["serializableConnections"] = Value::Array(new_conns);

    if mode.core() {
        crate::core_strip(&mut out);
        crate::remap_short_ids(&mut out);
    }

    let report = CompactReport {
        nodes_before: n,
        nodes_after: out["serializableNodes"].as_array().map_or(0, Vec::len),
        connections_before: conns_in.len(),
        connections_after: out["serializableConnections"].as_array().map_or(0, Vec::len),
    };
    Ok((out, report))
}
