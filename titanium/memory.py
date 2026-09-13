"""Cross-tick state: declarations live here, writes happen in tick().

Rule reminder: a bare name the bot writes becomes a latch (must init 0);
helpers only compute next values (one float back). Import the names in
entry.py and assign them there.
"""

shots_seen = 0.0
last_side = 0.0

# Own-strike detector (Shot: Last Self Shot changes on OUR strike only;
# -1.0 means none yet). have_prev guards the all-zero init (game vars
# start at 0, but the sensor idles at -1). Blind spot, documented:
# two consecutive same-type strikes read as one (id unchanged).
prev_shot = 0.0
have_prev = 0.0
struck = 0.0


def next_shots(prev, incoming):
    if incoming > 0.5:
        return prev + 1.0
    else:
        return prev


def next_side(prev, aim_z):
    if aim_z > 0.0:
        return 1.0
    else:
        return 0.0 - 1.0
