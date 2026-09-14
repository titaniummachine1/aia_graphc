"""`and`/`or` loud-blocked until the full-context divergence is root-caused.

History (2026-09-14): an eager bool_op fold was implemented and proved
bit-exact in ISOLATION (the probe bots below: or-chain vs nested-if, 3627
ticks, 0 channel diffs). In the FULL titanium bot the same rewrite changed
match behavior (titanium62/64 vs titanium61/63 — tick-exact 2x2 isolation).
Root cause not found; the frontend keeps the LOUD error so no author can
silently hit it. api.bool_and/bool_or stay fully supported (single nodes).
"""
from graphc import compile_source

src = '''
def tick(api):
    a = api.tennis_get_bool("Is Playing")
    b = api.tennis_get_bool("Ball Has Bounced")
    c = a and b
    api.tennis_move(0.0, 0.0, c)
'''
try:
    compile_source(src, ("tennis", "v15f"))
    raise SystemExit("FAIL: BoolOp compiled (should be loud-blocked)")
except SyntaxError as e:
    assert "not compilable yet" in str(e), e
    print("loud BoolOp rejection OK")

# api.bool_and/bool_or remain fine
d = compile_source('''
def tick(api):
    a = api.tennis_get_bool("Is Playing")
    b = api.tennis_get_bool("Ball Has Bounced")
    c = api.bool_and(a, b)
    d = api.bool_or(c, b)
    api.tennis_move(0.0, 0.0, d)
''', ("tennis", "v15f"))
kinds = [op["op"] for op in d["ops"]]
assert kinds.count("bool_op") == 2, kinds
print("api.bool_and/or helpers OK")
print("ALL OK")
