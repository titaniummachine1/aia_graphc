"""Underdog v4: walk to the incoming bounce, aim the far half, AutoSwing.

Autoswitch split (TennisAutoSwitch reference: raw controller Vector31 is
*either* move *or* aim, never both):
- walk wire: serve stance on serve, predicted bounce while the
  opponent's shot is incoming, own back-center otherwise (never chase
  your own shot across the net, never chase a dead ball).
- aim wire: legal T-target on serve, mirrored deep-middle otherwise
  (sensors read OWN half — negate x onto the opponent half).
- swing: the game's TennisAutoSwing node (Prefer Charge).
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
    tennis.aim(aim_x, aim_z)
    tennis.move(walk_x, walk_z, swing, 2.0)
