import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="MLS Pre-Match Analysis Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #10B981, #3B82F6);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .team-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #10B981;
        margin: 0.5rem 0;
    }
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Team data
@st.cache_data
def load_team_data():
    return {
        'portland': {
            'name': 'Portland Timbers',
            'record': {'wins': 11, 'draws': 8, 'losses': 10, 'points': 41, 'matches': 29},
            'position': 8,
            'conference': 'Western',
            'form': ['W', 'L', 'D', 'W', 'D'],
            'goals_for': 42,
            'goals_against': 44,
            'goal_diff': -2,
            'xG': 38.1,
            'xGA': 40.3,
            'playoff_chance': 68,
            'possession': 51.3,
            'pass_accuracy': 83.7,
            'shots_per_game': 11.7,
            'big_chances_created': 34,
            'big_chances_missed': 29,
            'clean_sheets': 8,
            'save_percent': 77.1,
            'ppda': 13.2,
            'field_tilt': 56.2,
            'g_plus': 4.1,
            'set_piece_xG': 7.2
        },
        'fc_dallas': {
            'name': 'FC Dallas',
            'record': {'wins': 9, 'draws': 10, 'losses': 11, 'points': 37, 'matches': 30},
            'position': 10,
            'conference': 'Western',
            'form': ['L', 'L', 'D', 'W', 'L'],
            'goals_for': 45,
            'goals_against': 49,
            'goal_diff': -4,
            'xG': 41.0,
            'xGA': 47.2,
            'playoff_chance': 32,
            'possession': 46.2,
            'pass_accuracy': 81.9,
            'shots_per_game': 10.6,
            'big_chances_created': 32,
            'big_chances_missed': 29,
            'clean_sheets': 6,
            'save_percent': 59.4,
            'ppda': 14.7,
            'field_tilt': 48.7,
            'g_plus': -2.1,
            'set_piece_xG': 6.5
        }
    }

@st.cache_data
def load_player_data():
    return {
        'portland': [
            {'name': 'Antony', 'position': 'LW', 'goals': 7, 'assists': 3, 'xG': 7.7, 'rating': 7.32, 'apps': 24, 'big_chances': 8, 'prog_runs': 34},
            {'name': 'Kevin Kelsy', 'position': 'ST', 'goals': 7, 'assists': 2, 'xG': 5.6, 'rating': 7.15, 'apps': 29, 'big_chances': 5, 'shots': 32},
            {'name': 'David Da Costa', 'position': 'CAM', 'goals': 4, 'assists': 6, 'xG': 2.9, 'rating': 7.39, 'apps': 29, 'big_chances': 11, 'key_passes': 57},
            {'name': 'Felipe Mora', 'position': 'ST', 'goals': 5, 'assists': 3, 'xG': 6.8, 'rating': 7.01, 'apps': 29, 'big_missed': 9},
            {'name': 'Santiago Moreno', 'position': 'RW', 'goals': 4, 'assists': 5, 'xG': 3.4, 'rating': 7.2, 'apps': 22, 'big_chances': 8},
            {'name': 'James Pantemis', 'position': 'GK', 'saves': 64, 'clean_sheets': 4, 'save_percent': 77.1, 'rating': 7.11, 'apps': 16}
        ],
        'fc_dallas': [
            {'name': 'Petar Musa', 'position': 'ST', 'goals': 16, 'assists': 6, 'xG': 13.1, 'rating': 7.41, 'apps': 27, 'big_chances': 11, 'shots': 60},
            {'name': 'Logan Farrington', 'position': 'ST', 'goals': 5, 'assists': 3, 'xG': 3.8, 'rating': 6.89, 'apps': 29, 'big_missed': 4},
            {'name': 'Shaq Moore', 'position': 'RB', 'goals': 3, 'assists': 3, 'rating': 6.95, 'apps': 29, 'key_passes': 34, 'crosses': 92},
            {'name': 'Patrickson Delgado', 'position': 'CM', 'goals': 0, 'assists': 5, 'rating': 6.8, 'apps': 26, 'key_passes': 25},
            {'name': 'Sebastien Ibeagha', 'position': 'CB', 'goals': 1, 'assists': 0, 'rating': 6.7, 'apps': 29, 'tackles': 29, 'clearances': 139},
            {'name': 'Maarten Paes', 'position': 'GK', 'saves': 63, 'clean_sheets': 3, 'save_percent': 59.4, 'rating': 6.89, 'apps': 22}
        ]
    }

@st.cache_data
def get_ml_predictions():
    return {
        'win_probability': {'portland': 48, 'draw': 29, 'fc_dallas': 23},
        'expected_goals': {'portland': 1.6, 'fc_dallas': 1.1},
        'key_factors': [
            {'factor': 'Home Advantage', 'weight': 0.18, 'favor': 'Portland', 'impact': '+15%'},
            {'factor': 'Recent Form', 'weight': 0.22, 'favor': 'Portland', 'impact': '+8%'},
            {'factor': 'xG Performance', 'weight': 0.19, 'favor': 'Even', 'impact': 'Neutral'},
            {'factor': 'Big Chances Created', 'weight': 0.15, 'favor': 'Portland', 'impact': '+5%'},
            {'factor': 'Defensive Solidity', 'weight': 0.14, 'favor': 'Portland', 'impact': '+6%'},
            {'factor': 'Set Piece Threat', 'weight': 0.12, 'favor': 'Portland', 'impact': '+4%'}
        ],
        'confidence': 78
    }

def main():
    # Load data
    team_data = load_team_data()
    player_data = load_player_data()
    ml_predictions = get_ml_predictions()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>⚽ MLS Pre-Match Analysis Dashboard</h1>
        <h2>Portland Timbers (HOME) vs FC Dallas (AWAY)</h2>
        <p>Providence Park, Portland • Advanced Analytics & ML Predictions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Portland Playoff Chance",
            value=f"{team_data['portland']['playoff_chance']}%",
            delta=f"{team_data['portland']['record']['points']} points"
        )
    
    with col2:
        st.metric(
            label="ML Model Confidence", 
            value=f"{ml_predictions['confidence']}%",
            delta="High Confidence"
        )
    
    with col3:
        st.metric(
            label="Dallas Playoff Chance",
            value=f"{team_data['fc_dallas']['playoff_chance']}%", 
            delta=f"{team_data['fc_dallas']['record']['points']} points"
        )
        
    with col4:
        st.metric(
            label="Expected Goals Total",
            value=f"{ml_predictions['expected_goals']['portland'] + ml_predictions['expected_goals']['fc_dallas']:.1f}",
            delta="Goals Expected"
        )
    
    # Sidebar for navigation
    st.sidebar.title("📊 Analysis Sections")
    tab = st.sidebar.selectbox(
        "Select Analysis:",
        ["Overview", "Performance Analysis", "Tactical Intelligence", "ML Prediction", "Key Players", "Match Intelligence"]
    )
    
    if tab == "Overview":
        show_overview(team_data)
    elif tab == "Performance Analysis":
        show_performance(team_data)
    elif tab == "Tactical Intelligence":
        show_tactical(team_data)
    elif tab == "ML Prediction":
        show_ml_prediction(ml_predictions)
    elif tab == "Key Players":
        show_key_players(player_data)
    elif tab == "Match Intelligence":
        show_match_intelligence(team_data, ml_predictions)

# Include all the function definitions from the previous file
# (show_overview, show_performance, show_tactical, show_ml_prediction, show_key_players, show_match_intelligence)

def show_overview(team_data):
    st.header("📈 Season Overview")
    
    # Team comparison cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🟢 Portland Timbers")
        portland = team_data['portland']
        
        # Form display
        form_colors = {'W': '🟢', 'D': '🟡', 'L': '🔴'}
        form_str = ' '.join([form_colors[result] for result in portland['form']])
        
        st.markdown(f"""
        **Record:** {portland['record']['wins']}-{portland['record']['draws']}-{portland['record']['losses']} 
        ({portland['record']['points']} points)
        
        **Position:** {portland['position']}th in Western Conference
        
        **Recent Form (L5):** {form_str}
        
        **Goals:** {portland['goals_for']} For, {portland['goals_against']} Against ({portland['goal_diff']:+d})
        
        **Expected Goals:** {portland['xG']} xG, {portland['xGA']} xGA
        """)
    
    with col2:
        st.markdown("### 🔵 FC Dallas")
        dallas = team_data['fc_dallas']
        
        form_colors = {'W': '🟢', 'D': '🟡', 'L': '🔴'}
        form_str = ' '.join([form_colors[result] for result in dallas['form']])
        
        st.markdown(f"""
        **Record:** {dallas['record']['wins']}-{dallas['record']['draws']}-{dallas['record']['losses']} 
        ({dallas['record']['points']} points)
        
        **Position:** {dallas['position']}th in Western Conference
        
        **Recent Form (L5):** {form_str}
        
        **Goals:** {dallas['goals_for']} For, {dallas['goals_against']} Against ({dallas['goal_diff']:+d})
        
        **Expected Goals:** {dallas['xG']} xG, {dallas['xGA']} xGA
        """)
    
    # Goals vs xG comparison
    st.subheader("Goals vs Expected Goals Analysis")
    
    fig = go.Figure()
    
    teams = ['Portland Timbers', 'FC Dallas']
    goals_for = [team_data['portland']['goals_for'], team_data['fc_dallas']['goals_for']]
    xg_for = [team_data['portland']['xG'], team_data['fc_dallas']['xG']]
    goals_against = [team_data['portland']['goals_against'], team_data['fc_dallas']['goals_against']]
    xga = [team_data['portland']['xGA'], team_data['fc_dallas']['xGA']]
    
    fig.add_trace(go.Bar(name='Goals For', x=teams, y=goals_for, marker_color='#10B981'))
    fig.add_trace(go.Bar(name='xG For', x=teams, y=xg_for, marker_color='#6EE7B7'))
    fig.add_trace(go.Bar(name='Goals Against', x=teams, y=goals_against, marker_color='#EF4444'))
    fig.add_trace(go.Bar(name='xGA', x=teams, y=xga, marker_color='#FCA5A5'))
    
    fig.update_layout(
        title="Goals vs Expected Goals Comparison",
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Model confidence display
    st.markdown(f"""
    <div class="prediction-box">
        <h3>Model Confidence: {ml_predictions['confidence']}%</h3>
        <p>Portland xG: {ml_predictions['expected_goals']['portland']} | Dallas xG: {ml_predictions['expected_goals']['fc_dallas']}</p>
    </div>
    """, unsafe_allow_html=True)

def show_key_players(player_data):
    st.header("⭐ Key Players Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🟢 Portland Timbers")
        for player in player_data['portland'][:4]:
            with st.expander(f"{player['name']} ({player['position']})"):
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Goals", player.get('goals', 0))
                with col_b:
                    st.metric("Assists", player.get('assists', 0))
                with col_c:
                    st.metric("Rating", player['rating'])
    
    with col2:
        st.subheader("🔵 FC Dallas")
        for player in player_data['fc_dallas'][:4]:
            with st.expander(f"{player['name']} ({player['position']})"):
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Goals", player.get('goals', 0))
                with col_b:
                    st.metric("Assists", player.get('assists', 0))
                with col_c:
                    st.metric("Rating", player['rating'])

def show_match_intelligence(team_data, ml_predictions):
    st.header("🧠 Match Intelligence Summary")
    
    # Main prediction
    st.markdown("""
    <div class="prediction-box">
        <h2>🏆 Expert Final Prediction</h2>
        <h1>Portland Timbers 2-1 FC Dallas</h1>
        <h3>Confidence: 78% • Expected Total Goals: 2.7</h3>
        <p>Home advantage, set piece superiority, and goalkeeper differential overcome Dallas's clinical finishing</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Strategic Analysis**
        
        Portland's home advantage at Providence Park, combined with superior goalkeeper 
        performance (77.1% vs 59.4% saves) and territorial control (56.2% field tilt), 
        creates significant edge despite Dallas having clinical finisher in Musa.
        """)
    
    with col2:
        st.success("""
        **Match Prediction Rationale**
        
        Portland 48% vs Dallas 23% - Home advantage, set piece superiority, 
        and goalkeeper differential overcome Dallas's clinical finishing. 
        Expect territorial dominance with set pieces proving decisive.
        """)
    
    # Match scenarios
    scenarios = {
        'Scenario': ['Portland Dominance', 'Tactical Stalemate', 'Dallas Counter-Attack', 'High-Scoring'],
        'Probability': [35, 30, 25, 10],
    }
    
    df_scenarios = pd.DataFrame(scenarios)
    
    fig = px.bar(df_scenarios, x='Scenario', y='Probability',
                title="Match Scenario Probabilities",
                color='Probability', color_continuous_scale='Viridis')
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()

def show_performance(team_data):
    st.header("📊 Performance Analysis")
    
    # Radar chart for team comparison
    st.subheader("Team Performance Radar")
    
    categories = ['Attack', 'Defense', 'Possession', 'Pressing', 'Set Pieces', 'Creativity']
    portland_values = [73, 64, 71, 78, 82, 76]
    dallas_values = [69, 58, 52, 65, 75, 68]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=portland_values + [portland_values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Portland Timbers',
        marker_color='#10B981'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=dallas_values + [dallas_values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='FC Dallas',
        marker_color='#3B82F6'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_tactical(team_data):
    st.header("🎯 Tactical Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"""
        **Portland's Tactical Style**
        
        **Possession:** {team_data['portland']['possession']}% (Control-based)
        **Field Tilt:** {team_data['portland']['field_tilt']}% (Territorial dominance)
        **Pressing:** PPDA {team_data['portland']['ppda']} (High intensity)
        **Set Pieces:** {team_data['portland']['set_piece_xG']} xG (Major threat)
        """)
    
    with col2:
        st.info(f"""
        **Dallas's Tactical Approach**
        
        **Possession:** {team_data['fc_dallas']['possession']}% (Direct style)
        **Field Tilt:** {team_data['fc_dallas']['field_tilt']}% (Defensive shape)
        **Pressing:** PPDA {team_data['fc_dallas']['ppda']} (Mid-block)
        **Clinical:** {((team_data['fc_dallas']['goals_for'] / team_data['fc_dallas']['xG']) * 100):.0f}% conversion rate
        """)

def show_ml_prediction(ml_predictions):
    st.header("🤖 Machine Learning Match Prediction")
    
    # Win probability pie chart
    labels = ['Portland Win', 'Draw', 'Dallas Win']
    values = [ml_predictions['win_probability']['portland'], 
             ml_predictions['win_probability']['draw'],
             ml_predictions['win_probability']['fc_dallas']]
    colors = ['#10B981', '#6B7280', '#3B82F6']
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=colors)])
    fig.update_layout(height=400)
