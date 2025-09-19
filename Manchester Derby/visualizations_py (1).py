"""
Custom visualization components for football analytics dashboard
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mplsoccer import Pitch
import seaborn as sns
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional

class FootballVisualizer:
    """
    Custom visualization components for football analytics
    """
    
    @staticmethod
    def create_xg_timeline(xg_data: pd.DataFrame, team_colors: Dict) -> go.Figure:
        """
        Create interactive xG timeline with events
        
        Args:
            xg_data: DataFrame with minute-by-minute xG data
            team_colors: Dictionary with team colors
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        # Add xG lines with fill
        fig.add_trace(go.Scatter(
            x=xg_data['minute'],
            y=xg_data['home_xg'],
            mode='lines+markers',
            name='Home Team',
            line=dict(color=team_colors.get('home', '#6CABDD'), width=3),
            fill='tonexty',
            fillcolor=f"rgba({','.join(map(str, hex_to_rgb(team_colors.get('home', '#6CABDD'))))}, 0.3)",
            hovertemplate='<b>Home Team</b><br>Minute: %{x}<br>xG: %{y:.2f}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=xg_data['minute'],
            y=xg_data['away_xg'],
            mode='lines+markers',
            name='Away Team',
            line=dict(color=team_colors.get('away', '#DA020E'), width=3),
            fill='tozeroy',
            fillcolor=f"rgba({','.join(map(str, hex_to_rgb(team_colors.get('away', '#DA020E'))))}, 0.3)",
            hovertemplate='<b>Away Team</b><br>Minute: %{x}<br>xG: %{y:.2f}<extra></extra>'
        ))
        
        # Add goal annotations
        goal_events = xg_data[xg_data['event_type'] == 'goal']
        for _, event in goal_events.iterrows():
            fig.add_annotation(
                x=event['minute'],
                y=max(event['home_xg'], event['away_xg']) + 0.1,
                text=f"⚽ {event['minute']}'<br>{event.get('player', '')}",
                showarrow=True,
                arrowhead=2,
                arrowcolor="green",
                bgcolor="white",
                bordercolor="green",
                borderwidth=2
            )
        
        fig.update_layout(
            title="Expected Goals Timeline",
            xaxis_title="Match Time (minutes)",
            yaxis_title="Cumulative xG",
            template="plotly_dark",
            height=500,
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def create_player_radar(player_stats: Dict, team_color: str, position: str) -> go.Figure:
        """
        Create player performance radar chart
        
        Args:
            player_stats: Player statistics dictionary
            team_color: Team color hex code
            position: Player position
            
        Returns:
            Plotly radar chart figure
        """
        # Position-specific metrics
        metric_mappings = {
            'GK': ['Shot Stopping', 'Distribution', 'Sweeping', 'Command', 'Reflexes'],
            'DEF': ['Defending', 'Passing', 'Aerial', 'Tackling', 'Positioning'],
            'MID': ['Passing', 'Vision', 'Pressing', 'Dribbling', 'Work Rate'],
            'ATT': ['Shooting', 'Dribbling', 'Pace', 'Finishing', 'Movement']
        }
        
        pos_key = position[:3].upper() if position else 'MID'
        metrics = metric_mappings.get(pos_key, metric_mappings['MID'])
        
        # Map stats to radar values (0-100 scale)
        values = []
        for metric in metrics:
            metric_key = metric.lower().replace(' ', '_')
            raw_value = player_stats.get(metric_key, 50)
            # Normalize to 0-100 scale
            normalized_value = min(100, max(0, raw_value))
            values.append(normalized_value)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],  # Close the shape
            theta=metrics + [metrics[0]],
            fill='toself',
            name=player_stats.get('name', 'Player'),
            line_color=team_color,
            fillcolor=f"rgba({','.join(map(str, hex_to_rgb(team_color)))}, 0.3)"
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10)
                ),
                angularaxis=dict(
                    tickfont=dict(size=12)
                )
            ),
            title=f"{player_stats.get('name', 'Player')} - Performance Profile",
            template="plotly_dark",
            height=500
        )
        
        return fig
    
    @staticmethod
    def create_pass_network_heatmap(pass_data: pd.DataFrame, players: List[str]) -> go.Figure:
        """
        Create pass network heatmap
        
        Args:
            pass_data: DataFrame with pass combinations
            players: List of player names
            
        Returns:
            Plotly heatmap figure
        """
        # Create pass matrix
        pass_matrix = np.zeros((len(players), len(players)))
        
        for _, row in pass_data.iterrows():
            from_idx = players.index(row['from_player']) if row['from_player'] in players else -1
            to_idx = players.index(row['to_player']) if row['to_player'] in players else -1
            
            if from_idx >= 0 and to_idx >= 0:
                pass_matrix[from_idx][to_idx] = row['passes']
        
        fig = px.imshow(
            pass_matrix,
            x=players,
            y=players,
            color_continuous_scale='Blues',
            title="Pass Network Intensity",
            labels=dict(x="To Player", y="From Player", color="Passes")
        )
        
        fig.update_layout(
            template="plotly_dark",
            height=600
        )
        
        return fig
    
    @staticmethod
    def create_formation_pitch(player_positions: Dict, team_color: str, formation: str) -> plt.Figure:
        """
        Create formation visualization on pitch
        
        Args:
            player_positions: Dictionary of player positions
            team_color: Team color hex code
            formation: Formation string (e.g., "4-3-3")
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        # Create pitch
        pitch = Pitch(
            pitch_color='#1a5d1a',
            line_color='white',
            linewidth=2,
            pitch_type='opta'
        )
        
        pitch.draw(ax=ax)
        
        # Plot player positions
        for player, position in player_positions.items():
            x, y = position['x'], position['y']
            touches = position.get('touches', 50)
            
            # Size based on touches
            size = max(300, min(800, touches * 8))
            
            ax.scatter(x, y, s=size, color=team_color, 
                      edgecolors='white', linewidth=2, zorder=5, alpha=0.8)
            
            # Player name
            name = player.split()[-1] if ' ' in player else player
            ax.text(x, y-3, name, fontsize=8, ha='center', 
                   color='white', weight='bold')
            
            # Touch count
            ax.text(x, y+3, str(touches), fontsize=6, ha='center', 
                   color='white', alpha=0.8)
        
        ax.set_title(f'Formation: {formation} - Average Positions', 
                    fontsize=16, color='white', pad=20)
        
        # Set dark background
        fig.patch.set_facecolor('#0d1421')
        ax.set_facecolor('#1a5d1a')
        
        return fig
    
    @staticmethod
    def create_player_heatmap(heatmap_data: List[Tuple], team_color: str, player_name: str) -> plt.Figure:
        """
        Create player position heatmap
        
        Args:
            heatmap_data: List of (x, y, intensity) tuples
            team_color: Team color hex code
            player_name: Player name for title
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        # Create pitch
        pitch = Pitch(
            pitch_color='#0d1421',
            line_color='white',
            linewidth=2,
            pitch_type='opta'
        )
        
        pitch.draw(ax=ax)
        
        # Plot heatmap points
        for x, y, intensity in heatmap_data:
            ax.scatter(x, y, s=intensity*80, c=team_color, 
                      alpha=0.7, edgecolors='white', linewidth=1)
            
            # Add intensity labels
            ax.text(x, y, str(intensity), fontsize=8, ha='center', va='center',
                   color='white', weight='bold')
        
        ax.set_title(f'{player_name} - Position Heatmap', 
                    fontsize=16, color='white', pad=20)
        
        # Set dark background
        fig.patch.set_facecolor('#0d1421')
        
        return fig
    
    @staticmethod
    def create_momentum_chart(momentum_data: pd.DataFrame) -> go.Figure:
        """
        Create match momentum visualization
        
        Args:
            momentum_data: DataFrame with momentum by periods
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        # Home momentum
        fig.add_trace(go.Bar(
            x=momentum_data['period'],
            y=momentum_data['home_momentum'],
            name='Home Team Momentum',
            marker_color='#6CABDD',
            text=momentum_data['home_momentum'],
            textposition='auto'
        ))
        
        # Away momentum
        fig.add_trace(go.Bar(
            x=momentum_data['period'],
            y=momentum_data['away_momentum'],
            name='Away Team Momentum',
            marker_color='#DA020E',
            text=momentum_data['away_momentum'],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Match Momentum by Period",
            xaxis_title="Time Period",
            yaxis_title="xG Change",
            template="plotly_dark",
            barmode='group',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_advanced_metrics_dashboard(metrics: Dict) -> go.Figure:
        """
        Create dashboard for advanced metrics
        
        Args:
            metrics: Dictionary of advanced metrics
            
        Returns:
            Plotly subplot figure
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("PPDA Intensity", "Field Tilt", "Pass Accuracy", "Duel Success"),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "indicator"}]]
        )
        
        # PPDA comparison
        fig.add_trace(
            go.Bar(x=['Home', 'Away'], y=metrics.get('ppda', [8.2, 15.1]),
                   marker_color=['#6CABDD', '#DA020E'], name="PPDA"),
            row=1, col=1
        )
        
        # Field tilt
        fig.add_trace(
            go.Scatter(x=[1, 2], y=metrics.get('field_tilt', [68, 32]),
                      mode='markers+lines', marker_size=20, name="Field Tilt"),
            row=1, col=2
        )
        
        # Pass accuracy
        fig.add_trace(
            go.Bar(x=['Home', 'Away'], y=metrics.get('pass_accuracy', [89, 78]),
                   marker_color=['#6CABDD', '#DA020E'], name="Pass %"),
            row=2, col=1
        )
        
        # Overall performance indicator
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=metrics.get('overall_performance', 75),
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Overall Performance"},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "#6CABDD"},
                       'steps': [{'range': [0, 50], 'color': "lightgray"},
                               {'range': [50, 80], 'color': "gray"}],
                       'threshold': {'line': {'color': "red", 'width': 4},
                                   'thickness': 0.75, 'value': 90}}
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            template="plotly_dark",
            height=600,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_tactical_analysis_viz(tactical_data: Dict) -> go.Figure:
        """
        Create tactical analysis visualization
        
        Args:
            tactical_data: Dictionary with tactical metrics
            
        Returns:
            Plotly figure object
        """
        # Create formation comparison
        formations = tactical_data.get('formations', {})
        
        fig = go.Figure()
        
        # Formation effectiveness radar
        categories = ['Attacking', 'Defensive', 'Possession', 'Pressing', 'Transitions']
        home_values = [85, 75, 90, 88, 82]
        away_values = [65, 78, 60, 72, 68]
        
        fig.add_trace(go.Scatterpolar(
            r=home_values + [home_values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Home Formation',
            line_color='#6CABDD'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=away_values + [away_values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Away Formation',
            line_color='#DA020E'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            title="Tactical Formation Effectiveness",
            template="plotly_dark"
        )
        
        return fig
    
    @staticmethod
    def create_prediction_dashboard(predictions: Dict) -> go.Figure:
        """
        Create prediction dashboard
        
        Args:
            predictions: Dictionary with prediction data
            
        Returns:
            Plotly subplot figure
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Next Match Win %", "Goals Prediction", "Form Trend", "Performance Risk"),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "scatter"}, {"type": "indicator"}]]
        )
        
        # Win probability
        teams = ['Home', 'Away']
        win_probs = predictions.get('win_probability', [75, 45])
        
        fig.add_trace(
            go.Bar(x=teams, y=win_probs, 
                   marker_color=['#6CABDD', '#DA020E'],
                   text=[f"{p}%" for p in win_probs],
                   textposition='auto'),
            row=1, col=1
        )
        
        # Goals prediction
        matches = ['Next 1', 'Next 2', 'Next 3', 'Next 4', 'Next 5']
        home_goals = predictions.get('goals_for_home', [2.3, 1.8, 2.1, 1.9, 2.0])
        away_goals = predictions.get('goals_for_away', [1.2, 1.5, 1.1, 1.3, 1.0])
        
        fig.add_trace(
            go.Scatter(x=matches, y=home_goals, name='Home Goals', 
                      line=dict(color='#6CABDD'), mode='lines+markers'),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=matches, y=away_goals, name='Away Goals',
                      line=dict(color='#DA020E'), mode='lines+markers'),
            row=1, col=2
        )
        
        # Form trend
        last_5_games = ['G-5', 'G-4', 'G-3', 'G-2', 'G-1']
        home_form = predictions.get('form_home', [80, 75, 85, 90, 88])
        away_form = predictions.get('form_away', [60, 55, 65, 62, 58])
        
        fig.add_trace(
            go.Scatter(x=last_5_games, y=home_form, name='Home Form',
                      line=dict(color='#6CABDD'), mode='lines+markers'),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=last_5_games, y=away_form, name='Away Form',
                      line=dict(color='#DA020E'), mode='lines+markers'),
            row=2, col=1
        )
        
        # Risk indicator
        risk_score = predictions.get('performance_risk', 25)
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=risk_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Risk Level"},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "red" if risk_score > 70 else "orange" if risk_score > 40 else "green"},
                       'steps': [{'range': [0, 30], 'color': "lightgreen"},
                               {'range': [30, 70], 'color': "yellow"},
                               {'range': [70, 100], 'color': "lightcoral"}]}
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            template="plotly_dark",
            height=700,
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def create_comparative_analysis(team1_data: Dict, team2_data: Dict) -> go.Figure:
        """
        Create comprehensive team comparison
        
        Args:
            team1_data: First team's data
            team2_data: Second team's data
            
        Returns:
            Plotly figure object
        """
        metrics = ['Goals', 'Assists', 'Shots', 'Passes', 'Tackles', 'Interceptions']
        team1_values = [team1_data.get(m.lower(), 0) for m in metrics]
        team2_values = [team2_data.get(m.lower(), 0) for m in metrics]
        
        fig = go.Figure()
        
        # Team 1 radar
        fig.add_trace(go.Scatterpolar(
            r=team1_values + [team1_values[0]],
            theta=metrics + [metrics[0]],
            fill='toself',
            name=team1_data.get('name', 'Team 1'),
            line_color=team1_data.get('color', '#6CABDD')
        ))
        
        # Team 2 radar
        fig.add_trace(go.Scatterpolar(
            r=team2_values + [team2_values[0]],
            theta=metrics + [metrics[0]],
            fill='toself',
            name=team2_data.get('name', 'Team 2'),
            line_color=team2_data.get('color', '#DA020E')
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, max(max(team1_values), max(team2_values))])
            ),
            title="Team Performance Comparison",
            template="plotly_dark"
        )
        
        return fig

# Utility functions
def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_custom_colorscale(team_color: str) -> List:
    """Create custom colorscale for team visualizations"""
    rgb = hex_to_rgb(team_color)
    return [
        [0.0, f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.0)'],
        [0.5, f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.5)'],
        [1.0, f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 1.0)']
    ]

def add_pitch_background(fig: go.Figure) -> go.Figure:
    """Add football pitch background to plotly figure"""
    # Add pitch outline
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=100, y1=100,
        line=dict(color="white", width=2),
        fillcolor="rgba(26, 93, 26, 0.3)"
    )
    
    # Add center line
    fig.add_shape(
        type="line",
        x0=50, y0=0, x1=50, y1=100,
        line=dict(color="white", width=2)
    )
    
    # Add center circle
    fig.add_shape(
        type="circle",
        x0=40, y0=40, x1=60, y1=60,
        line=dict(color="white", width=2)
    )
    
    return fig