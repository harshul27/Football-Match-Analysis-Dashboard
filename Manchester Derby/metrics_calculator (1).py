"""
Advanced metrics calculator for football analytics
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import math

class Position(Enum):
    """Player positions enumeration"""
    GOALKEEPER = "GK"
    CENTRE_BACK = "CB"
    FULL_BACK = "FB"
    WING_BACK = "WB"
    DEFENSIVE_MIDFIELDER = "CDM"
    CENTRAL_MIDFIELDER = "CM"
    ATTACKING_MIDFIELDER = "CAM"
    WINGER = "W"
    STRIKER = "ST"

@dataclass
class PlayerEvent:
    """Data class for player events"""
    minute: int
    player_id: str
    event_type: str
    x_coordinate: Optional[float] = None
    y_coordinate: Optional[float] = None
    outcome: Optional[bool] = None
    value: Optional[float] = None

class AdvancedMetricsCalculator:
    """
    Calculate advanced football analytics metrics
    """
    
    def __init__(self):
        self.pitch_length = 105  # meters
        self.pitch_width = 68   # meters
    
    def calculate_expected_goals(self, shots: List[Dict]) -> float:
        """
        Calculate Expected Goals (xG) using shot characteristics
        
        Args:
            shots: List of shot events with characteristics
            
        Returns:
            Total xG value
        """
        total_xg = 0.0
        
        for shot in shots:
            # Base probability factors
            distance = shot.get('distance', 20)  # meters from goal
            angle = shot.get('angle', 30)        # degrees
            shot_type = shot.get('type', 'foot')  # foot, header, etc.
            body_part = shot.get('body_part', 'right_foot')
            
            # Distance factor (closer = higher xG)
            distance_factor = max(0.1, 1 - (distance / 35))
            
            # Angle factor (central = higher xG)
            angle_factor = max(0.1, math.cos(math.radians(abs(angle))))
            
            # Shot type multipliers
            type_multipliers = {
                'header': 0.8,
                'foot': 1.0,
                'volley': 1.2,
                'penalty': 0.76
            }
            
            type_factor = type_multipliers.get(shot_type, 1.0)
            
            # Calculate base xG
            base_xg = distance_factor * angle_factor * type_factor
            
            # Apply situational modifiers
            if shot.get('first_time', False):
                base_xg *= 1.1
            if shot.get('through_ball', False):
                base_xg *= 1.15
            if shot.get('counter_attack', False):
                base_xg *= 1.05
            
            # Defensive pressure modifier
            pressure = shot.get('defensive_pressure', 1)  # 0-3 scale
            pressure_modifier = max(0.7, 1 - (pressure * 0.1))
            base_xg *= pressure_modifier
            
            total_xg += min(0.99, max(0.01, base_xg))
        
        return round(total_xg, 3)
    
    def calculate_expected_assists(self, key_passes: List[Dict]) -> float:
        """
        Calculate Expected Assists (xA)
        
        Args:
            key_passes: List of key pass events
            
        Returns:
            Total xA value
        """
        total_xa = 0.0
        
        for pass_event in key_passes:
            # Pass characteristics
            pass_length = pass_event.get('length', 15)
            pass_angle = pass_event.get('angle', 0)
            receiver_position = pass_event.get('receiver_position', {})
            
            # Calculate probability based on receiver's shooting position
            if receiver_position:
                shot_xg = self.calculate_expected_goals([{
                    'distance': receiver_position.get('distance_to_goal', 20),
                    'angle': receiver_position.get('angle_to_goal', 30),
                    'type': 'foot'
                }])
                
                # Adjust for pass difficulty
                pass_difficulty = min(1.0, pass_length / 30)
                xa_value = shot_xg * (1 - pass_difficulty * 0.3)
                
                total_xa += xa_value
        
        return round(total_xa, 3)
    
    def calculate_ppda(self, team_actions: Dict, opponent_actions: Dict) -> float:
        """
        Calculate Passes Per Defensive Action (PPDA)
        
        Args:
            team_actions: Defensive actions by the team
            opponent_actions: Passing actions by opponent
            
        Returns:
            PPDA value (lower = more intense pressing)
        """
        defensive_actions = (
            team_actions.get('tackles', 0) +
            team_actions.get('interceptions', 0) +
            team_actions.get('fouls', 0)
        )
        
        opponent_passes = opponent_actions.get('passes', 0)
        
        if defensive_actions == 0:
            return float('inf')
        
        return round(opponent_passes / defensive_actions, 2)
    
    def calculate_field_tilt(self, team_events: List[PlayerEvent]) -> float:
        """
        Calculate field tilt (territorial dominance)
        
        Args:
            team_events: List of team's events with coordinates
            
        Returns:
            Field tilt percentage (higher = more attacking)
        """
        if not team_events:
            return 50.0
        
        attacking_events = []
        for event in team_events:
            if event.x_coordinate is not None:
                # Convert to attacking direction (0-105m)
                attacking_events.append(event.x_coordinate)
        
        if not attacking_events:
            return 50.0
        
        # Calculate weighted position
        avg_position = np.mean(attacking_events)
        field_tilt = (avg_position / self.pitch_length) * 100
        
        return round(field_tilt, 1)
    
    def calculate_progressive_actions(self, actions: List[Dict]) -> int:
        """
        Calculate progressive passes and carries
        
        Args:
            actions: List of pass/carry events with start and end coordinates
            
        Returns:
            Number of progressive actions
        """
        progressive_count = 0
        
        for action in actions:
            start_x = action.get('start_x', 0)
            end_x = action.get('end_x', 0)
            
            # Progressive threshold: 10m closer to goal
            if end_x - start_x >= 10:
                progressive_count += 1
            
            # Or into final third
            elif start_x < 70 and end_x >= 70:
                progressive_count += 1
        
        return progressive_count
    
    def calculate_shot_creating_actions(self, events: List[Dict]) -> int:
        """
        Calculate shot-creating actions
        
        Args:
            events: List of events leading to shots
            
        Returns:
            Number of shot-creating actions
        """
        sca_count = 0
        shot_creating_types = [
            'pass_before_shot',
            'dribble_before_shot',
            'defensive_action_leading_to_shot',
            'foul_leading_to_shot'
        ]
        
        for event in events:
            if event.get('type') in shot_creating_types:
                sca_count += 1
        
        return sca_count
    
    def calculate_defensive_actions_per_game(self, defensive_events: List[Dict]) -> Dict[str, float]:
        """
        Calculate comprehensive defensive metrics
        
        Args:
            defensive_events: List of defensive actions
            
        Returns:
            Dictionary of defensive metrics
        """
        metrics = {
            'tackles': 0,
            'interceptions': 0,
            'clearances': 0,
            'blocks': 0,
            'aerial_duels_won': 0,
            'ground_duels_won': 0
        }
        
        for event in defensive_events:
            action_type = event.get('type')
            success = event.get('success', False)
            
            if action_type in metrics:
                if success:
                    metrics[action_type] += 1
            elif action_type == 'aerial_duel' and success:
                metrics['aerial_duels_won'] += 1
            elif action_type == 'ground_duel' and success:
                metrics['ground_duels_won'] += 1
        
        return metrics
    
    def calculate_possession_value(self, possession_sequence: List[Dict]) -> float:
        """
        Calculate possession value using Possession Value framework
        
        Args:
            possession_sequence: List of actions in possession sequence
            
        Returns:
            Possession value score
        """
        if not possession_sequence:
            return 0.0
        
        start_position = possession_sequence[0].get('position', {'x': 35, 'y': 34})
        end_position = possession_sequence[-1].get('position', {'x': 35, 'y': 34})
        
        # Calculate field advancement
        field_advancement = end_position['x'] - start_position['x']
        
        # Base value from field position
        end_zone_value = self._get_zone_value(end_position)
        start_zone_value = self._get_zone_value(start_position)
        
        possession_value = (end_zone_value - start_zone_value) + (field_advancement * 0.01)
        
        # Bonus for ending in shooting positions
        final_action = possession_sequence[-1].get('type')
        if final_action == 'shot':
            possession_value += 0.3
        elif final_action == 'key_pass':
            possession_value += 0.2
        elif final_action == 'cross':
            possession_value += 0.15
        
        return round(possession_value, 3)
    
    def _get_zone_value(self, position: Dict) -> float:
        """Get value of field zone based on position"""
        x, y = position.get('x', 35), position.get('y', 34)
        
        # Zone values (higher = more dangerous)
        if x >= 88:  # Penalty box
            return 1.0
        elif x >= 70:  # Final third
            if 20 <= y <= 48:  # Central
                return 0.7
            else:  # Wide
                return 0.5
        elif x >= 35:  # Middle third
            return 0.3
        else:  # Defensive third
            return 0.1
    
    def calculate_player_impact_score(self, player_stats: Dict, position: str, minutes_played: int) -> float:
        """
        Calculate comprehensive player impact score
        
        Args:
            player_stats: Player's match statistics
            position: Player position
            minutes_played: Minutes played in match
            
        Returns:
            Impact score (0-10 scale)
        """
        if minutes_played == 0:
            return 0.0
        
        # Position-specific weights
        weights = self._get_position_weights(position)
        
        # Calculate weighted score
        impact = 0.0
        
        for stat, weight in weights.items():
            stat_value = player_stats.get(stat, 0)
            
            # Per-90 normalization for stats that scale with time
            if stat in ['passes', 'touches', 'duels']:
                stat_value = (stat_value / minutes_played) * 90
            
            impact += stat_value * weight
        
        # Apply position-specific bonuses
        if position in ['ST', 'W']:
            impact += player_stats.get('goals', 0) * 2.0
            impact += player_stats.get('assists', 0) * 1.5
        elif position in ['CB', 'FB', 'CDM']:
            impact += player_stats.get('tackles', 0) * 0.3
            impact += player_stats.get('interceptions', 0) * 0.3
        
        return round(min(impact, 10.0), 2)
    
    def _get_position_weights(self, position: str) -> Dict[str, float]:
        """Get position-specific weights for impact calculation"""
        position_weights = {
            'GK': {
                'saves': 0.4, 'distribution': 0.1, 'sweeper_actions': 0.3,
                'command_of_area': 0.2
            },
            'CB': {
                'tackles': 0.3, 'interceptions': 0.3, 'clearances': 0.2,
                'aerial_duels': 0.2, 'pass_accuracy': 0.1
            },
            'FB': {
                'tackles': 0.2, 'crosses': 0.2, 'progressive_passes': 0.2,
                'duels_won': 0.2, 'assists': 0.2
            },
            'CDM': {
                'tackles': 0.25, 'interceptions': 0.25, 'pass_accuracy': 0.2,
                'progressive_passes': 0.2, 'duels_won': 0.1
            },
            'CM': {
                'pass_accuracy': 0.2, 'progressive_passes': 0.2, 'key_passes': 0.2,
                'tackles': 0.15, 'assists': 0.15, 'shot_creating_actions': 0.1
            },
            'CAM': {
                'key_passes': 0.3, 'assists': 0.25, 'shot_creating_actions': 0.2,
                'dribbles': 0.15, 'goals': 0.1
            },
            'W': {
                'dribbles': 0.25, 'crosses': 0.2, 'assists': 0.2,
                'goals': 0.15, 'key_passes': 0.15, 'pace': 0.05
            },
            'ST': {
                'goals': 0.4, 'shots_on_target': 0.2, 'assists': 0.15,
                'link_up_play': 0.15, 'movement': 0.1
            }
        }
        
        return position_weights.get(position, position_weights['CM'])
    
    def calculate_team_coordination_index(self, pass_network: pd.DataFrame) -> float:
        """
        Calculate team coordination based on pass network
        
        Args:
            pass_network: DataFrame with pass combinations
            
        Returns:
            Coordination index (0-100 scale)
        """
        if pass_network.empty:
            return 0.0
        
        # Calculate pass network density
        total_combinations = len(pass_network)
        unique_players = len(set(pass_network['from_player'].tolist() + 
                               pass_network['to_player'].tolist()))
        
        max_combinations = unique_players * (unique_players - 1)
        network_density = total_combinations / max_combinations if max_combinations > 0 else 0
        
        # Calculate pass distribution (how evenly distributed are passes)
        pass_counts = pass_network['passes'].values
        pass_variance = np.var(pass_counts)
        pass_mean = np.mean(pass_counts)
        
        distribution_score = 1 - (pass_variance / (pass_mean ** 2)) if pass_mean > 0 else 0
        
        # Combine metrics
        coordination_index = (network_density * 0.6 + distribution_score * 0.4) * 100
        
        return round(max(0, min(100, coordination_index)), 1)
    
    def calculate_pressing_triggers(self, events: List[Dict]) -> Dict[str, int]:
        """
        Analyze pressing triggers and success rates
        
        Args:
            events: List of pressing events
            
        Returns:
            Dictionary with pressing analysis
        """
        triggers = {
            'loose_ball': 0,
            'back_pass': 0,
            'poor_touch': 0,
            'wide_position': 0,
            'successful_presses': 0,
            'total_presses': len(events)
        }
        
        for event in events:
            trigger_type = event.get('trigger_type')
            if trigger_type in triggers:
                triggers[trigger_type] += 1
            
            if event.get('successful', False):
                triggers['successful_presses'] += 1
        
        # Calculate success rate
        if triggers['total_presses'] > 0:
            triggers['success_rate'] = round(
                (triggers['successful_presses'] / triggers['total_presses']) * 100, 1
            )
        else:
            triggers['success_rate'] = 0.0
        
        return triggers
    
    def calculate_transition_speed(self, transition_events: List[Dict]) -> Dict[str, float]:
        """
        Calculate transition speeds for different phases
        
        Args:
            transition_events: List of transition events with timestamps
            
        Returns:
            Dictionary with transition metrics
        """
        def_to_att_times = []
        att_to_def_times = []
        
        for event in transition_events:
            transition_type = event.get('type')
            duration = event.get('duration', 0)  # seconds
            
            if transition_type == 'defensive_to_attacking':
                def_to_att_times.append(duration)
            elif transition_type == 'attacking_to_defensive':
                att_to_def_times.append(duration)
        
        return {
            'avg_def_to_att': round(np.mean(def_to_att_times), 1) if def_to_att_times else 0.0,
            'avg_att_to_def': round(np.mean(att_to_def_times), 1) if att_to_def_times else 0.0,
            'fastest_def_to_att': round(min(def_to_att_times), 1) if def_to_att_times else 0.0,
            'fastest_att_to_def': round(min(att_to_def_times), 1) if att_to_def_times else 0.0
        }
    
    def calculate_set_piece_threat(self, set_pieces: List[Dict]) -> Dict[str, float]:
        """
        Calculate set piece threat metrics
        
        Args:
            set_pieces: List of set piece events
            
        Returns:
            Dictionary with set piece metrics
        """
        corners = [sp for sp in set_pieces if sp.get('type') == 'corner']
        free_kicks = [sp for sp in set_pieces if sp.get('type') == 'free_kick']
        throw_ins = [sp for sp in set_pieces if sp.get('type') == 'throw_in']
        
        # Calculate xG from set pieces
        total_xg = sum(sp.get('xg', 0) for sp in set_pieces)
        
        # Success rates
        corner_success = sum(1 for c in corners if c.get('successful', False))
        corner_rate = (corner_success / len(corners)) * 100 if corners else 0
        
        fk_success = sum(1 for fk in free_kicks if fk.get('successful', False))
        fk_rate = (fk_success / len(free_kicks)) * 100 if free_kicks else 0
        
        return {
            'total_set_pieces': len(set_pieces),
            'corners': len(corners),
            'free_kicks': len(free_kicks),
            'throw_ins': len(throw_ins),
            'total_xg': round(total_xg, 2),
            'corner_success_rate': round(corner_rate, 1),
            'free_kick_success_rate': round(fk_rate, 1),
            'set_piece_xg_per_attempt': round(total_xg / len(set_pieces), 3) if set_pieces else 0
        }
    
    def calculate_overload_situations(self, positional_data: List[Dict]) -> Dict[str, int]:
        """
        Calculate numerical overload situations
        
        Args:
            positional_data: List of positional snapshots with player counts by zone
            
        Returns:
            Dictionary with overload analysis
        """
        overloads = {
            'left_flank': 0,
            'right_flank': 0,
            'central': 0,
            'total_situations': 0
        }
        
        for snapshot in positional_data:
            attacking_players = snapshot.get('attacking_players', {})
            defending_players = snapshot.get('defending_players', {})
            
            # Check each zone for numerical advantage
            for zone in ['left_flank', 'right_flank', 'central']:
                att_count = attacking_players.get(zone, 0)
                def_count = defending_players.get(zone, 0)
                
                if att_count > def_count and att_count >= 2:
                    overloads[zone] += 1
                    overloads['total_situations'] += 1
        
        return overloads
    
    def calculate_defensive_line_analysis(self, defensive_events: List[Dict]) -> Dict[str, float]:
        """
        Analyze defensive line positioning and movement
        
        Args:
            defensive_events: List of defensive positioning events
            
        Returns:
            Dictionary with defensive line metrics
        """
        line_heights = []
        line_compactness = []
        offsides_caused = 0
        
        for event in defensive_events:
            if 'line_height' in event:
                line_heights.append(event['line_height'])
            
            if 'line_compactness' in event:
                line_compactness.append(event['line_compactness'])
            
            if event.get('caused_offside', False):
                offsides_caused += 1
        
        return {
            'avg_line_height': round(np.mean(line_heights), 1) if line_heights else 0.0,
            'line_height_variance': round(np.var(line_heights), 1) if line_heights else 0.0,
            'avg_compactness': round(np.mean(line_compactness), 1) if line_compactness else 0.0,
            'offsides_caused': offsides_caused,
            'defensive_stability': round(1 / (np.var(line_heights) + 1), 2) if line_heights else 0.0
        }
    
    def calculate_player_chemistry(self, pass_combinations: List[Dict]) -> Dict[str, float]:
        """
        Calculate chemistry between player pairs
        
        Args:
            pass_combinations: List of pass events between players
            
        Returns:
            Dictionary with chemistry ratings
        """
        chemistry_pairs = {}
        
        # Group passes by player pairs
        for pass_event in pass_combinations:
            from_player = pass_event.get('from')
            to_player = pass_event.get('to')
            success = pass_event.get('successful', True)
            
            if from_player and to_player:
                pair_key = tuple(sorted([from_player, to_player]))
                
                if pair_key not in chemistry_pairs:
                    chemistry_pairs[pair_key] = {'attempts': 0, 'successful': 0}
                
                chemistry_pairs[pair_key]['attempts'] += 1
                if success:
                    chemistry_pairs[pair_key]['successful'] += 1
        
        # Calculate chemistry scores
        chemistry_scores = {}
        for pair, stats in chemistry_pairs.items():
            if stats['attempts'] >= 5:  # Minimum threshold
                success_rate = stats['successful'] / stats['attempts']
                volume_bonus = min(1.2, stats['attempts'] / 20)  # Bonus for high volume
                
                chemistry_score = (success_rate * volume_bonus) * 100
                chemistry_scores[f"{pair[0]}-{pair[1]}"] = round(chemistry_score, 1)
        
        return chemistry_scores
    
    def calculate_fatigue_index(self, physical_data: List[Dict], minutes_played: int) -> Dict[str, float]:
        """
        Calculate player fatigue index based on physical output
        
        Args:
            physical_data: List of physical metrics throughout match
            minutes_played: Total minutes played
            
        Returns:
            Dictionary with fatigue metrics
        """
        if not physical_data or minutes_played == 0:
            return {'fatigue_index': 0.0, 'load_score': 0.0}
        
        # Extract physical metrics
        sprint_distances = [p.get('sprint_distance', 0) for p in physical_data]
        high_intensity_runs = [p.get('high_intensity_runs', 0) for p in physical_data]
        accelerations = [p.get('accelerations', 0) for p in physical_data]
        decelerations = [p.get('decelerations', 0) for p in physical_data]
        
        # Calculate load components
        total_sprint_distance = sum(sprint_distances)
        total_hi_runs = sum(high_intensity_runs)
        total_accelerations = sum(accelerations)
        total_decelerations = sum(decelerations)
        
        # Normalize by minutes played
        sprint_load = (total_sprint_distance / minutes_played) * 90
        intensity_load = (total_hi_runs / minutes_played) * 90
        acceleration_load = ((total_accelerations + total_decelerations) / minutes_played) * 90
        
        # Calculate composite load score
        load_score = (sprint_load * 0.4 + intensity_load * 0.3 + acceleration_load * 0.3)
        
        # Calculate fatigue index (higher = more fatigued)
        # Based on decline in performance metrics over time
        if len(physical_data) > 1:
            early_performance = np.mean([p.get('performance_index', 100) for p in physical_data[:len(physical_data)//2]])
            late_performance = np.mean([p.get('performance_index', 100) for p in physical_data[len(physical_data)//2:]])
            
            fatigue_index = max(0, (early_performance - late_performance) / early_performance * 100)
        else:
            fatigue_index = 0.0
        
        return {
            'fatigue_index': round(fatigue_index, 1),
            'load_score': round(load_score, 1),
            'sprint_load': round(sprint_load, 1),
            'intensity_load': round(intensity_load, 1),
            'acceleration_load': round(acceleration_load, 1)
        }
    
    def calculate_tactical_discipline(self, position_data: List[Dict], formation: str) -> float:
        """
        Calculate tactical discipline score
        
        Args:
            position_data: List of player positions throughout match
            formation: Team formation (e.g., "4-3-3")
            
        Returns:
            Tactical discipline score (0-100)
        """
        if not position_data:
            return 0.0
        
        # Get ideal formation positions
        ideal_positions = self._get_formation_positions(formation)
        
        total_deviation = 0.0
        valid_measurements = 0
        
        for snapshot in position_data:
            player_positions = snapshot.get('positions', {})
            
            for player, actual_pos in player_positions.items():
                if player in ideal_positions:
                    ideal_pos = ideal_positions[player]
                    
                    # Calculate positional deviation
                    deviation = math.sqrt(
                        (actual_pos['x'] - ideal_pos['x']) ** 2 + 
                        (actual_pos['y'] - ideal_pos['y']) ** 2
                    )
                    
                    total_deviation += deviation
                    valid_measurements += 1
        
        if valid_measurements == 0:
            return 0.0
        
        avg_deviation = total_deviation / valid_measurements
        
        # Convert to discipline score (lower deviation = higher discipline)
        max_deviation = 30  # Maximum expected deviation in meters
        discipline_score = max(0, (1 - avg_deviation / max_deviation)) * 100
        
        return round(discipline_score, 1)
    
    def _get_formation_positions(self, formation: str) -> Dict[str, Dict[str, float]]:
        """Get ideal positions for formation"""
        formation_templates = {
            "4-3-3": {
                'GK': {'x': 5, 'y': 34},
                'RB': {'x': 25, 'y': 10}, 'CB1': {'x': 20, 'y': 22}, 
                'CB2': {'x': 20, 'y': 46}, 'LB': {'x': 25, 'y': 58},
                'CDM': {'x': 40, 'y': 34}, 'CM1': {'x': 45, 'y': 22}, 
                'CM2': {'x': 45, 'y': 46},
                'RW': {'x': 70, 'y': 12}, 'ST': {'x': 80, 'y': 34}, 
                'LW': {'x': 70, 'y': 56}
            },
            "3-5-2": {
                'GK': {'x': 5, 'y': 34},
                'CB1': {'x': 20, 'y': 17}, 'CB2': {'x': 20, 'y': 34}, 
                'CB3': {'x': 20, 'y': 51},
                'RWB': {'x': 35, 'y': 8}, 'CDM': {'x': 40, 'y': 34},
                'CM1': {'x': 50, 'y': 24}, 'CM2': {'x': 50, 'y': 44},
                'LWB': {'x': 35, 'y': 60},
                'ST1': {'x': 75, 'y': 26}, 'ST2': {'x': 75, 'y': 42}
            }
        }
        
        return formation_templates.get(formation, formation_templates["4-3-3"])

class PredictiveMetrics:
    """
    Calculate predictive and future-looking metrics
    """
    
    @staticmethod
    def calculate_injury_risk(physical_load: Dict, player_history: Dict) -> Dict[str, Union[float, str]]:
        """
        Calculate injury risk based on load and history
        
        Args:
            physical_load: Current physical load metrics
            player_history: Historical injury data
            
        Returns:
            Dictionary with risk assessment
        """
        # Base risk factors
        current_load = physical_load.get('load_score', 0)
        fatigue_level = physical_load.get('fatigue_index', 0)
        
        # Historical factors
        previous_injuries = player_history.get('injuries_last_12_months', 0)
        games_played = player_history.get('games_played', 30)
        age = player_history.get('age', 25)
        
        # Calculate risk components
        load_risk = min(100, current_load / 10)  # Normalize load
        fatigue_risk = fatigue_level
        history_risk = min(100, previous_injuries * 20)
        age_risk = max(0, (age - 30) * 5)  # Increased risk after 30
        
        # Combined risk score
        total_risk = (load_risk * 0.3 + fatigue_risk * 0.3 + 
                     history_risk * 0.25 + age_risk * 0.15)
        
        # Risk categories
        if total_risk < 20:
            risk_category = "Low"
        elif total_risk < 50:
            risk_category = "Medium"
        elif total_risk < 75:
            risk_category = "High"
        else:
            risk_category = "Very High"
        
        return {
            'risk_score': round(total_risk, 1),
            'risk_category': risk_category,
            'load_component': round(load_risk, 1),
            'fatigue_component': round(fatigue_risk, 1),
            'history_component': round(history_risk, 1),
            'age_component': round(age_risk, 1)
        }
    
    @staticmethod
    def predict_next_match_performance(recent_form: List[Dict], opponent_strength: float) -> Dict[str, float]:
        """
        Predict next match performance metrics
        
        Args:
            recent_form: List of recent match performances
            opponent_strength: Opponent strength rating (0-1)
            
        Returns:
            Dictionary with predicted metrics
        """
        if not recent_form:
            return {
                'predicted_rating': 6.0,
                'goal_probability': 0.15,
                'assist_probability': 0.10,
                'key_passes': 2.0
            }
        
        # Calculate form trends
        recent_ratings = [match.get('rating', 6.0) for match in recent_form[-5:]]
        recent_goals = [match.get('goals', 0) for match in recent_form[-5:]]
        recent_assists = [match.get('assists', 0) for match in recent_form[-5:]]
        recent_key_passes = [match.get('key_passes', 2) for match in recent_form[-5:]]
        
        # Base predictions from recent form
        avg_rating = np.mean(recent_ratings)
        goal_rate = np.mean(recent_goals)
        assist_rate = np.mean(recent_assists)
        key_pass_rate = np.mean(recent_key_passes)
        
        # Adjust for opponent strength
        opponent_adjustment = 1 - (opponent_strength * 0.3)
        
        predicted_rating = avg_rating * opponent_adjustment
        goal_probability = goal_rate * opponent_adjustment
        assist_probability = assist_rate * opponent_adjustment
        predicted_key_passes = key_pass_rate * opponent_adjustment
        
        return {
            'predicted_rating': round(max(4.0, min(10.0, predicted_rating)), 1),
            'goal_probability': round(max(0, min(1, goal_probability)), 3),
            'assist_probability': round(max(0, min(1, assist_probability)), 3),
            'key_passes': round(max(0, predicted_key_passes), 1)
        }
    
    @staticmethod
    def calculate_market_value_impact(performance_change: float, age: int, position: str) -> Dict[str, Union[float, str]]:
        """
        Calculate impact on market value based on performance
        
        Args:
            performance_change: Recent performance change percentage
            age: Player age
            position: Player position
            
        Returns:
            Dictionary with market value analysis
        """
        # Position multipliers for market impact
        position_multipliers = {
            'ST': 1.2, 'CAM': 1.1, 'W': 1.1,
            'CM': 1.0, 'CDM': 0.9, 'CB': 0.8,
            'FB': 0.8, 'GK': 0.7
        }
        
        position_key = position if position in position_multipliers else 'CM'
        position_multiplier = position_multipliers[position_key]
        
        # Age factor (peak years have higher impact)
        if 23 <= age <= 27:
            age_factor = 1.2
        elif 28 <= age <= 30:
            age_factor = 1.0
        elif 31 <= age <= 33:
            age_factor = 0.7
        else:
            age_factor = 0.5
        
        # Calculate value change
        base_impact = performance_change * 0.5  # 50% correlation
        adjusted_impact = base_impact * position_multiplier * age_factor
        
        # Impact categories
        if adjusted_impact > 10:
            impact_category = "Significant Increase"
        elif adjusted_impact > 5:
            impact_category = "Moderate Increase"
        elif adjusted_impact > -5:
            impact_category = "Stable"
        elif adjusted_impact > -10:
            impact_category = "Moderate Decrease"
        else:
            impact_category = "Significant Decrease"
        
        return {
            'value_change_percent': round(adjusted_impact, 1),
            'impact_category': impact_category,
            'position_factor': position_multiplier,
            'age_factor': age_factor,
            'peak_years': 23 <= age <= 27
        }