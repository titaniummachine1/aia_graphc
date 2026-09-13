"""Strike targets: reverse-minimax attack scan over a fixed grid.

For each of 8 candidate landings on the opponent half we compute the
speed HE must sustain to catch our fastest shot there:
    req = max(0, dist(opp, pt) - 2.6) / t_fast(dist(us, pt))
and take the hardest to catch (0.35 band, tiebreak wider angle, then
faster flight). The shot id travels with its point (fastest option for
that distance). Edge aims shrink toward center under fatigue scatter.
Serve stays hardcoded diagonal Flat (game-proven in-box).
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


def _scan_best_x():
    # Fixed 8-point grid: deep/mid/half/net rows x both corners.
    o = 0.0 - intercept._own_sign()
    sx = intercept._self_x()
    sz = intercept._self_z()
    ox = intercept._opp_x()
    oz = intercept._opp_z()
    to_ox = ox - sx
    to_oz = oz - sz
    olen = api.clamp(api.sqrt(to_ox * to_ox + to_oz * to_oz), 0.001, 100.0)
    best_x = o * 13.0
    best_req = 0.0 - 1.0
    best_dot = 2.0
    best_t = 99999.0
    for i in range(8):
        if i == 0:
            px = o * 13.0
            pz = 5.0
        if i == 1:
            px = o * 13.0
            pz = 0.0 - 5.0
        if i == 2:
            px = o * 10.0
            pz = 5.0
        if i == 3:
            px = o * 10.0
            pz = 0.0 - 5.0
        if i == 4:
            px = o * 7.0
            pz = 5.0
        if i == 5:
            px = o * 7.0
            pz = 0.0 - 5.0
        if i == 6:
            px = o * 1.0
            pz = 5.0
        if i == 7:
            px = o * 1.0
            pz = 0.0 - 5.0
        sdx = px - sx
        sdz = pz - sz
        d_self = api.sqrt(sdx * sdx + sdz * sdz)
        tf = 0.214 + 0.0257 * d_self
        cand = 0.498 + 0.0034 * d_self
        if cand < tf:
            tf = cand
        cand = 0.285 + 0.0178 * d_self
        if cand < tf:
            tf = cand
        cand = 0.517 + 0.0069 * d_self
        if cand < tf:
            tf = cand
        cand = 0.235 + 0.0160 * d_self
        if cand < tf:
            tf = cand
        odx = px - ox
        odz = pz - oz
        slack = api.sqrt(odx * odx + odz * odz) - 2.6
        if slack < 0.0:
            slack = 0.0
        req = slack / api.clamp(tf, 0.2, 10.0)
        tx = px - sx
        tz = pz - sz
        tlen = api.clamp(api.sqrt(tx * tx + tz * tz), 0.001, 100.0)
        dot = (tx * to_ox + tz * to_oz) / (tlen * olen)
        if req > best_req + 0.35:
            better = 1.0
        else:
            better = 0.0
        if better < 0.5:
            if api.abs(req - best_req) <= 0.35:
                if dot < best_dot - 0.05:
                    better = 1.0
                else:
                    if api.abs(dot - best_dot) <= 0.05:
                        if tf < best_t:
                            better = 1.0
        if better > 0.5:
            best_x = px
            best_req = req
            best_dot = dot
            best_t = tf
    return best_x


def _scan_best_z():
    o = 0.0 - intercept._own_sign()
    sx = intercept._self_x()
    sz = intercept._self_z()
    ox = intercept._opp_x()
    oz = intercept._opp_z()
    to_ox = ox - sx
    to_oz = oz - sz
    olen = api.clamp(api.sqrt(to_ox * to_ox + to_oz * to_oz), 0.001, 100.0)
    best_z = 5.0
    best_req = 0.0 - 1.0
    best_dot = 2.0
    best_t = 99999.0
    for i in range(8):
        if i == 0:
            px = o * 13.0
            pz = 5.0
        if i == 1:
            px = o * 13.0
            pz = 0.0 - 5.0
        if i == 2:
            px = o * 10.0
            pz = 5.0
        if i == 3:
            px = o * 10.0
            pz = 0.0 - 5.0
        if i == 4:
            px = o * 7.0
            pz = 5.0
        if i == 5:
            px = o * 7.0
            pz = 0.0 - 5.0
        if i == 6:
            px = o * 1.0
            pz = 5.0
        if i == 7:
            px = o * 1.0
            pz = 0.0 - 5.0
        sdx = px - sx
        sdz = pz - sz
        d_self = api.sqrt(sdx * sdx + sdz * sdz)
        tf = 0.214 + 0.0257 * d_self
        cand = 0.498 + 0.0034 * d_self
        if cand < tf:
            tf = cand
        cand = 0.285 + 0.0178 * d_self
        if cand < tf:
            tf = cand
        cand = 0.517 + 0.0069 * d_self
        if cand < tf:
            tf = cand
        cand = 0.235 + 0.0160 * d_self
        if cand < tf:
            tf = cand
        odx = px - ox
        odz = pz - oz
        slack = api.sqrt(odx * odx + odz * odz) - 2.6
        if slack < 0.0:
            slack = 0.0
        req = slack / api.clamp(tf, 0.2, 10.0)
        tx = px - sx
        tz = pz - sz
        tlen = api.clamp(api.sqrt(tx * tx + tz * tz), 0.001, 100.0)
        dot = (tx * to_ox + tz * to_oz) / (tlen * olen)
        if req > best_req + 0.35:
            better = 1.0
        else:
            better = 0.0
        if better < 0.5:
            if api.abs(req - best_req) <= 0.35:
                if dot < best_dot - 0.05:
                    better = 1.0
                else:
                    if api.abs(dot - best_dot) <= 0.05:
                        if tf < best_t:
                            better = 1.0
        if better > 0.5:
            best_z = pz
            best_req = req
            best_dot = dot
            best_t = tf
    return best_z


def _scan_best_opt():
    o = 0.0 - intercept._own_sign()
    sx = intercept._self_x()
    sz = intercept._self_z()
    ox = intercept._opp_x()
    oz = intercept._opp_z()
    to_ox = ox - sx
    to_oz = oz - sz
    olen = api.clamp(api.sqrt(to_ox * to_ox + to_oz * to_oz), 0.001, 100.0)
    best_opt = 2.0
    best_req = 0.0 - 1.0
    best_dot = 2.0
    best_t = 99999.0
    for i in range(8):
        if i == 0:
            px = o * 13.0
            pz = 5.0
        if i == 1:
            px = o * 13.0
            pz = 0.0 - 5.0
        if i == 2:
            px = o * 10.0
            pz = 5.0
        if i == 3:
            px = o * 10.0
            pz = 0.0 - 5.0
        if i == 4:
            px = o * 7.0
            pz = 5.0
        if i == 5:
            px = o * 7.0
            pz = 0.0 - 5.0
        if i == 6:
            px = o * 1.0
            pz = 5.0
        if i == 7:
            px = o * 1.0
            pz = 0.0 - 5.0
        sdx = px - sx
        sdz = pz - sz
        d_self = api.sqrt(sdx * sdx + sdz * sdz)
        tf = 0.214 + 0.0257 * d_self
        opt = 0.0
        cand = 0.498 + 0.0034 * d_self
        if cand < tf:
            tf = cand
            opt = 1.0
        cand = 0.285 + 0.0178 * d_self
        if cand < tf:
            tf = cand
            opt = 2.0
        cand = 0.517 + 0.0069 * d_self
        if cand < tf:
            tf = cand
            opt = 4.0
        cand = 0.235 + 0.0160 * d_self
        if cand < tf:
            tf = cand
            opt = 6.0
        if cand < tf:
            opt = 7.0
        odx = px - ox
        odz = pz - oz
        slack = api.sqrt(odx * odx + odz * odz) - 2.6
        if slack < 0.0:
            slack = 0.0
        req = slack / api.clamp(tf, 0.2, 10.0)
        tx = px - sx
        tz = pz - sz
        tlen = api.clamp(api.sqrt(tx * tx + tz * tz), 0.001, 100.0)
        dot = (tx * to_ox + tz * to_oz) / (tlen * olen)
        if req > best_req + 0.35:
            better = 1.0
        else:
            better = 0.0
        if better < 0.5:
            if api.abs(req - best_req) <= 0.35:
                if dot < best_dot - 0.05:
                    better = 1.0
                else:
                    if api.abs(dot - best_dot) <= 0.05:
                        if tf < best_t:
                            better = 1.0
        if better > 0.5:
            best_opt = opt
            best_req = req
            best_dot = dot
            best_t = tf
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
    return _scan_best_x()


def attack_z():
    # Fatigue scatter compensation: edge aims pull toward center.
    z = _scan_best_z()
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
    return _scan_best_opt()
