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


def _reply_margin(ax, az, rz):
    # Our cover margin vs the opponent's reply to corner rz, given OUR
    # shot lands at (ax, az): opponent meets it (their reach vs ball
    # flight), replies from there to OUR far corner, we cover from home.
    # Positive = we have time to spare. Opponent takes the minimum.
    ball = t.ball_position()
    px = api.split_vector(ball, 0)
    py = api.split_vector(ball, 1)
    pz = api.split_vector(ball, 2)
    opp = api.position_of(t.opponent())
    ox = api.split_vector(opp, 0)
    oz = api.split_vector(opp, 2)
    home = t.center_of_back()
    hx = api.split_vector(home, 0)
    hz = api.split_vector(home, 2)
    spd = api.clamp(t.ball_speed(), 1.0, 50.0)
    dx = ax - px
    dz = az - pz
    t_ball = api.sqrt(dx * dx + dz * dz + py * py) / spd
    ex = ax - ox
    ez = az - oz
    t_opp = api.sqrt(ex * ex + ez * ez) / 8.5
    if t_ball > t_opp:
        t_hit = t_ball
    else:
        t_hit = t_opp
    if hx > 0.0:
        s = 1.0
    else:
        s = 0.0 - 1.0
    rx = s * 13.0
    fx = rx - ax
    fz = rz - az
    flight = api.sqrt(fx * fx + fz * fz) / 25.0
    avail = t_hit + flight
    gx = rx - hx
    gz = rz - hz
    need = api.sqrt(gx * gx + gz * gz) / 8.5
    return avail - need


def aim_value(ax, az):
    # Backpropagated value of landing OUR shot at (ax, az): the opponent
    # replies to whichever of THEIR corners hurts us most (minimum of
    # our cover margins). We then maximize over our candidates.
    m1 = _reply_margin(ax, az, 5.0)
    m2 = _reply_margin(ax, az, 0.0 - 5.0)
    if m1 > m2:
        return m2
    else:
        return m1


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
