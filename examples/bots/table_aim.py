"""Table aim — a range-bucketed aim table in plain Python, no api.*.

`aimz` is a frozen constant table (never written): static reads inline to
zero nodes, the dynamic lookup compiles to the backend's own select-chain.
`hist` is a module list the bot writes, so it becomes cross-tick RAM:
last four swing decisions, readable with static or dynamic indices.
"""
import AIA_Comp_Libry.tennis.v014 as tennis

hist = [0.0, 0.0, 0.0, 0.0]


def tick(api):
    aimz = [0.0 - 4.0, 0.0 - 2.0, 2.0, 4.0]

    base = tennis.center_of_back()
    bounce = tennis.predicted_bounce()
    d = api.distance(bounce, base)

    bucket = 0.0
    if d > 5.0:
        bucket = 1.0
    if d > 10.0:
        bucket = 2.0
    if d > 15.0:
        bucket = 3.0

    aim_z = aimz[bucket]
    deep_x = 0.0 - api.split_vector(base, 0)

    swing = tennis.auto_swing(2.0)
    if swing:
        seen = 1.0
    else:
        seen = 0.0
    hist[0] = hist[1]
    hist[1] = hist[2]
    hist[2] = hist[3]
    hist[3] = seen

    api.plot("T.aim_z", aim_z)
    api.plot("T.seen_now", hist[3])
    tennis.aim(deep_x, aim_z)

    walk_x = api.split_vector(base, 0)
    walk_z = api.split_vector(base, 2)
    if tennis.ball_incoming():
        walk_x = api.split_vector(bounce, 0)
        walk_z = api.split_vector(bounce, 2)
    tennis.move(walk_x, walk_z, swing, 2.0)
