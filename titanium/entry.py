"""Titanium rewrite — tick wires feet, memory, strike type, and target.

Feet (stateless, re-solved every tick): serve stance on serve; receive
park while Must Wait For Bounce (1.05u past bounce 1 toward bounce 2,
else in-game Receive Stance — interception code cannot run there);
rally chase = closed-form footrace ladder (walk 8.5 / sprint 13 /
racket 1.0 / swing 2.6, stamina-gated sprint) when the ball is ours,
else virtual-ball positioning (his ladder -> danger scan -> deep split).
Memory: rally counter + own-strike detector (telemetry only).
Strike: Flat serve into the hardcoded diagonal box (released at 0.7
charge); rally shot = reverse-minimax attack scan (hardest to catch,
fastest option travels with its point), always-hold Prefer Charge.
"""
import AIA_Comp_Libry.tennis.v15f as t
import aim
import intercept
from consts import SAFE_X, SAFE_Z
from memory import have_prev, next_shots, prev_shot, shots_seen, struck


def tick(api):
    serving = t.is_self_actively_serving()
    incoming = t.ball_incoming()
    must_wait = t.must_wait_for_bounce()

    if incoming:
        inc = 1.0
    else:
        inc = 0.0
    shots_seen = next_shots(shots_seen, inc)

    # --- own-strike occurrence this tick (telemetry only) ---
    cur_shot = t.shot_last_self_shot()
    hit = 0.0
    if cur_shot > 0.0 - 0.5:
        if have_prev > 0.5:
            if cur_shot != prev_shot:
                hit = 1.0
        have_prev = 1.0
    prev_shot = cur_shot
    if hit > 0.5:
        struck = struck + 1.0

    # --- feet ---
    stance = t.serve_stance()
    chase = intercept.want_chase()
    sprint = intercept.want_sprint() > 0.5
    if serving:
        walk_x = api.split_vector(stance, 0)
        walk_z = api.split_vector(stance, 2)
    else:
        if must_wait:
            walk_x = intercept.receive_x()
            walk_z = intercept.receive_z()
        else:
            if chase > 0.5:
                walk_x = intercept.plan_x()
                walk_z = intercept.plan_z()
            else:
                walk_x = intercept.pos_x()
                walk_z = intercept.pos_z()

    # --- strike type + target ---
    ball = t.ball_position()
    if serving:
        shot_id = 2.0
    else:
        shot_id = aim.attack_opt()

    base_x = intercept.home_x()
    if t.is_ad_court_serve():
        is_ad = 1.0
    else:
        is_ad = 0.0
    if serving:
        if t.serve_number() > 1.5:
            aim_x = aim.serve_box_x(base_x)
            aim_z = 3.0
        else:
            aim_x = aim.serve_box_x(base_x)
            aim_z = aim.serve_box_z(is_ad)
    else:
        aim_x = aim.attack_x()
        aim_z = aim.attack_z()

    aim_x = api.clamp(aim_x, 0.0 - SAFE_X, SAFE_X)
    aim_z = api.clamp(aim_z, 0.0 - SAFE_Z, SAFE_Z)

    # --- swing: always-hold rally, serve releases at 0.7 charge ---
    auto = t.auto_swing(shot_id)
    if serving:
        if t.self_swing_charge_pct() >= 0.7:
            swing = auto
        else:
            swing = t.self_swing_charge_pct() >= 0.0
    else:
        swing = auto

    api.plot("T.shots", shots_seen)
    api.plot("T.struck", struck)
    api.plot("T.hit", hit)
    api.plot("T.shot", shot_id)
    api.plot("T.aim_x", aim_x)
    api.plot("T.aim_z", aim_z)
    api.plot("T.walk_x", walk_x)
    api.plot("T.walk_z", walk_z)
    api.plot("T.chase", chase)
    t.aim(aim_x, aim_z)
    t.move(walk_x, walk_z, swing, shot_id, sprint)
