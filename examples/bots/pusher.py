"""Pusher — the human-simple baseline: walk to the ball, hit deep middle.

Reads like tennis, not like a graph. 20 lines.
"""
import AIA_Comp_Libry.tennis.v014 as tennis


def tick(api):
    serving = tennis.is_self_actively_serving()
    incoming = tennis.ball_incoming()

    bounce = tennis.predicted_bounce()
    base = tennis.center_of_back()
    stance = tennis.serve_stance()

    bounce_x = api.split_vector(bounce, 0)
    bounce_z = api.split_vector(bounce, 2)
    base_x = api.split_vector(base, 0)
    base_z = api.split_vector(base, 2)
    stance_x = api.split_vector(stance, 0)
    stance_z = api.split_vector(stance, 2)

    if serving:
        walk_x = stance_x
        walk_z = stance_z
    else:
        if incoming:
            walk_x = bounce_x
            walk_z = bounce_z
        else:
            walk_x = base_x
            walk_z = base_z

    # Strike deep down the middle of their half; swing charges and fires.
    aim_x = 0.0 - base_x
    aim_z = 0.0
    if serving:
        target = tennis.legal_serve_target()
        aim_x = api.split_vector(target, 0)
        aim_z = api.split_vector(target, 2)

    swing = tennis.auto_swing(2.0)
    tennis.aim(aim_x, aim_z)
    tennis.move(walk_x, walk_z, swing, 2.0)
