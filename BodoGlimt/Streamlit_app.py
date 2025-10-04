import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

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
    </style>
""", unsafe_allow_html=True)

# Data
season_data = pd.DataFrame([
    {"year": 2022, "possession": 54, "xg": 1.3, "goals": 1.31, "pass_acc": 81, "def_line": 40, "vert": 52},
    {"year": 2023, "possession": 57, "xg": 1.55, "goals": 1.65, "pass_acc": 83, "def_line": 43, "vert": 55},
    {"year": 2024, "possession": 50, "xg": 1.7, "goals": 1.75, "pass_acc": 81, "def_line": 44, "vert": 51},
    {"year": 2025, "possession": 54.5, "xg": 2.2, "goals": 2.0, "pass_acc": 84, "def_line": 46, "vert": 57}
])

playmakers = pd.DataFrame([
    {"year": 2022, "name": "Berg", "influence": 72},
    {"year": 2023, "name": "Vetlesen", "influence": 85},
    {"year": 2024, "name": "Hauge", "influence": 78},
    {"year": 2025, "name": "Evjen", "influence": 88}
])

attack_zones = {
    2022: pd.DataFrame([{"zone": "Left Wing", "value": 62}, {"zone": "Central", "value": 38}]),
    2023: pd.DataFrame([{"zone": "Left Wing", "value": 49}, {"zone": "Half-Space", "value": 32}, {"zone": "Right Flank", "value": 19}]),
    2024: pd.DataFrame([{"zone": "Half-Space", "value": 47}, {"zone": "Left Wing", "value": 37}, {"zone": "Central", "value": 16}]),
    2025: pd.DataFrame([{"zone": "Half-Space", "value": 51}, {"zone": "Right Flank", "value": 39}, {"zone": "Central", "value": 10}])
}

player_stats = {
    "Hogh": pd.DataFrame([
        {"season": 2023, "goals": 7, "xG": 8.1, "assists": 4},
        {"season": 2024, "goals": 11, "xG": 10.8, "assists": 6},
        {"season": 2025, "goals": 16, "xG": 14.1, "assists": 5}
    ]),
    "Berg": pd.DataFrame([
        {"season": 2023, "goals": 2, "assists": 6, "xA": 5.7},
        {"season": 2024, "goals": 4, "assists": 7, "xA": 6.9},
        {"season": 2025, "goals": 3, "assists": 8, "xA": 7.6}
    ]),
    "Hauge": pd.DataFrame([
        {"season": 2023, "goals": 4, "xG": 3.2, "assists": 2},
        {"season": 2024, "goals": 5, "xG": 4.6, "assists": 2},
        {"season": 2025, "goals": 6, "xG": 5.3, "assists": 3}
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

seasonal_performance = pd.DataFrame([
    {"season": "2023", "points": 58, "goals": 67, "conceded": 32},
    {"season": "2024", "points": 62, "goals": 73, "conceded": 35},
    {"season": "2025", "points": 65, "goals": 80, "conceded": 28}
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

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Evolution", "👥 Players", "⚽ Tottenham Match"])

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
    
    with col2:
        st.markdown("#### Key Playmaker by Season")
        for _, pm in playmakers.iterrows():
            with st.container():
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"**{pm['name']}** ({pm['year']})")
                    st.progress(pm['influence'] / 100)
                with cols[1]:
                    st.markdown(f"**{pm['influence']}%**")

with tab2:
    st.markdown("## 4-Year Tactical Evolution")
    
    # Multi-line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=season_data['year'], y=season_data['possession'],
                             mode='lines+markers', name='Possession %',
                             line=dict(color='#fbbf24', width=3)))
    fig.add_trace(go.Scatter(x=season_data['year'], y=season_data['xg'],
                             mode='lines+markers', name='xG/Game',
                             line=dict(color='#ef4444', width=3)))
    fig.add_trace(go.Scatter(x=season_data['year'], y=season_data['goals'],
                             mode='lines+markers', name='Goals/Game',
                             line=dict(color='#22c55e', width=3)))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#93c5fd',
        height=450,
        xaxis_title='Year',
        yaxis_title='Value',
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### Season-by-Season Performance")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=seasonal_performance['season'], y=seasonal_performance['points'],
                          name='Points', marker_color='#fbbf24'))
    fig2.add_trace(go.Bar(x=seasonal_performance['season'], y=seasonal_performance['goals'],
                          name='Goals', marker_color='#22c55e'))
    fig2.add_trace(go.Bar(x=seasonal_performance['season'], y=seasonal_performance['conceded'],
                          name='Conceded', marker_color='#ef4444'))
    
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#93c5fd',
        height=350,
        barmode='group'
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### Key Milestones")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info("**2022**\n\nAI intro")
    with col2:
        st.info("**2023**\n\nVetlesen sale")
    with col3:
        st.warning("**2024**\n\nHauge return, Europa semi")
    with col4:
        st.success("**2025**\n\nCL debut, Tottenham draw")

with tab3:
    st.markdown("## Player Performance Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Kasper Hogh")
        hogh_df = player_stats['Hogh']
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hogh_df['season'], y=hogh_df['goals'],
                                mode='lines+markers', name='Goals',
                                line=dict(color='#fbbf24', width=2)))
        fig.add_trace(go.Scatter(x=hogh_df['season'], y=hogh_df['xG'],
                                mode='lines+markers', name='xG',
                                line=dict(color='#ef4444', width=2)))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=250,
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**2025:** 16 goals in 21 matches")
        st.markdown("3.5 shots per 90 minutes")
    
    with col2:
        st.markdown("### Patrick Berg")
        berg_df = player_stats['Berg']
        fig = go.Figure()
        fig.add_trace(go.Bar(x=berg_df['season'], y=berg_df['assists'],
                            name='Assists', marker_color='#fbbf24'))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=250,
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**2025:** 8 assists, 7.6 xA")
        st.markdown("92.7 passes completed per 90")
    
    with col3:
        st.markdown("### Jens Petter Hauge")
        hauge_df = player_stats['Hauge']
        fig = go.Figure()
        fig.add_trace(go.Bar(x=hauge_df['season'], y=hauge_df['goals'],
                            name='Goals', marker_color='#fbbf24'))
        fig.add_trace(go.Bar(x=hauge_df['season'], y=hauge_df['assists'],
                            name='Assists', marker_color='#22c55e'))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#93c5fd',
            height=250,
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**2025:** 56 successful take-ons")
        st.markdown("1.8 dribbles per 90")

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
                            line=dict(color='#fbbf24', width=2),
                            fillcolor='rgba(251, 191, 36, 0.3)',
                            hovertemplate='<b>%{text}</b><br>xG: %{y:.2f}<extra></extra>',
                            text=spurs_match['event']))
    
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
        st.metric("Possession", "54.5%")
        st.metric("xG", "2.5")
        st.metric("Shots", "18")
        st.metric("Passes Completed", "520")
    
    with col2:
        st.markdown("#### Key Moments")
        st.markdown("**38'** - Hogh penalty miss (over bar)")
        st.markdown("**53'** - ⚽ Goal - Hauge (left cut-in)")
        st.markdown("**66'** - ⚽ Goal - Hauge (cutback)")
        st.markdown("**68'** - Van de Ven goal (Spurs)")
        st.markdown("**70'** - Bjorkan overlap chance")
        st.markdown("**89'** - Own goal - Gundersen (deflection)")
    
    st.markdown("---")
    st.markdown("#### Europa League vs Champions League Comparison")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=competition_comparison['metric'], y=competition_comparison['Europa'],
                        name='Europa League Semi (2024)', marker_color='#a855f7'))
    fig.add_trace(go.Bar(x=competition_comparison['metric'], y=competition_comparison['UCL'],
                        name='Champions League (2025)', marker_color='#fbbf24'))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#93c5fd',
        height=350,
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("Significant improvement across attacking metrics in UCL debut vs Europa semifinal")

# Footer
st.markdown("---")
st.markdown("Data spans 2022-2025 seasons | Formation: 4-3-3 | Style: High possession, progressive football")