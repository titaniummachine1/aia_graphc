"""Cross-court — a project split across files, compiled as one graph.

entry.py wires the decisions; court.py holds the aiming helpers.
"""
import AIA_Comp_Libry.tennis.v014 as tennis

import court


def tick(api):
    serving = tennis.is_self_actively_serving()
    incoming = tennis.ball_incoming()

    walk_x = court.home_walk_x(api)
    walk_z = court.home_walk_z(api)
    if serving:
        stance = tennis.serve_stance()
        walk_x = api.split_vector(stance, 0)
        walk_z = api.split_vector(stance, 2)
    else:
        if incoming:
            bounce = tennis.predicted_bounce()
            walk_x = api.split_vector(bounce, 0)
            walk_z = api.split_vector(bounce, 2)

    if serving:
        aim_x = api.split_vector(tennis.legal_serve_target(), 0)
        aim_z = api.split_vector(tennis.legal_serve_target(), 2)
    else:
        aim_x = court.deep_x(api)
        aim_z = court.cross_z(api)

    swing = tennis.auto_swing(2.0)
    tennis.aim(aim_x, aim_z)
    tennis.move(walk_x, walk_z, swing, 2.0)
