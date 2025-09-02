import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Inter Miami CF - Professional Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Global Styles for improved contrast */
    body {
        color: #2c3e50; /* A dark, readable gray */
    }

    .main-header {
        background: linear-gradient(135deg, #FF1493, #FF69B4, #000000);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .section-header {
        color: #2c3e50; /* Ensuring section headers are dark and visible */
        border-bottom: 3px solid #FF1493;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Updated tactical summary cards for better contrast and clean design */
    .insight-card {
        border-left: 4px solid #10B981;
        background: #F8F9FA;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    
    .weakness-card {
        border-left: 4px solid #EF4444;
        background: #F8F9FA;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    
    .recommendation-card {
        border-left: 4px solid #3B82F6;
        background: #F8F9FA;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }

    /* Streamlit overrides for contrast */
    [data-testid="stMetricValue"] {
        color: #2c3e50;
    }
    
    [data-testid="stMetricLabel"] {
        color: #555;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'Season Overview'

# Data definitions
@st.cache_data
def load_data():
    # Season Overview Statistics
    season_overview = {
        'matches': 21, 'wins': 12, 'draws': 4, 'losses': 5, 'points': 40,
        'position': 4, 'goalsFor': 36, 'goalsAgainst': 28, 'goalDifference': 8,
        'possessionAvg': 58.2, 'passAccuracy': 87.3, 'shotsPerGame': 16.8,
        'shotsOnTargetPerGame': 5.9, 'xG': 34.2, 'xGA': 22.1, 'xGDiff': 12.1
    }
    
    # Match Analysis Data
    match_data = pd.DataFrame([
        {'match': 'vs Nashville', 'date': '2025-03-02', 'possession': 61, 'shots': 18, 'xG': 2.1, 'xGA': 0.8},
        {'match': 'vs Charlotte', 'date': '2025-03-09', 'possession': 68, 'shots': 22, 'xG': 2.8, 'xGA': 0.4},
        {'match': '@ Montreal', 'date': '2025-03-17', 'possession': 52, 'shots': 13, 'xG': 1.2, 'xGA': 1.9},
        {'match': 'vs Colorado', 'date': '2025-03-30', 'possession': 59, 'shots': 17, 'xG': 1.8, 'xGA': 1.3},
        {'match': '@ NY Red Bulls', 'date': '2025-04-06', 'possession': 55, 'shots': 15, 'xG': 1.4, 'xGA': 1.6},
        {'match': 'vs Atlanta', 'date': '2025-04-14', 'possession': 63, 'shots': 19, 'xG': 2.6, 'xGA': 1.7}
    ])
    
    # Player Performance Data
    player_stats = pd.DataFrame([
        {'name': 'Lionel Messi', 'position': 'RW/AM', 'age': 37, 'apps': 19, 'goals': 17, 'assists': 15, 'xG': 15.2, 'rating': 8.9},
        {'name': 'Luis Suárez', 'position': 'ST', 'age': 37, 'apps': 18, 'goals': 8, 'assists': 4, 'xG': 9.1, 'rating': 7.2},
        {'name': 'Telasco Segovia', 'position': 'CM', 'age': 21, 'apps': 20, 'goals': 4, 'assists': 7, 'xG': 3.8, 'rating': 7.5},
        {'name': 'Jordi Alba', 'position': 'LB', 'age': 35, 'apps': 17, 'goals': 2, 'assists': 6, 'xG': 1.2, 'rating': 6.8},
        {'name': 'Sergio Busquets', 'position': 'CDM', 'age': 35, 'apps': 19, 'goals': 1, 'assists': 3, 'xG': 0.8, 'rating': 7.0}
    ])
    
    # League Comparison Data
    league_comparison = pd.DataFrame([
        {'metric': 'Progressive Passes/Game', 'miami': 47.8, 'league_avg': 52.3, 'percentile': 35},
        {'metric': 'Progressive Carries/Game', 'miami': 12.4, 'league_avg': 14.8, 'percentile': 28},
        {'metric': 'PPDA (Lower = Better)', 'miami': 14.7, 'league_avg': 12.8, 'percentile': 15},
        {'metric': 'High Turnovers/Game', 'miami': 8.4, 'league_avg': 11.2, 'percentile': 32},
        {'metric': 'Final Third Entries/Game', 'miami': 31.2, 'league_avg': 28.7, 'percentile': 72},
        {'metric': 'Build-up Success %', 'miami': 78.2, 'league_avg': 72.6, 'percentile': 78},
        {'metric': 'Counterpress Success %', 'miami': 61.7, 'league_avg': 67.4, 'percentile': 25},
        {'metric': 'Pressure Regains/Game', 'miami': 23.1, 'league_avg': 28.3, 'percentile': 22}
    ])
    
    # Pressing Metrics
    pressing_metrics = pd.DataFrame([
        {'team': 'Miami', 'ppda': 14.7, 'defensive_actions': 51.3, 'pressures_successful': 48.2, 'high_turnovers': 8.4, 'counterpress_success': 61.7},
        {'team': 'League Avg', 'ppda': 12.8, 'defensive_actions': 58.7, 'pressures_successful': 52.8, 'high_turnovers': 11.2, 'counterpress_success': 67.4},
        {'team': 'Elite Teams', 'ppda': 9.6, 'defensive_actions': 67.2, 'pressures_successful': 58.9, 'high_turnovers': 15.8, 'counterpress_success': 74.2}
    ])
    
    # Attacking Patterns
    attacking_patterns = pd.DataFrame([
        {'pattern': 'Messi-Busquets-Alba Triangle', 'frequency': 18.7, 'success': 74, 'avg_length': 4.2, 'zones': 'Left Mid-Final'},
        {'pattern': 'Central Overloads (Messi Drop)', 'frequency': 23.4, 'success': 68, 'avg_length': 3.8, 'zones': 'Central Mid'},
        {'pattern': 'Wide Rotations (Alba-Taylor)', 'frequency': 14.2, 'success': 61, 'avg_length': 5.1, 'zones': 'Left Wing'},
        {'pattern': 'Direct to Suárez', 'frequency': 19.8, 'success': 58, 'avg_length': 2.1, 'zones': 'Central Final'},
        {'pattern': 'Switch of Play', 'frequency': 12.3, 'success': 72, 'avg_length': 3.6, 'zones': 'Full Width'},
        {'pattern': 'Counter Attacks', 'frequency': 11.6, 'success': 69, 'avg_length': 4.9, 'zones': 'Transition'}
    ])
    
    # Movement Analysis
    movement_analysis = pd.DataFrame([
        {'zone': 'Defensive Third', 'player': 'Avilés', 'position': 'Left CB', 'touches': 342, 'progressive': 48, 'regains': 67, 'effectiveness': 72},
        {'zone': 'Defensive Third', 'player': 'Allen', 'position': 'Right CB', 'touches': 298, 'progressive': 42, 'regains': 71, 'effectiveness': 68},
        {'zone': 'Middle Third', 'player': 'Busquets', 'position': 'CDM', 'touches': 467, 'progressive': 89, 'regains': 34, 'effectiveness': 85},
        {'zone': 'Middle Third', 'player': 'Segovia', 'position': 'LCM', 'touches': 387, 'progressive': 67, 'regains': 28, 'effectiveness': 78},
        {'zone': 'Attacking Third', 'player': 'Messi', 'position': 'RW', 'touches': 234, 'progressive': 78, 'regains': 12, 'effectiveness': 92},
        {'zone': 'Attacking Third', 'player': 'Suárez', 'position': 'ST', 'touches': 187, 'progressive': 32, 'regains': 8, 'effectiveness': 71}
    ])
    
    return season_overview, match_data, player_stats, league_comparison, pressing_metrics, attacking_patterns, movement_analysis

# Load data
season_overview, match_data, player_stats, league_comparison, pressing_metrics, attacking_patterns, movement_analysis = load_data()

# Header
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 3rem; margin: 0;">Inter Miami CF</h1>
    <h2 style="margin: 0.5rem 0;">Professional Tactical Analysis Dashboard</h2>
    <p style="margin: 0; opacity: 0.9;">2025 MLS Season • Updated September 1, 2025</p>
    <div style="display: flex; justify-content: space-around; margin-top: 1.5rem;">
        <div>
            <h3 style="margin: 0; font-size: 2.5rem;">#4</h3>
            <p style="margin: 0;">Eastern Conference</p>
        </div>
        <div>
            <h3 style="margin: 0; font-size: 2.5rem;">40</h3>
            <p style="margin: 0;">Points</p>
        </div>
        <div>
            <h3 style="margin: 0; font-size: 2.5rem;">{}</h3>
            <p style="margin: 0;">Win Rate</p>
        </div>
    </div>
</div>
""".format(f"{(season_overview['wins']/season_overview['matches']*100):.1f}%"), unsafe_allow_html=True)

# Navigation Tabs - Emojis removed
tabs = st.tabs(["Season Overview", "Advanced Metrics", "Player Analytics", "Tactical Intelligence"])

# Season Overview Tab
with tabs[0]:
    st.markdown('<h2 class="section-header">Season Overview</h2>', unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Record", f"{season_overview['wins']}-{season_overview['draws']}-{season_overview['losses']}")
    with col2:
        st.metric("Goals For", season_overview['goalsFor'])
    with col3:
        st.metric("Goals Against", season_overview['goalsAgainst'])
    with col4:
        st.metric("xG Difference", f"+{season_overview['xGDiff']:.1f}")
    with col5:
        st.metric("Possession", f"{season_overview['possessionAvg']:.1f}%")
    with col6:
        st.metric("Pass Accuracy", f"{season_overview['passAccuracy']:.1f}%")
    
    st.markdown("---")
    
    # Performance Trend Chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Season Performance Trend")
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=match_data['date'], 
            y=match_data['xG'],
            mode='lines+markers',
            name='Expected Goals For',
            line=dict(color='#10B981', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=match_data['date'], 
            y=match_data['xGA'],
            mode='lines+markers',
            name='Expected Goals Against',
            line=dict(color='#EF4444', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=match_data['date'], 
            y=match_data['possession']/20,  # Scale for visibility
            mode='lines+markers',
            name='Possession % (scaled)',
            line=dict(color='#FF1493', width=2),
            marker=dict(size=6),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Match-by-Match Performance Analysis",
            xaxis_title="Date",
            yaxis_title="Expected Goals",
            yaxis2=dict(overlaying='y', side='right', title='Possession %'),
            height=400,
            hovermode='x unified',
            font=dict(color="#2c3e50")
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Performance Distribution")
        
        # Win/Draw/Loss Pie Chart
        labels = ['Wins', 'Draws', 'Losses']
        values = [season_overview['wins'], season_overview['draws'], season_overview['losses']]
        colors = ['#10B981', '#F59E0B', '#EF4444']
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values,
            hole=0.4,
            marker_colors=colors
        )])
        
        fig_pie.update_layout(
            title="Season Results",
            height=300,
            font=dict(color="#2c3e50")
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Key Performance Indicators
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #10B981, #059669); color: white; padding: 1rem; border-radius: 10px; text-align: center;">
            <h3 style="margin: 0; font-size: 2rem;">{(season_overview['wins']/season_overview['matches']*100):.1f}%</h3>
            <p style="margin: 0;">Win Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #3B82F6, #1D4ED8); color: white; padding: 1rem; border-radius: 10px; text-align: center;">
            <h3 style="margin: 0; font-size: 2rem;">{(season_overview['goalsFor']/season_overview['matches']):.1f}</h3>
            <p style="margin: 0;">Goals per Game</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #8B5CF6, #7C3AED); color: white; padding: 1rem; border-radius: 10px; text-align: center;">
            <h3 style="margin: 0; font-size: 2rem;">{(season_overview['xG']/season_overview['matches']):.1f}</h3>
            <p style="margin: 0;">xG per Game</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FF1493, #DC1435); color: white; padding: 1rem; border-radius: 10px; text-align: center;">
            <h3 style="margin: 0; font-size: 2rem;">{(season_overview['shotsOnTargetPerGame']/season_overview['shotsPerGame']*100):.1f}%</h3>
            <p style="margin: 0;">Shots on Target %</p>
        </div>
        """, unsafe_allow_html=True)

# Advanced Metrics Tab
with tabs[1]:
    st.markdown('<h2 class="section-header">Advanced Metrics Analysis</h2>', unsafe_allow_html=True)
    
    # League Comparison Chart
    st.subheader("Advanced Metrics vs League Average")
    
    fig_comparison = go.Figure()
    
    fig_comparison.add_trace(go.Bar(
        x=league_comparison['metric'],
        y=league_comparison['miami'],
        name='Inter Miami',
        marker_color='#FF1493'
    ))
    
    fig_comparison.add_trace(go.Bar(
        x=league_comparison['metric'],
        y=league_comparison['league_avg'],
        name='League Average',
        marker_color='#6B7280'
    ))
    
    fig_comparison.update_layout(
        title="Key Metrics Comparison",
        xaxis_title="Metrics",
        yaxis_title="Values",
        height=500,
        xaxis_tickangle=-45,
        font=dict(color="#2c3e50")
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # PPDA Analysis
    st.subheader("PPDA & Pressing Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background: #FEF2F2; border-left: 4px solid #EF4444; padding: 1.5rem; text-align: center; border-radius: 10px;">
            <h2 style="color: #EF4444; margin: 0; font-size: 2.5rem;">14.7</h2>
            <p style="margin: 0; font-weight: bold; color: #333;">Miami PPDA</p>
            <p style="margin: 0; font-size: 0.8rem; color: #444;">Passes Allowed Per Def. Action</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #FFFBEB; border-left: 4px solid #F59E0B; padding: 1.5rem; text-align: center; border-radius: 10px;">
            <h2 style="color: #F59E0B; margin: 0; font-size: 2.5rem;">12.8</h2>
            <p style="margin: 0; font-weight: bold; color: #333;">League Average</p>
            <p style="margin: 0; font-size: 0.8rem; color: #444;">League Standard</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: #F0FDF4; border-left: 4px solid #10B981; padding: 1.5rem; text-align: center; border-radius: 10px;">
            <h2 style="color: #10B981; margin: 0; font-size: 2.5rem;">9.6</h2>
            <p style="margin: 0; font-weight: bold; color: #333;">Elite Teams</p>
            <p style="margin: 0; font-size: 0.8rem; color: #444;">Top Quartile</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Radar Chart for Pressing Metrics
    st.subheader("Pressing Intensity Comparison")
    
    categories = ['Defensive Actions', 'Pressure Success', 'High Turnovers', 'Counterpress Success']
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=[51.3, 48.2, 8.4, 61.7],
        theta=categories,
        fill='toself',
        name='Miami',
        fillcolor='rgba(255, 20, 147, 0.3)',
        line=dict(color='#FF1493', width=3)
    ))
    
    fig_radar.add_trace(go.Scatterpolar(
        r=[58.7, 52.8, 11.2, 67.4],
        theta=categories,
        fill='toself',
        name='League Avg',
        fillcolor='rgba(245, 158, 11, 0.1)',
        line=dict(color='#F59E0B', width=2)
    ))
    
    fig_radar.add_trace(go.Scatterpolar(
        r=[67.2, 58.9, 15.8, 74.2],
        theta=categories,
        fill='toself',
        name='Elite Teams',
        fillcolor='rgba(16, 185, 129, 0.1)',
        line=dict(color='#10B981', width=2)
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 80],
                tickfont=dict(color="#444")
            ),
            angularaxis=dict(
                tickfont=dict(color="#444")
            )
        ),
        showlegend=True,
        height=500,
        font=dict(color="#2c3e50")
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Territory Control
    st.subheader("Territory Control Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        territory_data = pd.DataFrame({
            'Zone': ['Final Third', 'Middle Third', 'Own Half'],
            'Time_Percentage': [31.2, 39.9, 28.9],
            'Colors': ['#10B981', '#F59E0B', '#EF4444']
        })
        
        fig_territory = px.bar(
            territory_data, 
            x='Zone', 
            y='Time_Percentage',
            color='Colors',
            color_discrete_map={color: color for color in territory_data['Colors']},
            title="Field Territory Distribution"
        )
        
        fig_territory.update_layout(
            font=dict(color="#2c3e50"),
            xaxis=dict(tickfont=dict(color="#2c3e50")),
            yaxis=dict(tickfont=dict(color="#2c3e50"))
        )
        st.plotly_chart(fig_territory, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #3B82F6, #1D4ED8); color: white; padding: 1.5rem; border-radius: 10px; text-align: center; margin-bottom: 1rem;">
            <h2 style="margin: 0; font-size: 2.5rem;">0.67</h2>
            <p style="margin: 0; font-weight: bold;">Field Tilt</p>
            <p style="margin: 0; font-size: 0.8rem;">Attacking Direction Bias</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #8B5CF6, #7C3AED); color: white; padding: 1.5rem; border-radius: 10px; text-align: center;">
            <h2 style="margin: 0; font-size: 2.5rem;">42.8m</h2>
            <p style="margin: 0; font-weight: bold;">Avg Defensive Line</p>
            <p style="margin: 0; font-size: 0.8rem;">Field Position</p>
        </div>
        """, unsafe_allow_html=True)

# Player Analytics Tab
with tabs[2]:
    st.markdown('<h2 class="section-header">Player Performance Analytics</h2>', unsafe_allow_html=True)
    
    # Player Performance Table
    st.subheader("Player Statistics Overview")
    
    # Updated function to return a solid circle instead of an emoji
    def get_rating_icon(rating):
        if rating >= 8.5:
            return '<div style="background-color:#10B981; border-radius:50%; width:15px; height:15px; margin:auto;"></div>'
        elif rating >= 7.5:
            return '<div style="background-color:#3B82F6; border-radius:50%; width:15px; height:15px; margin:auto;"></div>'
        elif rating >= 7.0:
            return '<div style="background-color:#F59E0B; border-radius:50%; width:15px; height:15px; margin:auto;"></div>'
        else:
            return '<div style="background-color:#EF4444; border-radius:50%; width:15px; height:15px; margin:auto;"></div>'
    
    player_display = player_stats.copy()
    player_display['Rating_Icon'] = player_display['rating'].apply(get_rating_icon)
    player_display['Goals/Game'] = (player_display['goals'] / player_display['apps']).round(2)
    player_display['xG Difference'] = (player_display['goals'] - player_display['xG']).round(1)
    
    st.markdown(player_display[['name', 'position', 'age', 'apps', 'goals', 'assists', 'xG', 'Goals/Game', 'xG Difference', 'rating', 'Rating_Icon']].to_html(escape=False), unsafe_allow_html=True)

    
    # Goals vs Expected Goals Scatter Plot
    st.subheader("Goals vs Expected Goals Analysis")
    
    fig_scatter = px.scatter(
        player_stats, 
        x='xG', 
        y='goals',
        size='rating',
        color='position',
        hover_data=['name', 'assists', 'apps'],
        title="Goals vs Expected Goals by Player"
    )
    
    fig_scatter.add_trace(go.Scatter(
        x=[0, 20], 
        y=[0, 20],
        mode='lines',
        name='Expected Line (Goals = xG)',
        line=dict(dash='dash', color='gray')
    ))
    
    fig_scatter.update_layout(
        height=500,
        font=dict(color="#2c3e50"),
        xaxis=dict(tickfont=dict(color="#2c3e50")),
        yaxis=dict(tickfont=dict(color="#2c3e50"))
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Movement Analysis
    st.subheader("Player Movement & Effectiveness")
    
    for index, player in movement_analysis.iterrows():
        effectiveness_color = "#10B981" if player['effectiveness'] >= 80 else "#F59E0B" if player['effectiveness'] >= 70 else "#EF4444"
        
        st.markdown(f"""
        <div style="border: 2px solid {effectiveness_color}; border-radius: 10px; padding: 1rem; margin: 1rem 0; background: white;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div>
                    <h4 style="margin: 0; font-size: 1.2rem; color: #333;">{player['player']} ({player['position']})</h4>
                    <p style="margin: 0; color: #444; font-size: 0.9rem;">{player['zone']}</p>
                </div>
                <div style="text-align: right;">
                    <h3 style="margin: 0; color: {effectiveness_color}; font-size: 1.8rem;">{player['effectiveness']}%</h3>
                    <p style="margin: 0; color: #444; font-size: 0.8rem;">Effectiveness</p>
                </div>
            </div>
            <div style="display: flex; justify-content: space-around; margin-bottom: 1rem;">
                <div style="text-align: center; background: #F3F4F6; padding: 0.5rem; border-radius: 5px;">
                    <strong style="color: #2c3e50;">{player['touches']}</strong><br><small style="color: #444;">Touches</small>
                </div>
                <div style="text-align: center; background: #F3F4F6; padding: 0.5rem; border-radius: 5px;">
                    <strong style="color: #2c3e50;">{player['progressive']}</strong><br><small style="color: #444;">Progressive</small>
                </div>
                <div style="text-align: center; background: #F3F4F6; padding: 0.5rem; border-radius: 5px;">
                    <strong style="color: #2c3e50;">{player['regains']}</strong><br><small style="color: #444;">Regains</small>
                </div>
            </div>
            <div style="width: 100%; background: #E5E7EB; border-radius: 10px; height: 8px;">
                <div style="width: {player['effectiveness']}%; background: {effectiveness_color}; height: 8px; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Tactical Intelligence Tab
with tabs[3]:
    st.markdown('<h2 class="section-header">Tactical Intelligence Analysis</h2>', unsafe_allow_html=True)
    
    # Attacking Patterns Analysis
    st.subheader("Attacking Patterns & Combinations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pattern Success Rate Chart
        fig_patterns = px.bar(
            attacking_patterns,
            x='pattern',
            y='success',
            color='success',
            color_continuous_scale='RdYlGn',
            title="Pattern Success Rates"
        )
        fig_patterns.update_layout(
            xaxis_tickangle=-45,
            height=400,
            font=dict(color="#2c3e50")
        )
        st.plotly_chart(fig_patterns, use_container_width=True)
    
    with col2:
        # Pattern Frequency Chart
        fig_frequency = px.scatter(
            attacking_patterns,
            x='frequency',
            y='success',
            size='avg_length',
            hover_data=['pattern', 'zones'],
            title="Pattern Frequency vs Success Rate",
            labels={'frequency': 'Uses per Game', 'success': 'Success Rate %'}
        )
        fig_frequency.update_layout(
            font=dict(color="#2c3e50"),
            xaxis=dict(tickfont=dict(color="#2c3e50")),
            yaxis=dict(tickfont=dict(color="#2c3e50"))
        )
        st.plotly_chart(fig_frequency, use_container_width=True)
    
    # Detailed Pattern Analysis
    st.subheader("Detailed Pattern Breakdown")
    
    for index, pattern in attacking_patterns.iterrows():
        success_color = "#10B981" if pattern['success'] >= 70 else "#F59E0B" if pattern['success'] >= 60 else "#EF4444"
        
        st.markdown(f"""
        <div style="border: 1px solid #E5E7EB; border-radius: 10px; padding: 1.5rem; margin: 1rem 0; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div>
                    <h4 style="margin: 0; font-size: 1.2rem; color: #333;">{pattern['pattern']}</h4>
                    <p style="margin: 0.5rem 0; color: #444; font-size: 0.9rem;">Active in: {pattern['zones']}</p>
                </div>
                <div style="background: {success_color}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;">
                    {pattern['success']}% Success
                </div>
            </div>
            <div style="display: flex; justify-content: space-around; margin-bottom: 1rem;">
                <div style="text-align: center; background: #EFF6FF; padding: 1rem; border-radius: 8px; min-width: 80px;">
                    <div style="font-size: 1.5rem; font-weight: bold; color: #3B82F6;">{pattern['frequency']}</div>
                    <div style="font-size: 0.8rem; color: #1D4ED8;">Uses/Game</div>
                </div>
                <div style="text-align: center; background: #F3E8FF; padding: 1rem; border-radius: 8px; min-width: 80px;">
                    <div style="font-size: 1.5rem; font-weight: bold; color: #8B5CF6;">{pattern['avg_length']}</div>
                    <div style="font-size: 0.8rem; color: #7C3AED;">Avg Length</div>
                </div>
                <div style="text-align: center; background: #F0FDF4; padding: 1rem; border-radius: 8px; min-width: 80px;">
                    <div style="font-size: 1.5rem; font-weight: bold; color: #10B981;">{pattern['success']}%</div>
                    <div style="font-size: 0.8rem; color: #059669;">Success Rate</div>
                </div>
            </div>
            <div style="width: 100%; background: #E5E7EB; border-radius: 10px; height: 8px;">
                <div style="width: {pattern['success']}%; background: {success_color}; height: 8px; border-radius: 10px; transition: width 0.5s ease;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Formation Analysis
    st.subheader("Formation Analysis")
    
    formation_data = pd.DataFrame([
        {'formation': '4-3-3', 'usage': 67, 'effectiveness': 76},
        {'formation': '4-2-3-1', 'usage': 24, 'effectiveness': 52},
        {'formation': '3-4-2-1', 'usage': 9, 'effectiveness': 38}
    ])
    
    fig_formation = go.Figure()
    
    fig_formation.add_trace(go.Bar(
        x=formation_data['formation'],
        y=formation_data['usage'],
        name='Usage %',
        marker_color='#FF1493',
        yaxis='y'
    ))
    
    fig_formation.add_trace(go.Bar(
        x=formation_data['formation'],
        y=formation_data['effectiveness'],
        name='Effectiveness %',
        marker_color='#10B981',
        yaxis='y'
    ))
    
    fig_formation.update_layout(
        title="Formation Usage vs Effectiveness",
        xaxis_title="Formation",
        yaxis_title="Percentage",
        barmode='group',
        height=400,
        font=dict(color="#2c3e50")
    )
    
    st.plotly_chart(fig_formation, use_container_width=True)
    
    st.markdown("---")
    
    # Tactical Intelligence Summary - Emojis removed and styling updated
    st.subheader("Tactical Intelligence Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="insight-card">
            <h4 style="color: #059669; margin: 0 0 1rem 0;">Strengths</h4>
            <ul style="margin: 0; padding-left: 1rem; color: #444;">
                <li>High possession control (58.2%)</li>
                <li>Effective build-up play (78.2%)</li>
                <li>Strong final third presence</li>
                <li>Messi-Busquets-Alba triangle</li>
                <li>Superior field tilt (0.67)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="weakness-card">
            <h4 style="color: #DC2626; margin: 0 0 1rem 0;">Weaknesses</h4>
            <ul style="margin: 0; padding-left: 1rem; color: #444;">
                <li>Low pressing intensity (PPDA 14.7)</li>
                <li>Poor counterpress success (61.7%)</li>
                <li>Inconsistent shape discipline</li>
                <li>Limited progressive actions</li>
                <li>Below-average pressure regains</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="recommendation-card">
            <h4 style="color: #1D4ED8; margin: 0 0 1rem 0;">Recommendations</h4>
            <ul style="margin: 0; padding-left: 1rem; color: #444;">
                <li>Increase pressing triggers</li>
                <li>Improve counterpress coordination</li>
                <li>Develop alternative patterns</li>
                <li>Enhance progressive passing</li>
                <li>Work on defensive transitions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tactical Evolution Over Season
    st.subheader("Tactical Evolution Over Season")
    
    fig_evolution = make_subplots(
        specs=[[{"secondary_y": True}]],
        subplot_titles=("Tactical Metrics Evolution",)
    )
    
    fig_evolution.add_trace(
        go.Bar(
            x=match_data['date'],
            y=match_data['possession'],
            name="Possession %",
            marker_color='#FF1493'
        ),
        secondary_y=False,
    )
    
    fig_evolution.add_trace(
        go.Scatter(
            x=match_data['date'],
            y=match_data['xG'],
            mode='lines+markers',
            name="xG",
            line=dict(color='#10B981', width=3)
        ),
        secondary_y=True,
    )
    
    fig_evolution.add_trace(
        go.Scatter(
            x=match_data['date'],
            y=match_data['xGA'],
            mode='lines+markers',
            name="xGA",
            line=dict(color='#EF4444', width=3)
        ),
        secondary_y=True,
    )
    
    fig_evolution.update_xaxes(title_text="Match Date")
    fig_evolution.update_yaxes(title_text="Possession %", secondary_y=False)
    fig_evolution.update_yaxes(title_text="Expected Goals", secondary_y=True)
    
    fig_evolution.update_layout(
        height=500,
        font=dict(color="#2c3e50")
    )
    
    st.plotly_chart(fig_evolution, use_container_width=True)

# Sidebar with additional information - Emojis removed
with st.sidebar:
    st.markdown("### Dashboard Controls")
    
    # Season filter (placeholder for future enhancement)
    season = st.selectbox("Season", ["2025"], index=0)
    
    # Competition filter
    competition = st.selectbox("Competition", ["MLS Regular Season", "All Competitions"], index=0)
    
    # Date range
    st.markdown("### Analysis Period")
    st.markdown("<div style='background-color:#F0FDF4; padding:0.5rem; border-radius:5px; border-left: 4px solid #10B981;'>March 2025 - Current</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Key Insights")
    st.markdown("<div style='background-color:#F0FDF4; padding:0.5rem; border-radius:5px; border-left: 4px solid #10B981;'>**Strong Possession Game** - 58.2% average possession indicates good ball control</div>", unsafe_allow_html=True)
    st.markdown("<div style='background-color:#FEF2F2; padding:0.5rem; border-radius:5px; border-left: 4px solid #EF4444;'>**Pressing Concerns** - PPDA of 14.7 suggests passive defensive approach</div>", unsafe_allow_html=True)
    st.markdown("<div style='background-color:#EFF6FF; padding:0.5rem; border-radius:5px; border-left: 4px solid #3B82F6;'>**Messi Effect** - 17 goals in 19 apps demonstrates exceptional individual impact</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Data Sources")
    st.caption("""
    - MLS Official Match Data
    - SofaScore Advanced Stats  
    - FotMob Player Analytics
    - BeSoccer Tactical Analysis
    """)
    
    st.markdown("---")
    
    st.markdown("### Metrics Glossary")
    
    with st.expander("PPDA"):
        st.write("Passes Allowed Per Defensive Action - measures pressing intensity. Lower values indicate more aggressive pressing.")
    
    with st.expander("xG"):
        st.write("Expected Goals - statistical measure of the quality of chances created/conceded.")
    
    with st.expander("Progressive Actions"):
        st.write("Passes/carries that advance the ball significantly toward the opponent's goal.")
    
    with st.expander("Field Tilt"):
        st.write("Measure of territorial dominance - higher values indicate more attacking play.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1F2937, #111827); color: white; border-radius: 10px; margin-top: 2rem;">
    <h3 style="margin: 0 0 1rem 0;">Professional Football Analytics Dashboard</h3>
    <p style="margin: 0; color: #bbb;">Advanced tactical analysis beyond basic xG metrics</p>
    <p style="margin: 1rem 0 0 0; font-size: 0.8rem; opacity: 0.7; color: #aaa;">
        Comprehensive data integration • Progressive actions • PPDA analysis • Territory control • Tactical patterns
    </p>
    <div style="margin-top: 1rem; display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
        <span style="color:#FFD700;">Real-time Updates</span>
        <span style="color:#FFD700;">Advanced Analytics</span>
        <span style="color:#FFD700;">Tactical Intelligence</span>
    </div>
</div>
""", unsafe_allow_html=True)
