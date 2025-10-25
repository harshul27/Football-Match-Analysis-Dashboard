import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Crystal Palace 3-3 Bournemouth Analysis",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; /* Ensure header text is white */
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
        color: #1a1a1a; /* SET DARK TEXT COLOR for visibility on white background */
    }
    .insight-box {
        background: #f0f9ff;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin: 10px 0;
        color: #1a1a1a; /* SET DARK TEXT COLOR for visibility on light blue background */
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>⚽ Crystal Palace 3-3 AFC Bournemouth</h1>
    <h3>Premier League • Selhurst Park • October 2024</h3>
    <p><i>"A Battle of Halves: Tactical Masterclass Unfolds"</i></p>
</div>
""", unsafe_allow_html=True)

# Score display
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.markdown("### 🔵 Crystal Palace")
with col2:
    st.markdown("<h1 style='text-align: center;'>3 - 3</h1>", unsafe_allow_html=True)
with col3:
    st.markdown("### 🔴 Bournemouth")

st.markdown("---")

# Key Stats Cards
st.subheader("📊 Key Match Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card" style="border-left-color: #1e40af;">
        <h4>🎯 Mateta Hat-Trick</h4>
        <h2 style="color: #1e40af;">3</h2>
        <p>Goals from 10 shots</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card" style="border-left-color: #dc2626;">
        <h4>⚡ Bournemouth PPDA</h4>
        <h2 style="color: #dc2626;">7.2</h2>
        <p>Elite pressing (1st half)</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card" style="border-left-color: #059669;">
        <h4>📈 Progressive Passes</h4>
        <h2 style="color: #059669;">34</h2>
        <p>Palace 2nd half (+89%)</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card" style="border-left-color: #7c3aed;">
        <h4>👥 Nketiah Impact</h4>
        <h2 style="color: #7c3aed;">63'</h2>
        <p>Game-changing sub</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Sidebar navigation
st.sidebar.title("📑 Navigation")
tab_selection = st.sidebar.radio(
    "Select Analysis Section:",
    ["Overview", "Timeline", "Players", "Tactical", "Advanced"]
)

# Data preparation
@st.cache_data
def load_data():
    # Match Overview Data
    overview_stats = pd.DataFrame({
        'Metric': ['Possession', 'Shots', 'Shots on Target', 'xG', 'Passes', 'Pass Accuracy %'],
        'Palace': [48, 19, 11, 2.89, 387, 79],
        'Bournemouth': [52, 13, 7, 1.85, 421, 84]
    })
    
    # xG Timeline
    xg_timeline = pd.DataFrame({
        'Minute': [0, 7, 15, 30, 38, 45, 50, 61, 65, 69, 76, 88, 90],
        'Palace': [0, 0, 0.08, 0.24, 0.24, 0.42, 0.68, 0.94, 1.56, 2.18, 2.45, 2.45, 2.89],
        'Bournemouth': [0, 0.52, 0.52, 0.71, 1.18, 1.28, 1.28, 1.42, 1.42, 1.42, 1.58, 2.25, 2.25]
    })
    
    # Progressive Passes
    prog_passes = pd.DataFrame({
        'Period': ['First Half', 'Second Half'],
        'Palace': [18, 34],
        'Bournemouth': [24, 16]
    })
    
    # Aerial Duels
    aerial_duels = pd.DataFrame({
        'Period': ['First Half', 'Second Half'],
        'Palace Won': [8, 19],
        'Palace Total': [16, 24],
        'Bmouth Won': [11, 9],
        'Bmouth Total': [17, 18]
    })
    
    # Final Third Entries
    final_third = pd.DataFrame({
        'Period': ['0-15', '15-30', '30-45', '45-60', '60-75', '75-90'],
        'Palace': [7, 9, 8, 15, 21, 18],
        'Bournemouth': [14, 16, 18, 12, 9, 11]
    })
    
    # Crosses
    crosses_data = pd.DataFrame({
        'Side': ['Palace Left', 'Palace Right', 'Bmouth Left', 'Bmouth Right'],
        'First Half': [6, 4, 14, 6],
        'Second Half': [13, 8, 7, 5]
    })
    
    # PPDA
    ppda_data = pd.DataFrame({
        'Period': ['0-15', '15-30', '30-45', '45-60', '60-75', '75-90'],
        'Bournemouth': [7.2, 6.8, 7.5, 9.4, 11.5, 11.2],
        'Palace': [15.3, 14.8, 15.9, 12.6, 10.8, 10.3]
    })
    
    # Long Balls
    long_balls = pd.DataFrame({
        'Period': ['0-30', '30-45', '45-60', '60-75', '75-90'],
        'Palace': [8, 12, 15, 22, 11],
        'Bournemouth': [6, 7, 9, 8, 12]
    })
    
    # Defensive Line Height
    def_line = pd.DataFrame({
        'Period': ['0-15', '15-30', '30-45', '45-60', '60-75', '75-90'],
        'Palace': [38.5, 37.2, 36.8, 41.5, 44.8, 42.3],
        'Bournemouth': [52.8, 54.3, 51.6, 48.2, 42.7, 39.5]
    })
    
    # Ball Recoveries
    ball_recoveries = pd.DataFrame({
        'Period': ['1st Half', '2nd Half'],
        'Palace High': [6, 16],
        'Palace Mid': [21, 31],
        'Bmouth High': [18, 11],
        'Bmouth Mid': [23, 18]
    })
    
    # Pass Completion Zones
    pass_zones = pd.DataFrame({
        'Zone': ['Defensive 3rd', 'Middle 3rd', 'Final 3rd', 'Penalty Box'],
        'Palace': [88, 79, 68, 61],
        'Bournemouth': [92, 84, 73, 69]
    })
    
    # Pressing Success
    pressing = pd.DataFrame({
        'Zone': ['High Press', 'Mid Press', 'Defensive'],
        'Palace': [42, 48, 64],
        'Bournemouth': [61, 54, 52]
    })
    
    return {
        'overview': overview_stats,
        'xg_timeline': xg_timeline,
        'prog_passes': prog_passes,
        'aerial_duels': aerial_duels,
        'final_third': final_third,
        'crosses': crosses_data,
        'ppda': ppda_data,
        'long_balls': long_balls,
        'def_line': def_line,
        'ball_recoveries': ball_recoveries,
        'pass_zones': pass_zones,
        'pressing': pressing
    }

data = load_data()

# OVERVIEW TAB
if tab_selection == "Overview":
    st.header("📋 Match Overview")
    
    # Match Summary
    st.markdown("""
    <div class="insight-box">
    <h4>Match Summary</h4>
    <p>A thrilling encounter that showcased two distinct halves: Bournemouth's aggressive pressing and 
    dynamic pivot play dominated the first 45 minutes, establishing a 2-0 lead. However, Palace's tactical 
    adjustments - particularly the introduction of Nketiah creating a dual striker threat - combined with 
    superior aerial dominance and an 89% increase in progressive passes turned the tide completely.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Match Statistics
    st.subheader("📊 Match Statistics Comparison")
    fig = go.Figure()
    
    for idx, row in data['overview'].iterrows():
        fig.add_trace(go.Bar(
            name='Crystal Palace' if idx == 0 else '',
            y=[row['Metric']],
            x=[row['Palace']],
            orientation='h',
            marker_color='#1e40af',
            showlegend=(idx == 0),
            legendgroup='palace'
        ))
        fig.add_trace(go.Bar(
            name='Bournemouth' if idx == 0 else '',
            y=[row['Metric']],
            x=[row['Bournemouth']],
            orientation='h',
            marker_color='#dc2626',
            showlegend=(idx == 0),
            legendgroup='bmouth'
        ))
    
    fig.update_layout(
        barmode='group',
        height=400,
        title="Match Statistics",
        xaxis_title="Value",
        yaxis_title="Metric",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Crosses and Progressive Passes
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Crosses by Flank & Half")
        fig = go.Figure()
        fig.add_trace(go.Bar(name='First Half', x=data['crosses']['Side'], y=data['crosses']['First Half'], marker_color='#9333ea'))
        fig.add_trace(go.Bar(name='Second Half', x=data['crosses']['Side'], y=data['crosses']['Second Half'], marker_color='#06b6d4'))
        fig.update_layout(barmode='group', height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.info("Bournemouth's left flank dominance (14 crosses) waned in 2nd half")
    
    with col2:
        st.subheader("⚡ Progressive Passes by Half")
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Palace', x=data['prog_passes']['Period'], y=data['prog_passes']['Palace'], marker_color='#1e40af'))
        fig.add_trace(go.Bar(name='Bournemouth', x=data['prog_passes']['Period'], y=data['prog_passes']['Bournemouth'], marker_color='#dc2626'))
        fig.update_layout(barmode='group', height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.success("Palace's 89% increase (18→34) overwhelmed tired Bournemouth")
    
    # Aerial Duels and Pass Completion
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🦅 Aerial Duels by Half")
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Palace Won', x=data['aerial_duels']['Period'], y=data['aerial_duels']['Palace Won'], marker_color='#1e40af'))
        fig.add_trace(go.Bar(name='Bmouth Won', x=data['aerial_duels']['Period'], y=data['aerial_duels']['Bmouth Won'], marker_color='#dc2626'))
        fig.update_layout(barmode='group', height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.info("Palace 2nd half aerial superiority (79%) crucial to comeback")
    
    with col2:
        st.subheader("📍 Pass Completion by Zone")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['pass_zones']['Zone'], y=data['pass_zones']['Palace'], 
                                mode='lines+markers', name='Palace', line=dict(color='#1e40af', width=3)))
        fig.add_trace(go.Scatter(x=data['pass_zones']['Zone'], y=data['pass_zones']['Bournemouth'], 
                                mode='lines+markers', name='Bournemouth', line=dict(color='#dc2626', width=3)))
        fig.update_layout(height=350, yaxis_title="Completion %")
        st.plotly_chart(fig, use_container_width=True)
        st.info("Bournemouth maintained higher accuracy across all zones")

# TIMELINE TAB
elif tab_selection == "Timeline":
    st.header("⏱️ Match Timeline Analysis")
    
    # xG Timeline
    st.subheader("📈 xG Timeline Evolution")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['xg_timeline']['Minute'], y=data['xg_timeline']['Palace'],
                            fill='tozeroy', name='Crystal Palace', line=dict(color='#1e40af', width=2)))
    fig.add_trace(go.Scatter(x=data['xg_timeline']['Minute'], y=data['xg_timeline']['Bournemouth'],
                            fill='tozeroy', name='Bournemouth', line=dict(color='#dc2626', width=2)))
    fig.update_layout(height=400, xaxis_title="Minute", yaxis_title="Expected Goals (xG)")
    st.plotly_chart(fig, use_container_width=True)
    st.info("Bournemouth dominated first half xG (1.28 vs 0.42), Palace surged in second half")
    
    # Final Third Entries
    st.subheader("🎯 Final Third Entries by Period")
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Palace', x=data['final_third']['Period'], y=data['final_third']['Palace'], marker_color='#1e40af'))
    fig.add_trace(go.Bar(name='Bournemouth', x=data['final_third']['Period'], y=data['final_third']['Bournemouth'], marker_color='#dc2626'))
    fig.update_layout(barmode='group', height=350)
    st.plotly_chart(fig, use_container_width=True)
    st.success("Palace's entries surged from 7 (0-15') to 21 (60-75') as Bournemouth retreated")
    
    # PPDA
    st.subheader("🔥 PPDA - Pressing Intensity Evolution")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['ppda']['Period'], y=data['ppda']['Bournemouth'],
                            mode='lines+markers', name='Bournemouth', line=dict(color='#dc2626', width=3)))
    fig.add_trace(go.Scatter(x=data['ppda']['Period'], y=data['ppda']['Palace'],
                            mode='lines+markers', name='Palace', line=dict(color='#1e40af', width=3)))
    fig.update_layout(height=350, yaxis_title="PPDA (Lower = More Intense)")
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)
    st.warning("Bournemouth's elite pressing (7.2) unsustainable - dropped to 11.2 by final period")
    
    # Long Balls and Defensive Line
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 Long Balls from Defense")
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Palace', x=data['long_balls']['Period'], y=data['long_balls']['Palace'], marker_color='#1e40af'))
        fig.add_trace(go.Bar(name='Bournemouth', x=data['long_balls']['Period'], y=data['long_balls']['Bournemouth'], marker_color='#dc2626'))
        fig.update_layout(barmode='group', height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.info("Palace's long ball strategy peaked 60-75' (22) to bypass press")
    
    with col2:
        st.subheader("📏 Defensive Line Height")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['def_line']['Period'], y=data['def_line']['Bournemouth'],
                                fill='tozeroy', name='Bournemouth', line=dict(color='#dc2626', width=2)))
        fig.add_trace(go.Scatter(x=data['def_line']['Period'], y=data['def_line']['Palace'],
                                fill='tozeroy', name='Palace', line=dict(color='#1e40af', width=2)))
        fig.update_layout(height=350, yaxis_title="Meters from goal")
        st.plotly_chart(fig, use_container_width=True)
        st.warning("Bournemouth's line dropped 13.3m, Palace pushed up 6.3m")

# PLAYERS TAB
elif tab_selection == "Players":
    st.header("👥 Player Performance Analysis")
    
    # Player Radar Charts
    st.subheader("📊 Key Player Radar Charts")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Jean-Philippe Mateta")
        mateta_data = pd.DataFrame({
            'Stat': ['Goals', 'Shots', 'Touches in Box', 'Duels Won', 'Pass Accuracy'],
            'Value': [100, 85, 92, 68, 62]
        })
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=mateta_data['Value'],
            theta=mateta_data['Stat'],
            fill='toself',
            name='Mateta',
            marker_color='#1e40af'
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), height=300)
        st.plotly_chart(fig, use_container_width=True)
        st.success("**Hat-trick Hero:** 3 goals from 10 shots, 12 touches in box")
    
    with col2:
        st.markdown("#### Adam Wharton")
        wharton_data = pd.DataFrame({
            'Stat': ['Interceptions', 'Progressive Passes', 'Pass Accuracy', 'Tackles Won', 'Key Passes'],
            'Value': [95, 88, 91, 82, 78]
        })
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=wharton_data['Value'],
            theta=wharton_data['Stat'],
            fill='toself',
            name='Wharton',
            marker_color='#059669'
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), height=300)
        st.plotly_chart(fig, use_container_width=True)
        st.success("**Midfield Maestro:** 7+ interceptions, 14 progressive passes, 91% accuracy")
    
    with col3:
        st.markdown("#### Daniel Muñoz")
        munoz_data = pd.DataFrame({
            'Stat': ['Assists', 'Crosses Completed', 'Progressive Carries', 'Duels Won', 'Tackles'],
            'Value': [100, 75, 85, 71, 68]
        })
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=munoz_data['Value'],
            theta=munoz_data['Stat'],
            fill='toself',
            name='Muñoz',
            marker_color='#7c3aed'
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), height=300)
        st.plotly_chart(fig, use_container_width=True)
        st.success("**2nd Half Catalyst:** 2 assists, 8 progressive carries, 13 crosses")
    
    # Detailed Player Analysis
    st.subheader("🔍 Detailed Player Breakdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔵 Crystal Palace Key Performers")
        
        with st.expander("⚽ Mateta - Clinical Striker"):
            st.markdown("""
            - Hat-trick (65', 69', 90+7')
            - 10 shots (6 on target)
            - 12 touches in box
            - Movement created space for Nketiah
            - Clinical finishing in crucial moments
            """)
        
        with st.expander("🎯 Wharton - Defensive Anchor"):
            st.markdown("""
            - 7+ interceptions (game-high)
            - 14 progressive passes in 2nd half
            - Shut down Bournemouth's left-side triangulations
            - 91% pass accuracy under pressure
            - Key passes to Muñoz for both assists
            """)
        
        with st.expander("⚡ Muñoz - Second Half Dominator"):
            st.markdown("""
            - 2 assists (65', 69')
            - 13 crosses in 2nd half (vs 4 in 1st)
            - 8 progressive carries
            - Exploited space left by Truffert
            - Created constant overloads on right flank
            """)
        
        with st.expander("💪 Nketiah - Game Changer (63')"):
            st.markdown("""
            - Created 2v2 vs Bournemouth CBs
            - Forced Scott/Christie into confusion
            - Drew defenders away from Mateta
            - Changed tactical shape to 4-4-2
            - Palace scored twice within 4 minutes
            """)
    
    with col2:
        st.markdown("### 🔴 Bournemouth Key Performers")
        
        with st.expander("⭐ Semenyo - First Half Dynamo"):
            st.markdown("""
            - Assist for 2nd goal (38')
            - Won crucial second balls
            - 5/7 dribbles completed
            - 23 pressing actions (exhausting workrate)
            - Marked out by Richards & Muñoz in 2nd half
            """)
        
        with st.expander("🌟 Kroupi - Debut Dream Start"):
            st.markdown("""
            - Goal on debut (7')
            - Smart off-ball movement
            - Focal point for aerial attacks
            - Substitution hurt team structure
            - Lost aerial target for crosses
            """)
        
        with st.expander("🛡️ Senesi - Defensive Leader"):
            st.markdown("""
            - 8 clearances (team-high)
            - 6/8 aerial duels won
            - 91% pass accuracy
            - Yellow card via VAR
            - Struggled vs Palace's aerial bombardment
            """)
        
        with st.expander("🎯 Christie - Late Hero (88')"):
            st.markdown("""
            - Goal to secure 3-3 draw
            - Came on for Scott (68')
            - Unmarked run from deep
            - Finished Kluivert-Truffert-Doak buildup
            - More defensive role than Scott
            """)

# TACTICAL TAB
elif tab_selection == "Tactical":
    st.header("🎮 Tactical Analysis")
    
    # Formation Evolution
    st.subheader("🔄 Formation Evolution Throughout the Match")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #eff6ff; padding: 20px; border-radius: 10px; border-left: 4px solid #1e40af; color: #1a1a1a;">
        <h4 style="color: #1e40af;">🔵 Crystal Palace Formations</h4>
        
        <div style="background: white; padding: 10px; margin: 10px 0; border-radius: 5px; color: #1a1a1a;">
        <b>0-45': 3-4-2-1 / 3-4-3</b><br><br>
        <small>Back 3 + keeper, wingbacks high, 3-2-5 in attack</small>
        </div>
        
        <div style="background: white; padding: 10px; margin: 10px 0; border-radius: 5px; color: #1a1a1a;">
        <b>45-63': 4-2-3-1</b><br><br>
        <small>Richards pushed into midfield for control</small>
        </div>
        
        <div style="background: white; padding: 10px; margin: 10px 0; border-radius: 5px; color: #1a1a1a;">
        <b>63-90': 4-4-2 Dual Strikers</b><br><br>
        <small>Nketiah added, 2v2 vs CBs, 2 goals in 4 mins</small>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #fef2f2; padding: 20px; border-radius: 10px; border-left: 4px solid #dc2626; color: #1a1a1a;">
        <h4 style="color: #dc2626;">🔴 Bournemouth Formations</h4>
        
        <div style="background: white; padding: 10px; margin: 10px 0; border-radius: 5px; color: #1a1a1a;">
        <b>0-45': 4-2-4 High Press</b><br><br>
        <small>2 at back, fullbacks high, front 4 aggressive, PPDA 7.2</small>
        </div>
        
        <div style="background: white; padding: 10px; margin: 10px 0; border-radius: 5px; color: #1a1a1a;">
        <b>45-75': Gradual Retreat to 5-2-3</b><br><br>
        <small>Truffert deeper, PPDA dropped to 11.2</small>
        </div>
        
        <div style="background: white; padding: 10px; margin: 10px 0; border-radius: 5px; color: #1a1a1a;">
        <b>Post-Kroupi: Lost Focal Point</b><br><br>
        <small>No aerial target, relied on Semenyo + Doak width</small>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Ball Recoveries
    st.subheader("🛡️ Ball Recoveries by Zone")
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Palace High', x=data['ball_recoveries']['Period'], y=data['ball_recoveries']['Palace High'], marker_color='#1e40af'))
    fig.add_trace(go.Bar(name='Palace Mid', x=data['ball_recoveries']['Period'], y=data['ball_recoveries']['Palace Mid'], marker_color='#3b82f6'))
    fig.add_trace(go.Bar(name='Bmouth High', x=data['ball_recoveries']['Period'], y=data['ball_recoveries']['Bmouth High'], marker_color='#dc2626'))
    fig.add_trace(go.Bar(name='Bmouth Mid', x=data['ball_recoveries']['Period'], y=data['ball_recoveries']['Bmouth Mid'], marker_color='#ef4444'))
    fig.update_layout(barmode='group', height=400)
    st.plotly_chart(fig, use_container_width=True)
    st.warning("Complete tactical reversal: Bournemouth's high recoveries dropped 18→11, Palace increased 6→16")
    
    # Pressing Success and Key Insights
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Pressing Success by Zone")
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Palace', x=data['pressing']['Zone'], y=data['pressing']['Palace'], marker_color='#1e40af'))
        fig.add_trace(go.Bar(name='Bournemouth', x=data['pressing']['Zone'], y=data['pressing']['Bournemouth'], marker_color='#dc2626'))
        fig.update_layout(barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.info("Bournemouth most effective in High Press (61% success)")
    
    # The original code was cut off here. I'll complete the section to ensure full visibility.
    with col2:
        st.subheader("🔑 Tactical Insights Summary")
        st.markdown("""
        <div class="insight-box" style="border-left: 4px solid #f97316; background: #fff7ed; color: #1a1a1a;">
        <h5 style="color: #f97316;">Bournemouth's First Half Strategy</h5>
        <p><small>Overload wide areas, intense counter-press (PPDA 7.2), high defensive line to squeeze play.</small></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="insight-box" style="border-left: 4px solid #10b981; background: #ecfdf5; color: #1a1a1a;">
        <h5 style="color: #10b981;">Palace's Game-Winning Adjustment</h5>
        <p><small>Switch to 4-4-2 (Nketiah sub), bypass press with long balls and aggressive wingback play (Muñoz), capitalize on aerial superiority.</small></p>
        </div>
        """, unsafe_allow_html=True)
# END OF TABS (assuming "Advanced" is not implemented)
