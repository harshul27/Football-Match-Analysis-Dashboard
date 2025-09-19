"""
Data processing utilities for football analytics dashboard
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime

class FootballDataProcessor:
    """
    Advanced data processing for football match analytics
    """
    
    def __init__(self):
        self.match_data = {}
        self.player_data = {}
        self.tactical_data = {}
    
    @staticmethod
    def calculate_xg_buildup(events: List[Dict]) -> pd.DataFrame:
        """
        Calculate cumulative xG buildup throughout match
        
        Args:
            events: List of match events with xG values
            
        Returns:
            DataFrame with minute-by-minute xG accumulation
        """
        xg_timeline = []
        home_xg_cumulative = 0
        away_xg_cumulative = 0
        
        for event in events:
            if event.get('xg', 0) > 0:
                if event['team'] == 'home':
                    home_xg_cumulative += event['xg']
                else:
                    away_xg_cumulative += event['xg']
            
            xg_timeline.append({
                'minute': event['minute'],
                'home_xg': round(home_xg_cumulative, 2),
                'away_xg': round(away_xg_cumulative, 2),
                'event_type': event.get('event_type'),
                'player': event.get('player')
            })
        
        return pd.DataFrame(xg_timeline)
    
    @staticmethod
    def calculate_ppda(team_stats: Dict) -> float:
        """
        Calculate Passes Per Defensive Action (PPDA)
        Lower values indicate more intense pressing
        
        Args:
            team_stats: Dictionary containing team statistics
            
        Returns:
            PPDA value (float)
        """
        opponent_passes = team_stats.get('opponent_passes', 0)
        defensive_actions = (
            team_stats.get('tackles', 0) + 
            team_stats.get('interceptions', 0) + 
            team_stats.get('fouls', 0)
        )
        
        return round(opponent_passes / max(defensive_actions, 1), 2)
    
    @staticmethod
    def calculate_field_tilt(possession_zones: Dict) -> float:
        """
        Calculate field tilt percentage
        Higher values indicate more attacking play
        
        Args:
            possession_zones: Dictionary with possession by field zones
            
        Returns:
            Field tilt percentage (float)
        """
        final_third = possession_zones.get('final_third', 0)
        middle_third = possession_zones.get('middle_third', 0) * 0.5
        defensive_third = possession_zones.get('defensive_third', 0) * 0.1
        
        return round((final_third + middle_third + defensive_third), 1)
    
    @staticmethod
    def calculate_player_impact_score(player_stats: Dict) -> float:
        """
        Calculate comprehensive player impact score
        
        Args:
            player_stats: Player's match statistics
            
        Returns:
            Impact score (0-10 scale)
        """
        weights = {
            'goals': 3.0,
            'assists': 2.5,
            'xg': 2.0,
            'xa': 1.5,
            'key_passes': 0.3,
            'progressive_passes': 0.1,
            'progressive_carries': 0.15,
            'shot_creating_actions': 0.4,
            'duels_won': 0.1
        }
        
        impact = 0
        for stat, weight in weights.items():
            impact += player_stats.get(stat, 0) * weight
        
        return round(min(impact, 10), 2)
    
    @staticmethod
    def normalize_radar_metrics(player_stats: Dict, position: str) -> Dict:
        """
        Normalize player statistics for radar chart based on position
        
        Args:
            player_stats: Raw player statistics
            position: Player position (GK, DEF, MID, ATT)
            
        Returns:
            Normalized metrics dictionary (0-100 scale)
        """
        position_benchmarks = {
            'GK': {
                'saves': 8, 'distribution': 85, 'sweeping': 5,
                'commanding': 7, 'shot_stopping': 6
            },
            'DEF': {
                'defending': 12, 'passing': 80, 'aerial': 8,
                'tackling': 10, 'positioning': 90
            },
            'MID': {
                'passing': 85, 'vision': 8, 'pressing': 15,
                'dribbling': 5, 'shooting': 2, 'work_rate': 12
            },
            'ATT': {
                'shooting': 5, 'dribbling': 8, 'pace': 10,
                'finishing': 6, 'creativity': 6, 'movement': 8
            }
        }
        
        benchmarks = position_benchmarks.get(position[:3].upper(), position_benchmarks['MID'])
        normalized = {}
        
        for metric, benchmark in benchmarks.items():
            player_value = player_stats.get(metric, 0)
            normalized[metric] = min(100, (player_value / benchmark) * 100)
        
        return normalized
    
    @staticmethod
    def calculate_formation_compactness(player_positions: List[Tuple]) -> float:
        """
        Calculate team compactness based on player positions
        
        Args:
            player_positions: List of (x, y) coordinates
            
        Returns:
            Compactness value in meters
        """
        if len(player_positions) < 2:
            return 0
        
        positions = np.array(player_positions)
        
        # Calculate average distance between all players
        distances = []
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                dist = np.sqrt(np.sum((positions[i] - positions[j]) ** 2))
                distances.append(dist)
        
        return round(np.mean(distances), 1)
    
    @staticmethod
    def analyze_pass_network(passes: List[Dict]) -> pd.DataFrame:
        """
        Analyze pass network between players
        
        Args:
            passes: List of pass events with sender/receiver info
            
        Returns:
            DataFrame with pass network analysis
        """
        network_data = []
        
        for pass_event in passes:
            network_data.append({
                'from_player': pass_event['from'],
                'to_player': pass_event['to'],
                'passes': 1,
                'progressive': pass_event.get('progressive', False),
                'success': pass_event.get('success', True)
            })
        
        df = pd.DataFrame(network_data)
        
        # Aggregate pass counts
        network_summary = df.groupby(['from_player', 'to_player']).agg({
            'passes': 'sum',
            'progressive': 'sum',
            'success': 'sum'
        }).reset_index()
        
        network_summary['success_rate'] = (
            network_summary['success'] / network_summary['passes'] * 100
        ).round(1)
        
        return network_summary
    
    @staticmethod
    def calculate_momentum_shifts(xg_timeline: pd.DataFrame, window_size: int = 15) -> pd.DataFrame:
        """
        Calculate momentum shifts based on xG changes
        
        Args:
            xg_timeline: DataFrame with minute-by-minute xG
            window_size: Minutes for momentum calculation window
            
        Returns:
            DataFrame with momentum indicators
        """
        momentum_data = []
        
        for i in range(0, len(xg_timeline), window_size):
            window = xg_timeline.iloc[i:i+window_size]
            
            if len(window) > 1:
                home_xg_change = window['home_xg'].iloc[-1] - window['home_xg'].iloc[0]
                away_xg_change = window['away_xg'].iloc[-1] - window['away_xg'].iloc[0]
                
                momentum_data.append({
                    'period': f"{window['minute'].iloc[0]}-{window['minute'].iloc[-1]}'",
                    'home_momentum': round(home_xg_change, 2),
                    'away_momentum': round(away_xg_change, 2),
                    'momentum_shift': 'Home' if home_xg_change > away_xg_change else 'Away'
                })
        
        return pd.DataFrame(momentum_data)
    
    @staticmethod
    def generate_tactical_insights(team_stats: Dict, formation: str) -> List[str]:
        """
        Generate tactical insights based on team performance
        
        Args:
            team_stats: Team statistics dictionary
            formation: Team formation string
            
        Returns:
            List of tactical insight strings
        """
        insights = []
        
        # Possession-based insights
        possession = team_stats.get('possession_percent', 50)
        if possession > 60:
            insights.append(f"High possession ({possession}%) indicates controlling play")
        elif possession < 40:
            insights.append(f"Low possession ({possession}%) suggests counter-attacking approach")
        
        # Pressing insights
        ppda = team_stats.get('ppda', 15)
        if ppda < 10:
            insights.append(f"Intense pressing (PPDA: {ppda}) disrupting opponent build-up")
        elif ppda > 15:
            insights.append(f"Low pressing intensity (PPDA: {ppda}) allowing opponent possession")
        
        # Formation-specific insights
        if '3' in formation and 'wing' in str(team_stats.get('crosses', 0)):
            if team_stats.get('crosses', 0) > 12:
                insights.append("3-back formation enabling effective wing-back attacks")
            else:
                insights.append("3-back formation not maximizing width potential")
        
        # Creative insights
        key_passes = team_stats.get('key_passes', 0)
        if key_passes < 5:
            insights.append("Limited creativity in final third, need more key passes")
        
        return insights
    
    @staticmethod
    def predict_next_match_probability(recent_form: List[Dict], opponent_strength: float = 0.5) -> Dict:
        """
        Simple prediction model for next match
        
        Args:
            recent_form: List of recent match results and performances
            opponent_strength: Opponent relative strength (0-1 scale)
            
        Returns:
            Dictionary with win/draw/loss probabilities
        """
        if not recent_form:
            return {'win': 33.3, 'draw': 33.3, 'loss': 33.3}
        
        # Calculate form factor based on recent results
        form_points = sum([
            3 if match['result'] == 'win' else 1 if match['result'] == 'draw' else 0
            for match in recent_form[-5:]  # Last 5 matches
        ])
        
        max_points = len(recent_form[-5:]) * 3
        form_factor = form_points / max_points if max_points > 0 else 0.5
        
        # Adjust for opponent strength
        base_win_prob = form_factor * 60 * (1 - opponent_strength * 0.3)
        base_loss_prob = (1 - form_factor) * 60 * (opponent_strength + 0.2)
        base_draw_prob = 100 - base_win_prob - base_loss_prob
        
        # Ensure probabilities sum to 100 and are within reasonable bounds
        total = base_win_prob + base_draw_prob + base_loss_prob
        
        return {
            'win': round(max(10, min(80, base_win_prob / total * 100)), 1),
            'draw': round(max(10, min(50, base_draw_prob / total * 100)), 1),
            'loss': round(max(10, min(80, base_loss_prob / total * 100)), 1)
        }

class AdvancedMetrics:
    """
    Calculate innovative football metrics
    """
    
    @staticmethod
    def calculate_overload_index(attacking_players: int, defending_players: int) -> float:
        """
        Calculate numerical overload in specific zones
        
        Args:
            attacking_players: Number of attacking players in zone
            defending_players: Number of defending players in zone
            
        Returns:
            Overload index (ratio)
        """
        return round(attacking_players / max(defending_players, 1), 2)
    
    @staticmethod
    def calculate_defensive_gap_index(midfield_line: float, defensive_line: float) -> float:
        """
        Calculate gap between midfield and defensive lines
        
        Args:
            midfield_line: Average y-coordinate of midfield
            defensive_line: Average y-coordinate of defense
            
        Returns:
            Gap distance in meters
        """
        return round(abs(midfield_line - defensive_line), 1)
    
    @staticmethod
    def calculate_funnel_isolation_metric(dribble_events: List[Dict]) -> int:
        """
        Count successful 1v1 isolation situations
        
        Args:
            dribble_events: List of dribbling events
            
        Returns:
            Number of successful isolations
        """
        isolations = 0
        for event in dribble_events:
            if (event.get('defenders_beaten', 0) == 1 and 
                event.get('successful', False)):
                isolations += 1
        
        return isolations
    
    @staticmethod
    def calculate_run_efficiency(runs: List[Dict]) -> float:
        """
        Calculate efficiency of attacking runs
        
        Args:
            runs: List of attacking run events
            
        Returns:
            Efficiency ratio (successful/total)
        """
        if not runs:
            return 0.0
        
        successful_runs = sum(1 for run in runs if run.get('successful', False))
        return round(successful_runs / len(runs), 3)
    
    @staticmethod
    def calculate_role_vulnerability(player_events: List[Dict], position: str) -> float:
        """
        Calculate positional vulnerability based on events
        
        Args:
            player_events: List of events involving the player
            position: Player's position
            
        Returns:
            Vulnerability index (0-1 scale)
        """
        negative_events = [
            'dispossessed', 'tackle_failed', 'pass_intercepted', 
            'dribble_failed', 'lost_duel'
        ]
        
        total_events = len(player_events)
        negative_count = sum(
            1 for event in player_events 
            if event.get('event_type') in negative_events
        )
        
        return round(negative_count / max(total_events, 1), 3)