"""Author API for target ('soccer', 'v0.12') — GENERATED, do not edit.

Import this in bot projects instead of raw api.* strings:
    import AIA_Comp_Libry.soccer.v012 as t
The compiler maps these to the same ops as the api.* calls.
"""
from __future__ import annotations

TARGET = ('soccer', 'v0.12')

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

def backwards_clear_direction_from_team_carrier() -> object:
    """Clear backwards for the carrier. Game label: 'Backwards clear direction from team carrier'."""
    raise RuntimeError('author stub: compile with graphc')

def ball() -> object:
    """Ball position. Game label: 'Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def ball_carrier_shot_charge() -> float:
    """Shot charge of whoever holds the ball. Game label: 'Ball Carrier Shot Charge'."""
    raise RuntimeError('author stub: compile with graphc')

def ball_carrier_stamina() -> float:
    """Stamina of whoever holds the ball. Game label: 'Ball Carrier Stamina'."""
    raise RuntimeError('author stub: compile with graphc')

def ball_on_opponent_side() -> bool:
    """True when the ball is on their half. Game label: 'Ball On Opponent Side'."""
    raise RuntimeError('author stub: compile with graphc')

def ball_on_team_side() -> bool:
    """True when the ball is on your half. Game label: 'Ball On Team Side'."""
    raise RuntimeError('author stub: compile with graphc')

def ball_speed() -> float:
    """Current ball speed. Game label: 'Ball Speed'."""
    raise RuntimeError('author stub: compile with graphc')

def ball_velocity() -> object:
    """Ball velocity vector. Game label: 'Ball Velocity'."""
    raise RuntimeError('author stub: compile with graphc')

def center_field() -> object:
    """Center spot. Game label: 'Center Field'."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_team_carrier() -> object:
    """Safe clear direction for the carrier. Game label: 'Clear direction from team carrier'."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_team_carrier_avoid_all_walls() -> object:
    """Clear that stays in play. Game label: 'Clear direction from team carrier (avoid all walls)'."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_team_carrier_avoid_goal_lines() -> object:
    """Clear that stays in play past the lines. Game label: 'Clear direction from team carrier (avoid goal lines)'."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_team_carrier_avoid_sidelines() -> object:
    """Clear that stays in past the sidelines. Game label: 'Clear direction from team carrier (avoid sidelines)'."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_teammate_1() -> object:
    """Safe clear direction for teammate 1. Game label: 'Clear direction from Teammate 1'."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_teammate_2() -> object:
    """Safe clear direction for teammate 2. Game label: 'Clear direction from Teammate 2'."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_teammate_3() -> object:
    """Safe clear direction for teammate 3. Game label: 'Clear direction from Teammate 3'."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_teammate_4() -> object:
    """Safe clear direction for teammate 4. Game label: 'Clear direction from Teammate 4'."""
    raise RuntimeError('author stub: compile with graphc')

def current_simulation_time() -> float:
    """Match clock in seconds. Game label: 'Current Simulation Time'."""
    raise RuntimeError('author stub: compile with graphc')

def delta_time() -> float:
    """Frame delta in seconds. Game label: 'Delta Time'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_opponent_1() -> object:
    """Ball direction seen from opponent 1. Game label: 'Direction of ball from Opponent 1'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_opponent_2() -> object:
    """Ball direction seen from opponent 2. Game label: 'Direction of ball from Opponent 2'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_opponent_3() -> object:
    """Ball direction seen from opponent 3. Game label: 'Direction of ball from Opponent 3'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_opponent_4() -> object:
    """Ball direction seen from opponent 4. Game label: 'Direction of ball from Opponent 4'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_teammate_1() -> object:
    """Ball direction seen from teammate 1. Game label: 'Direction of ball from Teammate 1'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_teammate_2() -> object:
    """Ball direction seen from teammate 2. Game label: 'Direction of ball from Teammate 2'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_teammate_3() -> object:
    """Ball direction seen from teammate 3. Game label: 'Direction of ball from Teammate 3'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_teammate_4() -> object:
    """Ball direction seen from teammate 4. Game label: 'Direction of ball from Teammate 4'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_opponent_1() -> object:
    """Where opponent 1 would clear to find a teammate. Game label: 'Direction of clear teammate from Opponent 1'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_opponent_2() -> object:
    """Where opponent 2 would clear to find a teammate. Game label: 'Direction of clear teammate from Opponent 2'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_opponent_3() -> object:
    """Where opponent 3 would clear to find a teammate. Game label: 'Direction of clear teammate from Opponent 3'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_opponent_4() -> object:
    """Where opponent 4 would clear to find a teammate. Game label: 'Direction of clear teammate from Opponent 4'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_teammate_1() -> object:
    """Where teammate 1 should clear to find a teammate. Game label: 'Direction of clear teammate from Teammate 1'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_teammate_2() -> object:
    """Where teammate 2 should clear to find a teammate. Game label: 'Direction of clear teammate from Teammate 2'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_teammate_3() -> object:
    """Where teammate 3 should clear to find a teammate. Game label: 'Direction of clear teammate from Teammate 3'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_teammate_4() -> object:
    """Where teammate 4 should clear to find a teammate. Game label: 'Direction of clear teammate from Teammate 4'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_opponent_goal_from_teammate_1() -> object:
    """Their-goal direction from teammate 1. Game label: 'Direction of opponent goal from Teammate 1'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_opponent_goal_from_teammate_2() -> object:
    """Their-goal direction from teammate 2. Game label: 'Direction of opponent goal from Teammate 2'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_opponent_goal_from_teammate_3() -> object:
    """Their-goal direction from teammate 3. Game label: 'Direction of opponent goal from Teammate 3'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_opponent_goal_from_teammate_4() -> object:
    """Their-goal direction from teammate 4. Game label: 'Direction of opponent goal from Teammate 4'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_team_goal_from_teammate_1() -> object:
    """Own-goal direction from teammate 1. Game label: 'Direction of team goal from Teammate 1'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_team_goal_from_teammate_2() -> object:
    """Own-goal direction from teammate 2. Game label: 'Direction of team goal from Teammate 2'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_team_goal_from_teammate_3() -> object:
    """Own-goal direction from teammate 3. Game label: 'Direction of team goal from Teammate 3'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_team_goal_from_teammate_4() -> object:
    """Own-goal direction from teammate 4. Game label: 'Direction of team goal from Teammate 4'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_teammate_from_team_player_1() -> object:
    """Pass direction from team player 1. Game label: 'Direction of teammate from Team Player 1'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_teammate_from_team_player_2() -> object:
    """Pass direction from team player 2. Game label: 'Direction of teammate from Team Player 2'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_teammate_from_team_player_3() -> object:
    """Pass direction from team player 3. Game label: 'Direction of teammate from Team Player 3'."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_teammate_from_team_player_4() -> object:
    """Pass direction from team player 4. Game label: 'Direction of teammate from Team Player 4'."""
    raise RuntimeError('author stub: compile with graphc')

def distance_from_team_player_1_to_nearest_opponent() -> float:
    """How much space team player 1 has. Game label: 'Distance from Team Player 1 to nearest Opponent'."""
    raise RuntimeError('author stub: compile with graphc')

def distance_from_team_player_2_to_nearest_opponent() -> float:
    """How much space team player 2 has. Game label: 'Distance from Team Player 2 to nearest Opponent'."""
    raise RuntimeError('author stub: compile with graphc')

def distance_from_team_player_3_to_nearest_opponent() -> float:
    """How much space team player 3 has. Game label: 'Distance from Team Player 3 to nearest Opponent'."""
    raise RuntimeError('author stub: compile with graphc')

def distance_from_team_player_4_to_nearest_opponent() -> float:
    """How much space team player 4 has. Game label: 'Distance from Team Player 4 to nearest Opponent'."""
    raise RuntimeError('author stub: compile with graphc')

def field_depth() -> float:
    """Playable field length. Game label: 'Field Depth'."""
    raise RuntimeError('author stub: compile with graphc')

def field_width() -> float:
    """Playable field width. Game label: 'Field Width'."""
    raise RuntimeError('author stub: compile with graphc')

def fixed_delta_time() -> float:
    """Physics tick delta in seconds. Game label: 'Fixed Delta Time'."""
    raise RuntimeError('author stub: compile with graphc')

def get_furthest_open_opponent() -> object:
    """Position of the furthest open opponent. Game label: 'Get furthest open opponent'."""
    raise RuntimeError('author stub: compile with graphc')

def get_furthest_open_teammate() -> object:
    """Position of the furthest open teammate. Game label: 'Get furthest open teammate'."""
    raise RuntimeError('author stub: compile with graphc')

def get_most_open_opponent() -> object:
    """Position of the most open opponent. Game label: 'Get most open opponent'."""
    raise RuntimeError('author stub: compile with graphc')

def get_most_open_teammate() -> object:
    """Position of the most open teammate. Game label: 'Get most open teammate'."""
    raise RuntimeError('author stub: compile with graphc')

def get_nearest_open_opponent() -> object:
    """Position of the nearest open opponent. Game label: 'Get nearest open opponent'."""
    raise RuntimeError('author stub: compile with graphc')

def get_nearest_open_teammate() -> object:
    """Position of the nearest open teammate. Game label: 'Get nearest open teammate'."""
    raise RuntimeError('author stub: compile with graphc')

def goal_height() -> float:
    """Goal height. Game label: 'Goal Height'."""
    raise RuntimeError('author stub: compile with graphc')

def goal_width() -> float:
    """Goal mouth width. Game label: 'Goal Width'."""
    raise RuntimeError('author stub: compile with graphc')

def is_active_graph() -> bool:
    """True when this graph is the one driving the player. Game label: 'Is Active Graph'."""
    raise RuntimeError('author stub: compile with graphc')

def is_away_team() -> bool:
    """True when this brain plays the away team. Game label: 'Is Away Team'."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_headed_towards_opponent_goal() -> bool:
    """True when ball velocity aims at their goal. Game label: 'Is Ball Headed Towards Opponent Goal'."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_headed_towards_team_goal() -> bool:
    """True when ball velocity aims at your goal. Game label: 'Is Ball Headed Towards Team Goal'."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_loose() -> bool:
    """True when nobody holds the ball. Game label: 'Is Ball Loose'."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_opponent_player_1() -> bool:
    """True when the ball is near opponent 1. Game label: 'Is Ball Nearby Opponent Player 1'."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_opponent_player_2() -> bool:
    """True when the ball is near opponent 2. Game label: 'Is Ball Nearby Opponent Player 2'."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_opponent_player_3() -> bool:
    """True when the ball is near opponent 3. Game label: 'Is Ball Nearby Opponent Player 3'."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_opponent_player_4() -> bool:
    """True when the ball is near opponent 4. Game label: 'Is Ball Nearby Opponent Player 4'."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_team_player_1() -> bool:
    """True when the ball is near team player 1. Game label: 'Is Ball Nearby Team Player 1'."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_team_player_2() -> bool:
    """True when the ball is near team player 2. Game label: 'Is Ball Nearby Team Player 2'."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_team_player_3() -> bool:
    """True when the ball is near team player 3. Game label: 'Is Ball Nearby Team Player 3'."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_team_player_4() -> bool:
    """True when the ball is near team player 4. Game label: 'Is Ball Nearby Team Player 4'."""
    raise RuntimeError('author stub: compile with graphc')

def is_home_team() -> bool:
    """True when this brain plays the home team. Game label: 'Is Home Team'."""
    raise RuntimeError('author stub: compile with graphc')

def is_kickoff() -> bool:
    """True during kickoff setup. Game label: 'Is Kickoff'."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_kicking_off() -> bool:
    """True when the opponent kicks off. Game label: 'Is Opponent Kicking off'."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_1_closest_opponent_to_ball() -> bool:
    """True when opponent 1 is the closest opponent to the ball. Game label: 'Is Opponent Player 1 Closest Opponent to Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_1_open() -> bool:
    """True when opponent 1 has no close marker. Game label: 'Is Opponent Player 1 Open'."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_2_closest_opponent_to_ball() -> bool:
    """True when opponent 2 is the closest opponent to the ball. Game label: 'Is Opponent Player 2 Closest Opponent to Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_2_open() -> bool:
    """True when opponent 2 has no close marker. Game label: 'Is Opponent Player 2 Open'."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_3_closest_opponent_to_ball() -> bool:
    """True when opponent 3 is the closest opponent to the ball. Game label: 'Is Opponent Player 3 Closest Opponent to Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_3_open() -> bool:
    """True when opponent 3 has no close marker. Game label: 'Is Opponent Player 3 Open'."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_4_closest_opponent_to_ball() -> bool:
    """True when opponent 4 is the closest opponent to the ball. Game label: 'Is Opponent Player 4 Closest Opponent to Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_4_open() -> bool:
    """True when opponent 4 has no close marker. Game label: 'Is Opponent Player 4 Open'."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_kicking_off() -> bool:
    """True when your team kicks off. Game label: 'Is Team Kicking off'."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_1_closest_teammate_to_ball() -> bool:
    """True when team player 1 is the closest teammate to the ball. Game label: 'Is Team Player 1 Closest Teammate to Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_1_open() -> bool:
    """True when team player 1 has no close marker. Game label: 'Is Team Player 1 Open'."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_2_closest_teammate_to_ball() -> bool:
    """True when team player 2 is the closest teammate to the ball. Game label: 'Is Team Player 2 Closest Teammate to Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_2_open() -> bool:
    """True when team player 2 has no close marker. Game label: 'Is Team Player 2 Open'."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_3_closest_teammate_to_ball() -> bool:
    """True when team player 3 is the closest teammate to the ball. Game label: 'Is Team Player 3 Closest Teammate to Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_3_open() -> bool:
    """True when team player 3 has no close marker. Game label: 'Is Team Player 3 Open'."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_4_closest_teammate_to_ball() -> bool:
    """True when team player 4 is the closest teammate to the ball. Game label: 'Is Team Player 4 Closest Teammate to Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_4_open() -> bool:
    """True when team player 4 has no close marker. Game label: 'Is Team Player 4 Open'."""
    raise RuntimeError('author stub: compile with graphc')

def kickoff_circle_radius() -> float:
    """Center circle radius. Game label: 'Kickoff Circle Radius'."""
    raise RuntimeError('author stub: compile with graphc')

def lower_corner_away_side() -> object:
    """Corner position, away side lower. Game label: 'Lower Corner Away Side'."""
    raise RuntimeError('author stub: compile with graphc')

def lower_corner_home_side() -> object:
    """Corner position, home side lower. Game label: 'Lower Corner Home Side'."""
    raise RuntimeError('author stub: compile with graphc')

def lower_corner_opposing_side() -> object:
    """Opposing corner, lower. Game label: 'Lower Corner Opposing Side'."""
    raise RuntimeError('author stub: compile with graphc')

def lower_corner_team_side() -> object:
    """Team corner, lower. Game label: 'Lower Corner Team Side'."""
    raise RuntimeError('author stub: compile with graphc')

def lower_midfield() -> object:
    """Midfield position, lower. Game label: 'Lower Midfield'."""
    raise RuntimeError('author stub: compile with graphc')

def max_simulation_time() -> float:
    """Match length in seconds. Game label: 'Max Simulation Time'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_attacking() -> float:
    """Share of opponent play in attack 0-1. Game label: 'Opponent Attacking %'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_goal_center() -> object:
    """Middle of their goal. Game label: 'Opponent Goal Center'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_goal_left_post() -> object:
    """Their left post. Game label: 'Opponent Goal Left Post'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_goal_right_post() -> object:
    """Their right post. Game label: 'Opponent Goal Right Post'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_has_ball() -> bool:
    """True when an opponent holds the ball. Game label: 'Opponent Has Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_is_winning() -> bool:
    """True when the opponent leads. Game label: 'Opponent Is Winning'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_opponent_goal() -> object:
    """Opponent closest to their goal. Game label: 'Opponent Nearest Opponent Goal'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_team_goal() -> object:
    """Opponent closest to your goal. Game label: 'Opponent Nearest Team Goal'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_team_player_1() -> object:
    """Opponent closest to your player 1. Game label: 'Opponent Nearest Team Player 1'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_team_player_2() -> object:
    """Opponent closest to your player 2. Game label: 'Opponent Nearest Team Player 2'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_team_player_3() -> object:
    """Opponent closest to your player 3. Game label: 'Opponent Nearest Team Player 3'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_team_player_4() -> object:
    """Opponent closest to your player 4. Game label: 'Opponent Nearest Team Player 4'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_teammate_player_1_stamina() -> float:
    """Stamina of the opponent nearest your player 1. Game label: 'Opponent Nearest Teammate Player 1 Stamina'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_teammate_player_2_stamina() -> float:
    """Stamina of the opponent nearest your player 2. Game label: 'Opponent Nearest Teammate Player 2 Stamina'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_teammate_player_3_stamina() -> float:
    """Stamina of the opponent nearest your player 3. Game label: 'Opponent Nearest Teammate Player 3 Stamina'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_teammate_player_4_stamina() -> float:
    """Stamina of the opponent nearest your player 4. Game label: 'Opponent Nearest Teammate Player 4 Stamina'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_1() -> object:
    """Position of opponent 1. Game label: 'Opponent Player 1'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_1_has_ball() -> bool:
    """True when opponent 1 holds the ball. Game label: 'Opponent Player 1 Has Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_1_stamina() -> float:
    """Stamina of opponent 1. Game label: 'Opponent Player 1 Stamina'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_2() -> object:
    """Position of opponent 2. Game label: 'Opponent Player 2'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_2_has_ball() -> bool:
    """True when opponent 2 holds the ball. Game label: 'Opponent Player 2 Has Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_2_stamina() -> float:
    """Stamina of opponent 2. Game label: 'Opponent Player 2 Stamina'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_3() -> object:
    """Position of opponent 3. Game label: 'Opponent Player 3'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_3_has_ball() -> bool:
    """True when opponent 3 holds the ball. Game label: 'Opponent Player 3 Has Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_3_stamina() -> float:
    """Stamina of opponent 3. Game label: 'Opponent Player 3 Stamina'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_4() -> object:
    """Position of opponent 4. Game label: 'Opponent Player 4'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_4_has_ball() -> bool:
    """True when opponent 4 holds the ball. Game label: 'Opponent Player 4 Has Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_4_stamina() -> float:
    """Stamina of opponent 4. Game label: 'Opponent Player 4 Stamina'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_possession() -> float:
    """Opponent possession share 0-1. Game label: 'Opponent Possession %'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_score() -> float:
    """Opponent goals. Game label: 'Opponent Score'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_scored_last_point() -> bool:
    """True when the opponent scored last. Game label: 'Opponent Scored Last Point'."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_shots() -> float:
    """Opponent shot count. Game label: 'Opponent Shots'."""
    raise RuntimeError('author stub: compile with graphc')

def pi() -> float:
    """3.14159. Game label: 'Pi'."""
    raise RuntimeError('author stub: compile with graphc')

def player_interact_radius() -> float:
    """How close a player must be to touch the ball. Game label: 'Player Interact Radius'."""
    raise RuntimeError('author stub: compile with graphc')

def simulation_time_remaining() -> float:
    """Seconds left on the clock. Game label: 'Simulation Time Remaining'."""
    raise RuntimeError('author stub: compile with graphc')

def stamina_of_last_defending_opponent() -> float:
    """Stamina of the last defender. Game label: 'Stamina of last defending opponent'."""
    raise RuntimeError('author stub: compile with graphc')

def team_attacking() -> float:
    """Share of your play in attack 0-1. Game label: 'Team Attacking %'."""
    raise RuntimeError('author stub: compile with graphc')

def team_goal_center() -> object:
    """Middle of your goal. Game label: 'Team Goal Center'."""
    raise RuntimeError('author stub: compile with graphc')

def team_goal_left_post() -> object:
    """Your left post. Game label: 'Team Goal Left Post'."""
    raise RuntimeError('author stub: compile with graphc')

def team_goal_right_post() -> object:
    """Your right post. Game label: 'Team Goal Right Post'."""
    raise RuntimeError('author stub: compile with graphc')

def team_has_ball() -> bool:
    """True when a teammate (or you) holds the ball. Game label: 'Team Has Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def team_is_winning() -> bool:
    """True when your team leads. Game label: 'Team Is Winning'."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_1() -> object:
    """Position of team player 1. Game label: 'Team Player 1'."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_1_has_ball() -> bool:
    """True when team player 1 holds the ball. Game label: 'Team Player 1 Has Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_1_stamina() -> float:
    """Stamina of team player 1. Game label: 'Team Player 1 Stamina'."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_2() -> object:
    """Position of team player 2. Game label: 'Team Player 2'."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_2_has_ball() -> bool:
    """True when team player 2 holds the ball. Game label: 'Team Player 2 Has Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_2_stamina() -> float:
    """Stamina of team player 2. Game label: 'Team Player 2 Stamina'."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_3() -> object:
    """Position of team player 3. Game label: 'Team Player 3'."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_3_has_ball() -> bool:
    """True when team player 3 holds the ball. Game label: 'Team Player 3 Has Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_3_stamina() -> float:
    """Stamina of team player 3. Game label: 'Team Player 3 Stamina'."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_4() -> object:
    """Position of team player 4. Game label: 'Team Player 4'."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_4_has_ball() -> bool:
    """True when team player 4 holds the ball. Game label: 'Team Player 4 Has Ball'."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_4_stamina() -> float:
    """Stamina of team player 4. Game label: 'Team Player 4 Stamina'."""
    raise RuntimeError('author stub: compile with graphc')

def team_possession() -> float:
    """Your possession share 0-1. Game label: 'Team Possession %'."""
    raise RuntimeError('author stub: compile with graphc')

def team_score() -> float:
    """Your team goals. Game label: 'Team Score'."""
    raise RuntimeError('author stub: compile with graphc')

def team_scored_last_point() -> bool:
    """True when your team scored last. Game label: 'Team Scored Last Point'."""
    raise RuntimeError('author stub: compile with graphc')

def team_shots() -> float:
    """Your team shot count. Game label: 'Team Shots'."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_1_shot_charge() -> float:
    """Shot charge of teammate 1. Game label: 'Teammate 1 Shot Charge'."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_2_shot_charge() -> float:
    """Shot charge of teammate 2. Game label: 'Teammate 2 Shot Charge'."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_3_shot_charge() -> float:
    """Shot charge of teammate 3. Game label: 'Teammate 3 Shot Charge'."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_4_shot_charge() -> float:
    """Shot charge of teammate 4. Game label: 'Teammate 4 Shot Charge'."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_opponent_goal() -> object:
    """Teammate closest to their goal. Game label: 'Teammate Nearest Opponent Goal'."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_team_goal() -> object:
    """Teammate closest to your goal. Game label: 'Teammate Nearest Team Goal'."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_team_player_1() -> object:
    """Teammate closest to your player 1. Game label: 'Teammate Nearest Team Player 1'."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_team_player_2() -> object:
    """Teammate closest to your player 2. Game label: 'Teammate Nearest Team Player 2'."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_team_player_3() -> object:
    """Teammate closest to your player 3. Game label: 'Teammate Nearest Team Player 3'."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_team_player_4() -> object:
    """Teammate closest to your player 4. Game label: 'Teammate Nearest Team Player 4'."""
    raise RuntimeError('author stub: compile with graphc')

def upper_corner_away_side() -> object:
    """Corner position, away side upper. Game label: 'Upper Corner Away Side'."""
    raise RuntimeError('author stub: compile with graphc')

def upper_corner_home_side() -> object:
    """Corner position, home side upper. Game label: 'Upper Corner Home Side'."""
    raise RuntimeError('author stub: compile with graphc')

def upper_corner_opposing_side() -> object:
    """Opposing corner, upper. Game label: 'Upper Corner Opposing Side'."""
    raise RuntimeError('author stub: compile with graphc')

def upper_corner_team_side() -> object:
    """Team corner, upper. Game label: 'Upper Corner Team Side'."""
    raise RuntimeError('author stub: compile with graphc')

def upper_midfield() -> object:
    """Midfield position, upper. Game label: 'Upper Midfield'."""
    raise RuntimeError('author stub: compile with graphc')

def move(x: float, z: float) -> None:
    """Drive to field position (x, z). Exactly one controller call per tick."""
    raise RuntimeError('author stub: compile with graphc')

