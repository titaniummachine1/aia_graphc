"""Underdog v5: walk to the incoming bounce, aim the far half, AutoSwing.

Autoswitch split (TennisAutoSwitch reference: raw controller Vector31 is
*either* move *or* aim, never both):
- walk wire: serve stance on serve, predicted bounce while the
  opponent's shot is incoming, own back-center otherwise (never chase
  your own shot across the net, never chase a dead ball).
- aim wire: legal T-target on serve, mirrored deep-middle otherwise
  (sensors read OWN half — negate x onto the opponent half).
- swing: the game's TennisAutoSwing node (Prefer Charge).
U.* TimePlots mirror every wire for game-vs-sim channel parity.
One file, one tick, one controller call.
"""
import AIA_Comp_Libry.tennis.v014 as tennis


def tick(api):
    serving = tennis.is_self_actively_serving()
    incoming = tennis.ball_incoming()
    stance = tennis.serve_stance()
    bounce = tennis.predicted_bounce()
    home_base = tennis.center_of_back()
    stance_x = api.split_vector(stance, 0)
    stance_z = api.split_vector(stance, 2)
    bounce_x = api.split_vector(bounce, 0)
    bounce_z = api.split_vector(bounce, 2)
    base_x = api.split_vector(home_base, 0)
    base_z = api.split_vector(home_base, 2)
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
    serve_target = tennis.legal_serve_target()
    rally_base = tennis.center_of_back()
    serve_aim_x = api.split_vector(serve_target, 0)
    serve_aim_z = api.split_vector(serve_target, 2)
    rally_aim_x = 0.0 - api.split_vector(rally_base, 0)
    rally_aim_z = api.split_vector(rally_base, 2)
    if serving:
        aim_x = serve_aim_x
        aim_z = serve_aim_z
    else:
        aim_x = rally_aim_x
        aim_z = rally_aim_z
    swing = tennis.auto_swing(2.0)
    if serving:
        serving_flag = 1.0
    else:
        serving_flag = 0.0
    if swing:
        swing_flag = 1.0
    else:
        swing_flag = 0.0
    ball = tennis.ball_position()
    ball_x = api.split_vector(ball, 0)
    ball_y = api.split_vector(ball, 1)
    ball_z = api.split_vector(ball, 2)
    charge = tennis.self_swing_charge_pct()
    api.plot("U.serving", serving_flag)
    api.plot("U.swing", swing_flag)
    api.plot("U.charge", charge)
    api.plot("U.aim_x", aim_x)
    api.plot("U.aim_z", aim_z)
    api.plot("U.walk_x", walk_x)
    api.plot("U.walk_z", walk_z)
    api.plot("U.ball_x", ball_x)
    api.plot("U.ball_y", ball_y)
    api.plot("U.ball_z", ball_z)
    tennis.aim(aim_x, aim_z)
    tennis.move(walk_x, walk_z, swing, 2.0)
