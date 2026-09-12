//! graphc-rs CLI.
//!
//!   graphc-rs <description.json> <output.txt> [raw|o0|o1|o2]
//!       Compile a compiler description into a game save.
//!
//!   graphc-rs <save.txt> <output.txt> [raw|o0|o1|o2]
//!       Compact an existing save (any script — no Python/source needed).
//!       Auto-detected from the input JSON; defaults to `o2` (smallest
//!       behavior-preserving form).
//!
//! The 3rd arg overrides the description's `optimize` field. Prints a
//! one-line JSON report on success.

use std::path::PathBuf;
use std::process::exit;

fn die(msg: &str) -> ! {
    eprintln!("graphc-rs: {msg}");
    exit(1);
}

fn parse_mode(args: &[String], default: graphc::Mode) -> graphc::Mode {
    match args.get(2) {
        Some(m) => graphc::Mode::parse(m).unwrap_or_else(|e| die(&e)),
        None => default,
    }
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.len() < 2 || args.len() > 3 {
        eprintln!("usage: graphc-rs <description.json|save.txt> <output.txt> [raw|o0|o1|o2]");
        exit(2);
    }
    let in_path = PathBuf::from(&args[0]);
    let out_path = PathBuf::from(&args[1]);
    let text = std::fs::read_to_string(&in_path)
        .unwrap_or_else(|e| panic!("read {}: {e}", in_path.display()));
    let value: serde_json::Value =
        serde_json::from_str(&text).unwrap_or_else(|e| panic!("parse JSON: {e}"));

    let report = if value.get("serializableNodes").is_some() {
        // Save -> compact (no source needed).
        let mode = parse_mode(&args, graphc::Mode::O2);
        let (save, r) = graphc::compact(&value, mode).unwrap_or_else(|e| die(&e));
        write_save(&out_path, &save);
        serde_json::json!({
            "path": out_path.display().to_string(),
            "kind": "compact",
            "optimize": mode_name(mode),
            "nodes_before": r.nodes_before,
            "nodes_after": r.nodes_after,
            "connections_before": r.connections_before,
            "connections_after": r.connections_after,
        })
    } else {
        // Description -> compile.
        let mut desc: graphc::Description = serde_json::from_value(value)
            .unwrap_or_else(|e| panic!("parse description: {e}"));
        if let Some(mode) = args.get(2) {
            desc.optimize = mode.clone();
        }
        let mode = graphc::Mode::parse(&desc.optimize).unwrap_or(graphc::Mode::O0);
        let (save, r) = graphc::compile(&desc).unwrap_or_else(|e| die(&e));
        write_save(&out_path, &save);
        serde_json::json!({
            "path": out_path.display().to_string(),
            "kind": "compile",
            "optimize": mode_name(mode),
            "nodes": r.nodes,
            "connections": r.connections,
            "per_tick_transitions": r.connections,
            "size": r.nodes + r.connections,
        })
    };
    println!("{report}");
}

fn write_save(path: &PathBuf, save: &serde_json::Value) {
    std::fs::write(path, serde_json::to_string(save).unwrap())
        .unwrap_or_else(|e| panic!("write {}: {e}", path.display()));
}

fn mode_name(mode: graphc::Mode) -> &'static str {
    match mode {
        graphc::Mode::Raw => "raw",
        graphc::Mode::O0 => "o0",
        graphc::Mode::O1 => "o1",
        graphc::Mode::O2 => "o2",
    }
}
