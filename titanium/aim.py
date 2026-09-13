"""Strike targets: the shared minimax evaluator, our direction.

For each of 8 candidate landings on the opponent half we score how hard it
is for HIM to intercept a ball launched by us toward it — ladder tier he
must extend to * 1000 + required speed — and take the hardest. The shot id
travels with its point (fastest option for that distance). Edge aims shrink
toward center under fatigue scatter. Serve stays hardcoded diagonal Flat
(game-proven in-box). Same function as the danger scan, opposite direction:
no duplicate minimax logic anywhere.
"""
import AIA_Comp_Libry.tennis.v15f as t
import intercept


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


def _fast_opt(d):
    opt = 0.0
    t = 0.214 + 0.0257 * d
    cand = 0.498 + 0.0034 * d
    if cand < t:
        t = cand
        opt = 1.0
    cand = 0.285 + 0.0178 * d
    if cand < t:
        t = cand
        opt = 2.0
    cand = 0.517 + 0.0069 * d
    if cand < t:
        t = cand
        opt = 4.0
    cand = 0.235 + 0.0160 * d
    if cand < t:
        t = cand
        opt = 6.0
    cand = 0.235 + 0.0160 * d
    if cand < t:
        opt = 7.0
    return opt


def _self_d(px, pz):
    dx = px - intercept._self_x()
    dz = pz - intercept._self_z()
    return api.sqrt(dx * dx + dz * dz)


def _best_ax():
    # Fixed 8-point grid: deep/mid/half/net rows x both corners.
    o = 0.0 - intercept._own_sign()
    sx = intercept._self_x()
    sz = intercept._self_z()
    ox = intercept._opp_x()
    oz = intercept._opp_z()
    best_s = 0.0 - 1.0
    best_x = o * 13.0
    px = o * 13.0
    pz = 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    px = o * 13.0
    pz = 0.0 - 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    px = o * 10.0
    pz = 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    px = o * 10.0
    pz = 0.0 - 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    px = o * 7.0
    pz = 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    px = o * 7.0
    pz = 0.0 - 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    px = o * 1.0
    pz = 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    px = o * 1.0
    pz = 0.0 - 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_x = px
    return best_x


def _best_az():
    o = 0.0 - intercept._own_sign()
    sx = intercept._self_x()
    sz = intercept._self_z()
    ox = intercept._opp_x()
    oz = intercept._opp_z()
    best_s = 0.0 - 1.0
    best_z = 5.0
    px = o * 13.0
    pz = 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    px = o * 13.0
    pz = 0.0 - 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    px = o * 10.0
    pz = 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    px = o * 10.0
    pz = 0.0 - 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    px = o * 7.0
    pz = 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    px = o * 7.0
    pz = 0.0 - 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    px = o * 1.0
    pz = 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    px = o * 1.0
    pz = 0.0 - 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_z = pz
    return best_z


def _best_opt():
    o = 0.0 - intercept._own_sign()
    sx = intercept._self_x()
    sz = intercept._self_z()
    ox = intercept._opp_x()
    oz = intercept._opp_z()
    best_s = 0.0 - 1.0
    best_opt = 2.0
    px = o * 13.0
    pz = 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_opt = _fast_opt(_self_d(px, pz))
    px = o * 13.0
    pz = 0.0 - 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_opt = _fast_opt(_self_d(px, pz))
    px = o * 10.0
    pz = 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_opt = _fast_opt(_self_d(px, pz))
    px = o * 10.0
    pz = 0.0 - 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_opt = _fast_opt(_self_d(px, pz))
    px = o * 7.0
    pz = 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_opt = _fast_opt(_self_d(px, pz))
    px = o * 7.0
    pz = 0.0 - 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_opt = _fast_opt(_self_d(px, pz))
    px = o * 1.0
    pz = 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_opt = _fast_opt(_self_d(px, pz))
    px = o * 1.0
    pz = 0.0 - 5.0
    sc = intercept._vscore(ox, oz, sx, sz, px, pz)
    if sc > best_s:
        best_s = sc
        best_opt = _fast_opt(_self_d(px, pz))
    return best_opt


def _fat_shrink():
    deuce = t.deuce_fatigue()
    rally = t.rally_fatigue()
    if deuce < 0.0:
        deuce = 0.0
    if deuce > 20.0:
        deuce = 20.0
    if rally < 0.0:
        rally = 0.0
    if rally > 20.0:
        rally = 20.0
    shrink = 0.36 * (deuce + rally)
    if shrink > 2.0:
        shrink = 2.0
    return shrink


def attack_x():
    return _best_ax()


def attack_z():
    # Fatigue scatter compensation: edge aims pull toward center.
    z = _best_az()
    shrink = _fat_shrink()
    if api.abs(z) > 2.0:
        want = api.abs(z) - shrink
        if want < 2.0:
            want = 2.0
        if z > 0.0:
            return want
        else:
            return 0.0 - want
    else:
        return z


def attack_opt():
    return _best_opt()
