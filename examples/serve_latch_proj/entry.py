"""graphc rival: project-structured tennis bot (entry + helpers).

Both aims are computed every tick (the game evaluates both arms anyway),
then merged on the serve-phase sensor — assignments only inside branches.
"""

import AIA_Comp_Libry.tennis.v014 as t

import aim


def tick(api):
    serving = t.is_self_actively_serving()
    serve_no = t.serve_number()
    in_range = t.ball_in_swing_range()
    sx = aim.serve_aim_x(api)
    sz = aim.serve_aim_z(api, serve_no)
    rx = aim.rally_aim_x(api)
    rz = aim.rally_aim_z(api)
    if serving:
        mx = sx
        mz = sz
    else:
        mx = rx
        mz = rz
    t.move(mx, mz, in_range, 2.0)
