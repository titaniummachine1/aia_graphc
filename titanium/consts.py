"""Shared tuning numbers (module constants, inlined — never written)."""

# Court geometry, measured (sim court.rs, game-pinned 28 x 12).
COURT_HALF_LEN = 14.0
COURT_HALF_WID = 6.0

# Diagonal service box center on the opponent half (box: x 0..7,
# z half 0..6). Serve-area sensor is stubbed in game — hardcoded.
BOX_X = 3.5
BOX_Z = 3.0

# Rally aims stay inside these (pass-through gate honors ~3cm).
SAFE_X = 13.0
SAFE_Z = 5.0
DEEP_X = 11.0
CORNER_Z = 4.5

# Euler estimator horizon (literal trips x dt = seconds of flight).
DT = 0.016
GRAV = 9.81

# Second serve: aim box center (no corner risk).
SECOND_SERVE_Z = 3.0
