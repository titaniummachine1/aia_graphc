"""Author API for target ('soccer', 'v0.12') — GENERATED, do not edit.

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

Import this in bot projects instead of raw api.* strings:
    import AIA_Comp_Libry.soccer.v012 as t
The compiler maps these to the same ops as the api.* calls.
"""
from __future__ import annotations

TARGET = ('soccer', 'v0.12')

class Vector3:
    """Opaque 3D point: split via api.vec_split(v, 0/1/2) or feed
    t.move_vec(v). Never arithmetic directly."""

class Transform:
    """Opaque placed object (Self/Opponent/Ball): cannot split or
    do math on it; use a vector3 sensor instead."""

_SENSORS = {
    'backwards_clear_direction_from_team_carrier': ('vector3', 'Backwards clear direction from team carrier'),
    'ball': ('transform', 'Ball'),
    'ball_carrier_shot_charge': ('float', 'Ball Carrier Shot Charge'),
    'ball_carrier_stamina': ('float', 'Ball Carrier Stamina'),
    'ball_on_opponent_side': ('bool', 'Ball On Opponent Side'),
    'ball_on_team_side': ('bool', 'Ball On Team Side'),
    'ball_speed': ('float', 'Ball Speed'),
    'ball_velocity': ('vector3', 'Ball Velocity'),
    'center_field': ('vector3', 'Center Field'),
    'clear_direction_from_team_carrier': ('vector3', 'Clear direction from team carrier'),
    'clear_direction_from_team_carrier_avoid_all_walls': ('vector3', 'Clear direction from team carrier (avoid all walls)'),
    'clear_direction_from_team_carrier_avoid_goal_lines': ('vector3', 'Clear direction from team carrier (avoid goal lines)'),
    'clear_direction_from_team_carrier_avoid_sidelines': ('vector3', 'Clear direction from team carrier (avoid sidelines)'),
    'clear_direction_from_teammate_1': ('vector3', 'Clear direction from Teammate 1'),
    'clear_direction_from_teammate_2': ('vector3', 'Clear direction from Teammate 2'),
    'clear_direction_from_teammate_3': ('vector3', 'Clear direction from Teammate 3'),
    'clear_direction_from_teammate_4': ('vector3', 'Clear direction from Teammate 4'),
    'current_simulation_time': ('float', 'Current Simulation Time'),
    'delta_time': ('float', 'Delta Time'),
    'direction_of_ball_from_opponent_1': ('vector3', 'Direction of ball from Opponent 1'),
    'direction_of_ball_from_opponent_2': ('vector3', 'Direction of ball from Opponent 2'),
    'direction_of_ball_from_opponent_3': ('vector3', 'Direction of ball from Opponent 3'),
    'direction_of_ball_from_opponent_4': ('vector3', 'Direction of ball from Opponent 4'),
    'direction_of_ball_from_teammate_1': ('vector3', 'Direction of ball from Teammate 1'),
    'direction_of_ball_from_teammate_2': ('vector3', 'Direction of ball from Teammate 2'),
    'direction_of_ball_from_teammate_3': ('vector3', 'Direction of ball from Teammate 3'),
    'direction_of_ball_from_teammate_4': ('vector3', 'Direction of ball from Teammate 4'),
    'direction_of_clear_teammate_from_opponent_1': ('vector3', 'Direction of clear teammate from Opponent 1'),
    'direction_of_clear_teammate_from_opponent_2': ('vector3', 'Direction of clear teammate from Opponent 2'),
    'direction_of_clear_teammate_from_opponent_3': ('vector3', 'Direction of clear teammate from Opponent 3'),
    'direction_of_clear_teammate_from_opponent_4': ('vector3', 'Direction of clear teammate from Opponent 4'),
    'direction_of_clear_teammate_from_teammate_1': ('vector3', 'Direction of clear teammate from Teammate 1'),
    'direction_of_clear_teammate_from_teammate_2': ('vector3', 'Direction of clear teammate from Teammate 2'),
    'direction_of_clear_teammate_from_teammate_3': ('vector3', 'Direction of clear teammate from Teammate 3'),
    'direction_of_clear_teammate_from_teammate_4': ('vector3', 'Direction of clear teammate from Teammate 4'),
    'direction_of_opponent_goal_from_teammate_1': ('vector3', 'Direction of opponent goal from Teammate 1'),
    'direction_of_opponent_goal_from_teammate_2': ('vector3', 'Direction of opponent goal from Teammate 2'),
    'direction_of_opponent_goal_from_teammate_3': ('vector3', 'Direction of opponent goal from Teammate 3'),
    'direction_of_opponent_goal_from_teammate_4': ('vector3', 'Direction of opponent goal from Teammate 4'),
    'direction_of_team_goal_from_teammate_1': ('vector3', 'Direction of team goal from Teammate 1'),
    'direction_of_team_goal_from_teammate_2': ('vector3', 'Direction of team goal from Teammate 2'),
    'direction_of_team_goal_from_teammate_3': ('vector3', 'Direction of team goal from Teammate 3'),
    'direction_of_team_goal_from_teammate_4': ('vector3', 'Direction of team goal from Teammate 4'),
    'direction_of_teammate_from_team_player_1': ('vector3', 'Direction of teammate from Team Player 1'),
    'direction_of_teammate_from_team_player_2': ('vector3', 'Direction of teammate from Team Player 2'),
    'direction_of_teammate_from_team_player_3': ('vector3', 'Direction of teammate from Team Player 3'),
    'direction_of_teammate_from_team_player_4': ('vector3', 'Direction of teammate from Team Player 4'),
    'distance_from_team_player_1_to_nearest_opponent': ('float', 'Distance from Team Player 1 to nearest Opponent'),
    'distance_from_team_player_2_to_nearest_opponent': ('float', 'Distance from Team Player 2 to nearest Opponent'),
    'distance_from_team_player_3_to_nearest_opponent': ('float', 'Distance from Team Player 3 to nearest Opponent'),
    'distance_from_team_player_4_to_nearest_opponent': ('float', 'Distance from Team Player 4 to nearest Opponent'),
    'field_depth': ('float', 'Field Depth'),
    'field_width': ('float', 'Field Width'),
    'fixed_delta_time': ('float', 'Fixed Delta Time'),
    'get_furthest_open_opponent': ('vector3', 'Get furthest open opponent'),
    'get_furthest_open_teammate': ('vector3', 'Get furthest open teammate'),
    'get_most_open_opponent': ('vector3', 'Get most open opponent'),
    'get_most_open_teammate': ('vector3', 'Get most open teammate'),
    'get_nearest_open_opponent': ('vector3', 'Get nearest open opponent'),
    'get_nearest_open_teammate': ('vector3', 'Get nearest open teammate'),
    'goal_height': ('float', 'Goal Height'),
    'goal_width': ('float', 'Goal Width'),
    'is_active_graph': ('bool', 'Is Active Graph'),
    'is_away_team': ('bool', 'Is Away Team'),
    'is_ball_headed_towards_opponent_goal': ('bool', 'Is Ball Headed Towards Opponent Goal'),
    'is_ball_headed_towards_team_goal': ('bool', 'Is Ball Headed Towards Team Goal'),
    'is_ball_loose': ('bool', 'Is Ball Loose'),
    'is_ball_nearby_opponent_player_1': ('bool', 'Is Ball Nearby Opponent Player 1'),
    'is_ball_nearby_opponent_player_2': ('bool', 'Is Ball Nearby Opponent Player 2'),
    'is_ball_nearby_opponent_player_3': ('bool', 'Is Ball Nearby Opponent Player 3'),
    'is_ball_nearby_opponent_player_4': ('bool', 'Is Ball Nearby Opponent Player 4'),
    'is_ball_nearby_team_player_1': ('bool', 'Is Ball Nearby Team Player 1'),
    'is_ball_nearby_team_player_2': ('bool', 'Is Ball Nearby Team Player 2'),
    'is_ball_nearby_team_player_3': ('bool', 'Is Ball Nearby Team Player 3'),
    'is_ball_nearby_team_player_4': ('bool', 'Is Ball Nearby Team Player 4'),
    'is_home_team': ('bool', 'Is Home Team'),
    'is_kickoff': ('bool', 'Is Kickoff'),
    'is_opponent_kicking_off': ('bool', 'Is Opponent Kicking off'),
    'is_opponent_player_1_closest_opponent_to_ball': ('bool', 'Is Opponent Player 1 Closest Opponent to Ball'),
    'is_opponent_player_1_open': ('bool', 'Is Opponent Player 1 Open'),
    'is_opponent_player_2_closest_opponent_to_ball': ('bool', 'Is Opponent Player 2 Closest Opponent to Ball'),
    'is_opponent_player_2_open': ('bool', 'Is Opponent Player 2 Open'),
    'is_opponent_player_3_closest_opponent_to_ball': ('bool', 'Is Opponent Player 3 Closest Opponent to Ball'),
    'is_opponent_player_3_open': ('bool', 'Is Opponent Player 3 Open'),
    'is_opponent_player_4_closest_opponent_to_ball': ('bool', 'Is Opponent Player 4 Closest Opponent to Ball'),
    'is_opponent_player_4_open': ('bool', 'Is Opponent Player 4 Open'),
    'is_team_kicking_off': ('bool', 'Is Team Kicking off'),
    'is_team_player_1_closest_teammate_to_ball': ('bool', 'Is Team Player 1 Closest Teammate to Ball'),
    'is_team_player_1_open': ('bool', 'Is Team Player 1 Open'),
    'is_team_player_2_closest_teammate_to_ball': ('bool', 'Is Team Player 2 Closest Teammate to Ball'),
    'is_team_player_2_open': ('bool', 'Is Team Player 2 Open'),
    'is_team_player_3_closest_teammate_to_ball': ('bool', 'Is Team Player 3 Closest Teammate to Ball'),
    'is_team_player_3_open': ('bool', 'Is Team Player 3 Open'),
    'is_team_player_4_closest_teammate_to_ball': ('bool', 'Is Team Player 4 Closest Teammate to Ball'),
    'is_team_player_4_open': ('bool', 'Is Team Player 4 Open'),
    'kickoff_circle_radius': ('float', 'Kickoff Circle Radius'),
    'lower_corner_away_side': ('vector3', 'Lower Corner Away Side'),
    'lower_corner_home_side': ('vector3', 'Lower Corner Home Side'),
    'lower_corner_opposing_side': ('vector3', 'Lower Corner Opposing Side'),
    'lower_corner_team_side': ('vector3', 'Lower Corner Team Side'),
    'lower_midfield': ('vector3', 'Lower Midfield'),
    'max_simulation_time': ('float', 'Max Simulation Time'),
    'opponent_attacking': ('float', 'Opponent Attacking %'),
    'opponent_goal_center': ('transform', 'Opponent Goal Center'),
    'opponent_goal_left_post': ('transform', 'Opponent Goal Left Post'),
    'opponent_goal_right_post': ('transform', 'Opponent Goal Right Post'),
    'opponent_has_ball': ('bool', 'Opponent Has Ball'),
    'opponent_is_winning': ('bool', 'Opponent Is Winning'),
    'opponent_nearest_opponent_goal': ('transform', 'Opponent Nearest Opponent Goal'),
    'opponent_nearest_team_goal': ('transform', 'Opponent Nearest Team Goal'),
    'opponent_nearest_team_player_1': ('transform', 'Opponent Nearest Team Player 1'),
    'opponent_nearest_team_player_2': ('transform', 'Opponent Nearest Team Player 2'),
    'opponent_nearest_team_player_3': ('transform', 'Opponent Nearest Team Player 3'),
    'opponent_nearest_team_player_4': ('transform', 'Opponent Nearest Team Player 4'),
    'opponent_nearest_teammate_player_1_stamina': ('float', 'Opponent Nearest Teammate Player 1 Stamina'),
    'opponent_nearest_teammate_player_2_stamina': ('float', 'Opponent Nearest Teammate Player 2 Stamina'),
    'opponent_nearest_teammate_player_3_stamina': ('float', 'Opponent Nearest Teammate Player 3 Stamina'),
    'opponent_nearest_teammate_player_4_stamina': ('float', 'Opponent Nearest Teammate Player 4 Stamina'),
    'opponent_player_1': ('transform', 'Opponent Player 1'),
    'opponent_player_1_has_ball': ('bool', 'Opponent Player 1 Has Ball'),
    'opponent_player_1_stamina': ('float', 'Opponent Player 1 Stamina'),
    'opponent_player_2': ('transform', 'Opponent Player 2'),
    'opponent_player_2_has_ball': ('bool', 'Opponent Player 2 Has Ball'),
    'opponent_player_2_stamina': ('float', 'Opponent Player 2 Stamina'),
    'opponent_player_3': ('transform', 'Opponent Player 3'),
    'opponent_player_3_has_ball': ('bool', 'Opponent Player 3 Has Ball'),
    'opponent_player_3_stamina': ('float', 'Opponent Player 3 Stamina'),
    'opponent_player_4': ('transform', 'Opponent Player 4'),
    'opponent_player_4_has_ball': ('bool', 'Opponent Player 4 Has Ball'),
    'opponent_player_4_stamina': ('float', 'Opponent Player 4 Stamina'),
    'opponent_possession': ('float', 'Opponent Possession %'),
    'opponent_score': ('float', 'Opponent Score'),
    'opponent_scored_last_point': ('bool', 'Opponent Scored Last Point'),
    'opponent_shots': ('float', 'Opponent Shots'),
    'pi': ('float', 'Pi'),
    'player_interact_radius': ('float', 'Player Interact Radius'),
    'simulation_time_remaining': ('float', 'Simulation Time Remaining'),
    'stamina_of_last_defending_opponent': ('float', 'Stamina of last defending opponent'),
    'team_attacking': ('float', 'Team Attacking %'),
    'team_goal_center': ('transform', 'Team Goal Center'),
    'team_goal_left_post': ('transform', 'Team Goal Left Post'),
    'team_goal_right_post': ('transform', 'Team Goal Right Post'),
    'team_has_ball': ('bool', 'Team Has Ball'),
    'team_is_winning': ('bool', 'Team Is Winning'),
    'team_player_1': ('transform', 'Team Player 1'),
    'team_player_1_has_ball': ('bool', 'Team Player 1 Has Ball'),
    'team_player_1_stamina': ('float', 'Team Player 1 Stamina'),
    'team_player_2': ('transform', 'Team Player 2'),
    'team_player_2_has_ball': ('bool', 'Team Player 2 Has Ball'),
    'team_player_2_stamina': ('float', 'Team Player 2 Stamina'),
    'team_player_3': ('transform', 'Team Player 3'),
    'team_player_3_has_ball': ('bool', 'Team Player 3 Has Ball'),
    'team_player_3_stamina': ('float', 'Team Player 3 Stamina'),
    'team_player_4': ('transform', 'Team Player 4'),
    'team_player_4_has_ball': ('bool', 'Team Player 4 Has Ball'),
    'team_player_4_stamina': ('float', 'Team Player 4 Stamina'),
    'team_possession': ('float', 'Team Possession %'),
    'team_score': ('float', 'Team Score'),
    'team_scored_last_point': ('bool', 'Team Scored Last Point'),
    'team_shots': ('float', 'Team Shots'),
    'teammate_1_shot_charge': ('float', 'Teammate 1 Shot Charge'),
    'teammate_2_shot_charge': ('float', 'Teammate 2 Shot Charge'),
    'teammate_3_shot_charge': ('float', 'Teammate 3 Shot Charge'),
    'teammate_4_shot_charge': ('float', 'Teammate 4 Shot Charge'),
    'teammate_nearest_opponent_goal': ('transform', 'Teammate Nearest Opponent Goal'),
    'teammate_nearest_team_goal': ('transform', 'Teammate Nearest Team Goal'),
    'teammate_nearest_team_player_1': ('transform', 'Teammate Nearest Team Player 1'),
    'teammate_nearest_team_player_2': ('transform', 'Teammate Nearest Team Player 2'),
    'teammate_nearest_team_player_3': ('transform', 'Teammate Nearest Team Player 3'),
    'teammate_nearest_team_player_4': ('transform', 'Teammate Nearest Team Player 4'),
    'upper_corner_away_side': ('vector3', 'Upper Corner Away Side'),
    'upper_corner_home_side': ('vector3', 'Upper Corner Home Side'),
    'upper_corner_opposing_side': ('vector3', 'Upper Corner Opposing Side'),
    'upper_corner_team_side': ('vector3', 'Upper Corner Team Side'),
    'upper_midfield': ('vector3', 'Upper Midfield'),
}

__all__ = ['backwards_clear_direction_from_team_carrier', 'ball', 'ball_carrier_shot_charge', 'ball_carrier_stamina', 'ball_on_opponent_side', 'ball_on_team_side', 'ball_speed', 'ball_velocity', 'center_field', 'clear_direction_from_team_carrier', 'clear_direction_from_team_carrier_avoid_all_walls', 'clear_direction_from_team_carrier_avoid_goal_lines', 'clear_direction_from_team_carrier_avoid_sidelines', 'clear_direction_from_teammate_1', 'clear_direction_from_teammate_2', 'clear_direction_from_teammate_3', 'clear_direction_from_teammate_4', 'current_simulation_time', 'delta_time', 'direction_of_ball_from_opponent_1', 'direction_of_ball_from_opponent_2', 'direction_of_ball_from_opponent_3', 'direction_of_ball_from_opponent_4', 'direction_of_ball_from_teammate_1', 'direction_of_ball_from_teammate_2', 'direction_of_ball_from_teammate_3', 'direction_of_ball_from_teammate_4', 'direction_of_clear_teammate_from_opponent_1', 'direction_of_clear_teammate_from_opponent_2', 'direction_of_clear_teammate_from_opponent_3', 'direction_of_clear_teammate_from_opponent_4', 'direction_of_clear_teammate_from_teammate_1', 'direction_of_clear_teammate_from_teammate_2', 'direction_of_clear_teammate_from_teammate_3', 'direction_of_clear_teammate_from_teammate_4', 'direction_of_opponent_goal_from_teammate_1', 'direction_of_opponent_goal_from_teammate_2', 'direction_of_opponent_goal_from_teammate_3', 'direction_of_opponent_goal_from_teammate_4', 'direction_of_team_goal_from_teammate_1', 'direction_of_team_goal_from_teammate_2', 'direction_of_team_goal_from_teammate_3', 'direction_of_team_goal_from_teammate_4', 'direction_of_teammate_from_team_player_1', 'direction_of_teammate_from_team_player_2', 'direction_of_teammate_from_team_player_3', 'direction_of_teammate_from_team_player_4', 'distance_from_team_player_1_to_nearest_opponent', 'distance_from_team_player_2_to_nearest_opponent', 'distance_from_team_player_3_to_nearest_opponent', 'distance_from_team_player_4_to_nearest_opponent', 'field_depth', 'field_width', 'fixed_delta_time', 'get_furthest_open_opponent', 'get_furthest_open_teammate', 'get_most_open_opponent', 'get_most_open_teammate', 'get_nearest_open_opponent', 'get_nearest_open_teammate', 'goal_height', 'goal_width', 'is_active_graph', 'is_away_team', 'is_ball_headed_towards_opponent_goal', 'is_ball_headed_towards_team_goal', 'is_ball_loose', 'is_ball_nearby_opponent_player_1', 'is_ball_nearby_opponent_player_2', 'is_ball_nearby_opponent_player_3', 'is_ball_nearby_opponent_player_4', 'is_ball_nearby_team_player_1', 'is_ball_nearby_team_player_2', 'is_ball_nearby_team_player_3', 'is_ball_nearby_team_player_4', 'is_home_team', 'is_kickoff', 'is_opponent_kicking_off', 'is_opponent_player_1_closest_opponent_to_ball', 'is_opponent_player_1_open', 'is_opponent_player_2_closest_opponent_to_ball', 'is_opponent_player_2_open', 'is_opponent_player_3_closest_opponent_to_ball', 'is_opponent_player_3_open', 'is_opponent_player_4_closest_opponent_to_ball', 'is_opponent_player_4_open', 'is_team_kicking_off', 'is_team_player_1_closest_teammate_to_ball', 'is_team_player_1_open', 'is_team_player_2_closest_teammate_to_ball', 'is_team_player_2_open', 'is_team_player_3_closest_teammate_to_ball', 'is_team_player_3_open', 'is_team_player_4_closest_teammate_to_ball', 'is_team_player_4_open', 'kickoff_circle_radius', 'lower_corner_away_side', 'lower_corner_home_side', 'lower_corner_opposing_side', 'lower_corner_team_side', 'lower_midfield', 'max_simulation_time', 'opponent_attacking', 'opponent_goal_center', 'opponent_goal_left_post', 'opponent_goal_right_post', 'opponent_has_ball', 'opponent_is_winning', 'opponent_nearest_opponent_goal', 'opponent_nearest_team_goal', 'opponent_nearest_team_player_1', 'opponent_nearest_team_player_2', 'opponent_nearest_team_player_3', 'opponent_nearest_team_player_4', 'opponent_nearest_teammate_player_1_stamina', 'opponent_nearest_teammate_player_2_stamina', 'opponent_nearest_teammate_player_3_stamina', 'opponent_nearest_teammate_player_4_stamina', 'opponent_player_1', 'opponent_player_1_has_ball', 'opponent_player_1_stamina', 'opponent_player_2', 'opponent_player_2_has_ball', 'opponent_player_2_stamina', 'opponent_player_3', 'opponent_player_3_has_ball', 'opponent_player_3_stamina', 'opponent_player_4', 'opponent_player_4_has_ball', 'opponent_player_4_stamina', 'opponent_possession', 'opponent_score', 'opponent_scored_last_point', 'opponent_shots', 'pi', 'player_interact_radius', 'simulation_time_remaining', 'stamina_of_last_defending_opponent', 'team_attacking', 'team_goal_center', 'team_goal_left_post', 'team_goal_right_post', 'team_has_ball', 'team_is_winning', 'team_player_1', 'team_player_1_has_ball', 'team_player_1_stamina', 'team_player_2', 'team_player_2_has_ball', 'team_player_2_stamina', 'team_player_3', 'team_player_3_has_ball', 'team_player_3_stamina', 'team_player_4', 'team_player_4_has_ball', 'team_player_4_stamina', 'team_possession', 'team_score', 'team_scored_last_point', 'team_shots', 'teammate_1_shot_charge', 'teammate_2_shot_charge', 'teammate_3_shot_charge', 'teammate_4_shot_charge', 'teammate_nearest_opponent_goal', 'teammate_nearest_team_goal', 'teammate_nearest_team_player_1', 'teammate_nearest_team_player_2', 'teammate_nearest_team_player_3', 'teammate_nearest_team_player_4', 'upper_corner_away_side', 'upper_corner_home_side', 'upper_corner_opposing_side', 'upper_corner_team_side', 'upper_midfield', 'move']

def backwards_clear_direction_from_team_carrier() -> Vector3:
    """Clear backwards for the carrier.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Backwards clear direction from team carrier'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def ball() -> Transform:
    """Ball position.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def ball_carrier_shot_charge() -> float:
    """Shot charge of whoever holds the ball.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Ball Carrier Shot Charge'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def ball_carrier_stamina() -> float:
    """Stamina of whoever holds the ball.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Ball Carrier Stamina'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def ball_on_opponent_side() -> bool:
    """True when the ball is on their half.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Ball On Opponent Side'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def ball_on_team_side() -> bool:
    """True when the ball is on your half.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Ball On Team Side'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def ball_speed() -> float:
    """Current ball speed.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Ball Speed'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def ball_velocity() -> Vector3:
    """Ball velocity vector.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Ball Velocity'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def center_field() -> Vector3:
    """Center spot.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Center Field'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_team_carrier() -> Vector3:
    """Safe clear direction for the carrier.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Clear direction from team carrier'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_team_carrier_avoid_all_walls() -> Vector3:
    """Clear that stays in play.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Clear direction from team carrier (avoid all walls)'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_team_carrier_avoid_goal_lines() -> Vector3:
    """Clear that stays in play past the lines.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Clear direction from team carrier (avoid goal lines)'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_team_carrier_avoid_sidelines() -> Vector3:
    """Clear that stays in past the sidelines.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Clear direction from team carrier (avoid sidelines)'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_teammate_1() -> Vector3:
    """Safe clear direction for teammate 1.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Clear direction from Teammate 1'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_teammate_2() -> Vector3:
    """Safe clear direction for teammate 2.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Clear direction from Teammate 2'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_teammate_3() -> Vector3:
    """Safe clear direction for teammate 3.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Clear direction from Teammate 3'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_teammate_4() -> Vector3:
    """Safe clear direction for teammate 4.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Clear direction from Teammate 4'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def current_simulation_time() -> float:
    """Match clock in seconds.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Current Simulation Time'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def delta_time() -> float:
    """Frame delta in seconds.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Delta Time'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_opponent_1() -> Vector3:
    """Ball direction seen from opponent 1.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of ball from Opponent 1'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_opponent_2() -> Vector3:
    """Ball direction seen from opponent 2.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of ball from Opponent 2'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_opponent_3() -> Vector3:
    """Ball direction seen from opponent 3.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of ball from Opponent 3'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_opponent_4() -> Vector3:
    """Ball direction seen from opponent 4.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of ball from Opponent 4'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_teammate_1() -> Vector3:
    """Ball direction seen from teammate 1.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of ball from Teammate 1'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_teammate_2() -> Vector3:
    """Ball direction seen from teammate 2.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of ball from Teammate 2'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_teammate_3() -> Vector3:
    """Ball direction seen from teammate 3.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of ball from Teammate 3'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_teammate_4() -> Vector3:
    """Ball direction seen from teammate 4.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of ball from Teammate 4'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_opponent_1() -> Vector3:
    """Where opponent 1 would clear to find a teammate.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of clear teammate from Opponent 1'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_opponent_2() -> Vector3:
    """Where opponent 2 would clear to find a teammate.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of clear teammate from Opponent 2'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_opponent_3() -> Vector3:
    """Where opponent 3 would clear to find a teammate.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of clear teammate from Opponent 3'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_opponent_4() -> Vector3:
    """Where opponent 4 would clear to find a teammate.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of clear teammate from Opponent 4'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_teammate_1() -> Vector3:
    """Where teammate 1 should clear to find a teammate.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of clear teammate from Teammate 1'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_teammate_2() -> Vector3:
    """Where teammate 2 should clear to find a teammate.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of clear teammate from Teammate 2'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_teammate_3() -> Vector3:
    """Where teammate 3 should clear to find a teammate.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of clear teammate from Teammate 3'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_teammate_4() -> Vector3:
    """Where teammate 4 should clear to find a teammate.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of clear teammate from Teammate 4'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_opponent_goal_from_teammate_1() -> Vector3:
    """Their-goal direction from teammate 1.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of opponent goal from Teammate 1'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_opponent_goal_from_teammate_2() -> Vector3:
    """Their-goal direction from teammate 2.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of opponent goal from Teammate 2'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_opponent_goal_from_teammate_3() -> Vector3:
    """Their-goal direction from teammate 3.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of opponent goal from Teammate 3'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_opponent_goal_from_teammate_4() -> Vector3:
    """Their-goal direction from teammate 4.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of opponent goal from Teammate 4'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_team_goal_from_teammate_1() -> Vector3:
    """Own-goal direction from teammate 1.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of team goal from Teammate 1'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_team_goal_from_teammate_2() -> Vector3:
    """Own-goal direction from teammate 2.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of team goal from Teammate 2'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_team_goal_from_teammate_3() -> Vector3:
    """Own-goal direction from teammate 3.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of team goal from Teammate 3'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_team_goal_from_teammate_4() -> Vector3:
    """Own-goal direction from teammate 4.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of team goal from Teammate 4'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_teammate_from_team_player_1() -> Vector3:
    """Pass direction from team player 1.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of teammate from Team Player 1'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_teammate_from_team_player_2() -> Vector3:
    """Pass direction from team player 2.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of teammate from Team Player 2'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_teammate_from_team_player_3() -> Vector3:
    """Pass direction from team player 3.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of teammate from Team Player 3'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_teammate_from_team_player_4() -> Vector3:
    """Pass direction from team player 4.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Direction of teammate from Team Player 4'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def distance_from_team_player_1_to_nearest_opponent() -> float:
    """How much space team player 1 has.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Distance from Team Player 1 to nearest Opponent'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def distance_from_team_player_2_to_nearest_opponent() -> float:
    """How much space team player 2 has.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Distance from Team Player 2 to nearest Opponent'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def distance_from_team_player_3_to_nearest_opponent() -> float:
    """How much space team player 3 has.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Distance from Team Player 3 to nearest Opponent'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def distance_from_team_player_4_to_nearest_opponent() -> float:
    """How much space team player 4 has.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Distance from Team Player 4 to nearest Opponent'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def field_depth() -> float:
    """Playable field length.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Field Depth'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def field_width() -> float:
    """Playable field width.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Field Width'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def fixed_delta_time() -> float:
    """Physics tick delta in seconds.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Fixed Delta Time'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def get_furthest_open_opponent() -> Vector3:
    """Position of the furthest open opponent.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Get furthest open opponent'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def get_furthest_open_teammate() -> Vector3:
    """Position of the furthest open teammate.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Get furthest open teammate'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def get_most_open_opponent() -> Vector3:
    """Position of the most open opponent.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Get most open opponent'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def get_most_open_teammate() -> Vector3:
    """Position of the most open teammate.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Get most open teammate'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def get_nearest_open_opponent() -> Vector3:
    """Position of the nearest open opponent.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Get nearest open opponent'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def get_nearest_open_teammate() -> Vector3:
    """Position of the nearest open teammate.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Get nearest open teammate'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def goal_height() -> float:
    """Goal height.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Goal Height'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def goal_width() -> float:
    """Goal mouth width.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Goal Width'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_active_graph() -> bool:
    """True when this graph is the one driving the player.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Active Graph'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_away_team() -> bool:
    """True when this brain plays the away team.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Away Team'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_headed_towards_opponent_goal() -> bool:
    """True when ball velocity aims at their goal.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Ball Headed Towards Opponent Goal'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_headed_towards_team_goal() -> bool:
    """True when ball velocity aims at your goal.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Ball Headed Towards Team Goal'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_loose() -> bool:
    """True when nobody holds the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Ball Loose'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_opponent_player_1() -> bool:
    """True when the ball is near opponent 1.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Ball Nearby Opponent Player 1'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_opponent_player_2() -> bool:
    """True when the ball is near opponent 2.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Ball Nearby Opponent Player 2'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_opponent_player_3() -> bool:
    """True when the ball is near opponent 3.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Ball Nearby Opponent Player 3'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_opponent_player_4() -> bool:
    """True when the ball is near opponent 4.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Ball Nearby Opponent Player 4'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_team_player_1() -> bool:
    """True when the ball is near team player 1.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Ball Nearby Team Player 1'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_team_player_2() -> bool:
    """True when the ball is near team player 2.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Ball Nearby Team Player 2'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_team_player_3() -> bool:
    """True when the ball is near team player 3.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Ball Nearby Team Player 3'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_team_player_4() -> bool:
    """True when the ball is near team player 4.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Ball Nearby Team Player 4'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_home_team() -> bool:
    """True when this brain plays the home team.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Home Team'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_kickoff() -> bool:
    """True during kickoff setup.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Kickoff'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_kicking_off() -> bool:
    """True when the opponent kicks off.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Opponent Kicking off'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_1_closest_opponent_to_ball() -> bool:
    """True when opponent 1 is the closest opponent to the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Opponent Player 1 Closest Opponent to Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_1_open() -> bool:
    """True when opponent 1 has no close marker.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Opponent Player 1 Open'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_2_closest_opponent_to_ball() -> bool:
    """True when opponent 2 is the closest opponent to the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Opponent Player 2 Closest Opponent to Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_2_open() -> bool:
    """True when opponent 2 has no close marker.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Opponent Player 2 Open'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_3_closest_opponent_to_ball() -> bool:
    """True when opponent 3 is the closest opponent to the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Opponent Player 3 Closest Opponent to Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_3_open() -> bool:
    """True when opponent 3 has no close marker.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Opponent Player 3 Open'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_4_closest_opponent_to_ball() -> bool:
    """True when opponent 4 is the closest opponent to the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Opponent Player 4 Closest Opponent to Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_4_open() -> bool:
    """True when opponent 4 has no close marker.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Opponent Player 4 Open'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_kicking_off() -> bool:
    """True when your team kicks off.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Team Kicking off'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_1_closest_teammate_to_ball() -> bool:
    """True when team player 1 is the closest teammate to the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Team Player 1 Closest Teammate to Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_1_open() -> bool:
    """True when team player 1 has no close marker.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Team Player 1 Open'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_2_closest_teammate_to_ball() -> bool:
    """True when team player 2 is the closest teammate to the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Team Player 2 Closest Teammate to Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_2_open() -> bool:
    """True when team player 2 has no close marker.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Team Player 2 Open'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_3_closest_teammate_to_ball() -> bool:
    """True when team player 3 is the closest teammate to the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Team Player 3 Closest Teammate to Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_3_open() -> bool:
    """True when team player 3 has no close marker.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Team Player 3 Open'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_4_closest_teammate_to_ball() -> bool:
    """True when team player 4 is the closest teammate to the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Team Player 4 Closest Teammate to Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_4_open() -> bool:
    """True when team player 4 has no close marker.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Is Team Player 4 Open'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def kickoff_circle_radius() -> float:
    """Center circle radius.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Kickoff Circle Radius'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def lower_corner_away_side() -> Vector3:
    """Corner position, away side lower.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Lower Corner Away Side'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def lower_corner_home_side() -> Vector3:
    """Corner position, home side lower.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Lower Corner Home Side'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def lower_corner_opposing_side() -> Vector3:
    """Opposing corner, lower.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Lower Corner Opposing Side'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def lower_corner_team_side() -> Vector3:
    """Team corner, lower.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Lower Corner Team Side'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def lower_midfield() -> Vector3:
    """Midfield position, lower.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Lower Midfield'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def max_simulation_time() -> float:
    """Match length in seconds.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Max Simulation Time'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_attacking() -> float:
    """Share of opponent play in attack 0-1.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Opponent Attacking %'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_goal_center() -> Transform:
    """Middle of their goal.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Opponent Goal Center'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_goal_left_post() -> Transform:
    """Their left post.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Opponent Goal Left Post'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_goal_right_post() -> Transform:
    """Their right post.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Opponent Goal Right Post'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_has_ball() -> bool:
    """True when an opponent holds the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Opponent Has Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_is_winning() -> bool:
    """True when the opponent leads.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Opponent Is Winning'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_opponent_goal() -> Transform:
    """Opponent closest to their goal.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Opponent Nearest Opponent Goal'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_team_goal() -> Transform:
    """Opponent closest to your goal.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Opponent Nearest Team Goal'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_team_player_1() -> Transform:
    """Opponent closest to your player 1.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Opponent Nearest Team Player 1'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_team_player_2() -> Transform:
    """Opponent closest to your player 2.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Opponent Nearest Team Player 2'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_team_player_3() -> Transform:
    """Opponent closest to your player 3.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Opponent Nearest Team Player 3'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_team_player_4() -> Transform:
    """Opponent closest to your player 4.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Opponent Nearest Team Player 4'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_teammate_player_1_stamina() -> float:
    """Stamina of the opponent nearest your player 1.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Opponent Nearest Teammate Player 1 Stamina'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_teammate_player_2_stamina() -> float:
    """Stamina of the opponent nearest your player 2.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Opponent Nearest Teammate Player 2 Stamina'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_teammate_player_3_stamina() -> float:
    """Stamina of the opponent nearest your player 3.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Opponent Nearest Teammate Player 3 Stamina'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_teammate_player_4_stamina() -> float:
    """Stamina of the opponent nearest your player 4.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Opponent Nearest Teammate Player 4 Stamina'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_1() -> Transform:
    """Position of opponent 1.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Opponent Player 1'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_1_has_ball() -> bool:
    """True when opponent 1 holds the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Opponent Player 1 Has Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_1_stamina() -> float:
    """Stamina of opponent 1.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Opponent Player 1 Stamina'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_2() -> Transform:
    """Position of opponent 2.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Opponent Player 2'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_2_has_ball() -> bool:
    """True when opponent 2 holds the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Opponent Player 2 Has Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_2_stamina() -> float:
    """Stamina of opponent 2.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Opponent Player 2 Stamina'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_3() -> Transform:
    """Position of opponent 3.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Opponent Player 3'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_3_has_ball() -> bool:
    """True when opponent 3 holds the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Opponent Player 3 Has Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_3_stamina() -> float:
    """Stamina of opponent 3.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Opponent Player 3 Stamina'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_4() -> Transform:
    """Position of opponent 4.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Opponent Player 4'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_4_has_ball() -> bool:
    """True when opponent 4 holds the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Opponent Player 4 Has Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_4_stamina() -> float:
    """Stamina of opponent 4.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Opponent Player 4 Stamina'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_possession() -> float:
    """Opponent possession share 0-1.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Opponent Possession %'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_score() -> float:
    """Opponent goals.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Opponent Score'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_scored_last_point() -> bool:
    """True when the opponent scored last.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Opponent Scored Last Point'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_shots() -> float:
    """Opponent shot count.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Opponent Shots'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def pi() -> float:
    """3.14159.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Pi'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def player_interact_radius() -> float:
    """How close a player must be to touch the ball.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Player Interact Radius'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def simulation_time_remaining() -> float:
    """Seconds left on the clock.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Simulation Time Remaining'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def stamina_of_last_defending_opponent() -> float:
    """Stamina of the last defender.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Stamina of last defending opponent'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_attacking() -> float:
    """Share of your play in attack 0-1.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Team Attacking %'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_goal_center() -> Transform:
    """Middle of your goal.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Team Goal Center'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_goal_left_post() -> Transform:
    """Your left post.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Team Goal Left Post'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_goal_right_post() -> Transform:
    """Your right post.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Team Goal Right Post'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_has_ball() -> bool:
    """True when a teammate (or you) holds the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Team Has Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_is_winning() -> bool:
    """True when your team leads.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Team Is Winning'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_1() -> Transform:
    """Position of team player 1.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Team Player 1'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_1_has_ball() -> bool:
    """True when team player 1 holds the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Team Player 1 Has Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_1_stamina() -> float:
    """Stamina of team player 1.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Team Player 1 Stamina'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_2() -> Transform:
    """Position of team player 2.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Team Player 2'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_2_has_ball() -> bool:
    """True when team player 2 holds the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Team Player 2 Has Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_2_stamina() -> float:
    """Stamina of team player 2.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Team Player 2 Stamina'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_3() -> Transform:
    """Position of team player 3.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Team Player 3'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_3_has_ball() -> bool:
    """True when team player 3 holds the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Team Player 3 Has Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_3_stamina() -> float:
    """Stamina of team player 3.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Team Player 3 Stamina'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_4() -> Transform:
    """Position of team player 4.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Team Player 4'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_4_has_ball() -> bool:
    """True when team player 4 holds the ball.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Team Player 4 Has Ball'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_4_stamina() -> float:
    """Stamina of team player 4.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Team Player 4 Stamina'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_possession() -> float:
    """Your possession share 0-1.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Team Possession %'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_score() -> float:
    """Your team goals.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Team Score'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_scored_last_point() -> bool:
    """True when your team scored last.

    Returns: bool (game node SoccerGetBool).
    Game label: 'Team Scored Last Point'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def team_shots() -> float:
    """Your team shot count.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Team Shots'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_1_shot_charge() -> float:
    """Shot charge of teammate 1.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Teammate 1 Shot Charge'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_2_shot_charge() -> float:
    """Shot charge of teammate 2.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Teammate 2 Shot Charge'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_3_shot_charge() -> float:
    """Shot charge of teammate 3.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Teammate 3 Shot Charge'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_4_shot_charge() -> float:
    """Shot charge of teammate 4.

    Returns: float (game node SoccerGetFloat).
    Game label: 'Teammate 4 Shot Charge'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_opponent_goal() -> Transform:
    """Teammate closest to their goal.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Teammate Nearest Opponent Goal'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_team_goal() -> Transform:
    """Teammate closest to your goal.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Teammate Nearest Team Goal'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_team_player_1() -> Transform:
    """Teammate closest to your player 1.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Teammate Nearest Team Player 1'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_team_player_2() -> Transform:
    """Teammate closest to your player 2.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Teammate Nearest Team Player 2'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_team_player_3() -> Transform:
    """Teammate closest to your player 3.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Teammate Nearest Team Player 3'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_team_player_4() -> Transform:
    """Teammate closest to your player 4.

    Returns: transform (game node SoccerGetTransform).
    Game label: 'Teammate Nearest Team Player 4'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def upper_corner_away_side() -> Vector3:
    """Corner position, away side upper.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Upper Corner Away Side'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def upper_corner_home_side() -> Vector3:
    """Corner position, home side upper.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Upper Corner Home Side'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def upper_corner_opposing_side() -> Vector3:
    """Opposing corner, upper.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Upper Corner Opposing Side'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def upper_corner_team_side() -> Vector3:
    """Team corner, upper.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Upper Corner Team Side'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def upper_midfield() -> Vector3:
    """Midfield position, upper.

    Returns: vector3 (game node SoccerGetVector3).
    Game label: 'Upper Midfield'.
    Connections are automatic: use the return value directly;     illegal uses fail at compile time."""
    raise RuntimeError('author stub: compile with graphc')

def move(x: float, z: float) -> None:
    """Drive to field position (x, z). Exactly one controller call per tick.

    Args: x (float), z (float). Exactly one call per tick.
    Connections are automatic; type mismatches fail loudly."""
    raise RuntimeError('author stub: compile with graphc')

