"""graphc rival: project-structured tennis bot (entry + helpers).

Both aims are computed every tick (the game evaluates both arms anyway),
then merged on the serve-phase sensor — assignments only inside branches.
"""
import AIA_Comp_Libry.tennis.v014 as tennis

import aim


def tick(api):
    serving = tennis.is_self_actively_serving()
    serve_number = tennis.serve_number()
    ball_in_range = tennis.ball_in_swing_range()
    serve_x = aim.serve_aim_x(api)
    serve_z = aim.serve_aim_z(api, serve_number)
    rally_x = aim.rally_aim_x(api)
    rally_z = aim.rally_aim_z(api)
    if serving:
        move_x = serve_x
        move_z = serve_z
    else:
        move_x = rally_x
        move_z = rally_z
    tennis.move(move_x, move_z, ball_in_range, 2.0)
