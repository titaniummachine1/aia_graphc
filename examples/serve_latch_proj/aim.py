"""Serve-aim and rally-aim helpers (compiled inline at call sites).

One float per function: tuple unpacking is not compilable, so each aim
component is its own helper. Shared subexpressions CSE into one node.
"""

import AIA_Comp_Libry.tennis.v014 as t

SECOND_SERVE_SHORTEN = 0.5
RALLY_Z = 11.0


def serve_aim_x(api):
    return api.vec_split(t.legal_serve_target(), 0)


def serve_aim_z(api, serve_no):
    tz = api.vec_split(t.legal_serve_target(), 2)
    return tz - serve_no * SECOND_SERVE_SHORTEN


def rally_aim_x(api):
    return api.vec_split(t.center_of_half(), 0)


def rally_aim_z(api):
    return api.vec_split(t.center_of_half(), 2) + RALLY_Z
