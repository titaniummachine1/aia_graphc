"""Serve-aim and rally-aim helpers (compiled inline at call sites).

One float per function: tuple unpacking is not compilable, so each aim
component is its own helper. Shared subexpressions CSE into one node.
"""

import AIA_Comp_Libry.tennis.v014 as tennis

SECOND_SERVE_SHORTEN = 0.5
RALLY_Z = 11.0


def serve_aim_x(api):
    return api.split_vector(tennis.legal_serve_target(), 0)


def serve_aim_z(api, serve_number):
    target_z = api.split_vector(tennis.legal_serve_target(), 2)
    return target_z - serve_number * SECOND_SERVE_SHORTEN


def rally_aim_x(api):
    return api.split_vector(tennis.center_of_half(), 0)


def rally_aim_z(api):
    return api.split_vector(tennis.center_of_half(), 2) + RALLY_Z
