"""Aiming helpers for the cross-court project (inlined at each call site)."""
import AIA_Comp_Libry.tennis.v014 as tennis

DEEP_Z = 11.0


def home_walk_x(api):
    return api.split_vector(tennis.center_of_back(), 0)


def home_walk_z(api):
    return api.split_vector(tennis.center_of_back(), 2)


def deep_x(api):
    return 0.0 - api.split_vector(tennis.center_of_back(), 0)


def cross_z(api):
    return DEEP_Z
