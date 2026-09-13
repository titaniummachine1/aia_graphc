"""Where to stand + when: v54-style closed-form intercept ladder.

Per-tick stateless solve of  |B + V*t - P| <= s*t + r  (footrace in the
pitch plane against the ballistic ball), four tiers in strict order:
  walk (8.5, ring 0) -> sprint (13, ring 0) -> racket (13, ring 1.0)
  -> swing (13, ring 2.6),
each gated on the ball being low enough to take (y <= 2.7) at contact.

Ballistics use the measured game constants (g=28, bounce keeps 0.78,
ground 0.28), NOT earth gravity. The solve aims the RACKET: the ball is
shifted by the 0.55 m racket lead inside the solve, so the meet point is
where the body stands while the racket is on the ball.

The same ladder runs from the opponent's perspective (his meet point +
meet time = launch of a virtual ball that does not exist yet). While the
ball is his, we intercept the virtual ball (negative-t budget), shaded
deep-center. No Ball Incoming anywhere: chase = 2nd-bounce ownership
(primary) + live-ball-on-our-side fallback (sticky, no flicker).
"""
import AIA_Comp_Libry.tennis.v15f as t

WALK = 8.5
SPRINT = 13.0
R_RACKET = 1.0
R_SWING = 2.6
BALL_G = 28.0
GROUND = 0.28
KEEP = 0.78
TAKE_H = 2.7
LEAD = 0.55
STAM_GATE = 0.10
PARK_D = 1.05


def _own_sign():
    if home_x() > 0.0:
        return 1.0
    else:
        return 0.0 - 1.0


def home_x():
    return api.split_vector(t.center_of_back(), 0)


def home_z():
    return api.split_vector(t.center_of_back(), 2)


def bounce_x():
    return api.split_vector(t.predicted_bounce(), 0)


def bounce_z():
    return api.split_vector(t.predicted_bounce(), 2)


def _ball_x():
    return api.split_vector(t.ball_position(), 0)


def _ball_y():
    return api.split_vector(t.ball_position(), 1)


def _ball_z():
    return api.split_vector(t.ball_position(), 2)


def _vel_x():
    return api.split_vector(t.ball_velocity(), 0)


def _vel_y():
    return api.split_vector(t.ball_velocity(), 1)


def _vel_z():
    return api.split_vector(t.ball_velocity(), 2)


def _self_x():
    return api.split_vector(api.position_of(t.self()), 0)


def _self_z():
    return api.split_vector(api.position_of(t.self()), 2)


def _opp_x():
    return api.split_vector(api.position_of(t.opponent()), 0)


def _opp_z():
    return api.split_vector(api.position_of(t.opponent()), 2)


def _dist(ax, az, bx, bz):
    dx = ax - bx
    dz = az - bz
    return api.sqrt(dx * dx + dz * dz)


# ---- game ballistics (measured constants) ----

def _t_bounce():
    py = _ball_y()
    vy = _vel_y()
    inside = vy * vy + 56.0 * (py - GROUND)
    if inside < 0.0:
        inside = 0.0
    return (vy + api.sqrt(inside)) / BALL_G


def _y_at(T):
    py = _ball_y()
    vy = _vel_y()
    tb = _t_bounce()
    y_pre = py + vy * T - 14.0 * T * T
    vy2 = api.abs(vy - BALL_G * tb) * KEEP
    if vy2 < 0.5:
        vy2 = 0.5
    dt2 = T - tb
    if dt2 < 0.0:
        dt2 = 0.0
    y_post = GROUND + vy2 * dt2 - 14.0 * dt2 * dt2
    if T <= tb:
        return y_pre
    else:
        return y_post


# ---- quadratic footrace |B + V*t - P| <= s*t + r ----

def _eff_ours_x():
    return _ball_x() + _own_sign() * LEAD


def _eff_his_x():
    return _ball_x() - _own_sign() * LEAD


def _qa(s, vx, vz):
    a = vx * vx + vz * vz - s * s
    if api.abs(a) < 0.01:
        return 0.01
    else:
        return a


def _qb(px, pz, s, r, ex, ez, vx, vz):
    dx = ex - px
    dz = ez - pz
    return 2.0 * (vx * dx + vz * dz - s * r)


def _qc(px, pz, r, ex, ez):
    dx = ex - px
    dz = ez - pz
    return dx * dx + dz * dz - r * r


def _qT(px, pz, s, r, ex, ez, vx, vz):
    a = _qa(s, vx, vz)
    b = _qb(px, pz, s, r, ex, ez, vx, vz)
    c = _qc(px, pz, r, ex, ez)
    disc = b * b - 4.0 * a * c
    if disc < 0.0:
        disc = 0.0
    if disc > 1000000.0:
        disc = 1000000.0
    te = (0.0 - b - api.sqrt(disc)) / (2.0 * a)
    if te < 0.0:
        return 0.0
    else:
        return te


def _qok(px, pz, s, r, ex, ez, vx, vz):
    a = _qa(s, vx, vz)
    b = _qb(px, pz, s, r, ex, ez, vx, vz)
    c = _qc(px, pz, r, ex, ez)
    disc = b * b - 4.0 * a * c
    if disc < 0.0:
        return 0.0
    sq = api.sqrt(disc)
    te = (0.0 - b - sq) / (2.0 * a)
    tx = (0.0 - b + sq) / (2.0 * a)
    if a > 0.0:
        if tx > 0.0:
            win = 1.0
        else:
            win = 0.0
    else:
        if te > 0.0:
            win = 1.0
        else:
            win = 0.0
    if win < 0.5:
        return 0.0
    T = te
    if T < 0.0:
        T = 0.0
    if _y_at(T) > TAKE_H:
        return 0.0
    return 1.0


def _tier_s(tier):
    if tier > 0.5:
        return SPRINT
    else:
        return WALK


def _tier_r(tier):
    r = 0.0
    if tier > 1.5:
        r = R_RACKET
    if tier > 2.5:
        r = R_SWING
    return r


# ---- OUR ladder (tiers 0 walk, 1 sprint, 2 racket, 3 swing) ----

def _our_T(tier):
    return _qT(_self_x(), _self_z(), _tier_s(tier), _tier_r(tier),
               _eff_ours_x(), _ball_z(), _vel_x(), _vel_z())


def _our_ok(tier):
    return _qok(_self_x(), _self_z(), _tier_s(tier), _tier_r(tier),
                _eff_ours_x(), _ball_z(), _vel_x(), _vel_z())


def _our_meet_x(tier):
    return _ball_x() + _vel_x() * _our_T(tier)


def _our_meet_z(tier):
    return _ball_z() + _vel_z() * _our_T(tier)


def _w_ok():
    return _our_ok(0)


def _s_ok():
    if _our_ok(0) > 0.5:
        return 0.0
    return _our_ok(1)


def _r_ok():
    if _our_ok(0) > 0.5:
        return 0.0
    if _our_ok(1) > 0.5:
        return 0.0
    return _our_ok(2)


def _v_ok():
    if _our_ok(0) > 0.5:
        return 0.0
    if _our_ok(1) > 0.5:
        return 0.0
    if _our_ok(2) > 0.5:
        return 0.0
    return _our_ok(3)


def _meet_x():
    x = _our_meet_x(3)
    if _r_ok() > 0.5:
        x = _our_meet_x(2)
    if _s_ok() > 0.5:
        x = _our_meet_x(1)
    if _w_ok() > 0.5:
        x = _our_meet_x(0)
    return x


def _meet_z():
    z = _our_meet_z(3)
    if _r_ok() > 0.5:
        z = _our_meet_z(2)
    if _s_ok() > 0.5:
        z = _our_meet_z(1)
    if _w_ok() > 0.5:
        z = _our_meet_z(0)
    return z


def plan_x():
    # Serve in flight, pre-bounce: interception is impossible (the game
    # enforces Must Wait For Bounce), so hold the receive stance.
    if t.must_wait_for_bounce():
        return receive_x()
    x = _meet_x()
    if x > 15.0:
        x = 15.0
    if x < 0.0 - 15.0:
        x = 0.0 - 15.0
    if x * _own_sign() < 0.3:
        x = _own_sign() * 0.3
    if t.ball_in_swing_range():
        return _ball_x()
    else:
        return x


def plan_z():
    # See plan_x: no interception before the serve bounce.
    if t.must_wait_for_bounce():
        return receive_z()
    z = _meet_z()
    if z > 7.5:
        z = 7.5
    if z < 0.0 - 7.5:
        z = 0.0 - 7.5
    if t.ball_in_swing_range():
        return _ball_z()
    else:
        return z


# ---- HIS ladder (same solve from his position, his racket lead) ----

def _his_T(tier):
    return _qT(_opp_x(), _opp_z(), _tier_s(tier), _tier_r(tier),
               _eff_his_x(), _ball_z(), _vel_x(), _vel_z())


def _his_ok(tier):
    return _qok(_opp_x(), _opp_z(), _tier_s(tier), _tier_r(tier),
                _eff_his_x(), _ball_z(), _vel_x(), _vel_z())


def _ho_ok(tier):
    if tier < 0.5:
        return _his_ok(0)
    if tier < 1.5:
        if _his_ok(0) > 0.5:
            return 0.0
        return _his_ok(1)
    if tier < 2.5:
        if _his_ok(0) > 0.5:
            return 0.0
        if _his_ok(1) > 0.5:
            return 0.0
        return _his_ok(2)
    if _his_ok(0) > 0.5:
        return 0.0
    if _his_ok(1) > 0.5:
        return 0.0
    if _his_ok(2) > 0.5:
        return 0.0
    return _his_ok(3)


def _his_meet_x(tier):
    return _ball_x() + _vel_x() * _his_T(tier)


def _his_meet_z(tier):
    return _ball_z() + _vel_z() * _his_T(tier)


def opp_meet_x():
    # His launch point: first feasible tier, else where he stands.
    x = _opp_x()
    if _ho_ok(3) > 0.5:
        x = _his_meet_x(3)
    if _ho_ok(2) > 0.5:
        x = _his_meet_x(2)
    if _ho_ok(1) > 0.5:
        x = _his_meet_x(1)
    if _ho_ok(0) > 0.5:
        x = _his_meet_x(0)
    return x


def opp_meet_z():
    z = _opp_z()
    if _ho_ok(3) > 0.5:
        z = _his_meet_z(3)
    if _ho_ok(2) > 0.5:
        z = _his_meet_z(2)
    if _ho_ok(1) > 0.5:
        z = _his_meet_z(1)
    if _ho_ok(0) > 0.5:
        z = _his_meet_z(0)
    return z


def opp_t_meet():
    T = 999.0
    if _ho_ok(3) > 0.5:
        T = _his_T(3)
    if _ho_ok(2) > 0.5:
        T = _his_T(2)
    if _ho_ok(1) > 0.5:
        T = _his_T(1)
    if _ho_ok(0) > 0.5:
        T = _his_T(0)
    return T


# ---- chase / sprint gates (no Ball Incoming) ----

def _recv_known():
    # Landing prediction available once the game knows where the
    # opponent aims (time-to-ground > 0; 0.0 while the ball is dead).
    if t.ball_time_to_ground() > 0.05:
        return 1.0
    else:
        return 0.0


def want_chase():
    # Threat = the ball is ours to take: 2nd-bounce ownership (primary)
    # or a live ball on our side (sticky fallback, never flickers).
    if t.must_wait_for_bounce():
        return 0.0
    if _recv_known() > 0.5:
        b2x = api.split_vector(t.predicted_2nd_bounce(), 0)
        if b2x * _own_sign() > 0.0:
            return 1.0
    if t.ball_on_self_side():
        if t.ball_speed() > 0.1:
            return 1.0
    return 0.0


def want_sprint():
    # Sprint only when walking cannot do it and stamina allows it.
    if want_chase() < 0.5:
        return 0.0
    if t.self_stamina_pct() > STAM_GATE:
        if _s_ok() > 0.5:
            return 1.0
        if _r_ok() > 0.5:
            return 1.0
        if _v_ok() > 0.5:
            return 1.0
    return 0.0


# ---- serve receive: predictive park or in-game stance ----

def receive_x():
    # Predictive receive stance: 1.05 units behind the FIRST bounce
    # towards the SECOND bounce (room to swing after it lands).
    # Fallback: in-game Receive Stance until the aim is known.
    rsx = api.split_vector(t.receive_stance(), 0)
    if _recv_known() < 0.5:
        return rsx
    b1x = bounce_x()
    b1z = bounce_z()
    b2 = t.predicted_2nd_bounce()
    b2x = api.split_vector(b2, 0)
    b2z = api.split_vector(b2, 2)
    dx = b2x - b1x
    dz = b2z - b1z
    dist = api.sqrt(dx * dx + dz * dz)
    if dist > 0.001:
        return b1x + dx / dist * PARK_D
    else:
        return b1x


def receive_z():
    # See receive_x: same stance, z component (no half-clamp on z).
    rsz = api.split_vector(t.receive_stance(), 2)
    if _recv_known() < 0.5:
        return rsz
    b1x = bounce_x()
    b1z = bounce_z()
    b2 = t.predicted_2nd_bounce()
    b2x = api.split_vector(b2, 0)
    b2z = api.split_vector(b2, 2)
    dx = b2x - b1x
    dz = b2z - b1z
    dist = api.sqrt(dx * dx + dz * dz)
    if dist > 0.001:
        return b1z + dz / dist * PARK_D
    else:
        return b1z


# ---- positioning: virtual ball (his best reply before it exists) ----

def _vfeas(px, pz, s, r, ex, ez, vx, vz):
    # One footrace solve, no height gate (virtual balls have no altitude):
    # can the chaser at (px,pz) meet a ball at (ex,ez)~(vx,vz) with speed s
    # and ring r? Shared by every ladder, both perspectives.
    v2 = vx * vx + vz * vz
    a = v2 - s * s
    if api.abs(a) < 0.01:
        a = 0.01
    dx = ex - px
    dz = ez - pz
    b = 2.0 * (vx * dx + vz * dz - s * r)
    c = dx * dx + dz * dz - r * r
    disc = b * b - 4.0 * a * c
    if disc < 0.0:
        return 0.0
    sq = api.sqrt(disc)
    te = (0.0 - b - sq) / (2.0 * a)
    tx = (0.0 - b + sq) / (2.0 * a)
    if a > 0.0:
        if tx > 0.0:
            return 1.0
        else:
            return 0.0
    else:
        if te > 0.0:
            return 1.0
        else:
            return 0.0


def _vtier(px, pz, ex, ez, vx, vz):
    # How far the victim must extend down the ladder: 0 walk, 1 sprint,
    # 2 racket ring, 3 swing ring, 4 unreachable. Same tiers, both sides.
    if _vfeas(px, pz, WALK, 0.0, ex, ez, vx, vz) > 0.5:
        return 0.0
    if _vfeas(px, pz, SPRINT, 0.0, ex, ez, vx, vz) > 0.5:
        return 1.0
    if _vfeas(px, pz, SPRINT, R_RACKET, ex, ez, vx, vz) > 0.5:
        return 2.0
    if _vfeas(px, pz, SPRINT, R_SWING, ex, ez, vx, vz) > 0.5:
        return 3.0
    return 4.0


def _vscore(px, pz, lx, lz, tx, tz):
    # THE shared minimax evaluator, both directions: how hard is it for the
    # victim at (px,pz) to intercept a ball launched at (lx,lz) toward
    # (tx,tz)? Score = ladder tier * 1000 + required speed — the further the
    # victim must extend down the ladder, the better for the shooter.
    ddx = tx - lx
    ddz = tz - lz
    d_lp = api.sqrt(ddx * ddx + ddz * ddz)
    tf = _fast_t(d_lp)
    bvx = ddx / tf
    bvz = ddz / tf
    tier = _vtier(px, pz, lx, lz, bvx, bvz)
    vdx = tx - px
    vdz = tz - pz
    slack = api.sqrt(vdx * vdx + vdz * vdz) - R_SWING
    if slack < 0.0:
        slack = 0.0
    den = tf
    if den < 0.2:
        den = 0.2
    if den > 10.0:
        den = 10.0
    return tier * 1000.0 + slack / den


def _his_tier():
    # Which ladder rung HE wins on the live ball (0 walk .. 4 unreachable):
    # tells us if he is sprinting, from the same ladder, no second logic.
    if _ho_ok(0) > 0.5:
        return 0.0
    if _ho_ok(1) > 0.5:
        return 1.0
    if _ho_ok(2) > 0.5:
        return 2.0
    if _ho_ok(3) > 0.5:
        return 3.0
    return 4.0


def _our_tier():
    if _w_ok() > 0.5:
        return 0.0
    if _s_ok() > 0.5:
        return 1.0
    if _r_ok() > 0.5:
        return 2.0
    if _v_ok() > 0.5:
        return 3.0
    return 4.0


def _danger_x():
    # His hardest reply point on our half, scored by the shared evaluator.
    # Same function as our attack scan, opposite direction.
    s = _own_sign()
    ox = opp_meet_x()
    oz = opp_meet_z()
    ux = _self_x()
    uz = _self_z()
    best_s = 0.0 - 1.0
    best_x = s * 14.0
    px = s * 14.0
    pz = 6.0
    sc = _vscore(ux, uz, ox, oz, px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    px = s * 14.0
    pz = 0.0 - 6.0
    sc = _vscore(ux, uz, ox, oz, px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    px = s * 7.0
    pz = 6.0
    sc = _vscore(ux, uz, ox, oz, px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    px = s * 7.0
    pz = 0.0 - 6.0
    sc = _vscore(ux, uz, ox, oz, px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    px = s * 1.0
    pz = 6.0
    sc = _vscore(ux, uz, ox, oz, px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    px = s * 1.0
    pz = 0.0 - 6.0
    sc = _vscore(ux, uz, ox, oz, px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    return best_x


def _danger_z():
    # Same scan, z component (kept separate: one float per helper).
    s = _own_sign()
    ox = opp_meet_x()
    oz = opp_meet_z()
    ux = _self_x()
    uz = _self_z()
    best_s = 0.0 - 1.0
    best_z = 6.0
    px = s * 14.0
    pz = 6.0
    sc = _vscore(ux, uz, ox, oz, px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    px = s * 14.0
    pz = 0.0 - 6.0
    sc = _vscore(ux, uz, ox, oz, px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    px = s * 7.0
    pz = 6.0
    sc = _vscore(ux, uz, ox, oz, px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    px = s * 7.0
    pz = 0.0 - 6.0
    sc = _vscore(ux, uz, ox, oz, px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    px = s * 1.0
    pz = 6.0
    sc = _vscore(ux, uz, ox, oz, px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    px = s * 1.0
    pz = 0.0 - 6.0
    sc = _vscore(ux, uz, ox, oz, px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    return best_z


def _fast_t(d):
    # Fastest effective ball flight over all shot types (no lob).
    t = 0.214 + 0.0257 * d
    cand = 0.498 + 0.0034 * d
    if cand < t:
        t = cand
    cand = 0.285 + 0.0178 * d
    if cand < t:
        t = cand
    cand = 0.517 + 0.0069 * d
    if cand < t:
        t = cand
    cand = 0.235 + 0.0160 * d
    if cand < t:
        t = cand
    return t


def _virt_x():
    # His reply landing, habit-shaded toward his scoring spot.
    dz = _danger_z()
    az = api.split_vector(t.opponent_average_scoring_location(), 2)
    if az > 5.0:
        az = 5.0
    if az < 0.0 - 5.0:
        az = 0.0 - 5.0
    return _danger_x()


def _virt_z():
    dz = _danger_z()
    az = api.split_vector(t.opponent_average_scoring_location(), 2)
    if az > 5.0:
        az = 5.0
    if az < 0.0 - 5.0:
        az = 0.0 - 5.0
    return dz * 0.65 + az * 0.35


def _virt_flight():
    d = _dist(opp_meet_x(), opp_meet_z(), _virt_x(), _virt_z())
    f = _fast_t(d)
    if f < 0.2:
        f = 0.2
    if f > 10.0:
        f = 10.0
    return f


def _virt_T0():
    T = opp_t_meet()
    if T < 0.0:
        T = 0.0
    if T > 2.0:
        T = 2.0
    return T


def _vm_meet_x(speed, ring):
    # Earliest virtual-flight fraction we cover with the negative-t
    # budget (5-round bisection, walk first, then sprint).
    ox = opp_meet_x()
    oz = opp_meet_z()
    vx = _virt_x()
    vz = _virt_z()
    sx = _self_x()
    sz = _self_z()
    flight = _virt_flight()
    T0 = _virt_T0()
    lo = 0.0
    hi = flight
    for _ in range(5):
        mid = (lo + hi) * 0.5
        frac = mid / flight
        px = ox + (vx - ox) * frac
        pz = oz + (vz - oz) * frac
        ddx = px - sx
        ddz = pz - sz
        need = api.sqrt(ddx * ddx + ddz * ddz) - ring - LEAD
        have = speed * (T0 + mid)
        if have >= need:
            lo = mid
        else:
            hi = mid
    frac = lo / flight
    return ox + (vx - ox) * frac


def _vm_meet_z(speed, ring):
    ox = opp_meet_x()
    oz = opp_meet_z()
    vx = _virt_x()
    vz = _virt_z()
    sx = _self_x()
    sz = _self_z()
    flight = _virt_flight()
    T0 = _virt_T0()
    lo = 0.0
    hi = flight
    for _ in range(5):
        mid = (lo + hi) * 0.5
        frac = mid / flight
        px = ox + (vx - ox) * frac
        pz = oz + (vz - oz) * frac
        ddx = px - sx
        ddz = pz - sz
        need = api.sqrt(ddx * ddx + ddz * ddz) - ring - LEAD
        have = speed * (T0 + mid)
        if have >= need:
            lo = mid
        else:
            hi = mid
    frac = lo / flight
    return oz + (vz - oz) * frac


def _vm_ok(speed, ring):
    flight = _virt_flight()
    need = _dist(_self_x(), _self_z(), _virt_x(), _virt_z()) - ring
    if speed * (_virt_T0() + flight) >= need:
        return 1.0
    else:
        return 0.0


def pos_x():
    # Positioning target: earliest comfortable virtual tier, anchored
    # deep-center (split shade), held once reached (regen stamina).
    x = _virt_x()
    if x > 15.0:
        x = 15.0
    if x < 0.0 - 15.0:
        x = 0.0 - 15.0
    if _vm_ok(SPRINT, 0.0) > 0.5:
        x = _vm_meet_x(SPRINT, 0.0)
    if _vm_ok(WALK, 0.0) > 0.5:
        x = _vm_meet_x(WALK, 0.0)
    if x > 15.0:
        x = 15.0
    if x < 0.0 - 15.0:
        x = 0.0 - 15.0
    anchor = _own_sign() * 13.0
    z = _vm_meet_z(WALK, 0.0)
    if _vm_ok(WALK, 0.0) < 0.5:
        z = _virt_z()
    hold_x = anchor
    hold_z = z * 0.4
    if _dist(_self_x(), _self_z(), hold_x, hold_z) < 1.2:
        return _self_x()
    else:
        return hold_x


def pos_z():
    x = _virt_x()
    if x > 15.0:
        x = 15.0
    if x < 0.0 - 15.0:
        x = 0.0 - 15.0
    z = _virt_z()
    if _vm_ok(SPRINT, 0.0) > 0.5:
        z = _vm_meet_z(SPRINT, 0.0)
    if _vm_ok(WALK, 0.0) > 0.5:
        z = _vm_meet_z(WALK, 0.0)
    if z > 7.5:
        z = 7.5
    if z < 0.0 - 7.5:
        z = 0.0 - 7.5
    hold_z = z * 0.4
    hold_x = _own_sign() * 13.0
    if _dist(_self_x(), _self_z(), hold_x, hold_z) < 1.2:
        return _self_z()
    else:
        return hold_z
