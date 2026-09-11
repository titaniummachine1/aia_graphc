"""Author API for target ('tennis', 'v15f') — GENERATED, do not edit.

Assumed node-identical to v0.14 until measured.

Import this in bot projects instead of raw api.* strings:
    import AIA_Comp_Libry.tennis.v15f as t
The compiler maps these to the same ops as the api.* calls.
"""
from __future__ import annotations

TARGET = ('tennis', 'v15f')

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

def ball() -> object:
    """Ball position. Game label: 'Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def ball_has_bounced() -> bool:
    """True once the ball bounced since the last strike. Game label: 'Ball Has Bounced'."""
    raise RuntimeError('author stub: compile with graphc')

def ball_has_charged_effect() -> bool:
    """True when a charged-shot effect rides the ball. Game label: 'Ball Has Charged Effect'."""
    raise RuntimeError('author stub: compile with graphc')

def ball_in_swing_range() -> bool:
    """True when the ball is within strike radius. Game label: 'Ball In Swing Range'."""
    raise RuntimeError('author stub: compile with graphc')

def ball_incoming() -> bool:
    """True only while the opponent's shot travels un-bounced toward you; goes false at the first bounce. Game label: 'Ball Incoming'."""
    raise RuntimeError('author stub: compile with graphc')

def ball_on_self_side() -> bool:
    """True when the ball is over your half. Game label: 'Ball On Self Side'."""
    raise RuntimeError('author stub: compile with graphc')

def ball_position() -> object:
    """Ball court position (x, z). Game label: 'Ball Position'."""
    raise RuntimeError('author stub: compile with graphc')

def ball_speed() -> float:
    """Current ball speed. Game label: 'Ball Speed'."""
    raise RuntimeError('author stub: compile with graphc')

def ball_time_to_2nd_bounce() -> float:
    """Predicted seconds until the second bounce. Game label: 'Ball Time To 2nd Bounce'."""
    raise RuntimeError('author stub: compile with graphc')

def ball_time_to_ground() -> float:
    """Predicted seconds until the ball lands. Game label: 'Ball Time To Ground'."""
    raise RuntimeError('author stub: compile with graphc')

def ball_velocity() -> object:
    """Ball velocity vector. Game label: 'Ball Velocity'."""
    raise RuntimeError('author stub: compile with graphc')

def camera() -> object:
    """Camera position. Game label: 'Camera'."""
    raise RuntimeError('author stub: compile with graphc')

def camera_forward() -> object:
    """Camera facing direction. Game label: 'Camera Forward'."""
    raise RuntimeError('author stub: compile with graphc')

def camera_right() -> object:
    """Camera right direction. Game label: 'Camera Right'."""
    raise RuntimeError('author stub: compile with graphc')

def center_of_back() -> object:
    """Middle of your back court. Game label: 'Center Of Back'."""
    raise RuntimeError('author stub: compile with graphc')

def center_of_half() -> object:
    """Middle of your half (safe rally target). Game label: 'Center Of Half'."""
    raise RuntimeError('author stub: compile with graphc')

def court_depth() -> float:
    """Playable court length (baseline to baseline). Game label: 'Court Depth'."""
    raise RuntimeError('author stub: compile with graphc')

def court_width() -> float:
    """Playable court width (singles). Game label: 'Court Width'."""
    raise RuntimeError('author stub: compile with graphc')

def current_simulation_time() -> float:
    """Match clock in seconds. Game label: 'Current Simulation Time'."""
    raise RuntimeError('author stub: compile with graphc')

def delta_time() -> float:
    """Frame delta in seconds. Game label: 'Delta Time'."""
    raise RuntimeError('author stub: compile with graphc')

def deuce_fatigue() -> float:
    """Fatigue factor active at deuce. Game label: 'Deuce Fatigue'."""
    raise RuntimeError('author stub: compile with graphc')

def estimated_opponent_shot_location() -> object:
    """Game's guess at their landing spot. Game label: 'Estimated Opponent Shot Location'."""
    raise RuntimeError('author stub: compile with graphc')

def fixed_delta_time() -> float:
    """Physics tick delta in seconds. Game label: 'Fixed Delta Time'."""
    raise RuntimeError('author stub: compile with graphc')

def is_ad_court_serve() -> bool:
    """True when serving from the ad (left) side. Game label: 'Is Ad Court Serve'."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_playable() -> bool:
    """True when the ball is live and can be struck. Game label: 'Is Ball Playable'."""
    raise RuntimeError('author stub: compile with graphc')

def is_break_point() -> bool:
    """True when the receiver can break serve next point. Game label: 'Is Break Point'."""
    raise RuntimeError('author stub: compile with graphc')

def is_deuce() -> bool:
    """True at deuce (3+ points each, no advantage). Game label: 'Is Deuce'."""
    raise RuntimeError('author stub: compile with graphc')

def is_game_point() -> bool:
    """True when the next point wins the game for either side. Game label: 'Is Game Point'."""
    raise RuntimeError('author stub: compile with graphc')

def is_home() -> bool:
    """True when this brain plays the home side. Game label: 'Is Home'."""
    raise RuntimeError('author stub: compile with graphc')

def is_match_point() -> bool:
    """True when the next point wins the match for either side. Game label: 'Is Match Point'."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_charging() -> bool:
    """True while the opponent holds swing. Game label: 'Is Opponent Charging'."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_server_for_set() -> bool:
    """True when the opponent serves this set. Game label: 'Is Opponent Server For Set'."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_winning() -> bool:
    """True when the opponent leads the score. Game label: 'Is Opponent Winning'."""
    raise RuntimeError('author stub: compile with graphc')

def is_playing() -> bool:
    """True while the match simulation runs (not menus). Game label: 'Is Playing'."""
    raise RuntimeError('author stub: compile with graphc')

def is_second_serve() -> bool:
    """True when the upcoming serve is the second (after a fault). Game label: 'Is Second Serve'."""
    raise RuntimeError('author stub: compile with graphc')

def is_self_actively_serving() -> bool:
    """True when self is the current server. Game label: 'Is Self Actively Serving'."""
    raise RuntimeError('author stub: compile with graphc')

def is_self_charging() -> bool:
    """True while self holds swing (charge 0.17-1.0). Game label: 'Is Self Charging'."""
    raise RuntimeError('author stub: compile with graphc')

def is_self_server_for_set() -> bool:
    """True when self serves this set. Game label: 'Is Self Server For Set'."""
    raise RuntimeError('author stub: compile with graphc')

def is_self_winning() -> bool:
    """True when self leads the score. Game label: 'Is Self Winning'."""
    raise RuntimeError('author stub: compile with graphc')

def is_serve_phase() -> bool:
    """True while the ball is dead and the server prepares. Game label: 'Is Serve Phase'."""
    raise RuntimeError('author stub: compile with graphc')

def is_tied() -> bool:
    """True when the score is level. Game label: 'Is Tied'."""
    raise RuntimeError('author stub: compile with graphc')

def legal_serve_target() -> object:
    """Center of the legal diagonal serve box. Game label: 'Legal Serve Target'."""
    raise RuntimeError('author stub: compile with graphc')

def must_wait_for_bounce() -> bool:
    """True when the receiver must let the serve bounce first. Game label: 'Must Wait For Bounce'."""
    raise RuntimeError('author stub: compile with graphc')

def net_height() -> float:
    """Net tape height. Game label: 'Net Height'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent() -> object:
    """Opponent position. Game label: 'Opponent'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_aces() -> float:
    """Opponent ace count. Game label: 'Opponent Aces'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_average_scoring_location() -> object:
    """Where their winners usually land. Game label: 'Opponent Average Scoring Location'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_charged_shots() -> float:
    """Opponent fully-charged shot count. Game label: 'Opponent Charged Shots'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_double_faults() -> float:
    """Opponent double-fault count. Game label: 'Opponent Double Faults'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_faults() -> float:
    """Opponent serve-fault count. Game label: 'Opponent Faults'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_fouls() -> float:
    """Opponent foul count. Game label: 'Opponent Fouls'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_outs() -> float:
    """Opponent out count. Game label: 'Opponent Outs'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_points() -> float:
    """Opponent points in the current game. Game label: 'Opponent Points'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_scored_last_point() -> bool:
    """True when the opponent won the previous point. Game label: 'Opponent Scored Last Point'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_set_score() -> float:
    """Sets the opponent has won. Game label: 'Opponent Set Score'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_stamina_pct() -> float:
    """Opponent stamina 0-1. Game label: 'Opponent Stamina Pct'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_swing_charge_pct() -> float:
    """Opponent swing charge 0-1. Game label: 'Opponent Swing Charge Pct'."""
    raise RuntimeError('author stub: compile with graphc')

def predicted_2nd_bounce() -> object:
    """Where the ball will land second. Game label: 'Predicted 2nd Bounce'."""
    raise RuntimeError('author stub: compile with graphc')

def predicted_bounce() -> object:
    """Where the ball will land first. Game label: 'Predicted Bounce'."""
    raise RuntimeError('author stub: compile with graphc')

def rally_fatigue() -> float:
    """Fatigue factor growing with rally length. Game label: 'Rally Fatigue'."""
    raise RuntimeError('author stub: compile with graphc')

def random_aim_target() -> object:
    """A game-picked aim point. Game label: 'Random Aim Target'."""
    raise RuntimeError('author stub: compile with graphc')

def receive_stance() -> object:
    """Where the receiver should wait. Game label: 'Receive Stance'."""
    raise RuntimeError('author stub: compile with graphc')

def self() -> object:
    """Your position. Game label: 'Self'."""
    raise RuntimeError('author stub: compile with graphc')

def self_aces() -> float:
    """Your ace count. Game label: 'Self Aces'."""
    raise RuntimeError('author stub: compile with graphc')

def self_average_scoring_location() -> object:
    """Where your winners usually land. Game label: 'Self Average Scoring Location'."""
    raise RuntimeError('author stub: compile with graphc')

def self_charged_shots() -> float:
    """Your fully-charged shot count. Game label: 'Self Charged Shots'."""
    raise RuntimeError('author stub: compile with graphc')

def self_double_faults() -> float:
    """Your double-fault count. Game label: 'Self Double Faults'."""
    raise RuntimeError('author stub: compile with graphc')

def self_faults() -> float:
    """Your serve-fault count. Game label: 'Self Faults'."""
    raise RuntimeError('author stub: compile with graphc')

def self_fouls() -> float:
    """Your foul count. Game label: 'Self Fouls'."""
    raise RuntimeError('author stub: compile with graphc')

def self_has_advantage() -> bool:
    """True when you hold advantage at deuce. Game label: 'Self Has Advantage'."""
    raise RuntimeError('author stub: compile with graphc')

def self_outs() -> float:
    """Your out count. Game label: 'Self Outs'."""
    raise RuntimeError('author stub: compile with graphc')

def self_points() -> float:
    """Your points in the current game. Game label: 'Self Points'."""
    raise RuntimeError('author stub: compile with graphc')

def self_racket_center() -> object:
    """Your racket head position (strike point). Game label: 'Self Racket Center'."""
    raise RuntimeError('author stub: compile with graphc')

def self_scored_last_point() -> bool:
    """True when you won the previous point. Game label: 'Self Scored Last Point'."""
    raise RuntimeError('author stub: compile with graphc')

def self_set_score() -> float:
    """Sets (matches) you have won. Game label: 'Self Set Score'."""
    raise RuntimeError('author stub: compile with graphc')

def self_stamina_pct() -> float:
    """Your stamina 0-1 (sprint drains it). Game label: 'Self Stamina Pct'."""
    raise RuntimeError('author stub: compile with graphc')

def self_swing_charge_pct() -> float:
    """Your swing charge 0-1 (hold builds it). Game label: 'Self Swing Charge Pct'."""
    raise RuntimeError('author stub: compile with graphc')

def self_time_to_destination() -> float:
    """Seconds for you to reach your move target. Game label: 'Self Time To Destination'."""
    raise RuntimeError('author stub: compile with graphc')

def serve_number() -> float:
    """1 for first serve, 2 for second serve. Game label: 'Serve Number'."""
    raise RuntimeError('author stub: compile with graphc')

def serve_stance() -> object:
    """Where the server must stand (inside the serve area). Game label: 'Serve Stance'."""
    raise RuntimeError('author stub: compile with graphc')

def shot_ball() -> float:
    """Id of the shot currently in flight. Game label: 'Shot: Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def shot_curve_left() -> float:
    """Constant id of the curve-left shot. Game label: 'Shot: Curve Left'."""
    raise RuntimeError('author stub: compile with graphc')

def shot_curve_right() -> float:
    """Constant id of the curve-right shot. Game label: 'Shot: Curve Right'."""
    raise RuntimeError('author stub: compile with graphc')

def shot_drop() -> float:
    """Constant id of the drop shot. Game label: 'Shot: Drop'."""
    raise RuntimeError('author stub: compile with graphc')

def shot_flat() -> float:
    """Constant id of the flat shot. Game label: 'Shot: Flat'."""
    raise RuntimeError('author stub: compile with graphc')

def shot_last_opponent_shot() -> float:
    """Id of the opponent's most recent shot. Game label: 'Shot: Last Opponent Shot'."""
    raise RuntimeError('author stub: compile with graphc')

def shot_last_self_shot() -> float:
    """Id of your most recent shot. Game label: 'Shot: Last Self Shot'."""
    raise RuntimeError('author stub: compile with graphc')

def shot_lob() -> float:
    """Constant id of the lob shot. Game label: 'Shot: Lob'."""
    raise RuntimeError('author stub: compile with graphc')

def shot_most_scored_opponent_shot() -> float:
    """Id of the shot the opponent scored most with. Game label: 'Shot: Most Scored Opponent Shot'."""
    raise RuntimeError('author stub: compile with graphc')

def shot_most_scored_self_shot() -> float:
    """Id of the shot you scored most with. Game label: 'Shot: Most Scored Self Shot'."""
    raise RuntimeError('author stub: compile with graphc')

def shot_most_used_opponent_shot() -> float:
    """Id of the opponent's most frequent shot. Game label: 'Shot: Most Used Opponent Shot'."""
    raise RuntimeError('author stub: compile with graphc')

def shot_most_used_self_shot() -> float:
    """Id of your most frequent shot. Game label: 'Shot: Most Used Self Shot'."""
    raise RuntimeError('author stub: compile with graphc')

def shot_random() -> float:
    """Constant id asking the game to pick a shot. Game label: 'Shot: Random'."""
    raise RuntimeError('author stub: compile with graphc')

def shot_slice() -> float:
    """Constant id of the slice shot. Game label: 'Shot: Slice'."""
    raise RuntimeError('author stub: compile with graphc')

def shot_topspin() -> float:
    """Constant id of the topspin shot (feed to move shot). Game label: 'Shot: Topspin'."""
    raise RuntimeError('author stub: compile with graphc')

def sim_tick() -> float:
    """Current simulation tick. Game label: 'Sim Tick'."""
    raise RuntimeError('author stub: compile with graphc')

def trick_curve_left_modifier() -> object:
    """Aim offset curving a trick shot left. Game label: 'Trick Curve Left Modifier'."""
    raise RuntimeError('author stub: compile with graphc')

def trick_curve_right_modifier() -> object:
    """Aim offset curving a trick shot right. Game label: 'Trick Curve Right Modifier'."""
    raise RuntimeError('author stub: compile with graphc')

def trick_drop_modifier() -> object:
    """Aim offset making a trick shot drop. Game label: 'Trick Drop Modifier'."""
    raise RuntimeError('author stub: compile with graphc')

def trick_lob_modifier() -> object:
    """Aim offset making a trick shot lob. Game label: 'Trick Lob Modifier'."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_curve_left() -> bool:
    """True when the last shot curved left. Game label: 'Was Last Shot Curve Left'."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_curve_right() -> bool:
    """True when the last shot curved right. Game label: 'Was Last Shot Curve Right'."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_drop() -> bool:
    """True when the last struck shot was a drop shot. Game label: 'Was Last Shot Drop'."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_flat() -> bool:
    """True when the last struck shot was flat. Game label: 'Was Last Shot Flat'."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_lob() -> bool:
    """True when the last struck shot was a lob. Game label: 'Was Last Shot Lob'."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_slice() -> bool:
    """True when the last struck shot was slice. Game label: 'Was Last Shot Slice'."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_topspin() -> bool:
    """True when the last struck shot was topspin. Game label: 'Was Last Shot Topspin'."""
    raise RuntimeError('author stub: compile with graphc')

def was_last_shot_trick() -> bool:
    """True when the last shot was a trick shot. Game label: 'Was Last Shot Trick'."""
    raise RuntimeError('author stub: compile with graphc')

def move(x: float, z: float, swing: object = None, shot: object = None, sprint: object = None) -> None:
    """Drive to court position (x, z) and strike: swing truthy charges/hits, shot is a Shot:* id, sprint truthy sprints. Exactly one controller call per tick."""
    raise RuntimeError('author stub: compile with graphc')

def move_vec(v: object, swing: object = None, shot: object = None, sprint: object = None) -> None:
    """Same as move but driven by a vector (vec_make or a vector sensor)."""
    raise RuntimeError('author stub: compile with graphc')

