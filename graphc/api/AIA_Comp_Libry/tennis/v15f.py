"""Author API for target ('tennis', 'v15f') — GENERATED, do not edit.

Simple to use (humans + LLMs): import this module, call its
functions as plain values, and pass them to move()/move_vec().
You NEVER wire nodes, ports, or connections — the compiler assigns
every value a type (float/bool/vector/transform), checks every
connection, and emits the game save. Illegal wiring (bool into
arithmetic, vector into a float slot, transform into vec_split,
float where bool is needed) fails at compile time, loudly.

Types: float = number, bool = true/false, vector = 3D point
(split with api.vec_split or feed move_vec), transform = placed
object (opaque: Self/Opponent/Ball — pick a vector3 sensor instead).

Assumed node-identical to v0.14 until measured.

Import this in bot projects instead of raw api.* strings:
    import AIA_Comp_Libry.tennis.v15f as t
The compiler maps these to the same ops as the api.* calls.
"""
from __future__ import annotations

TARGET = ('tennis', 'v15f')

class Vector3:
    """Opaque 3D point: split via api.vec_split(v, 0/1/2) or feed
    t.move_vec(v). Never arithmetic directly."""

class Transform:
    """Opaque placed object (Self/Opponent/Ball): cannot split or
    do math on it; use a vector3 sensor instead."""

_SENSORS = {
    'ball': ('transform', 'Ball'),
    'ball_has_bounced': ('bool', 'Ball Has Bounced'),
    'ball_has_charged_effect': ('bool', 'Ball Has Charged Effect'),
    'ball_in_swing_range': ('bool', 'Ball In Swing Range'),
    'ball_incoming': ('bool', 'Ball Incoming'),
    'ball_on_self_side': ('bool', 'Ball On Self Side'),
    'ball_position': ('vector3', 'Ball Position'),
    'ball_speed': ('float', 'Ball Speed'),
    'ball_time_to_2nd_bounce': ('float', 'Ball Time To 2nd Bounce'),
    'ball_time_to_ground': ('float', 'Ball Time To Ground'),
    'ball_velocity': ('vector3', 'Ball Velocity'),
    'camera': ('transform', 'Camera'),
    'camera_forward': ('vector3', 'Camera Forward'),
    'camera_right': ('vector3', 'Camera Right'),
    'center_of_back': ('vector3', 'Center Of Back'),
    'center_of_half': ('vector3', 'Center Of Half'),
    'court_depth': ('float', 'Court Depth'),
    'court_width': ('float', 'Court Width'),
    'current_simulation_time': ('float', 'Current Simulation Time'),
    'delta_time': ('float', 'Delta Time'),
    'deuce_fatigue': ('float', 'Deuce Fatigue'),
    'estimated_opponent_shot_location': ('vector3', 'Estimated Opponent Shot Location'),
    'fixed_delta_time': ('float', 'Fixed Delta Time'),
    'is_ad_court_serve': ('bool', 'Is Ad Court Serve'),
    'is_ball_playable': ('bool', 'Is Ball Playable'),
    'is_break_point': ('bool', 'Is Break Point'),
    'is_deuce': ('bool', 'Is Deuce'),
    'is_game_point': ('bool', 'Is Game Point'),
    'is_home': ('bool', 'Is Home'),
    'is_match_point': ('bool', 'Is Match Point'),
    'is_opponent_charging': ('bool', 'Is Opponent Charging'),
    'is_opponent_server_for_set': ('bool', 'Is Opponent Server For Set'),
    'is_opponent_winning': ('bool', 'Is Opponent Winning'),
    'is_playing': ('bool', 'Is Playing'),
    'is_second_serve': ('bool', 'Is Second Serve'),
    'is_self_actively_serving': ('bool', 'Is Self Actively Serving'),
    'is_self_charging': ('bool', 'Is Self Charging'),
    'is_self_server_for_set': ('bool', 'Is Self Server For Set'),
    'is_self_winning': ('bool', 'Is Self Winning'),
    'is_serve_phase': ('bool', 'Is Serve Phase'),
    'is_tied': ('bool', 'Is Tied'),
    'legal_serve_target': ('vector3', 'Legal Serve Target'),
    'must_wait_for_bounce': ('bool', 'Must Wait For Bounce'),
    'net_height': ('float', 'Net Height'),
    'opponent': ('transform', 'Opponent'),
    'opponent_aces': ('float', 'Opponent Aces'),
    'opponent_average_scoring_location': ('vector3', 'Opponent Average Scoring Location'),
    'opponent_charged_shots': ('float', 'Opponent Charged Shots'),
    'opponent_double_faults': ('float', 'Opponent Double Faults'),
    'opponent_faults': ('float', 'Opponent Faults'),
    'opponent_fouls': ('float', 'Opponent Fouls'),
    'opponent_outs': ('float', 'Opponent Outs'),
    'opponent_points': ('float', 'Opponent Points'),
    'opponent_scored_last_point': ('bool', 'Opponent Scored Last Point'),
    'opponent_set_score': ('float', 'Opponent Set Score'),
    'opponent_stamina_pct': ('float', 'Opponent Stamina Pct'),
    'opponent_swing_charge_pct': ('float', 'Opponent Swing Charge Pct'),
    'predicted_2nd_bounce': ('vector3', 'Predicted 2nd Bounce'),
    'predicted_bounce': ('vector3', 'Predicted Bounce'),
    'rally_fatigue': ('float', 'Rally Fatigue'),
    'random_aim_target': ('vector3', 'Random Aim Target'),
    'receive_stance': ('vector3', 'Receive Stance'),
    'self': ('transform', 'Self'),
    'self_aces': ('float', 'Self Aces'),
    'self_average_scoring_location': ('vector3', 'Self Average Scoring Location'),
    'self_charged_shots': ('float', 'Self Charged Shots'),
    'self_double_faults': ('float', 'Self Double Faults'),
    'self_faults': ('float', 'Self Faults'),
    'self_fouls': ('float', 'Self Fouls'),
    'self_has_advantage': ('bool', 'Self Has Advantage'),
    'self_outs': ('float', 'Self Outs'),
    'self_points': ('float', 'Self Points'),
    'self_racket_center': ('transform', 'Self Racket Center'),
    'self_scored_last_point': ('bool', 'Self Scored Last Point'),
    'self_set_score': ('float', 'Self Set Score'),
    'self_stamina_pct': ('float', 'Self Stamina Pct'),
    'self_swing_charge_pct': ('float', 'Self Swing Charge Pct'),
    'self_time_to_destination': ('float', 'Self Time To Destination'),
    'serve_number': ('float', 'Serve Number'),
    'serve_stance': ('vector3', 'Serve Stance'),
    'shot_ball': ('float', 'Shot: Ball'),
    'shot_curve_left': ('float', 'Shot: Curve Left'),
    'shot_curve_right': ('float', 'Shot: Curve Right'),
    'shot_drop': ('float', 'Shot: Drop'),
    'shot_flat': ('float', 'Shot: Flat'),
    'shot_last_opponent_shot': ('float', 'Shot: Last Opponent Shot'),
    'shot_last_self_shot': ('float', 'Shot: Last Self Shot'),
    'shot_lob': ('float', 'Shot: Lob'),
    'shot_most_scored_opponent_shot': ('float', 'Shot: Most Scored Opponent Shot'),
    'shot_most_scored_self_shot': ('float', 'Shot: Most Scored Self Shot'),
    'shot_most_used_opponent_shot': ('float', 'Shot: Most Used Opponent Shot'),
    'shot_most_used_self_shot': ('float', 'Shot: Most Used Self Shot'),
    'shot_random': ('float', 'Shot: Random'),
    'shot_slice': ('float', 'Shot: Slice'),
    'shot_topspin': ('float', 'Shot: Topspin'),
    'sim_tick': ('float', 'Sim Tick'),
    'trick_curve_left_modifier': ('vector3', 'Trick Curve Left Modifier'),
    'trick_curve_right_modifier': ('vector3', 'Trick Curve Right Modifier'),
    'trick_drop_modifier': ('vector3', 'Trick Drop Modifier'),
    'trick_lob_modifier': ('vector3', 'Trick Lob Modifier'),
    'was_last_shot_curve_left': ('bool', 'Was Last Shot Curve Left'),
    'was_last_shot_curve_right': ('bool', 'Was Last Shot Curve Right'),
    'was_last_shot_drop': ('bool', 'Was Last Shot Drop'),
    'was_last_shot_flat': ('bool', 'Was Last Shot Flat'),
    'was_last_shot_lob': ('bool', 'Was Last Shot Lob'),
    'was_last_shot_slice': ('bool', 'Was Last Shot Slice'),
    'was_last_shot_topspin': ('bool', 'Was Last Shot Topspin'),
    'was_last_shot_trick': ('bool', 'Was Last Shot Trick'),
}

__all__ = ['ball', 'ball_has_bounced', 'ball_has_charged_effect', 'ball_in_swing_range', 'ball_incoming', 'ball_on_self_side', 'ball_position', 'ball_speed', 'ball_time_to_2nd_bounce', 'ball_time_to_ground', 'ball_velocity', 'camera', 'camera_forward', 'camera_right', 'center_of_back', 'center_of_half', 'court_depth', 'court_width', 'current_simulation_time', 'delta_time', 'deuce_fatigue', 'estimated_opponent_shot_location', 'fixed_delta_time', 'is_ad_court_serve', 'is_ball_playable', 'is_break_point', 'is_deuce', 'is_game_point', 'is_home', 'is_match_point', 'is_opponent_charging', 'is_opponent_server_for_set', 'is_opponent_winning', 'is_playing', 'is_second_serve', 'is_self_actively_serving', 'is_self_charging', 'is_self_server_for_set', 'is_self_winning', 'is_serve_phase', 'is_tied', 'legal_serve_target', 'must_wait_for_bounce', 'net_height', 'opponent', 'opponent_aces', 'opponent_average_scoring_location', 'opponent_charged_shots', 'opponent_double_faults', 'opponent_faults', 'opponent_fouls', 'opponent_outs', 'opponent_points', 'opponent_scored_last_point', 'opponent_set_score', 'opponent_stamina_pct', 'opponent_swing_charge_pct', 'predicted_2nd_bounce', 'predicted_bounce', 'rally_fatigue', 'random_aim_target', 'receive_stance', 'self', 'self_aces', 'self_average_scoring_location', 'self_charged_shots', 'self_double_faults', 'self_faults', 'self_fouls', 'self_has_advantage', 'self_outs', 'self_points', 'self_racket_center', 'self_scored_last_point', 'self_set_score', 'self_stamina_pct', 'self_swing_charge_pct', 'self_time_to_destination', 'serve_number', 'serve_stance', 'shot_ball', 'shot_curve_left', 'shot_curve_right', 'shot_drop', 'shot_flat', 'shot_last_opponent_shot', 'shot_last_self_shot', 'shot_lob', 'shot_most_scored_opponent_shot', 'shot_most_scored_self_shot', 'shot_most_used_opponent_shot', 'shot_most_used_self_shot', 'shot_random', 'shot_slice', 'shot_topspin', 'sim_tick', 'trick_curve_left_modifier', 'trick_curve_right_modifier', 'trick_drop_modifier', 'trick_lob_modifier', 'was_last_shot_curve_left', 'was_last_shot_curve_right', 'was_last_shot_drop', 'was_last_shot_flat', 'was_last_shot_lob', 'was_last_shot_slice', 'was_last_shot_topspin', 'was_last_shot_trick', 'move', 'move_vec']

def ball() -> Transform:
    """Ball position.

    Returns: transform (game node TennisGetTransform).
    Game label: 'Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def ball_has_bounced() -> bool:
    """True once the ball bounced since the last strike.

    Returns: bool (game node TennisGetBool).
    Game label: 'Ball Has Bounced'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def ball_has_charged_effect() -> bool:
    """True when a charged-shot effect rides the ball.

    Returns: bool (game node TennisGetBool).
    Game label: 'Ball Has Charged Effect'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def ball_in_swing_range() -> bool:
    """True when the ball is within strike radius.

    Returns: bool (game node TennisGetBool).
    Game label: 'Ball In Swing Range'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def ball_incoming() -> bool:
    """True only while the opponent's shot travels un-bounced toward you; goes false at the first bounce.

    Returns: bool (game node TennisGetBool).
    Game label: 'Ball Incoming'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def ball_on_self_side() -> bool:
    """True when the ball is over your half.

    Returns: bool (game node TennisGetBool).
    Game label: 'Ball On Self Side'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def ball_position() -> Vector3:
    """Ball court position (x, z).

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Ball Position'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def ball_speed() -> float:
    """Current ball speed.

    Returns: float (game node TennisGetFloat).
    Game label: 'Ball Speed'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def ball_time_to_2nd_bounce() -> float:
    """Predicted seconds until the second bounce.

    Returns: float (game node TennisGetFloat).
    Game label: 'Ball Time To 2nd Bounce'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def ball_time_to_ground() -> float:
    """Predicted seconds until the ball lands.

    Returns: float (game node TennisGetFloat).
    Game label: 'Ball Time To Ground'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def ball_velocity() -> Vector3:
    """Ball velocity vector.

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Ball Velocity'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def camera() -> Transform:
    """Camera position.

    Returns: transform (game node TennisGetTransform).
    Game label: 'Camera'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def camera_forward() -> Vector3:
    """Camera facing direction.

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Camera Forward'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def camera_right() -> Vector3:
    """Camera right direction.

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Camera Right'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def center_of_back() -> Vector3:
    """Middle of your back court.

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Center Of Back'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def center_of_half() -> Vector3:
    """Middle of your half (safe rally target).

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Center Of Half'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def court_depth() -> float:
    """Playable court length (baseline to baseline).

    Returns: float (game node TennisGetFloat).
    Game label: 'Court Depth'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def court_width() -> float:
    """Playable court width (singles).

    Returns: float (game node TennisGetFloat).
    Game label: 'Court Width'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def current_simulation_time() -> float:
    """Match clock in seconds.

    Returns: float (game node TennisGetFloat).
    Game label: 'Current Simulation Time'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def delta_time() -> float:
    """Frame delta in seconds.

    Returns: float (game node TennisGetFloat).
    Game label: 'Delta Time'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def deuce_fatigue() -> float:
    """Fatigue factor active at deuce.

    Returns: float (game node TennisGetFloat).
    Game label: 'Deuce Fatigue'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def estimated_opponent_shot_location() -> Vector3:
    """Game's guess at their landing spot. STALE outside the post-own-hit receive window (compiler warns) — prefer predicted_bounce for walking.

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Estimated Opponent Shot Location'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def fixed_delta_time() -> float:
    """Physics tick delta in seconds.

    Returns: float (game node TennisGetFloat).
    Game label: 'Fixed Delta Time'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_ad_court_serve() -> bool:
    """True when serving from the ad (left) side.

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Ad Court Serve'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_playable() -> bool:
    """True when the ball is live and can be struck.

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Ball Playable'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_break_point() -> bool:
    """True when the receiver can break serve next point.

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Break Point'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_deuce() -> bool:
    """True at deuce (3+ points each, no advantage).

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Deuce'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_game_point() -> bool:
    """True when the next point wins the game for either side.

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Game Point'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_home() -> bool:
    """True when this brain plays the home side.

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Home'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_match_point() -> bool:
    """True when the next point wins the match for either side.

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Match Point'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_charging() -> bool:
    """True while the opponent holds swing.

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Opponent Charging'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_server_for_set() -> bool:
    """True when the opponent serves this set.

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Opponent Server For Set'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_winning() -> bool:
    """True when the opponent leads the score.

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Opponent Winning'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_playing() -> bool:
    """True while the match simulation runs (not menus).

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Playing'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_second_serve() -> bool:
    """True when the upcoming serve is the second (after a fault).

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Second Serve'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_self_actively_serving() -> bool:
    """True when self is the current server.

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Self Actively Serving'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_self_charging() -> bool:
    """True while self holds swing (charge 0.17-1.0).

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Self Charging'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_self_server_for_set() -> bool:
    """True when self serves this set.

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Self Server For Set'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_self_winning() -> bool:
    """True when self leads the score.

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Self Winning'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_serve_phase() -> bool:
    """True while the ball is dead and the server prepares.

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Serve Phase'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_tied() -> bool:
    """True when the score is level.

    Returns: bool (game node TennisGetBool).
    Game label: 'Is Tied'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def legal_serve_target() -> Vector3:
    """Center of the legal diagonal serve box.

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Legal Serve Target'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def must_wait_for_bounce() -> bool:
    """True when the receiver must let the serve bounce first.

    Returns: bool (game node TennisGetBool).
    Game label: 'Must Wait For Bounce'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def net_height() -> float:
    """Net tape height.

    Returns: float (game node TennisGetFloat).
    Game label: 'Net Height'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent() -> Transform:
    """Opponent position.

    Returns: transform (game node TennisGetTransform).
    Game label: 'Opponent'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_aces() -> float:
    """Opponent ace count.

    Returns: float (game node TennisGetFloat).
    Game label: 'Opponent Aces'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_average_scoring_location() -> Vector3:
    """Where their winners usually land.

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Opponent Average Scoring Location'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_charged_shots() -> float:
    """Opponent fully-charged shot count.

    Returns: float (game node TennisGetFloat).
    Game label: 'Opponent Charged Shots'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_double_faults() -> float:
    """Opponent double-fault count.

    Returns: float (game node TennisGetFloat).
    Game label: 'Opponent Double Faults'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_faults() -> float:
    """Opponent serve-fault count.

    Returns: float (game node TennisGetFloat).
    Game label: 'Opponent Faults'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_fouls() -> float:
    """Opponent foul count.

    Returns: float (game node TennisGetFloat).
    Game label: 'Opponent Fouls'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_outs() -> float:
    """Opponent out count.

    Returns: float (game node TennisGetFloat).
    Game label: 'Opponent Outs'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_points() -> float:
    """Opponent points in the current game.

    Returns: float (game node TennisGetFloat).
    Game label: 'Opponent Points'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_scored_last_point() -> bool:
    """True when the opponent won the previous point.

    Returns: bool (game node TennisGetBool).
    Game label: 'Opponent Scored Last Point'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_set_score() -> float:
    """Sets the opponent has won.

    Returns: float (game node TennisGetFloat).
    Game label: 'Opponent Set Score'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_stamina_pct() -> float:
    """Opponent stamina 0-1.

    Returns: float (game node TennisGetFloat).
    Game label: 'Opponent Stamina Pct'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_swing_charge_pct() -> float:
    """Opponent swing charge 0-1.

    Returns: float (game node TennisGetFloat).
    Game label: 'Opponent Swing Charge Pct'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def predicted_2nd_bounce() -> Vector3:
    """Where the ball will land second.

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Predicted 2nd Bounce'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def predicted_bounce() -> Vector3:
    """Where the ball will land first.

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Predicted Bounce'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def rally_fatigue() -> float:
    """Fatigue factor growing with rally length.

    Returns: float (game node TennisGetFloat).
    Game label: 'Rally Fatigue'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def random_aim_target() -> Vector3:
    """A game-picked aim point.

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Random Aim Target'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def receive_stance() -> Vector3:
    """Where the receiver should wait.

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Receive Stance'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def self() -> Transform:
    """Your position.

    Returns: transform (game node TennisGetTransform).
    Game label: 'Self'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def self_aces() -> float:
    """Your ace count.

    Returns: float (game node TennisGetFloat).
    Game label: 'Self Aces'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def self_average_scoring_location() -> Vector3:
    """Where your winners usually land.

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Self Average Scoring Location'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def self_charged_shots() -> float:
    """Your fully-charged shot count.

    Returns: float (game node TennisGetFloat).
    Game label: 'Self Charged Shots'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def self_double_faults() -> float:
    """Your double-fault count.

    Returns: float (game node TennisGetFloat).
    Game label: 'Self Double Faults'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def self_faults() -> float:
    """Your serve-fault count.

    Returns: float (game node TennisGetFloat).
    Game label: 'Self Faults'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def self_fouls() -> float:
    """Your foul count.

    Returns: float (game node TennisGetFloat).
    Game label: 'Self Fouls'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def self_has_advantage() -> bool:
    """True when you hold advantage at deuce.

    Returns: bool (game node TennisGetBool).
    Game label: 'Self Has Advantage'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def self_outs() -> float:
    """Your out count.

    Returns: float (game node TennisGetFloat).
    Game label: 'Self Outs'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def self_points() -> float:
    """Your points in the current game.

    Returns: float (game node TennisGetFloat).
    Game label: 'Self Points'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def self_racket_center() -> Transform:
    """Your racket head position (strike point).

    Returns: transform (game node TennisGetTransform).
    Game label: 'Self Racket Center'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def self_scored_last_point() -> bool:
    """True when you won the previous point.

    Returns: bool (game node TennisGetBool).
    Game label: 'Self Scored Last Point'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def self_set_score() -> float:
    """Sets (matches) you have won.

    Returns: float (game node TennisGetFloat).
    Game label: 'Self Set Score'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def self_stamina_pct() -> float:
    """Your stamina 0-1 (sprint drains it).

    Returns: float (game node TennisGetFloat).
    Game label: 'Self Stamina Pct'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def self_swing_charge_pct() -> float:
    """Your swing charge 0-1 (hold builds it).

    Returns: float (game node TennisGetFloat).
    Game label: 'Self Swing Charge Pct'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def self_time_to_destination() -> float:
    """Seconds for you to reach your move target.

    Returns: float (game node TennisGetFloat).
    Game label: 'Self Time To Destination'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def serve_number() -> float:
    """1 for first serve, 2 for second serve.

    Returns: float (game node TennisGetFloat).
    Game label: 'Serve Number'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def serve_stance() -> Vector3:
    """Where the server must stand (inside the serve area).

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Serve Stance'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def shot_ball() -> float:
    """Id of the shot currently in flight.

    Returns: float (game node TennisGetFloat).
    Game label: 'Shot: Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def shot_curve_left() -> float:
    """Constant id of the curve-left shot.

    Returns: float (game node TennisGetFloat).
    Game label: 'Shot: Curve Left'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def shot_curve_right() -> float:
    """Constant id of the curve-right shot.

    Returns: float (game node TennisGetFloat).
    Game label: 'Shot: Curve Right'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def shot_drop() -> float:
    """Constant id of the drop shot.

    Returns: float (game node TennisGetFloat).
    Game label: 'Shot: Drop'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def shot_flat() -> float:
    """Constant id of the flat shot.

    Returns: float (game node TennisGetFloat).
    Game label: 'Shot: Flat'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def shot_last_opponent_shot() -> float:
    """Id of the opponent's most recent shot.

    Returns: float (game node TennisGetFloat).
    Game label: 'Shot: Last Opponent Shot'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def shot_last_self_shot() -> float:
    """Id of your most recent shot.

    Returns: float (game node TennisGetFloat).
    Game label: 'Shot: Last Self Shot'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def shot_lob() -> float:
    """Constant id of the lob shot.

    Returns: float (game node TennisGetFloat).
    Game label: 'Shot: Lob'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def shot_most_scored_opponent_shot() -> float:
    """Id of the shot the opponent scored most with.

    Returns: float (game node TennisGetFloat).
    Game label: 'Shot: Most Scored Opponent Shot'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def shot_most_scored_self_shot() -> float:
    """Id of the shot you scored most with.

    Returns: float (game node TennisGetFloat).
    Game label: 'Shot: Most Scored Self Shot'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def shot_most_used_opponent_shot() -> float:
    """Id of the opponent's most frequent shot.

    Returns: float (game node TennisGetFloat).
    Game label: 'Shot: Most Used Opponent Shot'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def shot_most_used_self_shot() -> float:
    """Id of your most frequent shot.

    Returns: float (game node TennisGetFloat).
    Game label: 'Shot: Most Used Self Shot'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def shot_random() -> float:
    """Constant id asking the game to pick a shot.

    Returns: float (game node TennisGetFloat).
    Game label: 'Shot: Random'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def shot_slice() -> float:
    """Constant id of the slice shot.

    Returns: float (game node TennisGetFloat).
    Game label: 'Shot: Slice'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def shot_topspin() -> float:
    """Constant id of the topspin shot (feed to move shot).

    Returns: float (game node TennisGetFloat).
    Game label: 'Shot: Topspin'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def sim_tick() -> float:
    """Current simulation tick.

    Returns: float (game node TennisGetFloat).
    Game label: 'Sim Tick'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def trick_curve_left_modifier() -> Vector3:
    """Aim offset curving a trick shot left.

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Trick Curve Left Modifier'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def trick_curve_right_modifier() -> Vector3:
    """Aim offset curving a trick shot right.

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Trick Curve Right Modifier'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def trick_drop_modifier() -> Vector3:
    """Aim offset making a trick shot drop.

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Trick Drop Modifier'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def trick_lob_modifier() -> Vector3:
    """Aim offset making a trick shot lob.

    Returns: vector3 (game node TennisGetVector3).
    Game label: 'Trick Lob Modifier'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_curve_left() -> bool:
    """True when the last shot curved left.

    Returns: bool (game node TennisGetBool).
    Game label: 'Was Last Shot Curve Left'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_curve_right() -> bool:
    """True when the last shot curved right.

    Returns: bool (game node TennisGetBool).
    Game label: 'Was Last Shot Curve Right'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_drop() -> bool:
    """True when the last struck shot was a drop shot.

    Returns: bool (game node TennisGetBool).
    Game label: 'Was Last Shot Drop'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_flat() -> bool:
    """True when the last struck shot was flat.

    Returns: bool (game node TennisGetBool).
    Game label: 'Was Last Shot Flat'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_lob() -> bool:
    """True when the last struck shot was a lob.

    Returns: bool (game node TennisGetBool).
    Game label: 'Was Last Shot Lob'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_slice() -> bool:
    """True when the last struck shot was slice.

    Returns: bool (game node TennisGetBool).
    Game label: 'Was Last Shot Slice'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_topspin() -> bool:
    """True when the last struck shot was topspin.

    Returns: bool (game node TennisGetBool).
    Game label: 'Was Last Shot Topspin'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_trick() -> bool:
    """True when the last shot was a trick shot.

    Returns: bool (game node TennisGetBool).
    Game label: 'Was Last Shot Trick'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def move(x: float, z: float, swing: bool | None = None, shot: float | None = None, sprint: bool | None = None) -> None:
    """Drive to court position (x, z) and strike: the request runs through the game's TennisAutoAim + TennisAutoMove assist before the controller. Swing: hold (truthy) builds charge, RELEASE strikes — holding forever never hits, gate it on charge (if chg >= 0.7: swing = False else: swing = in_range). Shot is a Shot:* id, sprint truthy sprints. Exactly one controller call per tick.

    Args: x (float court x), z (float court z), swing (bool|None charge/hit), shot (float|None Shot:* id), sprint (bool|None). Exactly one controller call per tick.
    Connections are automatic; type mismatches fail loudly."""
    raise RuntimeError('author stub: compile with graphc')

def move_vec(v: Vector3, swing: bool | None = None, shot: float | None = None, sprint: bool | None = None) -> None:
    """Same as move but driven by a vector (vec_make or a vector sensor).

    Args: v (vector from vec_make or a vector3 sensor).
    Connections are automatic; transform input fails loudly."""
    raise RuntimeError('author stub: compile with graphc')

def aim(x: float, z: float) -> None:
    """Strike-aim request for the next move call (autoswitch): the walk destination stays on the move wire — the game switches strike aim without touching how you walk. Pair with exactly one move per tick; aim without move fails loudly.

    Args: x (float court x), z (float court z).
    Connections are automatic; type mismatches fail loudly."""
    raise RuntimeError('author stub: compile with graphc')

def auto_swing(shot: float, mode: str | None = None) -> bool:
    """Game swing node: hold builds charge, release strikes (mode: Normal Only | Prefer Charge | Random, default Prefer Charge). Returns the swing bool — wire it into move's swing.

    Args: shot (float Shot:* id), mode (str|None swing mode).
    Connections are automatic; type mismatches fail loudly."""
    raise RuntimeError('author stub: compile with graphc')

