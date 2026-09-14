"""Where to stand + when: two-stage footrace ladder, walk-first selection.

STAGE 1 runs the ladder against the live ball (current pos/vel). STAGE 2
re-runs it from the bounced state (bounce point, post-bounce velocity with
the shot-specific forward keep and bounce vertical) — but only matters when
stage 1 cannot deliver. Same quadratic both stages: with tau = T - tb the
stage-2 footrace is |Pb + V2*tau - P| <= s*(tau+tb) + r, i.e. the same solve
with ring inflated by s*tb. Best interception point wins across stages.

TIER ORDER per stage (Minkowski rings): walk r=0 -> walk perfect r=1.0 ->
walk full r=2.6. Sprint tiers (ring 0 / perfect 1.0) run ONLY if walking
never reached perfect AND stamina is above reserve AND sprint reaches
perfect and beats walking — accuracy first, sprint-desperation never
selected. No Ball Incoming anywhere: chase = 2nd-bounce ownership (primary)
+ live-ball-on-our-side fallback (sticky, no flicker).

The same ladder runs from the opponent's perspective (his meet point +
meet time = launch of a virtual ball that does not exist yet). While the
ball is his, we intercept the virtual ball (negative-t budget), shaded
deep-center. Ballistics use the measured game constants (g=28, bounce keeps
per shot, ground 0.31). The solve aims the RACKET (0.55 lead shift).
"""
import AIA_Comp_Libry.tennis.v15f as t

WALK = 8.5
SPRINT = 13.0
R_RACKET = 1.0
R_SWING = 2.6
BALL_G = 28.0
GROUND = 0.28
FLOOR = 0.31
KEEP = 0.78
TAKE_H = 2.7
LEAD = 0.55
STAM_RESERVE = 0.50
PARK_D = 1.05
CONTACT_Y = 1.0


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


# ---- game ballistics, live ball (measured constants) ----

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


def _y_post(T, tb, vy2):
    dt = T - tb
    if dt < 0.0:
        dt = 0.0
    return FLOOR + vy2 * dt - 14.0 * dt * dt


# ---- bounced state of the LIVE ball (shot-specific, game-pinned) ----

def _live_shot():
    return t.shot_ball()


def _live_fwd():
    # Planar forward keep through the bounce, by live shot arg.
    sh = _live_shot()
    if sh < 0.5:
        return 1.2
    if sh < 1.5:
        return 0.6724
    if sh < 2.5:
        return 0.94
    if sh < 4.5:
        return 0.40
    return 0.94


def _live_vy2():
    # Post-bounce vertical speed: impact * shot restitution (+hop clamps),
    # spin floor kills it (dead ball stays down).
    sh = _live_shot()
    tb = _t_bounce()
    vyi = api.abs(_vel_y() - BALL_G * tb)
    if sh < 0.5:
        vy2 = vyi * 1.1076
        if vy2 < 2.4:
            vy2 = 2.4
    else:
        if sh < 1.5:
            vy2 = vyi * 1.008
            if vy2 < 2.04:
                vy2 = 2.04
        else:
            if sh < 2.5:
                vy2 = vyi * 0.78
                if vy2 < 2.4:
                    vy2 = 2.4
            else:
                if sh < 4.5:
                    vy2 = vyi * 0.8424
                    if vy2 < 9.6:
                        vy2 = 9.6
                    if vy2 > 11.8:
                        vy2 = 11.8
                else:
                    vy2 = vyi * 0.78
                    if vy2 < 2.4:
                        vy2 = 2.4
    if vy2 < 0.45:
        vy2 = 0.0
    return vy2


def _pb_x():
    return _ball_x() + _vel_x() * _t_bounce()


def _pb_z():
    return _ball_z() + _vel_z() * _t_bounce()


def _eff_ours_x():
    return _ball_x() + _own_sign() * LEAD


def _eff_his_x():
    return _ball_x() - _own_sign() * LEAD


# ---- quadratic footrace, both stages, shared ----

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


def _solve_T(px, pz, s, r, ex, ez, vx, vz, tmin):
    a = _qa(s, vx, vz)
    b = _qb(px, pz, s, r, ex, ez, vx, vz)
    c = _qc(px, pz, r, ex, ez)
    disc = b * b - 4.0 * a * c
    if disc < 0.0:
        disc = 0.0
    if disc > 1000000.0:
        disc = 1000000.0
    te = (0.0 - b - api.sqrt(disc)) / (2.0 * a)
    if te < tmin:
        return tmin
    else:
        return te


def _solve_ok(px, pz, s, r, ex, ez, vx, vz, tmin, tb, vy2, post):
    # post=0: live ball (takeable on full arc, valid from tmin=0).
    # post=1: bounced ball (takeable on post arc, valid from T>=tb).
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
        if tx > tmin:
            win = 1.0
        else:
            win = 0.0
    else:
        if te > tmin:
            win = 1.0
        else:
            win = 0.0
    if win < 0.5:
        return 0.0
    T = te
    if T < tmin:
        T = tmin
    if post < 0.5:
        y = _y_at(T)
    else:
        y = _y_post(T, tb, vy2)
    if y > TAKE_H:
        return 0.0
    return 1.0


def _tier_s(tier):
    if tier > 2.5:
        return SPRINT
    if tier > 0.5:
        return WALK
    return WALK


def _tier_r(tier):
    # tiers: 0 walk direct, 1 walk perfect, 2 walk full, 3 sprint direct,
    # 4 sprint perfect. Sprint-desperation is never selected.
    if tier > 3.5:
        return R_RACKET
    if tier > 2.5:
        return 0.0
    if tier > 1.5:
        return R_SWING
    if tier > 0.5:
        return R_RACKET
    return 0.0


def _mT(tier, stage):
    # Contact time for tier/stage (999 = infeasible).
    #
    # COMFORT TARGET (anti-late): aim the movement at the ball's PERFECT-ring
    # entry (r = 1.0), not the tier-ring entry. The tier ring answers "can we
    # cover the ball at all by then"; the perfect ring answers "where will the
    # ball be when it walks into the perfect window". Solving r = 1.0 returns
    # the later of (ball reaches 1.0 m) and (we reach that point) — when we
    # are fast enough the ball's time wins, so we PARK at the landing point
    # early and the held swing releases on the FIRST perfect tick (PERFECT
    # contact, no zero-slack arrival). When we are too slow, the solve
    # degrades to our own arrival — same physics as before, nothing lost.
    # Fallback: the tier-ring solve (old behavior) when the perfect point is
    # not coverable (tier 0 covers the racket center — a tighter ask than 1.0).
    s = _tier_s(tier)
    r = _tier_r(tier)
    if stage < 1.5:
        T1 = _solve_T(_self_x(), _self_z(), s, 1.0,
                      _eff_ours_x(), _ball_z(), _vel_x(), _vel_z(), 0.0)
        if _solve_ok(_self_x(), _self_z(), s, 1.0,
                     _eff_ours_x(), _ball_z(), _vel_x(), _vel_z(),
                     0.0, 0.0, 0.0, 0.0) > 0.5:
            return T1
        T = _solve_T(_self_x(), _self_z(), s, r,
                     _eff_ours_x(), _ball_z(), _vel_x(), _vel_z(), 0.0)
        if _solve_ok(_self_x(), _self_z(), s, r,
                     _eff_ours_x(), _ball_z(), _vel_x(), _vel_z(),
                     0.0, 0.0, 0.0, 0.0) > 0.5:
            return T
        else:
            return 999.0
    else:
        tb = _t_bounce()
        fwd = _live_fwd()
        ex = _pb_x() + _own_sign() * LEAD
        ez = _pb_z()
        vx = _vel_x() * fwd
        vz = _vel_z() * fwd
        rr = r + s * tb
        r1 = 1.0 + s * tb
        T1 = _solve_T(_self_x(), _self_z(), s, r1, ex, ez, vx, vz, tb)
        if _solve_ok(_self_x(), _self_z(), s, r1, ex, ez, vx, vz,
                     tb, tb, _live_vy2(), 1.0) > 0.5:
            return T1
        T = _solve_T(_self_x(), _self_z(), s, rr, ex, ez, vx, vz, tb)
        if _solve_ok(_self_x(), _self_z(), s, rr, ex, ez, vx, vz,
                     tb, tb, _live_vy2(), 1.0) > 0.5:
            return T
        else:
            return 999.0


def _mok(tier, stage):
    T = _mT(tier, stage)
    if T > 900.0:
        return 0.0
    else:
        return 1.0


def _mmx(tier, stage):
    T = _mT(tier, stage)
    if T > 900.0:
        return _self_x()
    if stage < 1.5:
        return _ball_x() + _vel_x() * T
    else:
        tb = _t_bounce()
        return _pb_x() + _vel_x() * _live_fwd() * (T - tb)


def _mmz(tier, stage):
    T = _mT(tier, stage)
    if T > 900.0:
        return _self_z()
    if stage < 1.5:
        return _ball_z() + _vel_z() * T
    else:
        tb = _t_bounce()
        return _pb_z() + _vel_z() * _live_fwd() * (T - tb)


# ---- comfort selection across stages (walk-first, sprint-gated) ----

def _cW0():
    if _mok(0, 1) > 0.5:
        return 1.0
    if _mok(0, 2) > 0.5:
        return 1.0
    return 0.0


def _cW1():
    if _mok(1, 1) > 0.5:
        return 1.0
    if _mok(1, 2) > 0.5:
        return 1.0
    return 0.0


def _cW2():
    if _mok(2, 1) > 0.5:
        return 1.0
    if _mok(2, 2) > 0.5:
        return 1.0
    return 0.0


def _cS0():
    if t.self_stamina_pct() > STAM_RESERVE:
        if _mok(3, 1) > 0.5:
            return 1.0
        if _mok(3, 2) > 0.5:
            return 1.0
    return 0.0


def _cS1():
    if t.self_stamina_pct() > STAM_RESERVE:
        if _mok(4, 1) > 0.5:
            return 1.0
        if _mok(4, 2) > 0.5:
            return 1.0
    return 0.0


def _cT(tier):
    # Earliest contact across stages (999 = nowhere).
    a = _mT(tier, 1)
    b = _mT(tier, 2)
    if a < b:
        return a
    else:
        return b


def _cMX(tier):
    a = _mT(tier, 1)
    b = _mT(tier, 2)
    if a < b:
        return _mmx(tier, 1)
    else:
        return _mmx(tier, 2)


def _cMZ(tier):
    a = _mT(tier, 1)
    b = _mT(tier, 2)
    if a < b:
        return _mmz(tier, 1)
    else:
        return _mmz(tier, 2)


def _picked():
    # Comfort order: stamina above 25% -> walk perfect when feasible
    # (better contact quality; walk-direct ring-0 is near-never feasible
    # so this rarely changes selection, but pins the preference) >
    # walk direct > sprint direct/perfect (reserve-gated) >
    # walk full > must-run fallback.
    if t.self_stamina_pct() > 0.25:
        if _cW1() > 0.5:
            return 1.0
    if _cW0() > 0.5:
        return 0.0
    if _cW1() > 0.5:
        return 1.0
    if _cS0() > 0.5:
        return 3.0
    if _cS1() > 0.5:
        return 4.0
    if _cW2() > 0.5:
        return 2.0
    return 9.0


def _pickT():
    p = _picked()
    if p < 0.5:
        return _cT(0)
    if p < 1.5:
        return _cT(1)
    if p < 2.5:
        return _cT(2)
    if p < 3.5:
        return _cT(3)
    if p < 4.5:
        return _cT(4)
    return 999.0


def _pickMX():
    p = _picked()
    if p < 0.5:
        return _cMX(0)
    if p < 1.5:
        return _cMX(1)
    if p < 2.5:
        return _cMX(2)
    if p < 3.5:
        return _cMX(3)
    if p < 4.5:
        return _cMX(4)
    return _self_x()


def _pickMZ():
    p = _picked()
    if p < 0.5:
        return _cMZ(0)
    if p < 1.5:
        return _cMZ(1)
    if p < 2.5:
        return _cMZ(2)
    if p < 3.5:
        return _cMZ(3)
    if p < 4.5:
        return _cMZ(4)
    return _self_z()


def _our_tier():
    p = _picked()
    if p > 8.5:
        return 4.0
    if p > 2.5:
        return p
    return p


def want_sprint():
    # Sprint flag follows the selection: 1 iff a sprint tier was picked.
    p = _picked()
    if p > 2.5:
        if p < 4.5:
            return 1.0
    return 0.0


def _fall_x():
    # Must-run fallback: at the live ball head-on (lob: take the landing).
    ball_now = t.ball_position()
    bpx = api.split_vector(ball_now, 0)
    bpy = api.split_vector(ball_now, 1)
    if bpy > 2.5:
        return _own_sign() * 13.0
    else:
        return bpx


def _fall_z():
    ball_now = t.ball_position()
    bpy = api.split_vector(ball_now, 1)
    bpz = api.split_vector(ball_now, 2)
    if bpy > 2.5:
        return bounce_z()
    else:
        return bpz


def plan_x():
    # Serve in flight, pre-bounce: interception is impossible (the game
    # enforces Must Wait For Bounce), so hold the receive stance.
    if t.must_wait_for_bounce():
        return receive_x()
    x = _pickMX()
    if _picked() > 8.5:
        x = _fall_x()
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
    z = _pickMZ()
    if _picked() > 8.5:
        z = _fall_z()
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
    return _solve_T(_opp_x(), _opp_z(), _tier_s(tier), _tier_r(tier),
                    _eff_his_x(), _ball_z(), _vel_x(), _vel_z(), 0.0)


def _his_ok(tier):
    return _solve_ok(_opp_x(), _opp_z(), _tier_s(tier), _tier_r(tier),
                     _eff_his_x(), _ball_z(), _vel_x(), _vel_z(),
                     0.0, 0.0, 0.0, 0.0)


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


def _his_tier():
    if _ho_ok(0) > 0.5:
        return 0.0
    if _ho_ok(1) > 0.5:
        return 1.0
    if _ho_ok(2) > 0.5:
        return 2.0
    if _ho_ok(3) > 0.5:
        return 3.0
    return 4.0


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
    # Ignore-ball rules (preserve stamina, punish the striker):
    # - 1st landing clearly out (line + ball-edge tol + 0.25 pad): his
    #   fault, the point resolves itself — never chase.
    # - 2nd landing outside the arena: his ball exits in flight and the
    #   STRIKER loses it — standing still wins, chasing wastes stamina.
    # - Live ball on our side whose next landing is outside the arena:
    #   same self-destruct — ignore.
    if t.must_wait_for_bounce():
        return 0.0
    if _recv_known() > 0.5:
        b1x = api.split_vector(t.predicted_bounce(), 0)
        b1z = api.split_vector(t.predicted_bounce(), 2)
        # 1st landing clearly out (line + ball-edge tol + 0.25 pad) = his
        # fault -> ignore, the point resolves itself. The 2nd-bounce check
        # is GONE (2026-09-14 correction): the 2nd bounce may land anywhere
        # and the RECEIVER loses it — deep balls and serves must be
        # returned, never ignored (ignoring them handed stock 14 aces).
        if b1x > 14.25:
            return 0.0
        if b1x < 0.0 - 14.25:
            return 0.0
        if b1z > 6.25:
            return 0.0
        if b1z < 0.0 - 6.25:
            return 0.0
        b2 = t.predicted_2nd_bounce()
        b2x = api.split_vector(b2, 0)
        if b2x * _own_sign() > 0.0:
            return 1.0
    if t.ball_on_self_side():
        if t.ball_speed() > 0.1:
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


# ---- shared minimax evaluator: per-(point, shot), two landings ----

def _t1_0(d):
    t = d / 31.2
    if t < 0.14:
        t = 0.14
    return t


def _t1_1(d):
    return 0.6232


def _t1_2(d):
    t = d / 36.4
    if t < 0.12:
        t = 0.12
    return t


def _t1_4(d):
    return 0.7951


def _t1_6(d):
    t = d / 24.936
    if t < 0.14:
        t = 0.14
    return t


def _vy2_0(d):
    t1 = _t1_0(d)
    vyi = api.abs((0.31 - 1.0) / t1 + 14.0 * t1 - 28.0 * t1)
    vy2 = vyi * 1.1076
    if vy2 < 2.4:
        vy2 = 2.4
    if vy2 < 0.45:
        vy2 = 0.0
    return vy2


def _vy2_1(d):
    t1 = _t1_1(d)
    vyi = api.abs((0.31 - 1.0) / t1 + 14.0 * t1 - 28.0 * t1)
    vy2 = vyi * 1.008
    if vy2 < 2.04:
        vy2 = 2.04
    if vy2 < 0.45:
        vy2 = 0.0
    return vy2


def _vy2_2(d):
    t1 = _t1_2(d)
    vyi = api.abs((0.31 - 1.0) / t1 + 14.0 * t1 - 28.0 * t1)
    vy2 = vyi * 0.78
    if vy2 < 2.4:
        vy2 = 2.4
    if vy2 < 0.45:
        vy2 = 0.0
    return vy2


def _vy2_4(d):
    t1 = _t1_4(d)
    vyi = api.abs((0.31 - 1.0) / t1 + 14.0 * t1 - 28.0 * t1)
    vy2 = vyi * 0.8424
    if vy2 < 9.6:
        vy2 = 9.6
    if vy2 > 11.8:
        vy2 = 11.8
    if vy2 < 0.45:
        vy2 = 0.0
    return vy2


def _vy2_6(d):
    t1 = _t1_6(d)
    vyi = api.abs((0.31 - 1.0) / t1 + 14.0 * t1 - 28.0 * t1)
    vy2 = vyi * 0.78
    if vy2 < 2.4:
        vy2 = 2.4
    if vy2 < 0.45:
        vy2 = 0.0
    return vy2


def _vtier_at(dv, tf, head, stam):
    # Cheapest tier covering a landing at distance dv by time tf (with
    # pre-launch head start): walk needs no stamina, everything above the
    # walk tier spends it — same preservation rule, both sides.
    if dv <= WALK * tf + head:
        return 0.0
    if stam > STAM_RESERVE:
        if dv <= SPRINT * tf + head:
            return 1.0
        if dv - R_RACKET <= SPRINT * tf + head:
            return 2.0
        if dv - R_SWING <= SPRINT * tf + head:
            return 3.0
    return 4.0


def _vscore(px, pz, vstam, lx, lz, tx, tz, t1, vy2, fwd, head):
    # THE shared minimax evaluator, both directions: how hard is it for the
    # victim at (px,pz) to intercept a ball launched at (lx,lz) toward
    # (tx,tz)? t1/vy2/fwd arrive precomputed per shot type (per-opt helpers
    # above — no dispatch branches in here, so no dead arms at any call
    # site). Two landings matter, not one: the victim takes whichever is
    # easier — first bounce (t1) or second bounce (t2, shot-specific bounce
    # physics: topspin kicks, slice skids, drop dies). After the second
    # bounce the point is lost, so nothing past t2 counts. Score =
    # easiest-landing tier * 1000 + required speed.
    #
    # Scoring legality (the real rules, both directions):
    # - 1st landing clearly out (beyond the line + ball-edge tolerance
    #   + 0.25 pad): the striker faults, nobody covers -> score 0.
    # - The 2nd bounce may land ANYWHERE (the in-flight arena bound is the
    #   FULL court length 28 / doubles 18, not the half-court — measured
    #   2026-09-14): a deep 1st-bounce-IN shot double-bounces the receiver
    #   out of court and WINS. No 2nd-bounce restriction. (An earlier
    #   build zero-scored b2 outside 13.9/8.9 — that misread killed the
    #   deep game and made want_chase ignore returnable serves.)
    if tx > 14.25:
        return 0.0
    if tx < 0.0 - 14.25:
        return 0.0
    if tz > 6.25:
        return 0.0
    if tz < 0.0 - 6.25:
        return 0.0
    t2 = t1 + 2.0 * vy2 / 28.0
    f = fwd * (t2 - t1) / t1
    b2x = tx + (tx - lx) * f
    b2z = tz + (tz - lz) * f
    vdx = tx - px
    vdz = tz - pz
    d1 = api.sqrt(vdx * vdx + vdz * vdz)
    tier1 = _vtier_at(d1, t1, head, vstam)
    slack1 = d1 - R_SWING
    if slack1 < 0.0:
        slack1 = 0.0
    den1 = t1
    if den1 < 0.2:
        den1 = 0.2
    if den1 > 10.0:
        den1 = 10.0
    s1 = tier1 * 1000.0 + slack1 / den1
    wdx = b2x - px
    wdz = b2z - pz
    d2 = api.sqrt(wdx * wdx + wdz * wdz)
    tier2 = _vtier_at(d2, t2, head, vstam)
    slack2 = d2 - R_SWING
    if slack2 < 0.0:
        slack2 = 0.0
    den2 = t2
    if den2 < 0.2:
        den2 = 0.2
    if den2 > 10.0:
        den2 = 10.0
    s2 = tier2 * 1000.0 + slack2 / den2
    if s1 < s2:
        return s1
    else:
        return s2


def _dgr_best(px, pz):
    # His optimal shot AT this point: max over shot types of our difficulty.
    Tm = opp_t_meet()
    if Tm < 0.0:
        Tm = 0.0
    if Tm > 2.0:
        Tm = 2.0
    head = WALK * Tm
    stam = t.self_stamina_pct()
    ux = _self_x()
    uz = _self_z()
    ox = opp_meet_x()
    oz = opp_meet_z()
    ddx = px - ox
    ddz = pz - oz
    d = api.sqrt(ddx * ddx + ddz * ddz)
    best = 0.0 - 1.0
    sc = _vscore(ux, uz, stam, ox, oz, px, pz, _t1_0(d), _vy2_0(d), 1.2, head)
    if sc > best:
        best = sc
    sc = _vscore(ux, uz, stam, ox, oz, px, pz, _t1_1(d), _vy2_1(d), 0.6724, head)
    if sc > best:
        best = sc
    sc = _vscore(ux, uz, stam, ox, oz, px, pz, _t1_2(d), _vy2_2(d), 0.94, head)
    if sc > best:
        best = sc
    sc = _vscore(ux, uz, stam, ox, oz, px, pz, _t1_4(d), _vy2_4(d), 0.40, head)
    if sc > best:
        best = sc
    sc = _vscore(ux, uz, stam, ox, oz, px, pz, _t1_6(d), _vy2_6(d), 0.94, head)
    if sc > best:
        best = sc
    sc = _vscore(ux, uz, stam, ox, oz, px, pz, _t1_6(d), _vy2_6(d), 0.94, head)
    if sc > best:
        best = sc
    return best


def _danger_x():
    # His hardest reply point on our half, scored by the shared evaluator.
    # Same function as our attack scan, opposite direction.
    s = _own_sign()
    ux = _self_x()
    uz = _self_z()
    best_s = 0.0 - 1.0
    best_x = s * 14.0
    px = s * 14.0
    pz = 6.0
    sc = _dgr_best(px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    px = s * 14.0
    pz = 0.0 - 6.0
    sc = _dgr_best(px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    px = s * 7.0
    pz = 6.0
    sc = _dgr_best(px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    px = s * 7.0
    pz = 0.0 - 6.0
    sc = _dgr_best(px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    px = s * 1.0
    pz = 6.0
    sc = _dgr_best(px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    px = s * 1.0
    pz = 0.0 - 6.0
    sc = _dgr_best(px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    return best_x


def _danger_z():
    # Same scan, z component (kept separate: one float per helper).
    s = _own_sign()
    ux = _self_x()
    uz = _self_z()
    best_s = 0.0 - 1.0
    best_z = 6.0
    px = s * 14.0
    pz = 6.0
    sc = _dgr_best(px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    px = s * 14.0
    pz = 0.0 - 6.0
    sc = _dgr_best(px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    px = s * 7.0
    pz = 6.0
    sc = _dgr_best(px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    px = s * 7.0
    pz = 0.0 - 6.0
    sc = _dgr_best(px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    px = s * 1.0
    pz = 6.0
    sc = _dgr_best(px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    px = s * 1.0
    pz = 0.0 - 6.0
    sc = _dgr_best(px, pz)
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
    # His reply landing: the danger scan (his hardest point on our half).
    return _danger_x()


def _virt_z():
    # Habit shade: danger scan pulled 35% toward his scoring habit.
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
