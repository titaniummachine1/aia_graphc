"""Titanium rewrite — tick wires feet, memory, strike type, and target.

Feet: serve stance on serve; rally: walk the bounce only when arrival
timing says go (reach_t <= t_land + margin — never camp in the zone,
camping scores LATE; every strike costs 0.36s recover, so the first
zone tick should BE the contact), hold home otherwise.
Memory: rally counter, last-attack side, own-strike detector
(Shot: Last Self Shot id change) + struck counter — bare names assigned
HERE, memory.py only declares and computes.
Strike: Flat serve into the hardcoded diagonal box (sensor stubbed);
rally Topspin on attackable balls else Flat, open-court corners blended
central by fatigue, clamped in-bounds. Shot id drives move AND swing.
"""
import AIA_Comp_Libry.tennis.v15f as t
import aim
import intercept
from consts import SAFE_X, SAFE_Z
from memory import have_prev, last_side, next_shots, next_side, prev_shot, shots_seen, struck


def tick(api):
    serving = t.is_self_actively_serving()
    incoming = t.ball_incoming()

    if incoming:
        inc = 1.0
    else:
        inc = 0.0
    shots_seen = next_shots(shots_seen, inc)

    # --- own-strike occurrence this tick (recoil starts HERE: 0.36s
    # defenseless, charge wiped — retreat, don't admire the shot) ---
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

    # --- feet: minimax cover (walk ladder, then stamina-gated sprint) ---
    # Serve receive: interception before the bounce is impossible (Must
    # Wait For Bounce), so hold the predictive receive stance (1.05u
    # behind bounce 1 towards bounce 2, else in-game Receive Stance).
    stance = t.serve_stance()
    must_wait = t.must_wait_for_bounce()
    serve_phase = t.is_serve_phase()
    if serving:
        walk_x = api.split_vector(stance, 0)
        walk_z = api.split_vector(stance, 2)
    else:
        if must_wait:
            walk_x = intercept.receive_x()
            walk_z = intercept.receive_z()
        else:
            if incoming:
                walk_x = intercept.plan_x()
                walk_z = intercept.plan_z()
            else:
                if serve_phase:
                    walk_x = intercept.receive_x()
                    walk_z = intercept.receive_z()
                else:
                    walk_x = intercept.home_x()
                    walk_z = intercept.home_z()

    # --- strike type (dropdown ids, NOT game args: 0/1/2) ---
    ball = t.ball_position()
    ball_high = api.split_vector(ball, 1)
    if serving:
        shot_id = 2.0
    else:
        shot_id = aim.pick_shot(ball_high, t.ball_speed())

    # --- strike target ---
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
        opp = api.position_of(t.opponent())
        opp_z = api.split_vector(opp, 2)
        corner = aim.pick_z(opp_z, last_side)
        risk = api.clamp(t.rally_fatigue() + t.deuce_fatigue(), 0.0, 1.0)
        aim_x = aim.rally_deep_x(base_x)
        # 1-ply: open court, blended central by fatigue. (The 2-ply
        # reply-backprop was reverted for real-game frame cost — the game
        # is NOT memoized, so each extra evaluation fans out.)
        aim_z = aim.blend_corner(corner, risk)

    last_side = next_side(last_side, aim_z)

    aim_x = api.clamp(aim_x, 0.0 - SAFE_X, SAFE_X)
    aim_z = api.clamp(aim_z, 0.0 - SAFE_Z, SAFE_Z)

    swing = t.auto_swing(shot_id)
    api.plot("T.shots", shots_seen)
    api.plot("T.struck", struck)
    api.plot("T.hit", hit)
    api.plot("T.shot", shot_id)
    api.plot("T.aim_x", aim_x)
    api.plot("T.aim_z", aim_z)
    api.plot("T.walk_x", walk_x)
    api.plot("T.walk_z", walk_z)
    t.aim(aim_x, aim_z)
    t.move(walk_x, walk_z, swing, shot_id)
