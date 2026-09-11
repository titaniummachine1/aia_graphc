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

def backwards_clear_direction_from_team_carrier() -> object:
    """Sensor 'Backwards clear direction from team carrier' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def ball() -> object:
    """Sensor 'Ball' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def ball_carrier_shot_charge() -> float:
    """Sensor 'Ball Carrier Shot Charge' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def ball_carrier_stamina() -> float:
    """Sensor 'Ball Carrier Stamina' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def ball_on_opponent_side() -> bool:
    """Sensor 'Ball On Opponent Side' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def ball_on_team_side() -> bool:
    """Sensor 'Ball On Team Side' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def ball_speed() -> float:
    """Sensor 'Ball Speed' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def ball_velocity() -> object:
    """Sensor 'Ball Velocity' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def center_field() -> object:
    """Sensor 'Center Field' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_team_carrier() -> object:
    """Sensor 'Clear direction from team carrier' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_team_carrier_avoid_all_walls() -> object:
    """Sensor 'Clear direction from team carrier (avoid all walls)' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_team_carrier_avoid_goal_lines() -> object:
    """Sensor 'Clear direction from team carrier (avoid goal lines)' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_team_carrier_avoid_sidelines() -> object:
    """Sensor 'Clear direction from team carrier (avoid sidelines)' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_teammate_1() -> object:
    """Sensor 'Clear direction from Teammate 1' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_teammate_2() -> object:
    """Sensor 'Clear direction from Teammate 2' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_teammate_3() -> object:
    """Sensor 'Clear direction from Teammate 3' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def clear_direction_from_teammate_4() -> object:
    """Sensor 'Clear direction from Teammate 4' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def current_simulation_time() -> float:
    """Sensor 'Current Simulation Time' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def delta_time() -> float:
    """Sensor 'Delta Time' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_opponent_1() -> object:
    """Sensor 'Direction of ball from Opponent 1' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_opponent_2() -> object:
    """Sensor 'Direction of ball from Opponent 2' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_opponent_3() -> object:
    """Sensor 'Direction of ball from Opponent 3' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_opponent_4() -> object:
    """Sensor 'Direction of ball from Opponent 4' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_teammate_1() -> object:
    """Sensor 'Direction of ball from Teammate 1' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_teammate_2() -> object:
    """Sensor 'Direction of ball from Teammate 2' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_teammate_3() -> object:
    """Sensor 'Direction of ball from Teammate 3' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_ball_from_teammate_4() -> object:
    """Sensor 'Direction of ball from Teammate 4' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_opponent_1() -> object:
    """Sensor 'Direction of clear teammate from Opponent 1' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_opponent_2() -> object:
    """Sensor 'Direction of clear teammate from Opponent 2' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_opponent_3() -> object:
    """Sensor 'Direction of clear teammate from Opponent 3' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_opponent_4() -> object:
    """Sensor 'Direction of clear teammate from Opponent 4' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_teammate_1() -> object:
    """Sensor 'Direction of clear teammate from Teammate 1' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_teammate_2() -> object:
    """Sensor 'Direction of clear teammate from Teammate 2' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_teammate_3() -> object:
    """Sensor 'Direction of clear teammate from Teammate 3' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_clear_teammate_from_teammate_4() -> object:
    """Sensor 'Direction of clear teammate from Teammate 4' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_opponent_goal_from_teammate_1() -> object:
    """Sensor 'Direction of opponent goal from Teammate 1' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_opponent_goal_from_teammate_2() -> object:
    """Sensor 'Direction of opponent goal from Teammate 2' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_opponent_goal_from_teammate_3() -> object:
    """Sensor 'Direction of opponent goal from Teammate 3' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_opponent_goal_from_teammate_4() -> object:
    """Sensor 'Direction of opponent goal from Teammate 4' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_team_goal_from_teammate_1() -> object:
    """Sensor 'Direction of team goal from Teammate 1' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_team_goal_from_teammate_2() -> object:
    """Sensor 'Direction of team goal from Teammate 2' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_team_goal_from_teammate_3() -> object:
    """Sensor 'Direction of team goal from Teammate 3' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_team_goal_from_teammate_4() -> object:
    """Sensor 'Direction of team goal from Teammate 4' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_teammate_from_team_player_1() -> object:
    """Sensor 'Direction of teammate from Team Player 1' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_teammate_from_team_player_2() -> object:
    """Sensor 'Direction of teammate from Team Player 2' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_teammate_from_team_player_3() -> object:
    """Sensor 'Direction of teammate from Team Player 3' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def direction_of_teammate_from_team_player_4() -> object:
    """Sensor 'Direction of teammate from Team Player 4' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def distance_from_team_player_1_to_nearest_opponent() -> float:
    """Sensor 'Distance from Team Player 1 to nearest Opponent' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def distance_from_team_player_2_to_nearest_opponent() -> float:
    """Sensor 'Distance from Team Player 2 to nearest Opponent' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def distance_from_team_player_3_to_nearest_opponent() -> float:
    """Sensor 'Distance from Team Player 3 to nearest Opponent' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def distance_from_team_player_4_to_nearest_opponent() -> float:
    """Sensor 'Distance from Team Player 4 to nearest Opponent' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def field_depth() -> float:
    """Sensor 'Field Depth' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def field_width() -> float:
    """Sensor 'Field Width' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def fixed_delta_time() -> float:
    """Sensor 'Fixed Delta Time' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def get_furthest_open_opponent() -> object:
    """Sensor 'Get furthest open opponent' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def get_furthest_open_teammate() -> object:
    """Sensor 'Get furthest open teammate' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def get_most_open_opponent() -> object:
    """Sensor 'Get most open opponent' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def get_most_open_teammate() -> object:
    """Sensor 'Get most open teammate' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def get_nearest_open_opponent() -> object:
    """Sensor 'Get nearest open opponent' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def get_nearest_open_teammate() -> object:
    """Sensor 'Get nearest open teammate' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def goal_height() -> float:
    """Sensor 'Goal Height' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def goal_width() -> float:
    """Sensor 'Goal Width' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_active_graph() -> bool:
    """Sensor 'Is Active Graph' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_away_team() -> bool:
    """Sensor 'Is Away Team' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_headed_towards_opponent_goal() -> bool:
    """Sensor 'Is Ball Headed Towards Opponent Goal' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_headed_towards_team_goal() -> bool:
    """Sensor 'Is Ball Headed Towards Team Goal' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_loose() -> bool:
    """Sensor 'Is Ball Loose' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_opponent_player_1() -> bool:
    """Sensor 'Is Ball Nearby Opponent Player 1' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_opponent_player_2() -> bool:
    """Sensor 'Is Ball Nearby Opponent Player 2' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_opponent_player_3() -> bool:
    """Sensor 'Is Ball Nearby Opponent Player 3' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_opponent_player_4() -> bool:
    """Sensor 'Is Ball Nearby Opponent Player 4' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_team_player_1() -> bool:
    """Sensor 'Is Ball Nearby Team Player 1' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_team_player_2() -> bool:
    """Sensor 'Is Ball Nearby Team Player 2' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_team_player_3() -> bool:
    """Sensor 'Is Ball Nearby Team Player 3' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_ball_nearby_team_player_4() -> bool:
    """Sensor 'Is Ball Nearby Team Player 4' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_home_team() -> bool:
    """Sensor 'Is Home Team' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_kickoff() -> bool:
    """Sensor 'Is Kickoff' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_kicking_off() -> bool:
    """Sensor 'Is Opponent Kicking off' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_1_closest_opponent_to_ball() -> bool:
    """Sensor 'Is Opponent Player 1 Closest Opponent to Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_1_open() -> bool:
    """Sensor 'Is Opponent Player 1 Open' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_2_closest_opponent_to_ball() -> bool:
    """Sensor 'Is Opponent Player 2 Closest Opponent to Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_2_open() -> bool:
    """Sensor 'Is Opponent Player 2 Open' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_3_closest_opponent_to_ball() -> bool:
    """Sensor 'Is Opponent Player 3 Closest Opponent to Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_3_open() -> bool:
    """Sensor 'Is Opponent Player 3 Open' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_4_closest_opponent_to_ball() -> bool:
    """Sensor 'Is Opponent Player 4 Closest Opponent to Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_opponent_player_4_open() -> bool:
    """Sensor 'Is Opponent Player 4 Open' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_kicking_off() -> bool:
    """Sensor 'Is Team Kicking off' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_1_closest_teammate_to_ball() -> bool:
    """Sensor 'Is Team Player 1 Closest Teammate to Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_1_open() -> bool:
    """Sensor 'Is Team Player 1 Open' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_2_closest_teammate_to_ball() -> bool:
    """Sensor 'Is Team Player 2 Closest Teammate to Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_2_open() -> bool:
    """Sensor 'Is Team Player 2 Open' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_3_closest_teammate_to_ball() -> bool:
    """Sensor 'Is Team Player 3 Closest Teammate to Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_3_open() -> bool:
    """Sensor 'Is Team Player 3 Open' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_4_closest_teammate_to_ball() -> bool:
    """Sensor 'Is Team Player 4 Closest Teammate to Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def is_team_player_4_open() -> bool:
    """Sensor 'Is Team Player 4 Open' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def kickoff_circle_radius() -> float:
    """Sensor 'Kickoff Circle Radius' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def lower_corner_away_side() -> object:
    """Sensor 'Lower Corner Away Side' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def lower_corner_home_side() -> object:
    """Sensor 'Lower Corner Home Side' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def lower_corner_opposing_side() -> object:
    """Sensor 'Lower Corner Opposing Side' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def lower_corner_team_side() -> object:
    """Sensor 'Lower Corner Team Side' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def lower_midfield() -> object:
    """Sensor 'Lower Midfield' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def max_simulation_time() -> float:
    """Sensor 'Max Simulation Time' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_attacking() -> float:
    """Sensor 'Opponent Attacking %' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_goal_center() -> object:
    """Sensor 'Opponent Goal Center' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_goal_left_post() -> object:
    """Sensor 'Opponent Goal Left Post' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_goal_right_post() -> object:
    """Sensor 'Opponent Goal Right Post' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_has_ball() -> bool:
    """Sensor 'Opponent Has Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_is_winning() -> bool:
    """Sensor 'Opponent Is Winning' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_opponent_goal() -> object:
    """Sensor 'Opponent Nearest Opponent Goal' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_team_goal() -> object:
    """Sensor 'Opponent Nearest Team Goal' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_team_player_1() -> object:
    """Sensor 'Opponent Nearest Team Player 1' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_team_player_2() -> object:
    """Sensor 'Opponent Nearest Team Player 2' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_team_player_3() -> object:
    """Sensor 'Opponent Nearest Team Player 3' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_team_player_4() -> object:
    """Sensor 'Opponent Nearest Team Player 4' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_teammate_player_1_stamina() -> float:
    """Sensor 'Opponent Nearest Teammate Player 1 Stamina' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_teammate_player_2_stamina() -> float:
    """Sensor 'Opponent Nearest Teammate Player 2 Stamina' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_teammate_player_3_stamina() -> float:
    """Sensor 'Opponent Nearest Teammate Player 3 Stamina' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_nearest_teammate_player_4_stamina() -> float:
    """Sensor 'Opponent Nearest Teammate Player 4 Stamina' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_1() -> object:
    """Sensor 'Opponent Player 1' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_1_has_ball() -> bool:
    """Sensor 'Opponent Player 1 Has Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_1_stamina() -> float:
    """Sensor 'Opponent Player 1 Stamina' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_2() -> object:
    """Sensor 'Opponent Player 2' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_2_has_ball() -> bool:
    """Sensor 'Opponent Player 2 Has Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_2_stamina() -> float:
    """Sensor 'Opponent Player 2 Stamina' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_3() -> object:
    """Sensor 'Opponent Player 3' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_3_has_ball() -> bool:
    """Sensor 'Opponent Player 3 Has Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_3_stamina() -> float:
    """Sensor 'Opponent Player 3 Stamina' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_4() -> object:
    """Sensor 'Opponent Player 4' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_4_has_ball() -> bool:
    """Sensor 'Opponent Player 4 Has Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_player_4_stamina() -> float:
    """Sensor 'Opponent Player 4 Stamina' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_possession() -> float:
    """Sensor 'Opponent Possession %' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_score() -> float:
    """Sensor 'Opponent Score' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_scored_last_point() -> bool:
    """Sensor 'Opponent Scored Last Point' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def opponent_shots() -> float:
    """Sensor 'Opponent Shots' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def pi() -> float:
    """Sensor 'Pi' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def player_interact_radius() -> float:
    """Sensor 'Player Interact Radius' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def simulation_time_remaining() -> float:
    """Sensor 'Simulation Time Remaining' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def stamina_of_last_defending_opponent() -> float:
    """Sensor 'Stamina of last defending opponent' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_attacking() -> float:
    """Sensor 'Team Attacking %' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_goal_center() -> object:
    """Sensor 'Team Goal Center' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_goal_left_post() -> object:
    """Sensor 'Team Goal Left Post' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_goal_right_post() -> object:
    """Sensor 'Team Goal Right Post' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_has_ball() -> bool:
    """Sensor 'Team Has Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_is_winning() -> bool:
    """Sensor 'Team Is Winning' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_1() -> object:
    """Sensor 'Team Player 1' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_1_has_ball() -> bool:
    """Sensor 'Team Player 1 Has Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_1_stamina() -> float:
    """Sensor 'Team Player 1 Stamina' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_2() -> object:
    """Sensor 'Team Player 2' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_2_has_ball() -> bool:
    """Sensor 'Team Player 2 Has Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_2_stamina() -> float:
    """Sensor 'Team Player 2 Stamina' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_3() -> object:
    """Sensor 'Team Player 3' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_3_has_ball() -> bool:
    """Sensor 'Team Player 3 Has Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_3_stamina() -> float:
    """Sensor 'Team Player 3 Stamina' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_4() -> object:
    """Sensor 'Team Player 4' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_4_has_ball() -> bool:
    """Sensor 'Team Player 4 Has Ball' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_player_4_stamina() -> float:
    """Sensor 'Team Player 4 Stamina' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_possession() -> float:
    """Sensor 'Team Possession %' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_score() -> float:
    """Sensor 'Team Score' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_scored_last_point() -> bool:
    """Sensor 'Team Scored Last Point' (bool). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def team_shots() -> float:
    """Sensor 'Team Shots' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_1_shot_charge() -> float:
    """Sensor 'Teammate 1 Shot Charge' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_2_shot_charge() -> float:
    """Sensor 'Teammate 2 Shot Charge' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_3_shot_charge() -> float:
    """Sensor 'Teammate 3 Shot Charge' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_4_shot_charge() -> float:
    """Sensor 'Teammate 4 Shot Charge' (float). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_opponent_goal() -> object:
    """Sensor 'Teammate Nearest Opponent Goal' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_team_goal() -> object:
    """Sensor 'Teammate Nearest Team Goal' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_team_player_1() -> object:
    """Sensor 'Teammate Nearest Team Player 1' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_team_player_2() -> object:
    """Sensor 'Teammate Nearest Team Player 2' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_team_player_3() -> object:
    """Sensor 'Teammate Nearest Team Player 3' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def teammate_nearest_team_player_4() -> object:
    """Sensor 'Teammate Nearest Team Player 4' (transform). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def upper_corner_away_side() -> object:
    """Sensor 'Upper Corner Away Side' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def upper_corner_home_side() -> object:
    """Sensor 'Upper Corner Home Side' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def upper_corner_opposing_side() -> object:
    """Sensor 'Upper Corner Opposing Side' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def upper_corner_team_side() -> object:
    """Sensor 'Upper Corner Team Side' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def upper_midfield() -> object:
    """Sensor 'Upper Midfield' (vector3). Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

def move(x: float, z: float) -> None:
    """Soccer controller. Compile-time only."""
    raise RuntimeError('author stub: compile with graphc')

