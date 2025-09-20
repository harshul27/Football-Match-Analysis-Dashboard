import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Manchester City Performance Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="⚽"
)

# Custom CSS
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
        margin: 0.5rem 0;
    }
    .warning-box {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff9800;
        margin: 0.5rem 0;
    }
    .danger-box {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f44336;
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px;
        padding: 8px 16px;
        border: 1px solid #e0e0e0;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_season_data():
    """Load Manchester City season data - NOTE: This is fictional data for demonstration"""
    
    # Season overview (fictional data)
    season_overview = {
        "matches_played": 4,
        "wins": 2,
        "draws": 0,
        "losses": 2,
        "points": 6,
        "position": 8,
        "goals_for": 7,
        "goals_against": 4,
        "goal_difference": 3,
        "clean_sheets": 2,
        "ppg": 1.5
    }
    
    # Match progression data
    match_progression = pd.DataFrame([
        {
            "matchday": 1, "opponent": "Wolves", "result": "W", "score": "4-0", 
            "points": 3, "cumulative_points": 3, "possession": 68, "venue": "Away", 
            "date": "Aug 16", "pass_accuracy": 91, "shots": 16, "fouls": 8, 
            "xg_for": 3.2, "xg_against": 0.8
        },
        {
            "matchday": 2, "opponent": "Tottenham", "result": "L", "score": "0-2", 
            "points": 0, "cumulative_points": 3, "possession": 52, "venue": "Home", 
            "date": "Aug 23", "pass_accuracy": 84, "shots": 9, "fouls": 12, 
            "xg_for": 1.1, "xg_against": 2.1
        },
        {
            "matchday": 3, "opponent": "Brighton", "result": "L", "score": "1-2", 
            "points": 0, "cumulative_points": 3, "possession": 62, "venue": "Away", 
            "date": "Aug 31", "pass_accuracy": 88, "shots": 12, "fouls": 11, 
            "xg_for": 1.4, "xg_against": 1.5
        },
        {
            "matchday": 4, "opponent": "Man Utd", "result": "W", "score": "3-0", 
            "points": 3, "cumulative_points": 6, "possession": 71, "venue": "Home", 
            "date": "Sep 14", "pass_accuracy": 92, "shots": 18, "fouls": 7, 
            "xg_for": 2.4, "xg_against": 1.0
        }
    ])
    
    # New signings data
    new_signings = {
        "donnarumma": {
            "name": "Gianluigi Donnarumma",
            "position": "Goalkeeper",
            "from": "Paris Saint-Germain",
            "fee": "£26 million",
            "games_played": 4,
            "clean_sheets": 2,
            "rating": 7.4,
            "impact": "Replacing Ederson - solid start with room for improvement"
        },
        "mcatee": {
            "name": "James McAtee",
            "position": "Attacking Midfielder",
            "from": "Sheffield United (recalled)",
            "fee": "Development player",
            "games_played": 3,
            "goals": 1,
            "assists": 1,
            "rating": 7.0,
            "impact": "Filling creative void - promising displays when given chances"
        }
    }
    
    # Detailed match analysis
    detailed_matches = {
        "wolves": {
            "date": "August 16, 2025",
            "venue": "Molineux Stadium (Away)",
            "result": "W 4-0",
            "key_factors": {
                "attack": "Clinical finishing - 4 goals from 16 shots, Haaland brace",
                "midfield": "Complete dominance with 91% pass accuracy",
                "defense": "Perfect debut for Donnarumma with clean sheet"
            },
            "player_ratings": {
                "haaland": 9.0, "foden": 8.5, "rodri": 8.2, 
                "donnarumma": 7.8, "doku": 8.0
            }
        },
        "tottenham": {
            "date": "August 23, 2025",
            "venue": "Etihad Stadium (Home)",
            "result": "L 0-2",
            "key_factors": {
                "attack": "Wasteful finishing - failed to convert dominance",
                "midfield": "Struggled without Gundogan's press resistance",
                "defense": "Individual errors cost dearly in key moments"
            },
            "player_ratings": {
                "haaland": 6.5, "foden": 6.0, "rodri": 6.8,
                "donnarumma": 6.0, "walker": 5.5
            }
        },
        "brighton": {
            "date": "August 31, 2025",
            "venue": "American Express Stadium (Away)",
            "result": "L 1-2",
            "key_factors": {
                "attack": "Haaland milestone goal but limited service",
                "midfield": "Nunes handball penalty crucial turning point",
                "defense": "Late winner shows ongoing vulnerability"
            },
            "player_ratings": {
                "haaland": 7.5, "silva": 6.8, "rodri": 6.5,
                "donnarumma": 6.5, "nunes": 4.5
            }
        },
        "man_utd": {
            "date": "September 14, 2025",
            "venue": "Etihad Stadium (Home)",
            "result": "W 3-0",
            "key_factors": {
                "attack": "Clinical return to form - Haaland double",
                "midfield": "Dominated possession and tempo throughout",
                "defense": "Solid clean sheet, Donnarumma commanding"
            },
            "player_ratings": {
                "haaland": 9.2, "foden": 8.3, "rodri": 8.7,
                "donnarumma": 8.0, "gvardiol": 8.1
            }
        }
    }
    
    return season_overview, match_progression, new_signings, detailed_matches

def create_points_progression_chart(match_data):
    """Create points progression chart"""
    fig = go.Figure()
    
    # Color mapping for results
    colors = {'W': 'green', 'D': 'orange', 'L': 'red'}
    
    fig.add_trace(go.Scatter(
        x=match_data['matchday'],
        y=match_data['cumulative_points'],
        mode='lines+markers',
        line=dict(color='#6CABDD', width=3),
        marker=dict(
            size=12,
            color=[colors[result] for result in match_data['result']],
            symbol='circle',
            line=dict(width=2, color='white')
        ),
        name='Points Progression',
        hovertemplate='<b>Matchday %{x}</b><br>' +
                      'vs %{customdata[0]}<br>' +
                      'Result: %{customdata[1]} (%{customdata[2]})<br>' +
                      'Points: %{y}<extra></extra>',
        customdata=np.column_stack((
            match_data['opponent'], 
            match_data['result'], 
            match_data['score']
        ))
    ))
    
    fig.update_layout(
        title="Manchester City Points Progression",
        xaxis_title="Matchday",
        yaxis_title="Cumulative Points",
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_performance_radar(match_data):
    """Create performance radar chart"""
    avg_metrics = {
        'Possession': match_data['possession'].mean(),
        'Pass Accuracy': match_data['pass_accuracy'].mean(),
        'Shots per Game': match_data['shots'].mean(),
        'xG per Game': match_data['xg_for'].mean() * 10,  # Scaled for radar
        'Defensive Stability': (100 - match_data['xg_against'].mean() * 20)
    }
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=list(avg_metrics.values()),
        theta=list(avg_metrics.keys()),
        fill='toself',
        name='Man City Performance',
        line=dict(color='#6CABDD', width=2),
        fillcolor='rgba(108, 171, 221, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title="Average Performance Metrics",
        height=400,
        showlegend=False
    )
    
    return fig

def create_xg_analysis_chart(match_data):
    """Create xG vs Goals analysis"""
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Expected vs Actual Goals', 'Goal Efficiency by Match'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Bar chart for xG vs Goals
    fig.add_trace(
        go.Bar(
            x=match_data['opponent'],
            y=match_data['xg_for'],
            name='Expected Goals',
            marker_color='lightblue',
            opacity=0.7
        ),
        row=1, col=1
    )
    
    goals_scored = [int(score.split('-')[0]) for score in match_data['score']]
    fig.add_trace(
        go.Bar(
            x=match_data['opponent'],
            y=goals_scored,
            name='Actual Goals',
            marker_color='blue'
        ),
        row=1, col=1
    )
    
    # Line chart for efficiency
    efficiency = [g/xg if xg > 0 else 0 for g, xg in zip(goals_scored, match_data['xg_for'])]
    fig.add_trace(
        go.Scatter(
            x=match_data['opponent'],
            y=efficiency,
            mode='lines+markers',
            name='Finishing Efficiency',
            line=dict(color='red', width=3),
            marker=dict(size=8)
        ),
        row=1, col=2
    )
    
    fig.add_hline(y=1, line_dash="dash", line_color="gray", row=1, col=2)
    
    fig.update_layout(height=400, title_text="Goal Analysis")
    
    return fig

def main():
    """Main application function"""
    
    # Load data
    season_overview, match_progression, new_signings, detailed_matches = load_season_data()
    
    # Header with disclaimer
    st.markdown("# ⚽ Manchester City Performance Dashboard")
    st.markdown("### Comprehensive Season Analysis Tool")
    
    # Important disclaimer
    st.markdown("""
    <div class="warning-box">
    <strong>⚠️ Data Disclaimer:</strong> This dashboard contains fictional data for demonstration purposes. 
    The "2025/26 season" data is entirely made up since we're currently in 2024. 
    This is a template for how such analysis could work with real data.
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar controls
    st.sidebar.header("📊 Dashboard Controls")
    
    # Main navigation
    tab1, tab2, tab3, tab4 = st.tabs(["Season Overview", "Match Analysis", "Player Performance", "Projections"])
    
    with tab1:
        st.subheader("📈 Season Overview")
        
        # Key metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Position", f"{season_overview['position']}th", delta=None)
        with col2:
            st.metric("Points", season_overview['points'], delta=f"PPG: {season_overview['ppg']}")
        with col3:
            st.metric("W-D-L", f"{season_overview['wins']}-{season_overview['draws']}-{season_overview['losses']}")
        with col4:
            st.metric("Goals", f"{season_overview['goals_for']}-{season_overview['goals_against']}")
        with col5:
            st.metric("Goal Diff", f"+{season_overview['goal_difference']}")
        
        # Points progression chart
        st.subheader("Points Progression")
        fig_points = create_points_progression_chart(match_progression)
        st.plotly_chart(fig_points, use_container_width=True)
        
        # Performance radar
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Performance Radar")
            fig_radar = create_performance_radar(match_progression)
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col2:
            st.subheader("xG Analysis")
            fig_xg = create_xg_analysis_chart(match_progression)
            st.plotly_chart(fig_xg, use_container_width=True)
        
        # New signings impact
        st.subheader("New Signings Impact")
        for key, player in new_signings.items():
            with st.expander(f"{player['name']} - {player['position']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Games Played", player['games_played'])
                with col2:
                    st.metric("Rating", f"{player['rating']}/10")
                with col3:
                    if 'goals' in player:
                        st.metric("Goals", player['goals'])
                    else:
                        st.metric("Clean Sheets", player['clean_sheets'])
                
                st.markdown(f"**Impact:** {player['impact']}")
    
    with tab2:
        st.subheader("🔍 Detailed Match Analysis")
        
        # Match selector
        selected_match = st.selectbox(
            "Select Match to Analyze",
            options=list(detailed_matches.keys()),
            format_func=lambda x: f"vs {x.replace('_', ' ').title()}"
        )
        
        match_data = detailed_matches[selected_match]
        
        # Match header
        col1, col2, col3 = st.columns([2, 3, 2])
        
        with col1:
            st.markdown("### Manchester City")
            result_parts = match_data['result'].split()
            city_score = result_parts[1].split('-')[0]
            st.markdown(f"# {city_score}")
        
        with col2:
            st.markdown(f"**{match_data['date']}**")
            st.markdown(f"*{match_data['venue']}*")
            result_text = "VICTORY" if match_data['result'].startswith('W') else "DEFEAT"
            color = "green" if match_data['result'].startswith('W') else "red"
            st.markdown(f"<h3 style='color: {color}; text-align: center;'>{result_text}</h3>", unsafe_allow_html=True)
        
        with col3:
            opponent = selected_match.replace('_', ' ').title()
            if opponent == "Man Utd":
                opponent = "Manchester United"
            st.markdown(f"### {opponent}")
            opp_score = result_parts[1].split('-')[1]
            st.markdown(f"# {opp_score}")
        
        # Match analysis
        st.subheader("Tactical Breakdown")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🔥 Attack**")
            st.markdown(f"*{match_data['key_factors']['attack']}*")
        
        with col2:
            st.markdown("**⚽ Midfield**")
            st.markdown(f"*{match_data['key_factors']['midfield']}*")
        
        with col3:
            st.markdown("**🛡️ Defense**")
            st.markdown(f"*{match_data['key_factors']['defense']}*")
        
        # Player ratings
        st.subheader("Player Ratings")
        ratings_data = pd.DataFrame(
            list(match_data['player_ratings'].items()),
            columns=['Player', 'Rating']
        )
        
        fig_ratings = px.bar(
            ratings_data, 
            x='Player', 
            y='Rating',
            color='Rating',
            color_continuous_scale='RdYlGn',
            range_color=[5, 10]
        )
        fig_ratings.update_layout(height=300)
        st.plotly_chart(fig_ratings, use_container_width=True)
    
    with tab3:
        st.subheader("👥 Player Performance Analysis")
        
        # Match statistics comparison
        match_stats = match_progression[['opponent', 'possession', 'pass_accuracy', 'shots', 'xg_for']].copy()
        
        st.subheader("Performance by Match")
        fig_comparison = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Possession %', 'Pass Accuracy %', 'Shots per Game', 'Expected Goals')
        )
        
        # Possession
        fig_comparison.add_trace(
            go.Bar(x=match_stats['opponent'], y=match_stats['possession'], name='Possession'),
            row=1, col=1
        )
        
        # Pass accuracy
        fig_comparison.add_trace(
            go.Bar(x=match_stats['opponent'], y=match_stats['pass_accuracy'], name='Pass Accuracy'),
            row=1, col=2
        )
        
        # Shots
        fig_comparison.add_trace(
            go.Bar(x=match_stats['opponent'], y=match_stats['shots'], name='Shots'),
            row=2, col=1
        )
        
        # xG
        fig_comparison.add_trace(
            go.Bar(x=match_stats['opponent'], y=match_stats['xg_for'], name='xG'),
            row=2, col=2
        )
        
        fig_comparison.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Average performance metrics
        st.subheader("Season Averages")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Avg Possession", f"{match_stats['possession'].mean():.1f}%")
        with col2:
            st.metric("Avg Pass Accuracy", f"{match_stats['pass_accuracy'].mean():.1f}%")
        with col3:
            st.metric("Avg Shots", f"{match_stats['shots'].mean():.1f}")
        with col4:
            st.metric("Avg xG", f"{match_stats['xg_for'].mean():.2f}")
    
    with tab4:
        st.subheader("🔮 Season Projections")
        
        st.markdown("""
        <div class="warning-box">
        <strong>Note:</strong> These projections are based on the first 4 matches and are purely illustrative.
        </div>
        """, unsafe_allow_html=True)
        
        # Current trajectory
        current_ppg = season_overview['ppg']
        projected_points = current_ppg * 38
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Current PPG", f"{current_ppg:.2f}")
        with col2:
            st.metric("Projected Points", f"{projected_points:.0f}")
        with col3:
            projected_position = "6th-8th" if projected_points > 55 else "8th-12th"
            st.metric("Est. Final Position", projected_position)
        with col4:
            europa_chance = "High" if projected_points > 55 else "Medium"
            st.metric("European Qualification", europa_chance)
        
        # Scenario analysis
        st.subheader("Scenario Analysis")
        
        scenarios = pd.DataFrame({
            'Scenario': ['Current Trend', 'Improved Form', 'Poor Form'],
            'PPG': [1.5, 2.0, 1.0],
            'Final Points': [57, 76, 38],
            'Est. Position': ['7th-9th', '4th-6th', '12th-15th'],
            'Europe': ['Conference League', 'Champions League', 'No Europe']
        })
        
        st.dataframe(scenarios, use_container_width=True)
        
        # Performance trends
        st.subheader("Key Performance Indicators")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="success-box">
            <strong>Strengths:</strong>
            <ul>
            <li>Strong attacking output when clicking</li>
            <li>New signings integrating well</li>
            <li>Home form solid</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="danger-box">
            <strong>Areas for Improvement:</strong>
            <ul>
            <li>Consistency in big matches</li>
            <li>Away form needs work</li>
            <li>Defensive stability</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("**Data Sources:** Fictional data for demonstration | **Last Updated:** " + datetime.now().strftime("%Y-%m-%d %H:%M"))

if __name__ == "__main__":
    main()
