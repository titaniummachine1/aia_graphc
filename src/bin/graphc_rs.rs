//! graphc-rs CLI: description JSON -> game save graph.
//!
//! Usage: graphc-rs <description.json> <output.txt>
//! Prints a one-line JSON cost report on success.

use std::path::PathBuf;

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.len() != 2 {
        eprintln!("usage: graphc-rs <description.json> <output.txt>");
        std::process::exit(2);
    }
    let desc_path = PathBuf::from(&args[0]);
    let out_path = PathBuf::from(&args[1]);
    let text = std::fs::read_to_string(&desc_path)
        .unwrap_or_else(|e| panic!("read {}: {e}", desc_path.display()));
    let desc: graphc::Description =
        serde_json::from_str(&text).unwrap_or_else(|e| panic!("parse description: {e}"));
    match graphc::compile(&desc) {
        Ok((save, report)) => {
            std::fs::write(&out_path, serde_json::to_string(&save).unwrap())
                .unwrap_or_else(|e| panic!("write {}: {e}", out_path.display()));
            println!(
                "{}",
                serde_json::json!({
                    "path": out_path.display().to_string(),
                    "nodes": report.nodes,
                    "connections": report.connections,
                    "per_tick_transitions": report.nodes + report.connections,
                })
            );
        }
        Err(e) => {
            eprintln!("graphc-rs: {e}");
            std::process::exit(1);
        }
    }
}