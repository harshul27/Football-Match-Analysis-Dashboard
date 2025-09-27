import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# Page configuration
st.set_page_config(
    page_title="Football Tactical Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a professional, subtle dark theme
st.markdown("""
<style>
    /* Overall page and main content background */
    .stApp {
        background-color: #0d0d0d;
    }

    /* Set default text color for the entire app */
    body, p, li {
        color: #e0e0e0;
    }
    .st-emotion-cache-1c7y2c1, .st-emotion-cache-18ni7ap, .st-emotion-cache-1629p8f, .st-emotion-cache-z5fcl4 {
        color: #e0e0e0 !important;
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #f0f0f0 !important;
    }

    /* Main header banner */
    .main-header {
        background: linear-gradient(135deg, #1a1a1a, #0d0d0d);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    /* Metric cards with subtle red and dark accents */
    .metric-card {
        background: linear-gradient(135deg, #260000, #1a0000);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Stat containers for basic metrics */
    .stat-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        background: #1a1a1a;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #cc1c1c;
        color: #e0e0e0;
    }
    
    /* Insight boxes for analyst notes */
    .insight-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #cc1c1c;
        background: #1a1a1a;
        color: #e0e0e0;
    }
    
    /* Tactical notes */
    .tactical-note {
        padding: 1rem;
        border-radius: 8px;
        background: #1a1a1a;
        border-left: 4px solid #ef4444;
        margin: 1rem 0;
        color: #e0e0e0;
    }

    /* Sidebar styling */
    .st-emotion-cache-1629p8f {
        background-color: #121212;
        color: white;
    }

    /* Ensure containers have a dark background */
    .st-emotion-cache-13k65z8 {
        background-color: #1a1a1a;
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
    }
    
    /* Specific styles for player performance boxes */
    .player-card {
        background: #1a1a1a;
        border-left: 4px solid #cc1c1c;
    }
    
    /* General plot background and font */
    .js-plotly-plot {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
    }
    .modebar-container {
        background-color: #1a1a1a !important;
    }
    .plotly .axis-title, .plotly .legendtext, .plotly .xtick, .plotly .ytick {
        fill: #e0e0e0 !important;
        color: #e0e0e0 !important;
    }
    /* Streamlit DataFrame styling, setting text/header color */
    [data-testid="stDataFrame"] div:first-child { 
        color: #f0f0f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for timeline
if 'timeline_index' not in st.session_state:
    st.session_state.timeline_index = 0
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False

# Match data
match_info = {
    'date': '2025-09-20',
    'competition': 'Premier League',
    'venue': 'Turf Moor',
    'score': {'Burnley': 1, 'Forest': 1},
    'xG': {'Burnley': 1.08, 'Forest': 2.13},
    'possession': {'Burnley': 37, 'Forest': 63},
    'passes': {'Burnley': 307, 'Forest': 501},
    'passAccuracy': {'Burnley': 76, 'Forest': 85},
    'shots': {'Burnley': 12, 'Forest': 17},
    'shotsOnTarget': {'Burnley': 5, 'Forest': 8}
}

# Timeline data
timeline_data = [
    {'minute': 0, 'Burnley': 0, 'Forest': 0, 'event': 'Kick-off', 
     'description': 'Forest begin with high press, Zinchenko wide positioning',
     'ppda_forest': 8.5, 'ppda_burnley': 12.2, 'possession_forest': 65, 'possession_burnley': 35},
    {'minute': 2, 'Burnley': 0, 'Forest': 0.11, 'event': 'Williams Goal', 
     'description': 'Early goal from Neco Williams, build-up through Luiz retention',
     'ppda_forest': 8.5, 'ppda_burnley': 12.2, 'possession_forest': 65, 'possession_burnley': 35},
    {'minute': 15, 'Burnley': 0.25, 'Forest': 0.34, 'event': 'Forest Press Peak', 
     'description': 'Forest PPDA at 8.5, Burnley struggling with high press',
     'ppda_forest': 8.5, 'ppda_burnley': 12.2, 'possession_forest': 67, 'possession_burnley': 33},
    {'minute': 20, 'Burnley': 0.42, 'Forest': 0.34, 'event': 'Anthony Goal', 
     'description': 'Burnley equalizer after Zinchenko error - failed clearance leads to goal',
     'ppda_forest': 11.0, 'ppda_burnley': 14.2, 'possession_forest': 62, 'possession_burnley': 38},
    {'minute': 30, 'Burnley': 0.48, 'Forest': 0.67, 'event': 'Tactical Networks', 
     'description': 'Forest triangulate left side (Zinchenko-Ndoye-Luiz), Burnley overload right',
     'ppda_forest': 11.0, 'ppda_burnley': 14.2, 'possession_forest': 64, 'possession_burnley': 36},
    {'minute': 45, 'Burnley': 0.51, 'Forest': 1.20, 'event': 'Half-time', 
     'description': 'Forest dominate chances creation, PPDA drops to 15.0',
     'ppda_forest': 15.0, 'ppda_burnley': 13.3, 'possession_forest': 65, 'possession_burnley': 35},
    {'minute': 54, 'Burnley': 0.61, 'Forest': 1.35, 'event': 'Hudson-Odoi Introduction', 
     'description': 'Forest increase width, subs enhance crossing threat',
     'ppda_forest': 9.0, 'ppda_burnley': 10.0, 'possession_forest': 62, 'possession_burnley': 38},
    {'minute': 60, 'Burnley': 0.68, 'Forest': 1.52, 'event': 'Pressing Shift', 
     'description': 'Burnley switch to higher press, Forest press drops',
     'ppda_forest': 13.2, 'ppda_burnley': 10.9, 'possession_forest': 60, 'possession_burnley': 40},
    {'minute': 75, 'Burnley': 0.89, 'Forest': 1.89, 'event': 'Laurent On', 
     'description': 'Burnley bring on Laurent to stiffen pivot, Hartman overlaps more',
     'ppda_forest': 13.2, 'ppda_burnley': 10.9, 'possession_forest': 58, 'possession_burnley': 42},
    {'minute': 88, 'Burnley': 1.02, 'Forest': 2.07, 'event': 'Final Forest Push', 
     'description': 'Zinchenko to Ndoye cross, blocked by Dubravka',
     'ppda_forest': 13.2, 'ppda_burnley': 10.9, 'possession_forest': 60, 'possession_burnley': 40},
    {'minute': 90, 'Burnley': 1.08, 'Forest': 2.13, 'event': 'Full-time', 
     'description': 'Forest statistical dominance doesn\'t convert to victory',
     'ppda_forest': 13.2, 'ppda_burnley': 10.9, 'possession_forest': 60, 'possession_burnley': 40}
]

# PPDA data
ppda_data = [
    {'segment': '0-15\'', 'Forest': 8.5, 'Burnley': 12.0, 'Forest_Description': 'Aggressive early press', 'Burnley_Description': 'Struggling with press'},
    {'segment': '16-30\'', 'Forest': 11.0, 'Burnley': 14.0, 'Forest_Description': 'Sustained pressure', 'Burnley_Description': 'Adapting to intensity'},
    {'segment': '31-45\'', 'Forest': 15.0, 'Burnley': 13.0, 'Forest_Description': 'Press intensity drops', 'Burnley_Description': 'Better circulation'},
    {'segment': '46-60\'', 'Forest': 9.0, 'Burnley': 10.0, 'Forest_Description': 'Second-half intensity', 'Burnley_Description': 'Counter-pressing'},
    {'segment': '61-75\'', 'Forest': 13.2, 'Burnley': 10.9, 'Forest_Description': 'Managed pressing', 'Burnley_Description': 'Higher energy phase'}
]

# Player performance data
player_performance = [
    {'name': 'Zinchenko', 'team': 'Forest', 'progressive_passes': 5, 'final_third_entries': 13, 
     'pass_accuracy': 91, 'key_moment': '19\' Defensive error leading to goal', 
     'tactical_role': 'Progressive left-back, high positioning', 'performance_rating': 7.2},
    {'name': 'Gibbs-White', 'team': 'Forest', 'shot_creating_actions': 2, 'recoveries': 8, 'dribbles': 3,
     'key_moment': 'Dropping deep to link play', 'tactical_role': 'Fluid #10, creating connections', 'performance_rating': 7.8},
    {'name': 'Chris Wood', 'team': 'Forest', 'box_touches': 7, 'aerial_duels_won': 4, 'shots': 3,
     'key_moment': 'Physical presence in final third', 'tactical_role': 'Target man with link-up evolution', 'performance_rating': 7.1},
    {'name': 'Josh Cullen', 'team': 'Burnley', 'passes': 56, 'pass_accuracy': 87, 'recoveries': 9,
     'key_moment': 'Controlling tempo from deep', 'tactical_role': 'Deep-lying playmaker in pivot', 'performance_rating': 8.1},
    {'name': 'Jaidon Anthony', 'team': 'Burnley', 'goals': 1, 'shots': 3, 'dribbles': 3,
     'key_moment': '20\' Clinical finish for equalizer', 'tactical_role': 'Left-wing threat, cutting inside', 'performance_rating': 8.4}
]

# Header
st.markdown("""
<div class="main-header">
    <h1>BURNLEY vs NOTTINGHAM FOREST</h1>
    <div style="display: flex; justify-content: center; align-items: center; gap: 2rem; font-size: 1.5rem; margin: 1rem 0;">
        <div style="text-align: center;">
            <div style="font-size: 2rem; font-weight: bold;">BURNLEY</div>
            <div style="font-size: 0.9rem; opacity: 0.7;">Scott Parker</div>
        </div>
        <div style="font-size: 4rem; font-weight: bold; color: #f0f0f0;">1 - 1</div>
        <div style="text-align: center;">
            <div style="font-size: 2rem; font-weight: bold;">FOREST</div>
            <div style="font-size: 0.9rem; opacity: 0.7;">Ange Postecoglou</div>
        </div>
    </div>
    <div style="opacity: 0.8;">Premier League • September 20, 2025 • Turf Moor</div>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
tab_selection = st.sidebar.selectbox(
    "Choose Analysis",
    ["Match Overview", "Tactical Analysis", "Live Timeline", "Manager Comparison", "Advanced Metrics", "Europa League Campaign"]
)

# Tab 1: Match Overview
if tab_selection == "Match Overview":
    st.title("📊 Match Overview")
    
    # Key stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Forest xG</h3>
            <div style="font-size: 2rem; font-weight: bold;">{match_info['xG']['Forest']}</div>
            <div>vs {match_info['xG']['Burnley']} Burnley</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Forest Possession</h3>
            <div style="font-size: 2rem; font-weight: bold;">{match_info['possession']['Forest']}%</div>
            <div>vs {match_info['possession']['Burnley']}% Burnley</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Forest Passes</h3>
            <div style="font-size: 2rem; font-weight: bold;">{match_info['passes']['Forest']}</div>
            <div>{match_info['passAccuracy']['Forest']}% accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Forest PPDA</h3>
            <div style="font-size: 2rem; font-weight: bold;">12.7</div>
            <div>High pressing</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Match statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Basic Match Statistics")
        stats_data = {
            'Metric': ['Shots', 'Shots on Target', 'Big Chances', 'Corners', 'Fouls'],
            'Burnley': [12, 5, 1, 5, 12],
            'Forest': [17, 8, 3, 8, 11]
        }
        
        for i, metric in enumerate(stats_data['Metric']):
            st.markdown(f"""
            <div class="stat-container">
                <span style="font-weight: bold; color:white;">{metric}</span>
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <span style="background: #ef4444; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-weight: bold;">
                        {stats_data['Burnley'][i]}
                    </span>
                    <span style="color: #9ca3af;">vs</span>
                    <span style="background: #cc1c1c; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-weight: bold;">
                        {stats_data['Forest'][i]}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-box">
            <span style="font-weight: bold;">Analyst Note:</span> Forest dominated all attacking metrics - 8 shots on target vs 5, 
            3 big chances vs 1, and 8 corners vs 5. This statistical dominance supports their higher xG output.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Shot Conversion Analysis")
        conversion_data = pd.DataFrame({
            'Team': ['Burnley', 'Forest'],
            'Shots': [12, 17],
            'On Target': [5, 8],
            'Goals': [1, 1]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Total Shots', x=conversion_data['Team'], y=conversion_data['Shots'], 
                             marker_color='#333333'))
        fig.add_trace(go.Bar(name='On Target', x=conversion_data['Team'], y=conversion_data['On Target'], 
                             marker_color='#cc1c1c'))
        fig.add_trace(go.Bar(name='Goals', x=conversion_data['Team'], y=conversion_data['Goals'], 
                             marker_color='#ef4444'))
        
        fig.update_layout(
            title="Shot Conversion Comparison", 
            barmode='group', 
            height=400,
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font_color="#f0f0f0"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="tactical-note">
            <span style="font-weight: bold;">Key Insight:</span> Despite Forest's dominance in chances created, Burnley were more clinical - 
            8.3% conversion vs 5.9%. This efficiency gap kept Burnley competitive despite being outplayed.
        </div>
        """, unsafe_allow_html=True)
    
    # xG Timeline
    st.subheader("Expected Goals Timeline")
    st.markdown("Cumulative xG showing chance creation throughout the match. Forest's consistent threat vs Burnley's early burst.")
    
    timeline_df = pd.DataFrame(timeline_data)
    fig_timeline = go.Figure()
    fig_timeline.add_trace(go.Scatter(x=timeline_df['minute'], y=timeline_df['Forest'], 
                                     mode='lines+markers', name='Nottingham Forest',
                                     line=dict(color='#cc1c1c', width=3)))
    fig_timeline.add_trace(go.Scatter(x=timeline_df['minute'], y=timeline_df['Burnley'], 
                                     mode='lines+markers', name='Burnley FC',
                                     line=dict(color='#ef4444', width=3)))
    
    fig_timeline.update_layout(
        title="xG Development Throughout Match", 
        xaxis_title="Match Time (minutes)",
        yaxis_title="Expected Goals",
        height=500,
        paper_bgcolor="#1a1a1a",
        plot_bgcolor="#1a1a1a",
        font_color="#f0f0f0"
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        <span style="font-weight: bold;">Match Flow Analysis:</span> Forest's xG grew steadily throughout the match (2.13 total), 
        while Burnley's main threat came in the first half (0.51 by HT). Second-half xG: Forest 0.93, Burnley 0.57.
    </div>
    """, unsafe_allow_html=True)

# Tab 2: Tactical Analysis
elif tab_selection == "Tactical Analysis":
    st.title("⚽ Tactical Analysis")
    
    st.subheader("Formation Analysis & Tactical Setup")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔴 Burnley Formation")
        st.markdown("""
        <div style="background: linear-gradient(to bottom, #ef4444, #dc2626); height: 300px; border-radius: 10px; position: relative; color: white; display: flex; align-items: center; justify-content: center;">
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: bold;">5-4-1 → 3-2-3-2</div>
                <div style="margin-top: 1rem;">Tactical Evolution</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
        st.markdown("""
        <div class="tactical-note">
            <h5 style="color: #dc2626; font-weight: bold; margin-bottom: 0.5rem;">Tactical Setup:</h5>
            <p style="font-size: 0.9rem; margin-bottom: 0.5rem; color:#e0e0e0;">
                5-4-1 defensive block transitioning to 3-2-3-2 in attack. Cullen-Laurent pivot controls tempo, 
                with Hartman providing aggressive left-sided width.
            </p>
            <div style="font-size: 0.8rem; font-weight: bold; color:#e0e0e0;">
                Key Pattern: Back three buildup with Cullen as deep distributor. 
                Anthony cuts inside from left while Hartman provides overlapping width.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🔴 Forest Formation")
        st.markdown("""
        <div style="background: linear-gradient(to bottom, #cc1c1c, #991c1c); height: 300px; border-radius: 10px; position: relative; color: white; display: flex; align-items: center; justify-content: center;">
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: bold;">4-2-3-1</div>
                <div style="margin-top: 1rem;">High Possession System</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
        st.markdown("""
        <div class="tactical-note" style="border-left: 4px solid #cc1c1c;">
            <h5 style="color: #cc1c1c; font-weight: bold; margin-bottom: 0.5rem;">Tactical Setup:</h5>
            <p style="font-size: 0.9rem; margin-bottom: 0.5rem; color:#e0e0e0;">
                4-2-3-1 with high fullbacks in Ange's possession-based system. Patient build-up through triangular 
                combinations with Luiz-Anderson double pivot.
            </p>
            <div style="font-size: 0.8rem; font-weight: bold; color:#e0e0e0;">
                Key Pattern: Back four buildup with Zinchenko progression left. 
                Gibbs-White drops deep to create overloads while fullbacks advance.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # PPDA Analysis
    st.subheader("Pressing Intensity Analysis (PPDA)")
    st.markdown("Passes Per Defensive Action - Lower values indicate more aggressive pressing.")
    
    ppda_df = pd.DataFrame(ppda_data)
    fig_ppda = go.Figure()
    fig_ppda.add_trace(go.Bar(name='Forest (Lower = More Aggressive)', x=ppda_df['segment'], 
                             y=ppda_df['Forest'], marker_color='#cc1c1c'))
    fig_ppda.add_trace(go.Bar(name='Burnley', x=ppda_df['segment'], 
                             y=ppda_df['Burnley'], marker_color='#ef4444'))
    
    fig_ppda.update_layout(
        title="PPDA Throughout Match", 
        xaxis_title="Time Periods",
        yaxis_title="PPDA Value",
        height=400,
        paper_bgcolor="#1a1a1a",
        plot_bgcolor="#1a1a1a",
        font_color="#e0e0e0"
    )
    st.plotly_chart(fig_ppda, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="insight-box">
            <span style="font-weight: bold;">Forest Pressing Pattern:</span> Most intense in opening 15 minutes (8.5 PPDA) and after HT (9.0 PPDA). 
            Classic Postecoglou high-energy starts to each half, with tactical management in middle periods.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tactical-note">
            <span style="font-weight: bold;">Burnley Response:</span> Adapted well in final third of match (10.9 PPDA) as Parker's side 
            pushed for winner. Counter-pressing improved significantly after adjustments.
        </div>
        """, unsafe_allow_html=True)
    
    # Cross effectiveness analysis
    st.subheader("Wide Play & Cross Effectiveness Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cross effectiveness pie chart
        cross_data = pd.DataFrame({
            'Team': ['Forest Effective', 'Forest Ineffective', 'Burnley Effective', 'Burnley Ineffective'],
            'Values': [8, 11, 3, 9],
            'Colors': ['#cc1c1c', '#330000', '#ef4444', '#4d0000']
        })
        
        fig_cross = go.Figure(data=[go.Pie(labels=cross_data['Team'], values=cross_data['Values'],
                                          marker_colors=cross_data['Colors'])])
        fig_cross.update_layout(
            title="Cross Effectiveness Comparison", 
            height=400,
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font_color="#e0e0e0"
        )
        st.plotly_chart(fig_cross, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="tactical-note" style="border-left: 4px solid #cc1c1c;">
            <h6 style="color: #cc1c1c; font-weight: bold; margin-bottom: 0.5rem;">Forest Cross Analysis</h6>
            <div style="font-size: 0.9rem; color: #e0e0e0;">
                <div>Total Crosses: 19</div>
                <div>Successful: 8 (26% effectiveness)</div>
                <div>Hudson-Odoi Impact: 50% success rate</div>
                <div><strong>Key Pattern:</strong> Left-sided combinations through Zinchenko-Ndoye</div>
            </div>
        </div>
        
        <div class="tactical-note">
            <h6 style="color: #ef4444; font-weight: bold; margin-bottom: 0.5rem;">Burnley Cross Analysis</h6>
            <div style="font-size: 0.9rem; color: #e0e0e0;">
                <div>Total Crosses: 12</div>
                <div>Successful: 3 (12% effectiveness)</div>
                <div>Main Source: Hartman overlaps (4 crosses)</div>
                <div><strong>Issue:</strong> Limited target men in box</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Player performance
    st.subheader("Key Player Performances & Tactical Roles")
    
    player_df = pd.DataFrame(player_performance)
    
    for i, (idx, player) in enumerate(player_df.iterrows()):
        if i % 2 == 0:
            col1, col2 = st.columns(2)
            current_col = col1
        else:
            current_col = col2
            
        team_color = "#1a1a1a"
        text_color = "#e0e0e0"
        
        current_col.markdown(f"""
        <div class="player-card" style="background: {team_color}; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <h6 style="color: {text_color}; font-weight: bold; font-size: 1.1rem; margin: 0;">{player['name']}</h6>
                <span style="background: {'#cc1c1c' if player['performance_rating'] >= 8 else '#ef4444' if player['performance_rating'] >= 7 else '#555555'}; 
                            color: white;
                            padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">
                    {player['performance_rating']}/10
                </span>
            </div>
            <div style="color: {text_color}; font-size: 0.85rem; margin-bottom: 0.5rem;">
                <strong>Role:</strong> {player['tactical_role']}
            </div>
            <div style="color: {text_color}; font-size: 0.85rem; margin-bottom: 0.75rem;">
                <strong>Key Moment:</strong> {player['key_moment']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Tab 3: Live Timeline
elif tab_selection == "Live Timeline":
    st.title("⏯️ Live Match Timeline Analysis")
    
    # Timeline controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col2:
        if st.button("▶️ Play" if not st.session_state.is_playing else "⏸️ Pause", use_container_width=True):
            st.session_state.is_playing = not st.session_state.is_playing
    
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.timeline_index = 0
            st.session_state.is_playing = False
    
    # Timeline slider
    st.session_state.timeline_index = st.slider(
        "Match Timeline", 
        0, len(timeline_data) - 1, 
        st.session_state.timeline_index
    )
    
    # Current event display
    current_event = timeline_data[st.session_state.timeline_index]
    
    st.markdown(f"""
    <div class="metric-card">
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2rem; text-align: center;">
            <div>
                <div style="font-size: 2rem; font-weight: bold; color:white;">{current_event['minute']}'</div>
                <div style="font-size: 1.2rem; opacity: 0.9; color:white;">{current_event['event']}</div>
            </div>
            <div>
                <div style="font-size: 0.9rem; opacity: 0.75; margin-bottom: 0.25rem; color:white;">Current xG</div>
                <div style="font-size: 1.2rem; color:white;">
                    Forest {current_event['Forest']:.2f} - {current_event['Burnley']:.2f} Burnley
                </div>
            </div>
            <div>
                <div style="font-size: 0.9rem; opacity: 0.75; margin-bottom: 0.25rem; color:white;">Possession</div>
                <div style="font-size: 1.2rem; color:white;">
                    {current_event['possession_forest']}% - {current_event['possession_burnley']}%
                </div>
            </div>
        </div>
        <div style="margin-top: 1.5rem; font-size: 0.9rem; opacity: 0.9; font-style: italic; color:white;">
            {current_event['description']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Multi-line timeline chart
    timeline_subset = timeline_data[:st.session_state.timeline_index + 1]
    timeline_df_subset = pd.DataFrame(timeline_subset)
    
    fig_multi = make_subplots(specs=[[{"secondary_y": True}]])
    
    # xG lines
    fig_multi.add_trace(
        go.Scatter(x=timeline_df_subset['minute'], y=timeline_df_subset['Forest'], 
                  mode='lines+markers', name='Forest xG', line=dict(color='#cc1c1c', width=4)),
        secondary_y=False
    )
    fig_multi.add_trace(
        go.Scatter(x=timeline_df_subset['minute'], y=timeline_df_subset['Burnley'], 
                  mode='lines+markers', name='Burnley xG', line=dict(color='#ef4444', width=4)),
        secondary_y=False
    )
    
    # PPDA lines
    fig_multi.add_trace(
        go.Scatter(x=timeline_df_subset['minute'], y=timeline_df_subset['ppda_forest'], 
                  mode='lines', name='Forest PPDA', line=dict(color='#991c1c', width=2, dash='dash')),
        secondary_y=True
    )
    fig_multi.add_trace(
        go.Scatter(x=timeline_df_subset['minute'], y=timeline_df_subset['ppda_burnley'], 
                  mode='lines', name='Burnley PPDA', line=dict(color='#dc2626', width=2, dash='dash')),
        secondary_y=True
    )
    
    # Possession lines
    fig_multi.add_trace(
        go.Scatter(x=timeline_df_subset['minute'], y=timeline_df_subset['possession_forest'], 
                  mode='lines', name='Forest Possession %', line=dict(color='#4d0000', width=1, dash='dot')),
        secondary_y=True
    )
    
    fig_multi.update_xaxes(title_text="Minutes")
    fig_multi.update_yaxes(title_text="Expected Goals", secondary_y=False)
    fig_multi.update_yaxes(title_text="PPDA / Possession %", secondary_y=True)
    fig_multi.update_layout(
        title="Live Match Timeline Analysis", 
        height=600,
        paper_bgcolor="#1a1a1a",
        plot_bgcolor="#1a1a1a",
        font_color="#f0f0f0"
    )
    
    st.plotly_chart(fig_multi, use_container_width=True)
    
    # Progress bar
    progress_percentage = ((st.session_state.timeline_index + 1) / len(timeline_data)) * 100
    st.markdown(f"""
    <div style="margin-top: 2rem; background:#1a1a1a; padding:1rem; border-radius:8px;">
        <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: #e0e0e0; margin-bottom: 0.5rem;">
            <span>Match Progress</span>
            <span>{progress_percentage:.0f}% Complete</span>
        </div>
        <div style="width: 100%; background: #333333; border-radius: 20px; height: 12px;">
            <div style="background: linear-gradient(90deg, #cc1c1c, #991c1c); height: 12px; border-radius: 20px; width: {progress_percentage}%; transition: all 0.5s;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key tactical moments
    st.subheader("Key Tactical Moments")
    
    tactical_moments = [
        {"minute": "2'", "event": "Williams Goal", "description": "Forest's early goal demonstrates Ange's aggressive start philosophy. High press (8.5 PPDA) forces Burnley errors, with Luiz retention and Zinchenko positioning creating the opportunity for Williams.", "color": "#cc1c1c"},
        {"minute": "20'", "event": "Anthony Equalizer", "description": "Burnley's clinical response highlights their efficiency. Zinchenko's failed clearance (individual error under pressure) leads to Foster assist and Anthony finish. 8.3% conversion rate proving decisive.", "color": "#ef4444"},
        {"minute": "54'", "event": "Hudson-Odoi Impact", "description": "Substitution transforms Forest's wide threat. Cross effectiveness jumps to 50% for Hudson-Odoi specifically, adding pace and directness to complement patient build-up patterns.", "color": "#cc1c1c"},
        {"minute": "75'", "event": "Laurent Defensive Adjustment", "description": "Parker's tactical response shores up Burnley's pivot. Laurent's introduction allows more structured pressing (PPDA drops to 10.9) while maintaining defensive stability in final 15 minutes.", "color": "#ef4444"}
    ]
    
    for moment in tactical_moments:
        st.markdown(f"""
        <div style="border-left: 4px solid {moment['color']}; background: #1a1a1a; padding: 1rem; border-radius: 0 8px 8px 0; margin: 1rem 0;">
            <div style="font-weight: bold; color: white;">{moment['minute']} - {moment['event']}</div>
            <div style="font-size: 0.9rem; color: #e0e0e0;">{moment['description']}</div>
        </div>
        """, unsafe_allow_html=True)

# Tab 4: Manager Comparison
elif tab_selection == "Manager Comparison":
    st.title("👥 Manager Comparison - The Postecoglou Project")
    
    st.markdown("""
    <div class="main-header" style="background: linear-gradient(135deg, #1a1a1a, #0d0d0d); padding: 2rem; border-radius: 10px; margin-bottom: 2rem; color: white; text-align: center;">
        <h3 style="font-size: 2rem; margin-bottom: 0.5rem; color: white;">THE POSTECOGLOU PROJECT</h3>
        <p style="font-size: 1.2rem; opacity: 0.9; color: white;">From Tottenham to Trent End: A Tactical Revolution in Progress</p>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2rem; margin-top: 2rem; text-align: center;">
            <div style="background: #1a1a1a; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; font-weight: bold; color: #cc1c1c;">+22%</div>
                <div style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem; color:#e0e0e0;">Possession Increase</div>
                <div style="font-size: 0.7rem; opacity: 0.75; margin-top: 0.25rem; color:#e0e0e0;">From Nuno's 41% to Ange's 63%</div>
            </div>
            <div style="background: #1a1a1a; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; font-weight: bold; color: #cc1c1c;">2.13</div>
                <div style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem; color:#e0e0e0;">xG per 90 vs Burnley</div>
                <div style="font-size: 0.7rem; opacity: 0.75; margin-top: 0.25rem; color:#e0e0e0;">111% increase from Nuno era</div>
            </div>
            <div style="background: #1a1a1a; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; font-weight: bold; color: #cc1c1c;">12.7</div>
                <div style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem; color:#e0e0e0;">Current PPDA</div>
                <div style="font-size: 0.7rem; opacity: 0.75; margin-top: 0.25rem; color:#e0e0e0;">37% more aggressive pressing</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistical comparison
    st.subheader("The Numbers Behind the Revolution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Core Tactical Metrics")
        comparison_data = {
            'Metric': ['Possession %', 'PPDA', 'xG per 90', 'Final Third Entries'],
            'Nuno Era': [41.0, 20.1, 1.01, 18],
            'Ange Era': [63.0, 12.7, 1.80, 39],
            'Ange Spurs': [57.2, 13.6, 1.70, 58]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # FIX: Removed the problematic .style.background_color() call to resolve AttributeError
        st.dataframe(comparison_df, use_container_width=True)
    
    with col2:
        # Radar chart
        radar_data = pd.DataFrame({
            'Metric': ['Possession', 'Press Intensity', 'Chance Creation', 'Pass Accuracy', 'Build-up Quality'],
            'Nuno': [41, 30, 35, 78, 25],
            'Ange_Forest': [63, 63, 75, 85, 70],
            'Ange_Spurs': [57.2, 59, 65, 87, 82]
        })
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_data['Nuno'],
            theta=radar_data['Metric'],
            fill='toself',
            name='Nuno Forest',
            line_color='#ef4444'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_data['Ange_Forest'],
            theta=radar_data['Metric'],
            fill='toself',
            name='Ange Forest',
            line_color='#cc1c1c'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_data['Ange_Spurs'],
            theta=radar_data['Metric'],
            fill='toself',
            name='Ange Spurs',
            line_color='#f59e0b'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Tactical Revolution Comparison",
            height=400,
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font_color="#f0f0f0"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)

# Tab 5: Advanced Metrics
elif tab_selection == "Advanced Metrics":
    st.title("⚡ Advanced Metrics")
    
    # Key advanced metrics
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        {"title": "Transition Exposure", "value": "14.1m", "subtitle": "Forest avg gap", "color": "#cc1c1c"},
        {"title": "Build-Up Chains 10+", "value": "15", "subtitle": "Forest vs 6 Burnley", "color": "#cc1c1c"},
        {"title": "Sustained Threat", "value": "0.29", "subtitle": "Forest vs 0.11 Burnley", "color": "#cc1c1c"},
        {"title": "Flank Isolation", "value": "14", "subtitle": "Total 1v1 battles", "color": "#cc1c1c"}
    ]
    
    for i, metric in enumerate(metrics):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #260000, #1a0000); color: #e0e0e0; padding: 1.5rem; border-radius: 10px; text-align: center;">
                <h3 style="font-size: 1rem; margin-bottom: 0.5rem; color:#f0f0f0;">{metric['title']}</h3>
                <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.25rem; color:white;">{metric['value']}</div>
                <div style="font-size: 0.8rem; opacity: 0.9; color:#e0e0e0;">{metric['subtitle']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Transition vulnerability analysis
    st.subheader("Transition Vulnerability Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        transition_data = pd.DataFrame({
            'Team': ['Forest', 'Burnley'],
            'Avg Gap (m)': [14.1, 18.8],
            'Max Gap (m)': [21, 24],
            'Vulnerability Rating': [6.2, 7.8]
        })
        
        fig_transition = go.Figure()
        fig_transition.add_trace(go.Bar(name='Avg Gap (m)', x=transition_data['Team'], 
                                       y=transition_data['Avg Gap (m)'], marker_color='#cc1c1c'))
        fig_transition.add_trace(go.Bar(name='Max Gap (m)', x=transition_data['Team'], 
                                       y=transition_data['Max Gap (m)'], marker_color='#ef4444'))
        
        fig_transition.update_layout(
            title="Transition Exposure Comparison", 
            height=400,
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font_color="#e0e0e0"
        )
        st.plotly_chart(fig_transition, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
            <h6 style="color: #f0f0f0; font-weight: bold; margin-bottom: 0.5rem;">Forest: Better Defensive Structure</h6>
            <div style="font-size: 0.9rem; color: #e0e0e0;">
                <div>Average Gap: 14.1m (vs 18.8m Burnley)</div>
                <div>Max Exposure: 21m (vs 24m Burnley)</div>
                <div>Vulnerability Rating: 6.2/10</div>
                <p style="font-size: 0.8rem; margin-top: 0.5rem; font-style: italic;">
                    Ange's lessons from Spurs showing - better midfield-defense connection under pressure
                </p>
            </div>
        </div>
        
        <div class="tactical-note">
            <h6 style="color: #ef4444; font-weight: bold; margin-bottom: 0.5rem;">Key Insight</h6>
            <p style="font-size: 0.9rem; color: #e0e0e0;">
                Despite high line, Forest's transition exposure metrics are superior to Burnley's. 
                This suggests better coached positional discipline when losing possession.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Build-up quality metrics
    st.subheader("Build-Up Quality & Sustained Possession")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stat-container">
            <h6 style="color: #e0e0e0; font-weight: bold; margin-bottom: 1rem;">Build-Up Chains Analysis</h6>
            <div style="color: #e0e0e0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Forest 10+ Pass Chains:</span>
                    <span style="font-weight: bold;">15</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Burnley 10+ Pass Chains:</span>
                    <span style="font-weight: bold;">6</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Forest Avg Length:</span>
                    <span style="font-weight: bold;">8.7 passes</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Completion Rate:</span>
                    <span style="font-weight: bold;">73%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-container">
            <h6 style="color: #e0e0e0; font-weight: bold; margin-bottom: 1rem;">Sustained Threat Index</h6>
            <div style="text-align: center; margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; font-weight: bold; color: #cc1c1c;">0.29</div>
                <div style="font-size: 0.9rem; color: #e0e0e0;">Forest STI</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #ef4444;">0.11</div>
                <div style="font-size: 0.9rem; color: #e0e0e0;">Burnley STI</div>
            </div>
            <p style="font-size: 0.8rem; color: #e0e0e0; margin-top: 0.75rem; font-style: italic;">
                Share of 7+ pass sequences ending in final third
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-container">
            <h6 style="color: #e0e0e0; font-weight: bold; margin-bottom: 1rem;">Comparison Context</h6>
            <div style="font-size: 0.9rem; color: #e0e0e0;">
                <div style="margin-bottom: 0.5rem;">
                    <strong>Ange Spurs STI:</strong> 0.34
                </div>
                <div style="margin-bottom: 0.5rem;">
                    <strong>Premier League Avg:</strong> 0.18
                </div>
                <div style="margin-bottom: 0.5rem;">
                    <strong>Nuno Forest:</strong> 0.14
                </div>
            </div>
            <p style="font-size: 0.8rem; color: #e0e0e0; margin-top: 0.75rem; font-style: italic;">
                Forest approaching Spurs-level sustained possession quality
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Flank isolation & 1v1 battles
    st.subheader("Flank Isolation & Individual Battles")
    
    col1, col2 = st.columns(2)
    
    with col1:
        battles_data = pd.DataFrame({
            'Player': ['Ndoye vs Walker', 'Anthony vs Williams', 'Hudson-Odoi vs Walker', 'Hartman vs Bakwa'],
            'Battles': [4, 3, 2, 3],
            'Success Rate': [75, 67, 50, 33]
        })
        
        fig_battles = go.Figure()
        fig_battles.add_trace(go.Bar(name='Total Battles', x=battles_data['Player'], 
                                    y=battles_data['Battles'], marker_color='#cc1c1c'))
        fig_battles.add_trace(go.Bar(name='Success Rate %', x=battles_data['Player'], 
                                    y=battles_data['Success Rate'], marker_color='#ef4444'))
        
        fig_battles.update_layout(
            title="Key 1v1 Battles", 
            height=400, 
            xaxis_tickangle=-45,
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font_color="#e0e0e0"
        )
        st.plotly_chart(fig_battles, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
            <h6 style="color: #f0f0f0; font-weight: bold; margin-bottom: 0.5rem;">Forest Wing Dominance</h6>
            <div style="font-size: 0.9rem; color: #e0e0e0;">
                <div><strong>Ndoye vs Walker:</strong> 4 battles, 75% success</div>
                <div><strong>Key Impact:</strong> Left flank overloads creating consistent threat</div>
                <div><strong>Hudson-Odoi Effect:</strong> Added pace and directness post-substitution</div>
            </div>
        </div>
        
        <div class="tactical-note">
            <h6 style="color: #ef4444; font-weight: bold; margin-bottom: 0.5rem;">Burnley Counter-Threat</h6>
            <div style="font-size: 0.9rem; color: #e0e0e0;">
                <div><strong>Anthony vs Williams:</strong> 3 battles, 67% success</div>
                <div><strong>Clinical Edge:</strong> Lower volume but higher conversion</div>
                <div><strong>Tactical Role:</strong> Quick transitions and cutting inside</div>
            </div>
        </div>
        
        <div class="insight-box">
            <h6 style="color: #f0f0f0; font-weight: bold; margin-bottom: 0.5rem;">Total Isolation Metric</h6>
            <div style="font-size: 0.9rem; color: #e0e0e0;">
                <strong>14 Total 1v1 Battles</strong> - High isolation frequency indicates both teams' 
                willingness to create wide overloads and commit to individual duels.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Cross effectiveness detailed analysis
    st.subheader("Cross Effectiveness Deep Dive")
    
    col1, col2, col3 = st.columns(3)
    
    effectiveness_data = [
        {"team": "Forest", "rate": "26%", "total": 19, "successful": 8, "hudson_rate": "50%", "color": "#cc1c1c"},
        {"team": "Burnley", "rate": "12%", "total": 12, "successful": 3, "hartman": "4 crosses", "color": "#ef4444"}
    ]
    
    for i, data in enumerate(effectiveness_data):
        with [col1, col2][i]:
            bg_color = "#1a1a1a"
            text_color = "#e0e0e0"
            
            st.markdown(f"""
            <div class="stat-container" style="background: {bg_color}; padding: 1.5rem; border-radius: 8px;">
                <h6 style="color: {text_color}; font-weight: bold; margin-bottom: 1rem;">{data['team']} Cross Analysis</h6>
                <div style="text-align: center; margin-bottom: 1rem;">
                    <div style="font-size: 2rem; font-weight: bold; color: {data['color']};">{data['rate']}</div>
                    <div style="font-size: 0.9rem; color: {text_color};">Overall Effectiveness</div>
                </div>
                <div style="font-size: 0.9rem; color: {text_color};">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                        <span>Total Crosses:</span>
                        <span style="font-weight: bold;">{data['total']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                        <span>Successful:</span>
                        <span style="font-weight: bold;">{data['successful']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>{'Hudson-Odoi Rate:' if data['team'] == 'Forest' else 'Hartman Contribution:'}:</span>
                        <span style="font-weight: bold;">{'50%' if data['team'] == 'Forest' else '4 crosses'}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        # Pie chart for cross effectiveness
        cross_pie_data = pd.DataFrame({
            'Category': ['Forest Successful', 'Forest Failed', 'Burnley Successful', 'Burnley Failed'],
            'Values': [8, 11, 3, 9],
            'Colors': ['#cc1c1c', '#330000', '#ef4444', '#4d0000']
        })
        
        fig_cross_pie = go.Figure(data=[go.Pie(labels=cross_pie_data['Category'], values=cross_pie_data['Values'],
                                              marker_colors=cross_pie_data['Colors'])])
        fig_cross_pie.update_layout(
            title="Quality Differential", 
            height=300,
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font_color="#e0e0e0"
        )
        st.plotly_chart(fig_cross_pie, use_container_width=True)
    
    st.markdown("""
    <div class="tactical-note">
        <h6 style="color: #ef4444; font-weight: bold; margin-bottom: 0.5rem;">Tactical Insight</h6>
        <p style="font-size: 0.9rem; color: #e0e0e0;">
            Forest's superior cross effectiveness (26% vs 12%) stems from better movement patterns and timing. 
            Hudson-Odoi's 50% success rate demonstrates the impact of pace and crossing technique, while Burnley's 
            struggles reflect limited aerial targets and predictable crossing positions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Final verdict
    st.markdown("""
    <div class="metric-card" style="background: linear-gradient(135deg, #260000, #1a0000);">
        <h4 style="font-size: 1.5rem; margin-bottom: 1rem;">Advanced Metrics Verdict</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
            <div>
                <h6 style="font-size: 1.1rem; margin-bottom: 0.75rem;">Postecoglou's Tactical DNA Confirmed</h6>
                <ul style="font-size: 0.9rem; line-height: 1.6; color:white;">
                    <li><strong>Transition Discipline:</strong> Better defensive structure than expected (14.1m avg gap)</li>
                    <li><strong>Build-up Quality:</strong> 15 sequences of 10+ passes vs Burnley's 6</li>
                    <li><strong>Sustained Threat:</strong> 0.29 STI approaching Spurs level (0.34)</li>
                    <li><strong>Wide Dominance:</strong> 26% cross effectiveness, 14 successful 1v1 battles</li>
                </ul>
            </div>
            <div>
                <h6 style="font-size: 1.1rem; margin-bottom: 0.75rem;">Areas for Continued Development</h6>
                <ul style="font-size: 0.9rem; line-height: 1.6; color:white;">
                    <li><strong>Clinical Finishing:</strong> 2.13 xG only converted to 1 goal</li>
                    <li><strong>Individual Errors:</strong> Zinchenko mistake costly in high-line system</li>
                    <li><strong>Final Third Density:</strong> Need better box occupation for crosses</li>
                    <li><strong>Game Management:</strong> Converting dominance to consistent victories</li>
                </ul>
            </div>
        </div>
        
        <div style="margin-top: 1.5rem; padding: 1rem; background: #1a1a1a; border-radius: 8px;">
            <p style="font-size: 1rem; line-height: 1.6; color:white;">
                <strong>The Data's Conclusion:</strong> Forest's advanced metrics reveal a team rapidly adopting 
                Postecoglou's principles with impressive statistical backing. The challenge now shifts from 
                tactical implementation to result optimization - converting 2.13 xG performances into consistent victories.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Tab 6: Europa League Campaign
elif tab_selection == "Europa League Campaign":
    st.title("🏆 Europa League Campaign")
    
    # Europa League header
    st.markdown("""
    <div class="metric-card" style="background: linear-gradient(135deg, #260000, #1a0000);">
        <h3 style="font-size: 2rem; margin-bottom: 0.5rem;">EUROPA LEAGUE CAMPAIGN</h3>
        <p style="font-size: 1.2rem; opacity: 0.9;">Forest vs Real Betis • September 24, 2025</p>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 1.5rem; margin-top: 2rem; text-align: center;">
            <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #fbbf24;">2-2</div>
                <div style="font-size: 0.8rem; opacity: 0.9; color:#e0e0e0;">Final Score</div>
            </div>
            <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #cc1c1c;">1.98</div>
                <div style="font-size: 0.8rem; opacity: 0.9; color:#e0e0e0;">xG Generated</div>
            </div>
            <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #cc1c1c;">45%</div>
                <div style="font-size: 0.8rem; opacity: 0.9; color:#e0e0e0;">Possession</div>
            </div>
            <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #f59e0b;">Igor Jesus</div>
                <div style="font-size: 0.8rem; opacity: 0.9; color:#e0e0e0;">2 Goals</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Innovative "Ange-ball" metrics
    st.subheader("Innovative 'Ange-ball' Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #260000, #1a0000);">
            <h6 style="font-size: 1rem; font-weight: bold; margin-bottom: 0.5rem;">Possession Progression</h6>
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.25rem;">118</div>
            <div style="font-size: 0.8rem; opacity: 0.9;">meters per minute</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #260000, #1a0000);">
            <h6 style="font-size: 1rem; font-weight: bold; margin-bottom: 0.5rem;">Sustained Threats</h6>
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.25rem;">19</div>
            <div style="font-size: 0.8rem; opacity: 0.9;">8+ pass sequences to box</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #260000, #1a0000);">
            <h6 style="font-size: 1rem; font-weight: bold; margin-bottom: 0.5rem;">Triangle Formations</h6>
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.25rem;">17</div>
            <div style="font-size: 0.8rem; opacity: 0.9;">3+ player triangles</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Igor Jesus performance
    st.subheader("Igor Jesus - Star Performer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Igor Jesus stats
        igor_stats = pd.DataFrame({
            'Metric': ['Goals', 'Expected Goals', 'Box Touches', 'Shots'],
            'Value': [2, 1.20, 9, 4],
            'Color': ['#cc1c1c', '#991c1c', '#ef4444', '#f59e0b']
        })
        
        for i, row in igor_stats.iterrows():
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem; background: #1a1a1a; border-radius: 8px; margin-bottom: 0.5rem;">
                <span style="font-weight: bold; color: white;">{row['Metric']}</span>
                <span style="font-size: 1.5rem; font-weight: bold; color: white;">{row['Value']}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tactical-note">
            <h6 style="color: #ef4444; font-weight: bold; margin-bottom: 0.5rem;">European Quality</h6>
            <p style="font-size: 0.9rem; color: #e0e0e0;">
                Igor Jesus exceeded his xG with clinical finishing, showing the kind of 
                edge Forest need to succeed in European competition. His two goals from 1.20 xG 
                demonstrates the clinical finishing required at this level.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # European performance comparison
    st.subheader("European vs Premier League Performance")
    
    european_comparison = pd.DataFrame({
        'Competition': ['Premier League', 'Europa League'],
        'Possession %': [63, 45],
        'xG per 90': [2.13, 1.98],
        'PPDA': [12.7, 14.2],
        'Pass Accuracy': [85, 79]
    })
    
    # Create comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig_comp1 = go.Figure()
        fig_comp1.add_trace(go.Bar(
            name='Possession %',
            x=european_comparison['Competition'],
            y=european_comparison['Possession %'],
            marker_color=['#cc1c1c', '#ef4444']
        ))
        fig_comp1.update_layout(
            title="Possession Comparison", 
            height=300,
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font_color="#e0e0e0"
        )
        st.plotly_chart(fig_comp1, use_container_width=True)
    
    with col2:
        fig_comp2 = go.Figure()
        fig_comp2.add_trace(go.Bar(
            name='xG per 90',
            x=european_comparison['Competition'],
            y=european_comparison['xG per 90'],
            marker_color=['#cc1c1c', '#ef4444']
        ))
        fig_comp2.update_layout(
            title="Chance Creation Comparison", 
            height=300,
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font_color="#e0e0e0"
        )
        st.plotly_chart(fig_comp2, use_container_width=True)
    
    # Tactical adaptations
    st.subheader("Tactical Adaptations for European Competition")
    
    adaptations = [
        {
            "aspect": "Possession Strategy",
            "pl_approach": "Dominated possession (63%) with patient build-up",
            "european_approach": "More direct approach (45%) adapting to higher quality opposition",
            "effectiveness": "Successful adaptation - maintained threat creation"
        },
        {
            "aspect": "Pressing Intensity", 
            "pl_approach": "Aggressive PPDA of 12.7 against Burnley",
            "european_approach": "Slightly less intense 14.2 PPDA vs Betis",
            "effectiveness": "Smart energy management for European fixture congestion"
        },
        {
            "aspect": "Clinical Finishing",
            "pl_approach": "Struggled to convert 2.13 xG vs Burnley (1 goal)",
            "european_approach": "Better conversion of 1.98 xG vs Betis (2 goals)",
            "effectiveness": "Igor Jesus showing European-level clinical edge"
        }
    ]
    
    for adaptation in adaptations:
        st.markdown(f"""
        <div style="background: #1a1a1a; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #cc1c1c; margin: 1rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h6 style="color: #cc1c1c; font-weight: bold; margin-bottom: 0.75rem;">{adaptation['aspect']}</h6>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 0.75rem;">
                <div style="background: #260000; padding: 0.75rem; border-radius: 6px;">
                    <div style="font-weight: bold; color: #f0f0f0; font-size: 0.8rem; margin-bottom: 0.25rem;">PREMIER LEAGUE</div>
                    <div style="font-size: 0.85rem; color: #f0f0f0;">{adaptation['pl_approach']}</div>
                </div>
                <div style="background: #260000; padding: 0.75rem; border-radius: 6px;">
                    <div style="font-weight: bold; color: #f0f0f0; font-size: 0.8rem; margin-bottom: 0.25rem;">EUROPA LEAGUE</div>
                    <div style="font-size: 0.85rem; color: #f0f0f0;">{adaptation['european_approach']}</div>
                </div>
            </div>
            <div style="background: #260000; padding: 0.5rem; border-radius: 6px;">
                <span style="font-weight: bold; color: #cc1c1c; font-size: 0.8rem;">EFFECTIVENESS: </span>
                <span style="color: #f0f0f0; font-size: 0.85rem;">{adaptation['effectiveness']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Campaign assessment
    st.subheader("Europa League Campaign Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #260000, #1a0000);">
            <h6 style="font-size: 1.1rem; font-weight: bold; margin-bottom: 1rem;">✅ Positive Signs</h6>
            <ul style="font-size: 0.9rem; line-height: 1.6; margin: 0; padding-left: 1.5rem;">
                <li>Maintained attacking identity with lower possession (45%)</li>
                <li>Clinical finishing from Igor Jesus (2 goals from 1.98 xG)</li>
                <li>All "Ange-ball" metrics above European averages</li>
                <li>Defensive line height (52m) shows tactical confidence</li>
                <li>Triangle formations (17) indicate good player relationships</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #ef4444, #dc2626);">
            <h6 style="font-size: 1.1rem; font-weight: bold; margin-bottom: 1rem;">⚠️ Areas for Improvement</h6>
            <ul style="font-size: 0.9rem; line-height: 1.6; margin: 0; padding-left: 1.5rem;">
                <li>Game management - led 2-0 but drew 2-2</li>
                <li>Set piece conversion - 0/5 free kicks converted</li>
                <li>Possession control in European competition</li>
                <li>Individual defensive errors still occurring</li>
                <li>Need better squad rotation for fixture congestion</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # European outlook
    st.markdown("""
    <div class="metric-card" style="background: linear-gradient(135deg, #260000, #1a0000);">
        <h4 style="font-size: 1.5rem; margin-bottom: 1rem;">🌍 European Competition Verdict</h4>
        <p style="font-size: 1rem; line-height: 1.6; margin-bottom: 1rem;">
            Forest's debut Europa League performance shows promising signs of tactical adaptability. 
            The ability to maintain core "Ange-ball" principles while adjusting possession approach 
            demonstrates growing tactical maturity under Postecoglou.
        </p>
        <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px;">
            <p style="font-size: 0.95rem; line-height: 1.5; margin: 0;">
                <strong>Key Takeaway:</strong> Igor Jesus's clinical finishing (2 goals from 1.98 xG) provides 
                the European-level quality needed for continental success. The challenge now is consistency 
                across both domestic and European fixtures while managing squad rotation effectively.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Auto-play functionality for timeline
if st.session_state.is_playing and tab_selection == "Live Timeline":
    time.sleep(1.5)
    if st.session_state.timeline_index < len(timeline_data) - 1:
        st.session_state.timeline_index += 1
        st.rerun()
    else:
        st.session_state.is_playing = False
        st.rerun()

# Footer
st.markdown("""
---
<div style="text-align: center; color: #f0f0f0; margin-top: 2rem;">
    <p>Football Tactical Dashboard | Burnley vs Nottingham Forest Analysis</p>
    <p style="font-size: 0.8rem;">Built with Streamlit | Data visualized with Plotly</p>
</div>
""", unsafe_allow_html=True)
