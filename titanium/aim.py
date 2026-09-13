"""Strike targets: serve box from geometry, rally open-court + fatigue blend."""
import AIA_Comp_Libry.tennis.v15f as t


def serve_box_x(base_x):
    # Opponent-half box center: mirror our own back-center x onto their
    # half (sensors read OWN half — negate x). Magnitude is BOX_X 3.5.
    if base_x > 0.0:
        s = 1.0
    else:
        s = 0.0 - 1.0
    return 0.0 - s * 3.5


def serve_box_z(is_ad):
    if is_ad > 0.5:
        return 0.0 - 3.0
    else:
        return 3.0


def rally_deep_x(base_x):
    return 0.0 - base_x


def pick_shot(ball_high, ball_speed):
    # Dropdown ids: 0 Topspin, 1 Slice, 2 Flat (3+ are situational).
    # Attackable ball (high and slow) gets Topspin dip; else Flat pace.
    # Serve forces Flat in tick (titanium serves Flat too).
    if ball_high > 1.5:
        if ball_speed < 20.0:
            return 0.0
        else:
            return 2.0
    else:
        return 2.0


def pick_z(opp_z, last_side):
    # Open court first; opponent central -> alternate corners so the
    # attack never telegraphs.
    if opp_z > 1.0:
        return 0.0 - 4.5
    else:
        if opp_z > 0.0 - 1.0:
            if last_side > 0.5:
                return 0.0 - 4.5
            else:
                return 4.5
        else:
            return 4.5


def blend_corner(corner, risk):
    # Fatigue pulls the corner toward middle (0.0): risk 0 = full corner.
    return corner + (0.0 - corner) * risk
