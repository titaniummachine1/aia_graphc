"""Vec geometry demo — RLBot-style vector math, compiled to a graph.

RLBot bots lean on `Vec3` (`sub`, `.length()`, `.dist()`, normalize). The
compiler now has the same building blocks as plain `api.*` helpers, so tennis
code reads the same way — but it still compiles to a static node graph (no
packet, no sockets): every helper below is one game node.

    api.make_vector(x, y, z)   -> Vec3(x, y, z)          (ConstructVector3)
    api.vec_sub(a, b)          -> a - b                  (SubtractVector3)
    api.vec_add(a, b)          -> a + b                  (AddVector3)
    api.vec_scale(v, s)        -> v * s                  (ScaleVector3)
    api.normalize(v)           -> unit vector            (Normalize)
    api.magnitude(v)           -> length(v)              (Magnitude)
    api.distance(a, b)         -> |a - b|                (Distance)
    api.split_vector(v, i)     -> component i (0=x,1=y,2=z)

Type-checked at compile time: feeding a transform (Self/Opponent/Ball) or a
float where a vector is expected fails loudly.
"""
import AIA_Comp_Libry.tennis.v15f as t


def tick(api):
    ball = t.ball_position()
    bounce = t.predicted_bounce()

    # Unit direction from the ball to where it will land, then lead it a little.
    toward = api.normalize(api.vec_sub(bounce, ball))
    lead = api.vec_add(ball, api.vec_scale(toward, 2.0))

    # How far the ball is from our back-centre — a plain distance, like
    # `Vec3.dist` in RLBot.
    reach = api.distance(ball, t.center_of_back())
    api.plot("vec.reach", reach)

    t.move_vec(lead, t.ball_in_swing_range(), 2.0)
