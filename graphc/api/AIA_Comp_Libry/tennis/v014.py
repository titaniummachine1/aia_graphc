"""Author API for target ('tennis', 'v0.14') — GENERATED, do not edit.

Import this in bot projects instead of raw api.* strings:
    import AIA_Comp_Libry.tennis.v014 as t
The compiler maps these to the same ops as the api.* calls.
"""
from __future__ import annotations

TARGET = ('tennis', 'v0.14')

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

def ball() -> object:
    """Sensor 'Ball' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def ball_has_bounced() -> bool:
    """Sensor 'Ball Has Bounced' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def ball_has_charged_effect() -> bool:
    """Sensor 'Ball Has Charged Effect' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def ball_in_swing_range() -> bool:
    """Sensor 'Ball In Swing Range' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def ball_incoming() -> bool:
    """Sensor 'Ball Incoming' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def ball_on_self_side() -> bool:
    """Sensor 'Ball On Self Side' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def ball_position() -> object:
    """Sensor 'Ball Position' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def ball_speed() -> float:
    """Sensor 'Ball Speed' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def ball_time_to_2nd_bounce() -> float:
    """Sensor 'Ball Time To 2nd Bounce' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def ball_time_to_ground() -> float:
    """Sensor 'Ball Time To Ground' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def ball_velocity() -> object:
    """Sensor 'Ball Velocity' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def camera() -> object:
    """Sensor 'Camera' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def camera_forward() -> object:
    """Sensor 'Camera Forward' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def camera_right() -> object:
    """Sensor 'Camera Right' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def center_of_back() -> object:
    """Sensor 'Center Of Back' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def center_of_half() -> object:
    """Sensor 'Center Of Half' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def court_depth() -> float:
    """Sensor 'Court Depth' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def court_width() -> float:
    """Sensor 'Court Width' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def current_simulation_time() -> float:
    """Sensor 'Current Simulation Time' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def delta_time() -> float:
    """Sensor 'Delta Time' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def deuce_fatigue() -> float:
    """Sensor 'Deuce Fatigue' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def estimated_opponent_shot_location() -> object:
    """Sensor 'Estimated Opponent Shot Location' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def fixed_delta_time() -> float:
    """Sensor 'Fixed Delta Time' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_ad_court_serve() -> bool:
    """Sensor 'Is Ad Court Serve' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_playable() -> bool:
    """Sensor 'Is Ball Playable' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_break_point() -> bool:
    """Sensor 'Is Break Point' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_deuce() -> bool:
    """Sensor 'Is Deuce' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_game_point() -> bool:
    """Sensor 'Is Game Point' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_home() -> bool:
    """Sensor 'Is Home' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_match_point() -> bool:
    """Sensor 'Is Match Point' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_charging() -> bool:
    """Sensor 'Is Opponent Charging' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_server_for_set() -> bool:
    """Sensor 'Is Opponent Server For Set' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_winning() -> bool:
    """Sensor 'Is Opponent Winning' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_playing() -> bool:
    """Sensor 'Is Playing' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_second_serve() -> bool:
    """Sensor 'Is Second Serve' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_self_actively_serving() -> bool:
    """Sensor 'Is Self Actively Serving' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_self_charging() -> bool:
    """Sensor 'Is Self Charging' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_self_server_for_set() -> bool:
    """Sensor 'Is Self Server For Set' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_self_winning() -> bool:
    """Sensor 'Is Self Winning' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_serve_phase() -> bool:
    """Sensor 'Is Serve Phase' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_tied() -> bool:
    """Sensor 'Is Tied' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def legal_serve_target() -> object:
    """Sensor 'Legal Serve Target' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def must_wait_for_bounce() -> bool:
    """Sensor 'Must Wait For Bounce' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def net_height() -> float:
    """Sensor 'Net Height' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent() -> object:
    """Sensor 'Opponent' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_aces() -> float:
    """Sensor 'Opponent Aces' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_average_scoring_location() -> object:
    """Sensor 'Opponent Average Scoring Location' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_charged_shots() -> float:
    """Sensor 'Opponent Charged Shots' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_double_faults() -> float:
    """Sensor 'Opponent Double Faults' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_faults() -> float:
    """Sensor 'Opponent Faults' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_fouls() -> float:
    """Sensor 'Opponent Fouls' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_outs() -> float:
    """Sensor 'Opponent Outs' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_points() -> float:
    """Sensor 'Opponent Points' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_scored_last_point() -> bool:
    """Sensor 'Opponent Scored Last Point' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_set_score() -> float:
    """Sensor 'Opponent Set Score' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_stamina_pct() -> float:
    """Sensor 'Opponent Stamina Pct' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_swing_charge_pct() -> float:
    """Sensor 'Opponent Swing Charge Pct' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def predicted_2nd_bounce() -> object:
    """Sensor 'Predicted 2nd Bounce' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def predicted_bounce() -> object:
    """Sensor 'Predicted Bounce' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def rally_fatigue() -> float:
    """Sensor 'Rally Fatigue' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def random_aim_target() -> object:
    """Sensor 'Random Aim Target' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def receive_stance() -> object:
    """Sensor 'Receive Stance' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def self() -> object:
    """Sensor 'Self' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def self_aces() -> float:
    """Sensor 'Self Aces' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def self_average_scoring_location() -> object:
    """Sensor 'Self Average Scoring Location' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def self_charged_shots() -> float:
    """Sensor 'Self Charged Shots' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def self_double_faults() -> float:
    """Sensor 'Self Double Faults' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def self_faults() -> float:
    """Sensor 'Self Faults' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def self_fouls() -> float:
    """Sensor 'Self Fouls' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def self_has_advantage() -> bool:
    """Sensor 'Self Has Advantage' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def self_outs() -> float:
    """Sensor 'Self Outs' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def self_points() -> float:
    """Sensor 'Self Points' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def self_racket_center() -> object:
    """Sensor 'Self Racket Center' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def self_scored_last_point() -> bool:
    """Sensor 'Self Scored Last Point' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def self_set_score() -> float:
    """Sensor 'Self Set Score' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def self_stamina_pct() -> float:
    """Sensor 'Self Stamina Pct' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def self_swing_charge_pct() -> float:
    """Sensor 'Self Swing Charge Pct' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def self_time_to_destination() -> float:
    """Sensor 'Self Time To Destination' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def serve_number() -> float:
    """Sensor 'Serve Number' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def serve_stance() -> object:
    """Sensor 'Serve Stance' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def shot_ball() -> float:
    """Sensor 'Shot: Ball' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def shot_curve_left() -> float:
    """Sensor 'Shot: Curve Left' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def shot_curve_right() -> float:
    """Sensor 'Shot: Curve Right' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def shot_drop() -> float:
    """Sensor 'Shot: Drop' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def shot_flat() -> float:
    """Sensor 'Shot: Flat' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def shot_last_opponent_shot() -> float:
    """Sensor 'Shot: Last Opponent Shot' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def shot_last_self_shot() -> float:
    """Sensor 'Shot: Last Self Shot' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def shot_lob() -> float:
    """Sensor 'Shot: Lob' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def shot_most_scored_opponent_shot() -> float:
    """Sensor 'Shot: Most Scored Opponent Shot' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def shot_most_scored_self_shot() -> float:
    """Sensor 'Shot: Most Scored Self Shot' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def shot_most_used_opponent_shot() -> float:
    """Sensor 'Shot: Most Used Opponent Shot' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def shot_most_used_self_shot() -> float:
    """Sensor 'Shot: Most Used Self Shot' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def shot_random() -> float:
    """Sensor 'Shot: Random' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def shot_slice() -> float:
    """Sensor 'Shot: Slice' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def shot_topspin() -> float:
    """Sensor 'Shot: Topspin' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def sim_tick() -> float:
    """Sensor 'Sim Tick' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def trick_curve_left_modifier() -> object:
    """Sensor 'Trick Curve Left Modifier' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def trick_curve_right_modifier() -> object:
    """Sensor 'Trick Curve Right Modifier' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def trick_drop_modifier() -> object:
    """Sensor 'Trick Drop Modifier' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def trick_lob_modifier() -> object:
    """Sensor 'Trick Lob Modifier' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_curve_left() -> bool:
    """Sensor 'Was Last Shot Curve Left' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_curve_right() -> bool:
    """Sensor 'Was Last Shot Curve Right' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_drop() -> bool:
    """Sensor 'Was Last Shot Drop' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_flat() -> bool:
    """Sensor 'Was Last Shot Flat' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_lob() -> bool:
    """Sensor 'Was Last Shot Lob' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_slice() -> bool:
    """Sensor 'Was Last Shot Slice' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_topspin() -> bool:
    """Sensor 'Was Last Shot Topspin' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_trick() -> bool:
    """Sensor 'Was Last Shot Trick' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def move(x: float, z: float, swing=None, shot=None, sprint=None) -> None:
    """Tennis controller. Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def move_vec(v, swing=None, shot=None, sprint=None) -> None:
    """Tennis vector controller. Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

