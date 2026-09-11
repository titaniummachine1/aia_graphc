"""Open-court — hit where the opponent is NOT.

Plain if/else on the opponent's Z reads like a human coaching cue:
"if they're on the left, hit right."
"""
import AIA_Comp_Libry.tennis.v014 as tennis


def tick(api):
    serving = tennis.is_self_actively_serving()
    incoming = tennis.ball_incoming()

    bounce = tennis.predicted_bounce()
    base = tennis.center_of_back()
    opponent = api.position_of(tennis.opponent())

    walk_x = api.split_vector(base, 0)
    walk_z = api.split_vector(base, 2)
    if incoming:
        walk_x = api.split_vector(bounce, 0)
        walk_z = api.split_vector(bounce, 2)

    opponent_z = api.split_vector(opponent, 2)
    deep_x = 0.0 - api.split_vector(base, 0)

    if opponent_z > 0.0:
        aim_x = deep_x
        aim_z = 0.0 - 4.0
    else:
        aim_x = deep_x
        aim_z = 4.0

    if serving:
        target = tennis.legal_serve_target()
        aim_x = api.split_vector(target, 0)
        aim_z = api.split_vector(target, 2)

    swing = tennis.auto_swing(2.0)
    tennis.aim(aim_x, aim_z)
    tennis.move(walk_x, walk_z, swing, 2.0)
