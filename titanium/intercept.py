"""Where to stand + when: closed-form ballistics replaces the Euler loop.

Old assumption (wrong): walk to the bounce ASAP and wait there.
Game truth: contact is tiered by zone time — first tick inside the
perfect radius (<=1.0m) is PERFECT, camping 2+ zone ticks scores LATE
(and every strike costs 0.36s recover). So the goal is ARRIVAL
TIMING: reach the bounce as the ball does, never camp.

Ballistics (exact, ~10 ops — replaces 120-step Euler):
  t_land = (vy + sqrt(vy^2 + 2*G*py)) / G   (positive root, y=0 crossing)
  land_x = px + vx * t_land,  land_z = pz + vz * t_land
Gravity only bends y; x/z are linear.

Minimax cover (the cheap trick): assume the opponent intercepts
perfectly, then plays THEIR best shot against us — the deep corner
farthest from our position. Their prep time is our negative head
start: strike happens no earlier than max(ball-to-bounce, opp-to-bounce)
and the ball still must fly bounce->corner. Ladder, earliest first:
  1. three path steps (1/3, 2/3, landing) checked WALKING — first
     reachable-in-time wins (never cross the net: clamped own half);
  2. else the same 3 steps SPRINTING — only if stamina is above threshold
     AND sprint lands inside the perfect window (arrive <=1s early —
     sprinting into a camp scores LATE all the same);
  3. else walk the landing, best effort.
Stamina: below threshold we only ever walk (sprint drains 0.010/tick,
walking is neutral).
"""
import AIA_Comp_Libry.tennis.v15f as t


def bounce_x():
    return api.split_vector(t.predicted_bounce(), 0)


def bounce_z():
    return api.split_vector(t.predicted_bounce(), 2)


def home_x():
    return api.split_vector(t.center_of_back(), 0)


def home_z():
    return api.split_vector(t.center_of_back(), 2)


def land_t():
    p = t.ball_position()
    v = t.ball_velocity()
    py = api.split_vector(p, 1)
    vy = api.split_vector(v, 1)
    if py > 0.0:
        disc = vy * vy + 2.0 * 9.81 * py
        return (vy + api.sqrt(disc)) / 9.81
    else:
        return 0.0


def land_x():
    p = t.ball_position()
    v = t.ball_velocity()
    px = api.split_vector(p, 0)
    vx = api.split_vector(v, 0)
    py = api.split_vector(p, 1)
    vy = api.split_vector(v, 1)
    if py > 0.0:
        disc = vy * vy + 2.0 * 9.81 * py
        tland = (vy + api.sqrt(disc)) / 9.81
        return px + vx * tland
    else:
        return px


def land_z():
    p = t.ball_position()
    v = t.ball_velocity()
    pz = api.split_vector(p, 2)
    vx = api.split_vector(v, 0)
    vz = api.split_vector(v, 2)
    py = api.split_vector(p, 1)
    vy = api.split_vector(v, 1)
    if py > 0.0:
        disc = vy * vy + 2.0 * 9.81 * py
        tland = (vy + api.sqrt(disc)) / 9.81
        return pz + vz * tland
    else:
        return pz


def _own_sign():
    if home_x() > 0.0:
        return 1.0
    else:
        return 0.0 - 1.0


def opp_aim_x():
    # Deep corner x on OUR half (both corners share it).
    return _own_sign() * 13.0


def opp_aim_z(us_z):
    # Minimax: the corner FARTHEST from us is the opponent's best shot.
    d_hi = api.abs(us_z - 5.0)
    d_lo = api.abs(us_z + 5.0)
    if d_hi > d_lo:
        return 5.0
    else:
        return 0.0 - 5.0


def _ball_speed():
    return api.clamp(t.ball_speed(), 1.0, 50.0)


def _strike_t(bx, bz):
    # Negative head start: opponent strikes no earlier than ball-arrival
    # AND own-arrival at the bounce (they need both, like we do).
    ball = t.ball_position()
    px = api.split_vector(ball, 0)
    py = api.split_vector(ball, 1)
    pz = api.split_vector(ball, 2)
    opp = api.position_of(t.opponent())
    ox = api.split_vector(opp, 0)
    oz = api.split_vector(opp, 2)
    spd = _ball_speed()
    dx = bx - px
    dz = bz - pz
    t_ball = api.sqrt(dx * dx + dz * dz + py * py) / spd
    ex = bx - ox
    ez = bz - oz
    t_opp = api.sqrt(ex * ex + ez * ez) / 8.5
    if t_ball > t_opp:
        return t_ball
    else:
        return t_opp


def _clamp_half(tx):
    s = _own_sign()
    if tx * s > 0.0:
        return tx
    else:
        return s * 0.5


def _need_at(bx, bz, ax, az, sx, sz, f, speed):
    qx = bx + (ax - bx) * f
    qz = bz + (az - bz) * f
    ex = qx - sx
    ez = qz - sz
    return api.sqrt(ex * ex + ez * ez) / speed


def _avail_at(strike, dba, f, spd):
    return strike + dba * f / spd


def plan_x():
    s = _own_sign()
    self_pos = api.position_of(t.self())
    sx = api.split_vector(self_pos, 0)
    sz = api.split_vector(self_pos, 2)
    bx = bounce_x()
    bz = bounce_z()
    ax = s * 13.0
    az = opp_aim_z(sz)
    spd = _ball_speed()
    strike = _strike_t(bx, bz)
    dabx = ax - bx
    dabz = az - bz
    dba = api.sqrt(dabx * dabx + dabz * dabz)
    stamina = t.self_stamina_pct()
    # Walk ladder, earliest first.
    f = 0.33
    if _need_at(bx, bz, ax, az, sx, sz, f, 8.5) > _avail_at(strike, dba, f, spd):
        f = 0.66
        if _need_at(bx, bz, ax, az, sx, sz, f, 8.5) > _avail_at(strike, dba, f, spd):
            f = 1.0
            if _need_at(bx, bz, ax, az, sx, sz, f, 8.5) > _avail_at(strike, dba, f, spd):
                won = 0.0
            else:
                won = 1.0
        else:
            won = 1.0
    else:
        won = 1.0
    if won > 0.5:
        return _clamp_half(bx + (ax - bx) * f)
    # Sprint ladder: stamina-gated, and only into the perfect window
    # (sprinting into a camp scores LATE all the same).
    if stamina > 0.3:
        f = 0.33
        if _sprint_ok(bx, bz, ax, az, sx, sz, f, strike, dba, spd) > 0.5:
            return _clamp_half(bx + (ax - bx) * f)
        else:
            f = 0.66
            if _sprint_ok(bx, bz, ax, az, sx, sz, f, strike, dba, spd) > 0.5:
                return _clamp_half(bx + (ax - bx) * f)
            else:
                f = 1.0
                if _sprint_ok(bx, bz, ax, az, sx, sz, f, strike, dba, spd) > 0.5:
                    return _clamp_half(bx + (ax - bx) * f)
    return _clamp_half(ax)


def _sprint_ok(bx, bz, ax, az, sx, sz, f, strike, dba, spd):
    need = _need_at(bx, bz, ax, az, sx, sz, f, 13.0)
    avail = _avail_at(strike, dba, f, spd)
    if need > avail:
        return 0.0
    else:
        if avail - need > 1.0:
            return 0.0
        else:
            return 1.0


def plan_z():
    self_pos = api.position_of(t.self())
    sx = api.split_vector(self_pos, 0)
    sz = api.split_vector(self_pos, 2)
    bx = bounce_x()
    bz = bounce_z()
    ax = _own_sign() * 13.0
    az = opp_aim_z(sz)
    spd = _ball_speed()
    strike = _strike_t(bx, bz)
    dabx = ax - bx
    dabz = az - bz
    dba = api.sqrt(dabx * dabx + dabz * dabz)
    stamina = t.self_stamina_pct()
    f = 0.33
    if _need_at(bx, bz, ax, az, sx, sz, f, 8.5) > _avail_at(strike, dba, f, spd):
        f = 0.66
        if _need_at(bx, bz, ax, az, sx, sz, f, 8.5) > _avail_at(strike, dba, f, spd):
            f = 1.0
            if _need_at(bx, bz, ax, az, sx, sz, f, 8.5) > _avail_at(strike, dba, f, spd):
                won = 0.0
            else:
                won = 1.0
        else:
            won = 1.0
    else:
        won = 1.0
    if won > 0.5:
        return bz + (az - bz) * f
    if stamina > 0.3:
        f = 0.33
        if _sprint_ok(bx, bz, ax, az, sx, sz, f, strike, dba, spd) > 0.5:
            return bz + (az - bz) * f
        else:
            f = 0.66
            if _sprint_ok(bx, bz, ax, az, sx, sz, f, strike, dba, spd) > 0.5:
                return bz + (az - bz) * f
            else:
                f = 1.0
                if _sprint_ok(bx, bz, ax, az, sx, sz, f, strike, dba, spd) > 0.5:
                    return bz + (az - bz) * f
    return az
