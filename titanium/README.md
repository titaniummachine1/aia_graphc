# Titanium rewrite — CLEAN ROOM, not the titanium repo.
#
# This folder is a fresh Python reimplementation of titanium-grade tennis
# behavior for the graphc compiler. It is NOT titanium, NOT a port of its
# nodes, and NOT affiliated with its author. Strategy was re-derived from
# observed behavior (serve/rally/aim patterns) + measured game facts:
# rally aim passes through within ~3cm, serves land via in-box fallback,
# serve-area sensors read stub constants in v0.14 AND v15f (probed).
#
# Layout: entry.py holds tick() + cross-tick state writes (bare names);
# consts.py holds tuning numbers; intercept.py predicts where to stand;
# memory.py holds latch declarations + next-value functions; aim.py holds
# strike-target functions. Every helper returns one float.
#
# Build: python -m graphc titanium/entry.py -o titaniumpy.txt --install
# Sim check: tennis_tournament --home titaniumpy --away underdog
