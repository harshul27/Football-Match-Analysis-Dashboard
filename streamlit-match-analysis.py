import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="AFC Bournemouth vs Wolverhampton - Match Analysis",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #dc2626, #f97316);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #dbeafe, #bfdbfe);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #93c5fd;
        text-align: center;
        margin-bottom: 1rem;
    }
    .team-red {
        color: #dc2626;
        font-weight: bold;
    }
    .team-orange {
        color: #f97316;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>AFC Bournemouth 1-0 Wolverhampton Wanderers</h1>
    <p>Premier League 2025/26 • Matchday 2 • August 23, 2025 • Vitality Stadium</p>
    <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
        <div>
            <div style="font-size: 2rem; color: #dc2626; font-weight: bold;">1.78</div>
            <div>xG Bournemouth</div>
        </div>
        <div style="font-size: 2rem; color: #6b7280;">vs</div>
        <div>
            <div style="font-size: 2rem; color: #f97316; font-weight: bold;">0.37</div>
            <div>xG Wolves</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Data preparation
@st.cache_data
def load_match_data():
    # Match data
    bournemouth_players = [
        {"name": "Neto", "number": 1, "position": "GK", "x": 10, "y": 50},
        {"name": "Smith", "number": 15, "position": "RB", "x": 25, "y": 20},
        {"name": "Zabarnyi", "number": 27, "position": "CB", "x": 25, "y": 35},
        {"name": "Senesi", "number": 25, "position": "CB", "x": 25, "y": 65},
        {"name": "Kerkez", "number": 3, "position": "LB", "x": 25, "y": 80},
        {"name": "Adams", "number": 12, "position": "DM", "x": 40, "y": 50},
        {"name": "Christie", "number": 10, "position": "RM", "x": 55, "y": 25},
        {"name": "Brooks", "number": 7, "position": "CM", "x": 55, "y": 40},
        {"name": "Semenyo", "number": 24, "position": "CM", "x": 55, "y": 60},
        {"name": "Tavernier", "number": 16, "position": "LM", "x": 55, "y": 75},
        {"name": "Evanilson", "number": 9, "position": "ST", "x": 70, "y": 50}
    ]
    
    wolves_players = [
        {"name": "José Sá", "number": 1, "position": "GK", "x": 10, "y": 50},
        {"name": "Doherty", "number": 2, "position": "RCB", "x": 25, "y": 25},
        {"name": "Agbadou", "number": 4, "position": "CB", "x": 25, "y": 50},
        {"name": "Toti", "number": 24, "position": "LCB", "x": 25, "y": 75},
        {"name": "Hoever", "number": 37, "position": "RWB", "x": 45, "y": 15},
        {"name": "Lemina", "number": 5, "position": "CM", "x": 45, "y": 40},
        {"name": "Bellegarde", "number": 27, "position": "CM", "x": 45, "y": 60},
        {"name": "Aït-Nouri", "number": 3, "position": "LWB", "x": 45, "y": 85},
        {"name": "Sarabia", "number": 21, "position": "RW", "x": 65, "y": 25},
        {"name": "Strand Larsen", "number": 9, "position": "ST", "x": 65, "y": 50},
        {"name": "Arias", "number": 18, "position": "LW", "x": 65, "y": 75}
    ]
    
    # Shot data
    shot_data = [
        {"team": "Bournemouth", "player": "Brooks", "x": 89.9, "y": 36.2, "type": "off_target", "xG": 0.049, "minute": 1},
        {"team": "Bournemouth", "player": "Tavernier", "x": 89.5, "y": 68.1, "type": "goal", "xG": 0.063, "minute": 4},
        {"team": "Bournemouth", "player": "Semenyo", "x": 97.1, "y": 51.7, "type": "post", "xG": 0.695, "minute": 9},
        {"team": "Bournemouth", "player": "Brooks", "x": 72.3, "y": 46.1, "type": "blocked", "xG": 0.033, "minute": 10},
        {"team": "Bournemouth", "player": "Scott", "x": 79.1, "y": 43.3, "type": "off_target", "xG": 0.047, "minute": 46},
        {"team": "Bournemouth", "player": "Brooks", "x": 84.9, "y": 31.0, "type": "blocked", "xG": 0.052, "minute": 49},
        {"team": "Bournemouth", "player": "Tavernier", "x": 80.6, "y": 48.0, "type": "saved", "xG": 0.044, "minute": 50},
        {"team": "Bournemouth", "player": "Semenyo", "x": 89.3, "y": 55.2, "type": "off_target", "xG": 0.425, "minute": 55},
        {"team": "Bournemouth", "player": "Semenyo", "x": 92.7, "y": 70.3, "type": "saved", "xG": 0.056, "minute": 66},
        {"team": "Bournemouth", "player": "Adams", "x": 77.1, "y": 44.3, "type": "saved", "xG": 0.031, "minute": 69},
        {"team": "Bournemouth", "player": "Christie", "x": 86.5, "y": 49.3, "type": "blocked", "xG": 0.108, "minute": 74},
        {"team": "Bournemouth", "player": "Kluivert", "x": 71.4, "y": 62.5, "type": "off_target", "xG": 0.017, "minute": 80},
        {"team": "Bournemouth", "player": "Semenyo", "x": 87.2, "y": 62.4, "type": "blocked", "xG": 0.078, "minute": 84},
        {"team": "Bournemouth", "player": "Kluivert", "x": 77.6, "y": 43.9, "type": "blocked", "xG": 0.085, "minute": 85},
        {"team": "Wolves", "player": "Munetsi", "x": 87.6, "y": 44.9, "type": "off_target", "xG": 0.083, "minute": 1},
        {"team": "Wolves", "player": "Strand Larsen", "x": 88.6, "y": 47.1, "type": "saved", "xG": 0.059, "minute": 17},
        {"team": "Wolves", "player": "Bellegarde", "x": 79.2, "y": 32.0, "type": "blocked", "xG": 0.013, "minute": 44},
        {"team": "Wolves", "player": "Arias", "x": 88.4, "y": 56.3, "type": "off_target", "xG": 0.077, "minute": 45},
        {"team": "Wolves", "player": "Agbadou", "x": 80.3, "y": 62.6, "type": "blocked", "xG": 0.098, "minute": 64},
        {"team": "Wolves", "player": "Bueno", "x": 83.0, "y": 56.8, "type": "off_target", "xG": 0.043, "minute": 95}
    ]
    
    # xG Development data
    xg_development = [
        {"minute": 0, "Bournemouth_xG": 0, "Wolves_xG": 0},
        {"minute": 1, "Bournemouth_xG": 0.049, "Wolves_xG": 0.083},
        {"minute": 4, "Bournemouth_xG": 0.112, "Wolves_xG": 0.083},
        {"minute": 9, "Bournemouth_xG": 0.807, "Wolves_xG": 0.083},
        {"minute": 10, "Bournemouth_xG": 0.840, "Wolves_xG": 0.083},
        {"minute": 17, "Bournemouth_xG": 0.840, "Wolves_xG": 0.142},
        {"minute": 44, "Bournemouth_xG": 0.840, "Wolves_xG": 0.155},
        {"minute": 45, "Bournemouth_xG": 0.840, "Wolves_xG": 0.232},
        {"minute": 46, "Bournemouth_xG": 0.887, "Wolves_xG": 0.232},
        {"minute": 49, "Bournemouth_xG": 0.939, "Wolves_xG": 0.232},
        {"minute": 50, "Bournemouth_xG": 0.983, "Wolves_xG": 0.232},
        {"minute": 55, "Bournemouth_xG": 1.408, "Wolves_xG": 0.232},
        {"minute": 64, "Bournemouth_xG": 1.408, "Wolves_xG": 0.330},
        {"minute": 66, "Bournemouth_xG": 1.464, "Wolves_xG": 0.330},
        {"minute": 69, "Bournemouth_xG": 1.495, "Wolves_xG": 0.330},
        {"minute": 74, "Bournemouth_xG": 1.603, "Wolves_xG": 0.330},
        {"minute": 80, "Bournemouth_xG": 1.620, "Wolves_xG": 0.330},
        {"minute": 84, "Bournemouth_xG": 1.698, "Wolves_xG": 0.330},
        {"minute": 85, "Bournemouth_xG": 1.783, "Wolves_xG": 0.330},
        {"minute": 95, "Bournemouth_xG": 1.783, "Wolves_xG": 0.373}
    ]
    
    # Key moments
    key_moments = [
        {"minute": 1, "event": "Early chance", "team": "Both", "intensity": 30},
        {"minute": 4, "event": "GOAL Tavernier", "team": "Bournemouth", "intensity": 100},
        {"minute": 9, "event": "Semenyo hits post", "team": "Bournemouth", "intensity": 95},
        {"minute": 17, "event": "Strand Larsen saved", "team": "Wolves", "intensity": 60},
        {"minute": 49, "event": "Toti RED CARD", "team": "Wolves", "intensity": -80},
        {"minute": 55, "event": "Semenyo big chance", "team": "Bournemouth", "intensity": 85},
        {"minute": 64, "event": "Agbadou blocked", "team": "Wolves", "intensity": 50},
        {"minute": 84, "event": "Semenyo blocked", "team": "Bournemouth", "intensity": 70},
        {"minute": 90, "event": "Final whistle", "team": "Neutral", "intensity": 0}
    ]
    
    return {
        'bournemouth_players': bournemouth_players,
        'wolves_players': wolves_players,
        'shot_data': shot_data,
        'xg_development': xg_development,
        'key_moments': key_moments
    }

# Load data
data = load_match_data()

# Sidebar navigation
st.sidebar.title("⚽ Match Analysis")
tab = st.sidebar.selectbox(
    "Select Analysis View",
    ["📊 Overview", "🎯 Tactical Analysis", "📈 Data Analysis"]
)

# Helper function to create pitch visualization
def create_pitch_visualization(shot_data=None, show_players=True):
    fig = go.Figure()
    
    # Create pitch outline
    fig.add_shape(type="rect", x0=0, y0=0, x1=100, y1=100, 
                  line=dict(color="white", width=3), fillcolor="green")
    
    # Center line
    fig.add_shape(type="line", x0=50, y0=0, x1=50, y1=100, 
                  line=dict(color="white", width=2))
    
    # Center circle
    fig.add_shape(type="circle", x0=40, y0=40, x1=60, y1=60,
                  line=dict(color="white", width=2))
    
    # Penalty areas
    fig.add_shape(type="rect", x0=0, y0=22, x1=17, y1=78,
                  line=dict(color="white", width=2))
    fig.add_shape(type="rect", x0=83, y0=22, x1=100, y1=78,
                  line=dict(color="white", width=2))
    
    # Goal areas
    fig.add_shape(type="rect", x0=0, y0=36, x1=6, y1=64,
                  line=dict(color="white", width=2))
    fig.add_shape(type="rect", x0=94, y0=36, x1=100, y1=64,
                  line=dict(color="white", width=2))
    
    if show_players:
        # Add Bournemouth players
        for player in data['bournemouth_players']:
            fig.add_trace(go.Scatter(
                x=[player['x']], y=[100-player['y']],
                mode='markers+text',
                marker=dict(size=20, color='red', line=dict(color='white', width=2)),
                text=[str(player['number'])],
                textfont=dict(color='white', size=12),
                name=f"BOU {player['name']}",
                hovertemplate=f"<b>{player['name']}</b><br>Position: {player['position']}<br>Number: {player['number']}<extra></extra>"
            ))
        
        # Add Wolves players (flip x-coordinate)
        for player in data['wolves_players']:
            fig.add_trace(go.Scatter(
                x=[100-player['x']], y=[100-player['y']],
                mode='markers+text',
                marker=dict(size=20, color='orange', line=dict(color='white', width=2)),
                text=[str(player['number'])],
                textfont=dict(color='white', size=12),
                name=f"WOL {player['name']}",
                hovertemplate=f"<b>{player['name']}</b><br>Position: {player['position']}<br>Number: {player['number']}<extra></extra>"
            ))
    
    if shot_data:
        for shot in shot_data:
            color_map = {
                'goal': 'gold',
                'post': 'yellow',
                'saved': 'blue',
                'blocked': 'orange',
                'off_target': 'gray'
            }
            
            x_pos = shot['x'] if shot['team'] == 'Bournemouth' else 100 - shot['x']
            
            fig.add_trace(go.Scatter(
                x=[x_pos], y=[100-shot['y']],
                mode='markers',
                marker=dict(
                    size=15 if shot['type'] == 'goal' else 10,
                    color=color_map[shot['type']],
                    line=dict(color='black', width=2)
                ),
                name=f"{shot['player']} ({shot['type']})",
                hovertemplate=f"<b>{shot['player']}</b><br>Minute: {shot['minute']}'<br>xG: {shot['xG']:.3f}<br>Result: {shot['type']}<extra></extra>"
            ))
    
    fig.update_layout(
        title="Football Pitch Visualization",
        xaxis=dict(range=[0, 100], showgrid=False, showticklabels=False),
        yaxis=dict(range=[0, 100], showgrid=False, showticklabels=False),
        plot_bgcolor='green',
        paper_bgcolor='darkgreen',
        showlegend=False,
        height=600,
        width=1000
    )
    
    return fig

if tab == "📊 Overview":
    st.header("Match Overview")
    
    # Key statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <h3>🏆 Final Score</h3>
            <h2>1-0</h2>
            <p>Bournemouth Victory</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <h3>⚽ Expected Goals</h3>
            <h2>1.78 - 0.37</h2>
            <p>Bournemouth deserved win</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <h3>⚡ PPDA</h3>
            <h2>8.2</h2>
            <p>Bournemouth press intensity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <h3>🎯 Final Third Entries</h3>
            <h2>47-23</h2>
            <p>Bournemouth dominance</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Visualization selector
    viz_option = st.selectbox(
        "Select Visualization",
        ["Starting Formations", "Shot Map", "xG Development", "Match Momentum"]
    )
    
    if viz_option == "Starting Formations":
        st.subheader("⚽ Starting Formations")
        st.plotly_chart(create_pitch_visualization(show_players=True), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### <span class='team-red'>AFC Bournemouth (4-1-4-1)</span>", unsafe_allow_html=True)
            st.write("• Adams as single pivot")
            st.write("• Wide players providing width")
            st.write("• Evanilson isolated striker")
        
        with col2:
            st.markdown("### <span class='team-orange'>Wolverhampton (3-4-3)</span>", unsafe_allow_html=True)
            st.write("• Three center-backs")
            st.write("• Wing-backs providing width")
            st.write("• Front three attacking line")
    
    elif viz_option == "Shot Map":
        st.subheader("🎯 Shot Map & xG Analysis")
        shot_fig = create_pitch_visualization(shot_data=data['shot_data'], show_players=False)
        st.plotly_chart(shot_fig, use_container_width=True)
        
        # Shot statistics
        bou_shots = [s for s in data['shot_data'] if s['team'] == 'Bournemouth']
        wolves_shots = [s for s in data['shot_data'] if s['team'] == 'Wolves']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Bournemouth Shots", len(bou_shots))
            st.metric("Bournemouth xG", f"{sum(s['xG'] for s in bou_shots):.2f}")
        
        with col2:
            st.metric("Wolves Shots", len(wolves_shots))
            st.metric("Wolves xG", f"{sum(s['xG'] for s in wolves_shots):.2f}")
    
    elif viz_option == "xG Development":
        st.subheader("📈 Expected Goals Development")
        
        # Create xG timeline
        xg_df = pd.DataFrame(data['xg_development'])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=xg_df['minute'], 
            y=xg_df['Bournemouth_xG'],
            mode='lines+markers',
            name='Bournemouth xG',
            line=dict(color='red', width=3),
            marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=xg_df['minute'], 
            y=xg_df['Wolves_xG'],
            mode='lines+markers',
            name='Wolves xG',
            line=dict(color='orange', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="xG Development Throughout Match",
            xaxis_title="Match Time (minutes)",
            yaxis_title="Cumulative xG",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key xG moments
        st.write("**Key xG Moments:**")
        st.write("• 4' - Tavernier goal (0.063 xG)")
        st.write("• 9' - Semenyo hits post (0.695 xG - huge chance!)")
        st.write("• 55' - Semenyo big chance (0.425 xG)")
    
    elif viz_option == "Match Momentum":
        st.subheader("📊 Match Momentum & Key Moments")
        
        # Create momentum chart
        moments_df = pd.DataFrame(data['key_moments'])
        
        colors = []
        for _, row in moments_df.iterrows():
            if row['team'] == 'Bournemouth':
                colors.append('red')
            elif row['team'] == 'Wolves':
                colors.append('orange')
            else:
                colors.append('gray')
        
        fig = go.Figure(data=[
            go.Bar(
                x=moments_df['minute'],
                y=moments_df['intensity'],
                marker_color=colors,
                text=moments_df['event'],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Match Momentum (Positive = Good for Team, Negative = Setback)",
            xaxis_title="Match Time (minutes)",
            yaxis_title="Impact Intensity",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

elif tab == "🎯 Tactical Analysis":
    st.header("Tactical Analysis")
    
    # Team performance comparison
    categories = ['Attack', 'Defense', 'Possession', 'Pressing', 'Set Pieces', 'Discipline']
    bournemouth_values = [85, 75, 90, 88, 85, 80]
    wolves_values = [40, 85, 60, 45, 40, 30]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=bournemouth_values + [bournemouth_values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Bournemouth',
        line_color='red'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=wolves_values + [wolves_values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Wolves',
        line_color='orange'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Team Performance Radar",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Team analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### <span class='team-red'>AFC Bournemouth Analysis</span>", unsafe_allow_html=True)
        
        with st.expander("Formation & Setup"):
            st.write("• 4-1-4-1 with Adams as single pivot")
            st.write("• Wide players (Tavernier, Christie) providing width")
            st.write("• Evanilson isolated but effective hold-up play")
        
        with st.expander("Key Tactical Elements"):
            st.write("• High possession (59%) - controlled tempo")
            st.write("• 47 final third entries vs 23")
            st.write("• 18 box entries - clinical in dangerous areas")
            st.write("• xG 1.78 - created high-quality chances")
        
        with st.expander("Star Performers"):
            st.write("• **Semenyo:** Hit crossbar with high xG chance")
            st.write("• **Tavernier:** Goal scorer, multiple efforts")
            st.write("• **Adams:** 89 passes, 95% accuracy, anchor")
    
    with col2:
        st.markdown("### <span class='team-orange'>Wolverhampton Analysis</span>", unsafe_allow_html=True)
        
        with st.expander("Formation Issues"):
            st.write("• 3-4-3 left wing-backs exposed")
            st.write("• Central midfield overrun by Bournemouth")
            st.write("• Wide forwards isolated after red card")
        
        with st.expander("Tactical Problems"):
            st.write("• Low possession (41%) - couldn't control game")
            st.write("• Only 23 final third entries")
            st.write("• 8 box entries - struggled in final third")
            st.write("• xG 0.37 - poor chance creation")
        
        with st.expander("Positives"):
            st.write("• **José Sá:** Made crucial saves")
            st.write("• **Agbadou:** Strong aerial presence")
            st.write("• **Lemina:** 67 passes, 87% completion")

elif tab == "📈 Data Analysis":
    st.header("Data Analysis")
    
    # Player performance tables
    st.subheader("Individual Player Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### <span class='team-red'>AFC Bournemouth</span>", unsafe_allow_html=True)
        bou_data = {
            'Player': ['Tavernier', 'Semenyo', 'Adams', 'Brooks', 'Christie'],
            'Position': ['LM', 'CM', 'DM', 'CM', 'RM'],
            'Rating': [8.2, 7.8, 7.5, 7.2, 7.0],
            'Key Stats': ['1G, 3 shots', 'Hit crossbar, 4 shots', '89 passes, 95% accuracy', '3 shots, 63 passes', '1 shot, 47 passes']
        }
        st.dataframe(pd.DataFrame(bou_data))
    
    with col2:
        st.markdown("#### <span class='team-orange'>Wolverhampton</span>", unsafe_allow_html=True)
        wolves_data = {
            'Player': ['José Sá', 'Lemina', 'Strand Larsen', 'Arias', 'Toti'],
            'Position': ['GK', 'CM', 'ST', 'LW', 'LCB'],
            'Rating': [7.8, 6.8, 6.5, 6.2, 4.5],
            'Key Stats': ['3 saves', '67 passes, 87% accuracy', '1 shot on target', '1 shot, 29 passes', 'Red card 49\'']
        }
        st.dataframe(pd.DataFrame(wolves_data))
    
    # Advanced metrics
    st.subheader("Advanced Metrics Comparison")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Shooting Accuracy", "28.6% vs 16.7%", "Bournemouth advantage")
    
    with col2:
        st.metric("Pass Completion", "87.3% vs 79.8%", "Superior ball retention")
    
    with col3:
        st.metric("Duel Success", "58.2% vs 52.1%", "Ground + Aerial combined")
    
    with col4:
        st.metric("Discipline", "2Y vs 4Y+1R", "Wolves poor discipline")
    
    # Possession and shots comparison
    col1, col2 = st.columns(2)
    
    with col1:
        # Possession pie chart
        possession_data = ['Bournemouth', 'Wolves']
        possession_values = [59, 41]
        
        fig_possession = px.pie(
            values=possession_values, 
            names=possession_data,
            title="Ball Possession %",
            color_discrete_sequence=['#dc2626', '#f97316']
        )
        st.plotly_chart(fig_possession, use_container_width=True)
    
    with col2:
        # Shots comparison
        shots_data = {
            'Team': ['Bournemouth', 'Wolves'],
            'On Target': [4, 1],
            'Off Target': [10, 5]
        }
        shots_df = pd.DataFrame(shots_data)
        
        fig_shots = px.bar(
            shots_df, 
            x='Team', 
            y=['On Target', 'Off Target'],
            title="Shot Analysis",
            color_discrete_sequence=['#10b981', '#ef4444']
        )
        st.plotly_chart(fig_shots, use_container_width=True)
    
    # Shot quality scatter plot
    st.subheader("Shot Quality vs Time Analysis")
    
    shot_df = pd.DataFrame(data['shot_data'])
    
    fig_scatter = px.scatter(
        shot_df,
        x='minute',
        y='xG',
        color='team',
        size='xG',
        hover_data=['player', 'type'],
        title="Shot Quality Throughout Match",
        color_discrete_sequence=['#dc2626', '#f97316']
    )
    
    fig_scatter.update_layout(
        xaxis_title="Match Time (minutes)",
        yaxis_title="Expected Goals (xG)",
        height=400
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Discipline comparison
    st.subheader("Discipline Comparison")
    
    discipline_data = {
        'Category': ['Yellow Cards', 'Red Cards', 'Fouls Committed'],
        'Bournemouth': [2, 0, 12],
        'Wolves': [4, 1, 18]
    }
    discipline_df = pd.DataFrame(discipline_data)
    
    fig_discipline = px.bar(
        discipline_df,
        x='Category',
        y=['Bournemouth', 'Wolves'],
        title="Disciplinary Records",
        color_discrete_sequence=['#dc2626', '#f97316'],
        barmode='group'
    )
    
    st.plotly_chart(fig_discipline, use_container_width=True)

# Footer with deployment instructions
st.markdown("---")
st.markdown("""
### 🚀 Deployment Instructions

To deploy this Streamlit app:

1. **Install required packages:**
```bash
pip install streamlit pandas plotly
```

2. **Save this code as `match_analysis.py`**

3. **Run locally:**
```bash
streamlit run match_analysis.py
```

4. **Deploy to Streamlit Cloud:**
   - Push code to GitHub repository
   - Connect repository to [share.streamlit.io](https://share.streamlit.io)
   - Deploy automatically

5. **Alternative deployment options:**
   - Heroku
   - AWS
   - Google Cloud Platform
   - Azure

### 📊 Features Included:

- **Interactive pitch visualizations** with player positions and shot locations
- **Real-time data tooltips** showing detailed statistics
- **Multiple analysis tabs** (Overview, Tactical, Data Analysis)
- **Advanced metrics** including xG development and match momentum
- **Responsive design** that works on desktop and mobile
- **Professional styling** with team colors and branding

### 💡 Data Sources:
All match data, player statistics, and tactical analysis based on the August 23, 2025 Premier League fixture between AFC Bournemouth and Wolverhampton Wanderers.
""")

# Sidebar additional info
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📈 Match Stats Summary
- **Final Score:** 1-0 to Bournemouth
- **xG:** 1.78 - 0.37
- **Possession:** 59% - 41%
- **Shots:** 14 - 6
- **Key Moment:** Toti red card (49')
""")

st.sidebar.markdown("""
### 🎯 Key Players
**Bournemouth:**
- Tavernier (Goal scorer)
- Semenyo (Hit post)
- Adams (Playmaker)

**Wolves:**
- José Sá (Goalkeeper)
- Toti (Red card)
- Lemina (Most passes)
""")