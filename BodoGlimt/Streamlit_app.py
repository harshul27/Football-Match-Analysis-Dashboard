import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="FK Bodø/Glimt - Tactical Evolution Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom right, #0f172a, #1e3a8a, #0f172a);
    }
    .stMetric {
        background-color: rgba(30, 41, 59, 0.5);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3b82f6;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: #93c5fd;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563eb;
        color: white;
    }
    h1 {
        background: linear-gradient(to right, #fbbf24, #fef08a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .highlight-box {
        background-color: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #fbbf24;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Enhanced Data with more details for all seasons
season_data = pd.DataFrame([
    {"year": 2022, "possession": 54, "xg": 1.3, "goals": 1.31, "pass_acc": 81, "def_line": 40, "vert": 52,
     "matches": 30, "wins": 15, "draws": 7, "losses": 8, "points": 52, "goals_scored": 39, "goals_conceded": 35},
    {"year": 2023, "possession": 57, "xg": 1.55, "goals": 1.65, "pass_acc": 83, "def_line": 43, "vert": 55,
     "matches": 30, "wins": 18, "draws": 4, "losses": 8, "points": 58, "goals_scored": 67, "goals_conceded": 32},
    {"year": 2024, "possession": 50, "xg": 1.7, "goals": 1.75, "pass_acc": 81, "def_line": 44, "vert": 51,
     "matches": 30, "wins": 19, "draws": 5, "losses": 6, "points": 62, "goals_scored": 73, "goals_conceded": 35},
    {"year": 2025, "possession": 54.5, "xg": 2.2, "goals": 2.0, "pass_acc": 84, "def_line": 46, "vert": 57,
     "matches": 30, "wins": 20, "draws": 5, "losses": 5, "points": 65, "goals_scored": 80, "goals_conceded": 28}
])

# Defensive metrics by season
defensive_stats = pd.DataFrame([
    {"year": 2022, "tackles": 15.8, "interceptions": 7.2, "blocks": 2.5, "clearances": 13.5, "duels_won": 51},
    {"year": 2023, "tackles": 16.9, "interceptions": 7.9, "blocks": 2.8, "clearances": 14.2, "duels_won": 54},
    {"year": 2024, "tackles": 17.8, "interceptions": 8.1, "blocks": 2.7, "clearances": 14.8, "duels_won": 52},
    {"year": 2025, "tackles": 19.7, "interceptions": 8.6, "blocks": 2.9, "clearances": 16.1, "duels_won": 56}
])

# Progressive metrics by season
progressive_stats = pd.DataFrame([
    {"year": 2022, "prog_passes": 19.2, "prog_carries": 12.1, "key_passes": 7.8, "big_chances": 1.5},
    {"year": 2023, "prog_passes": 20.8, "prog_carries": 13.1, "key_passes": 8.5, "big_chances": 1.7},
    {"year": 2024, "prog_passes": 21.5, "prog_carries": 13.9, "key_passes": 8.9, "big_chances": 1.9},
    {"year": 2025, "prog_passes": 23.1, "prog_carries": 15.2, "key_passes": 9.7, "big_chances": 2.3}
])

# Shooting efficiency
shooting_stats = pd.DataFrame([
    {"year": 2022, "shots_per_game": 14.2, "shots_on_target": 4.5, "conversion": 12, "shot_accuracy": 31.7},
    {"year": 2023, "shots_per_game": 15.9, "shots_on_target": 4.98, "conversion": 13, "shot_accuracy": 31.3},
    {"year": 2024, "shots_per_game": 16.1, "shots_on_target": 5.21, "conversion": 13, "shot_accuracy": 32.4},
    {"year": 2025, "shots_per_game": 17.3, "shots_on_target": 6.05, "conversion": 15, "shot_accuracy": 35.0}
])

# Goalkeeper stats
gk_stats = pd.DataFrame([
    {"year": 2022, "saves": 38, "clean_sheets": 9, "save_pct": 65, "goals_conceded_90": 1.05},
    {"year": 2023, "saves": 42, "clean_sheets": 11, "save_pct": 69, "goals_conceded_90": 0.95},
    {"year": 2024, "saves": 43, "clean_sheets": 8, "save_pct": 70, "goals_conceded_90": 1.12},
    {"year": 2025, "saves": 51, "clean_sheets": 10, "save_pct": 71, "goals_conceded_90": 0.9}
])

playmakers = pd.DataFrame([
    {"year": 2022, "name": "Berg", "influence": 72, "goals": 3, "assists": 5, "key_passes": 142},
    {"year": 2023, "name": "Vetlesen", "influence": 85, "goals": 8, "assists": 7, "key_passes": 178},
    {"year": 2024, "name": "Hauge", "influence": 78, "goals": 5, "assists": 2, "key_passes": 156},
    {"year": 2025, "name": "Evjen", "influence": 88, "goals": 9, "assists": 11, "key_passes": 195}
])

attack_zones = {
    2022: pd.DataFrame([{"zone": "Left Wing", "value": 62}, {"zone": "Central", "value": 38}]),
    2023: pd.DataFrame([{"zone": "Left Wing", "value": 49}, {"zone": "Half-Space", "value": 32}, {"zone": "Right Flank", "value": 19}]),
    2024: pd.DataFrame([{"zone": "Half-Space", "value": 47}, {"zone": "Left Wing", "value": 37}, {"zone": "Central", "value": 16}]),
    2025: pd.DataFrame([{"zone": "Half-Space", "value": 51}, {"zone": "Right Flank", "value": 39}, {"zone": "Central", "value": 10}])
}

player_stats = {
    "Hogh": pd.DataFrame([
        {"season": 2023, "goals": 7, "xG": 8.1, "assists": 4, "shots": 42, "minutes": 1450},
        {"season": 2024, "goals": 11, "xG": 10.8, "assists": 6, "shots": 61, "minutes": 2045},
        {"season": 2025, "goals": 16, "xG": 14.1, "assists": 5, "shots": 73, "minutes": 1880}
    ]),
    "Berg": pd.DataFrame([
        {"season": 2023, "goals": 2, "assists": 6, "xA": 5.7, "passes": 88.2, "accuracy": 87},
        {"season": 2024, "goals": 4, "assists": 7, "xA": 6.9, "passes": 90.3, "accuracy": 87},
        {"season": 2025, "goals": 3, "assists": 8, "xA": 7.6, "passes": 92.7, "accuracy": 89}
    ]),
    "Hauge": pd.DataFrame([
        {"season": 2023, "goals": 4, "xG": 3.2, "assists": 2, "dribbles": 1.3, "take_ons": 31},
        {"season": 2024, "goals": 5, "xG": 4.6, "assists": 2, "dribbles": 1.4, "take_ons": 39},
        {"season": 2025, "goals": 6, "xG": 5.3, "assists": 3, "dribbles": 1.8, "take_ons": 56}
    ])
}

spurs_match = pd.DataFrame([
    {"minute": 0, "xG": 0, "score": "0-0", "event": "Kick-off"},
    {"minute": 38, "xG": 0.3, "score": "0-0", "event": "Hogh penalty miss (over bar)"},
    {"minute": 53, "xG": 0.7, "score": "1-0", "event": "Hauge goal (left cut-in)"},
    {"minute": 66, "xG": 1.4, "score": "2-0", "event": "Hauge goal (cutback)"},
    {"minute": 68, "xG": 1.6, "score": "2-1", "event": "Van de Ven goal (Spurs)"},
    {"minute": 70, "xG": 2.1, "score": "2-1", "event": "Bjorkan overlap chance"},
    {"minute": 89, "xG": 2.5, "score": "2-2", "event": "Own goal (Gundersen deflection)"},
    {"minute": 90, "xG": 2.5, "score": "2-2", "event": "Full time"}
])

competition_comparison = pd.DataFrame([
    {"metric": "Possession", "Europa": 48, "UCL": 54.5},
    {"metric": "xG", "Europa": 1.4, "UCL": 2.5},
    {"metric": "Shots", "Europa": 13, "UCL": 18},
    {"metric": "Pass Acc", "Europa": 79, "UCL": 84},
    {"metric": "Dribbles", "Europa": 16, "UCL": 22}
])

# Header
st.markdown("<h1>FK Bodø/Glimt</h1>", unsafe_allow_html=True)
st.markdown("### Tactical Evolution Dashboard 2022-2025")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### 🏆 Champions League Debut")
    st.markdown("**2025 Season**")
    st.markdown("---")
    selected_season = st.selectbox("Select Season", [2022, 2023, 2024, 2025], index=3)
    st.markdown("---")
    st.markdown("**Formation:** 4-3-3")
    st.markdown("**Style:** High possession, progressive football")
    st.markdown("---")
    st.markdown("### Season Achievements")
    if selected_season == 2022:
        st.info("AI-based tactical analysis introduced")
    elif selected_season == 2023:
        st.info("Star player Vetlesen sold")
    elif selected_season == 2024:
        st.warning("Hauge returns, Europa League semi-final")
    elif selected_season == 2025:
        st.success("Champions League debut season")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview", 
    "📈 Evolution", 
    "👥 Players", 
    "⚽ Tottenham Match",
    "🛡️ Defensive Analysis",
    "📊 Advanced Metrics"
])

with tab1:
    st.markdown(f"## Season {selected_season} Overview")
    
    # Key Metrics
    season_row = season_data[season_data['year'] == selected_season].iloc[0]
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("Possession", f"{season_row['possession']}%")
    with col2:
        st.metric("xG/Game", f"{season_row['xg']:.2f}")
    with col3:
        st.metric("Goals/Game", f"{season_row['goals']:.2f}")
    with col4:
        st.metric("Pass Accuracy", f"{season_row['pass_acc']}%")
    with col5:
        st.metric("Def Line Height", f"{season_row['def_line']}")
    with col6:
        st.metric("Verticality", f"{season_row['vert']}")
    
    st.markdown("---")
    
    # Season Record
    st.markdown(f"### Season {selected_season} Record")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Matches", season_row['matches'])
    with col2:
        st.metric("Wins", season_row['wins'])
    with col3:
        st.metric("Points", season_row['points'])
    with col4:
        st.metric("Goal Difference", f"+{season_row['goals_scored'] - season_row['goals_conceded']}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Attack Zone Distribution")
        zones_df = attack_zones[selected_season]
        fig = px.bar(zones_df, x='zone', y='value', 
                     color_discrete_sequence=['#fbbf24'],
                     labels={'value': 'Percentage', 'zone': 'Zone'})
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            showlegend=False,
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Pie chart for attack distribution
        st.markdown("#### Attack Distribution")
        fig_pie = px.pie(zones_df, values='value', names='zone',
                         color_discrete_sequence=px.colors.sequential.YlOrRd)
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=300
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("#### Key Playmaker Performance")
        pm_row = playmakers[playmakers['year'] == selected_season].iloc[0]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['Goals', 'Assists', 'Key Passes/10'],
            y=[pm_row['goals'], pm_row['assists'], pm_row['key_passes']/10],
            marker_color=['#fbbf24', '#22c55e', '#3b82f6'],
            text=[pm_row['goals'], pm_row['assists'], pm_row['key_passes']],
            textposition='auto'
        ))
        fig.update_layout(
            title=f"{pm_row['name']} - Season Stats",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Playmaker Influence Over Time")
        for _, pm in playmakers.iterrows():
            cols = st.columns([3, 1])
            with cols[0]:
                st.markdown(f"**{pm['name']}** ({pm['year']})")
                st.progress(pm['influence'] / 100)
            with cols[1]:
                st.markdown(f"**{pm['influence']}%**")

with tab2:
    st.markdown("## 4-Year Tactical Evolution")
    
    # Multi-line chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=season_data['year'], y=season_data['possession'],
                  mode='lines+markers', name='Possession %',
                  line=dict(color='#fbbf24', width=3)),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=season_data['year'], y=season_data['xg'],
                  mode='lines+markers', name='xG/Game',
                  line=dict(color='#ef4444', width=3)),
        secondary_y=True
    )
    fig.add_trace(
        go.Scatter(x=season_data['year'], y=season_data['goals'],
                  mode='lines+markers', name='Goals/Game',
                  line=dict(color='#22c55e', width=3)),
        secondary_y=True
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#93c5fd',
        height=450,
        hovermode='x unified'
    )
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="Possession %", secondary_y=False)
    fig.update_yaxes(title_text="Goals & xG per Game", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Points & Results Progression")
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=season_data['year'], y=season_data['points'],
                              name='Points', marker_color='#fbbf24',
                              text=season_data['points'], textposition='auto'))
        fig2.add_trace(go.Scatter(x=season_data['year'], y=season_data['wins'],
                                  mode='lines+markers', name='Wins',
                                  line=dict(color='#22c55e', width=3),
                                  yaxis='y2'))
        
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=350,
            yaxis2=dict(overlaying='y', side='right')
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("#### Goals Scored vs Conceded")
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=season_data['year'], y=season_data['goals_scored'],
                              name='Goals Scored', marker_color='#22c55e'))
        fig3.add_trace(go.Bar(x=season_data['year'], y=season_data['goals_conceded'],
                              name='Goals Conceded', marker_color='#ef4444'))
        
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=350,
            barmode='group'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("---")
    
    # Progressive stats evolution
    st.markdown("#### Progressive Play Evolution")
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=progressive_stats['year'], y=progressive_stats['prog_passes'],
                              mode='lines+markers', name='Progressive Passes',
                              line=dict(color='#fbbf24', width=2)))
    fig4.add_trace(go.Scatter(x=progressive_stats['year'], y=progressive_stats['prog_carries'],
                              mode='lines+markers', name='Progressive Carries',
                              line=dict(color='#22c55e', width=2)))
    fig4.add_trace(go.Scatter(x=progressive_stats['year'], y=progressive_stats['key_passes'],
                              mode='lines+markers', name='Key Passes',
                              line=dict(color='#3b82f6', width=2)))
    
    fig4.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#93c5fd',
        height=350
    )
    st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### Key Milestones")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info("**2022**\n\nAI intro\n\n52 points")
    with col2:
        st.info("**2023**\n\nVetlesen sale\n\n58 points")
    with col3:
        st.warning("**2024**\n\nHauge return\nEuropa semi\n\n62 points")
    with col4:
        st.success("**2025**\n\nCL debut\nTottenham draw\n\n65 points")

with tab3:
    st.markdown("## Player Performance Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Kasper Hogh")
        hogh_df = player_stats['Hogh']
        
        # Goals vs xG
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hogh_df['season'], y=hogh_df['goals'],
                                mode='lines+markers', name='Goals',
                                line=dict(color='#fbbf24', width=3)))
        fig.add_trace(go.Scatter(x=hogh_df['season'], y=hogh_df['xG'],
                                mode='lines+markers', name='xG',
                                line=dict(color='#ef4444', width=3)))
        fig.update_layout(
            title="Goals vs Expected Goals",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=250
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Shot efficiency
        fig2 = go.Figure()
        hogh_df['shots_per_90'] = (hogh_df['shots'] / hogh_df['minutes']) * 90
        fig2.add_trace(go.Bar(x=hogh_df['season'], y=hogh_df['shots_per_90'],
                              marker_color='#3b82f6',
                              text=hogh_df['shots_per_90'].round(1),
                              textposition='auto'))
        fig2.update_layout(
            title="Shots per 90 Minutes",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=200
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("**2025 Stats:**")
        st.markdown("- 16 goals in 21 matches")
        st.markdown("- 3.5 shots per 90")
        st.markdown("- Overperforming xG by 1.9 goals")
    
    with col2:
        st.markdown("### Patrick Berg")
        berg_df = player_stats['Berg']
        
        # Assists progression
        fig = go.Figure()
        fig.add_trace(go.Bar(x=berg_df['season'], y=berg_df['assists'],
                            name='Assists', marker_color='#fbbf24',
                            text=berg_df['assists'], textposition='auto'))
        fig.add_trace(go.Scatter(x=berg_df['season'], y=berg_df['xA'],
                                mode='lines+markers', name='xA',
                                line=dict(color='#ef4444', width=3)))
        fig.update_layout(
            title="Assists vs Expected Assists",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=250
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Passing accuracy
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=berg_df['season'], y=berg_df['accuracy'],
                                 mode='lines+markers',
                                 line=dict(color='#22c55e', width=3),
                                 marker=dict(size=12)))
        fig2.update_layout(
            title="Pass Accuracy %",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=200,
            yaxis_range=[85, 90]
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("**2025 Stats:**")
        st.markdown("- 8 assists, 7.6 xA")
        st.markdown("- 92.7 passes per 90")
        st.markdown("- 89% pass accuracy")
    
    with col3:
        st.markdown("### Jens Petter Hauge")
        hauge_df = player_stats['Hauge']
        
        # Goals and assists
        fig = go.Figure()
        fig.add_trace(go.Bar(x=hauge_df['season'], y=hauge_df['goals'],
                            name='Goals', marker_color='#fbbf24'))
        fig.add_trace(go.Bar(x=hauge_df['season'], y=hauge_df['assists'],
                            name='Assists', marker_color='#22c55e'))
        fig.update_layout(
            title="Goals and Assists",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=250,
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Dribbling progression
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=hauge_df['season'], y=hauge_df['take_ons'],
                                 mode='lines+markers',
                                 line=dict(color='#a855f7', width=3),
                                 marker=dict(size=12),
                                 fill='tozeroy'))
        fig2.update_layout(
            title="Successful Take-Ons per Season",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=200
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("**2025 Stats:**")
        st.markdown("- 56 successful take-ons")
        st.markdown("- 1.8 dribbles per 90")
        st.markdown("- 34.2 km/h top speed")
    
    st.markdown("---")
    
    # Comparison table
    st.markdown("#### Player Comparison 2025")
    comparison_data = {
        'Player': ['Hogh', 'Berg', 'Hauge'],
        'Goals': [16, 3, 6],
        'Assists': [5, 8, 3],
        'Key Contribution': ['Finishing', 'Playmaking', 'Dribbling']
    }
    st.table(pd.DataFrame(comparison_data))

with tab4:
    st.markdown("## Champions League vs Tottenham - September 30, 2025")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        st.markdown("### FK Bodø/Glimt")
    with col2:
        st.markdown("## 2 - 2")
    with col3:
        st.markdown("### Tottenham")
    
    st.markdown("---")
    
    # Match Flow
    st.markdown("#### Match Flow & xG Timeline")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=spurs_match['minute'], y=spurs_match['xG'],
                            mode='lines', fill='tozeroy',
                            line=dict(color='#fbbf24', width=3),
                            fillcolor='rgba(251, 191, 36, 0.3)',
                            hovertemplate='<b>%{text}</b><br>xG: %{y:.2f}<extra></extra>',
                            text=spurs_match['event']))
    
    # Add markers for goals
    goals = spurs_match[spurs_match['event'].str.contains('goal', case=False, na=False)]
    goals_markers = spurs_match[spurs_match['score'].str.contains('-', na=False)]
    fig.add_trace(go.Scatter(x=goals_markers['minute'], y=goals_markers['xG'],
                            mode='markers',
                            marker=dict(size=15, color='#ef4444', symbol='star'),
                            showlegend=False,
                            hoverinfo='skip'))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#93c5fd',
        height=350,
        xaxis_title='Minutes',
        yaxis_title='Cumulative xG'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Match Statistics")
        stats_df = pd.DataFrame({
            'Metric': ['Possession', 'xG', 'Shots', 'Shots on Target', 'Passes Completed', 'Pass Accuracy', 'Dribbles', 'Recoveries'],
            'Bodo/Glimt': ['54.5%', '2.5', '18', '8', '520', '84%', '22', '39'],
            'Tottenham': ['45.5%', '1.6', '12', '5', '445', '81%', '14', '31']
        })
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        # Radar comparison
        st.markdown("#### Performance Comparison")
        categories = ['Possession', 'Shots', 'Pass Acc', 'Dribbles', 'Recoveries']
        bodo_values = [54.5, 18, 84, 22, 39]
        spurs_values = [45.5, 12, 81, 14, 31]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=bodo_values,
            theta=categories,
            fill='toself',
            name='Bodo/Glimt',
            line_color='#fbbf24'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=spurs_values,
            theta=categories,
            fill='toself',
            name='Tottenham',
            line_color='#3b82f6'
        ))
        fig_radar.update_layout(
            polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(gridcolor='#334155')),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=350
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        st.markdown("#### Key Moments")
        moments = [
            ("38'", "Hogh penalty miss (over bar)", "miss"),
            ("53'", "Goal - Hauge (left cut-in)", "goal"),
            ("66'", "Goal - Hauge (cutback)", "goal"),
            ("68'", "Van de Ven goal (Spurs)", "conceded"),
            ("70'", "Bjorkan overlap chance", "chance"),
            ("89'", "Own goal - Gundersen (deflection)", "conceded")
        ]
        
        for minute, event, type_event in moments:
            if type_event == "goal":
                st.success(f"**{minute}** - {event}")
            elif type_event == "conceded":
                st.error(f"**{minute}** - {event}")
            elif type_event == "miss":
                st.warning(f"**{minute}** - {event}")
            else:
                st.info(f"**{minute}** - {event}")
        
        # Player heatmap
        st.markdown("#### Top Performers")
        player_perf = pd.DataFrame({
            'Player': ['Hauge', 'Berg', 'Bjorkan', 'Hogh'],
            'Touches': [64, 72, 51, 37],
            'Key Actions': [12, 11, 7, 6]
        })
        
        fig_players = px.bar(player_perf, x='Player', y=['Touches', 'Key Actions'],
                            barmode='group',
                            color_discrete_sequence=['#fbbf24', '#3b82f6'])
        fig_players.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=250
        )
        st.plotly_chart(fig_players, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### Europa League vs Champions League Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Europa League Semi-Final 2024")
        europa_stats = {
            'Metric': ['Possession', 'xG', 'Shots', 'Pass Accuracy', 'Dribbles'],
            'Value': ['48%', '1.4', '13', '79%', '16']
        }
        st.dataframe(pd.DataFrame(europa_stats), hide_index=True, use_container_width=True)
        st.error("**Result:** Loss on aggregate")
    
    with col2:
        st.markdown("##### Champions League 2025")
        ucl_stats = {
            'Metric': ['Possession', 'xG', 'Shots', 'Pass Accuracy', 'Dribbles'],
            'Value': ['54.5%', '2.5', '18', '84%', '22'],
            'Change': ['+6.5%', '+1.1', '+5', '+5%', '+6']
        }
        st.dataframe(pd.DataFrame(ucl_stats), hide_index=True, use_container_width=True)
        st.success("**Result:** 2-2 Draw vs Tottenham")
    
    # Comparison chart
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(x=competition_comparison['metric'], 
                              y=competition_comparison['Europa'],
                              name='Europa League Semi (2024)', 
                              marker_color='#a855f7'))
    fig_comp.add_trace(go.Bar(x=competition_comparison['metric'], 
                              y=competition_comparison['UCL'],
                              name='Champions League (2025)', 
                              marker_color='#fbbf24'))
    
    fig_comp.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#93c5fd',
        height=350,
        barmode='group'
    )
    st.plotly_chart(fig_comp, use_container_width=True)
    
    st.info("Significant improvement across attacking metrics in UCL debut vs Europa semifinal")

with tab5:
    st.markdown("## Defensive Analysis 2022-2025")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Defensive Actions per 90 Evolution")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=defensive_stats['year'], y=defensive_stats['tackles'],
                                mode='lines+markers', name='Tackles',
                                line=dict(color='#ef4444', width=3)))
        fig.add_trace(go.Scatter(x=defensive_stats['year'], y=defensive_stats['interceptions'],
                                mode='lines+markers', name='Interceptions',
                                line=dict(color='#fbbf24', width=3)))
        fig.add_trace(go.Scatter(x=defensive_stats['year'], y=defensive_stats['blocks'],
                                mode='lines+markers', name='Blocks',
                                line=dict(color='#3b82f6', width=3)))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Duels Won per Game")
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=defensive_stats['year'], 
                             y=defensive_stats['duels_won'],
                             marker_color='#22c55e',
                             text=defensive_stats['duels_won'],
                             textposition='auto'))
        
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=350
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # Goalkeeper performance
    st.markdown("#### Goalkeeper Performance - Nikita Haikin")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=gk_stats['year'], y=gk_stats['saves'],
                             name='Saves', marker_color='#fbbf24'))
        fig3.add_trace(go.Bar(x=gk_stats['year'], y=gk_stats['clean_sheets'],
                             name='Clean Sheets', marker_color='#22c55e'))
        
        fig3.update_layout(
            title="Saves and Clean Sheets",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=300,
            barmode='group'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=gk_stats['year'], y=gk_stats['save_pct'],
                                 mode='lines+markers',
                                 line=dict(color='#3b82f6', width=3),
                                 marker=dict(size=12),
                                 fill='tozeroy'))
        
        fig4.update_layout(
            title="Save Percentage Evolution",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=300,
            yaxis_range=[60, 75]
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # Defensive metrics summary
    st.markdown("#### Defensive Improvement Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        improvement = defensive_stats.iloc[-1]['tackles'] - defensive_stats.iloc[0]['tackles']
        st.metric("Tackles per 90", f"{defensive_stats.iloc[-1]['tackles']:.1f}", 
                 f"+{improvement:.1f} since 2022")
    
    with col2:
        improvement = defensive_stats.iloc[-1]['interceptions'] - defensive_stats.iloc[0]['interceptions']
        st.metric("Interceptions per 90", f"{defensive_stats.iloc[-1]['interceptions']:.1f}", 
                 f"+{improvement:.1f} since 2022")
    
    with col3:
        improvement = gk_stats.iloc[-1]['save_pct'] - gk_stats.iloc[0]['save_pct']
        st.metric("GK Save %", f"{gk_stats.iloc[-1]['save_pct']}%", 
                 f"+{improvement}% since 2022")
    
    with col4:
        improvement = season_data.iloc[0]['goals_conceded'] - season_data.iloc[-1]['goals_conceded']
        st.metric("Goals Conceded", f"{season_data.iloc[-1]['goals_conceded']}", 
                 f"-{improvement} since 2022")

with tab6:
    st.markdown("## Advanced Metrics & Analytics")
    
    # Shooting efficiency over time
    st.markdown("#### Shooting Efficiency Evolution")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(x=shooting_stats['year'], y=shooting_stats['conversion'],
                  name='Conversion %', marker_color='#fbbf24'),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(x=shooting_stats['year'], y=shooting_stats['shot_accuracy'],
                      mode='lines+markers', name='Shot Accuracy %',
                      line=dict(color='#22c55e', width=3)),
            secondary_y=True
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=350
        )
        fig.update_yaxes(title_text="Conversion %", secondary_y=False)
        fig.update_yaxes(title_text="Shot Accuracy %", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=shooting_stats['year'], 
                                 y=shooting_stats['shots_per_game'],
                                 mode='lines+markers',
                                 line=dict(color='#ef4444', width=3),
                                 marker=dict(size=10),
                                 fill='tozeroy'))
        
        fig2.update_layout(
            title="Shots per Game Progression",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=350
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # xG Performance Analysis
    st.markdown("#### Expected Goals (xG) Performance")
    
    xg_performance = season_data.copy()
    xg_performance['xG_total'] = xg_performance['xg'] * xg_performance['matches']
    xg_performance['xG_diff'] = xg_performance['goals_scored'] - xg_performance['xG_total']
    
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=xg_performance['year'], 
                         y=xg_performance['goals_scored'],
                         name='Actual Goals', marker_color='#22c55e'))
    fig3.add_trace(go.Scatter(x=xg_performance['year'], 
                             y=xg_performance['xG_total'],
                             mode='lines+markers', name='Expected Goals (xG)',
                             line=dict(color='#ef4444', width=3, dash='dash')))
    
    fig3.update_layout(
        title="Goals Scored vs Expected Goals (xG)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#93c5fd',
        height=350
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("---")
    
    # Performance heatmap
    st.markdown("#### Season Performance Heatmap")
    
    heatmap_data = pd.DataFrame({
        'Season': [2022, 2023, 2024, 2025],
        'Attack': [season_data['goals'].tolist()[i] * 10 for i in range(4)],
        'Defense': [(100 - (season_data['goals_conceded'].tolist()[i] / season_data['matches'].tolist()[i]) * 10) for i in range(4)],
        'Possession': season_data['possession'].tolist(),
        'Efficiency': [(season_data['points'].tolist()[i] / season_data['matches'].tolist()[i]) * 100 / 3 for i in range(4)]
    })
    
    fig_heatmap = px.imshow(heatmap_data.set_index('Season').T,
                            color_continuous_scale='YlOrRd',
                            aspect='auto',
                            labels=dict(color="Performance Score"))
    fig_heatmap.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#93c5fd',
        height=300
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.markdown("---")
    
    # Key insights
    st.markdown("#### Key Analytical Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
        st.markdown("**Offensive Growth**")
        st.markdown(f"- Goals/game: {season_data.iloc[0]['goals']:.2f} → {season_data.iloc[-1]['goals']:.2f}")
        st.markdown(f"- xG/game: {season_data.iloc[0]['xg']:.2f} → {season_data.iloc[-1]['xg']:.2f}")
        st.markdown(f"- Conversion rate: {shooting_stats.iloc[0]['conversion']}% → {shooting_stats.iloc[-1]['conversion']}%")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
        st.markdown("**Defensive Solidity**")
        st.markdown(f"- Goals conceded: {season_data.iloc[0]['goals_conceded']} → {season_data.iloc[-1]['goals_conceded']}")
        st.markdown(f"- Clean sheets: {gk_stats.iloc[0]['clean_sheets']} → {gk_stats.iloc[-1]['clean_sheets']}")
        st.markdown(f"- Save %: {gk_stats.iloc[0]['save_pct']}% → {gk_stats.iloc[-1]['save_pct']}%")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
        st.markdown("**Tactical Evolution**")
        st.markdown(f"- Possession: {season_data.iloc[0]['possession']}% → {season_data.iloc[-1]['possession']}%")
        st.markdown(f"- Pass accuracy: {season_data.iloc[0]['pass_acc']}% → {season_data.iloc[-1]['pass_acc']}%")
        st.markdown(f"- Defensive line: {season_data.iloc[0]['def_line']} → {season_data.iloc[-1]['def_line']}")
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("### Dashboard Information")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Data Coverage:** 2022-2025 seasons")
with col2:
    st.markdown("**Formation:** 4-3-3 (Consistent)")
with col3:
    st.markdown("**Style:** High possession, progressive football")

st.markdown("---")
st.caption("FK Bodø/Glimt Tactical Evolution Dashboard | Data compiled from official match statistics and tactical analysis")
