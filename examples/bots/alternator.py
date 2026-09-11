"""Alternator — adds memory with a plain Python variable.

`shots_seen` is a module variable the bot writes, so the compiler makes it
a cross-tick latch automatically (writes => dynamic). Constants like LEFT
are never written, so they stay inlined. No api.var / api.set_var.
"""
import AIA_Comp_Libry.tennis.v014 as tennis

LEFT = -4.0
RIGHT = 4.0
shots_seen = 0.0


def tick(api):
    serving = tennis.is_self_actively_serving()
    incoming = tennis.ball_incoming()

    if incoming:
        shots_seen = shots_seen + 1.0

    base = tennis.center_of_back()
    bounce = tennis.predicted_bounce()
    walk_x = api.split_vector(base, 0)
    walk_z = api.split_vector(base, 2)
    if incoming:
        walk_x = api.split_vector(bounce, 0)
        walk_z = api.split_vector(bounce, 2)

    deep_x = 0.0 - api.split_vector(base, 0)
    if shots_seen % 2.0 > 0.5:
        aim_z = RIGHT
    else:
        aim_z = LEFT
    aim_x = deep_x

    if serving:
        target = tennis.legal_serve_target()
        aim_x = api.split_vector(target, 0)
        aim_z = api.split_vector(target, 2)

    swing = tennis.auto_swing(2.0)
    tennis.aim(aim_x, aim_z)
    tennis.move(walk_x, walk_z, swing, 2.0)
