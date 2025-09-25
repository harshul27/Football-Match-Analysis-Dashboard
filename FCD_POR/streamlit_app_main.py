import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import json
import requests
import io
import base64

# --- Utility Functions to Load Data from JSON string ---
@st.cache_data
def load_data():
    # Load the JSON data from a string
    data_str = """
{
  "meta": {
    "generated_at": "2025-09-24T20:04:00Z",
    "sources": [
      {"site": "FotMob", "url": "https://www.fotmob.com/teams/307690/stats/portland-timbers", "accessed": "2025-09-24"},
      {"site": "FotMob", "url": "https://www.fotmob.com/teams/6399/stats/fc-dallas", "accessed": "2025-09-24"},
      {"site": "ESPN", "url": "https://www.espn.com/soccer/team/stats/_/id/9723/portland-timbers", "accessed": "2025-09-24"},
      {"site": "ESPN", "url": "https://www.espn.com/soccer/team/stats/_/id/185/fc-dallas", "accessed": "2025-09-24"},
      {"site": "American Soccer Analysis", "url": "https://www.americansocceranalysis.com/", "accessed": "2025-09-24"},
      {"site": "Soccerment", "url": "https://soccerment.com/mls-2025-data-driven-insights-from-the-first-5-rounds/", "accessed": "2025-09-24"}
    ]
  },
  "teams": {
    "portland_timbers": {
      "season_stats": {
        "matches_played": 29,
        "wins": 11,
        "draws": 8,
        "losses": 10,
        "points": 41,
        "goals_for": 42,
        "goals_against": 44,
        "goal_difference": -2,
        "xG_for": 38.1,
        "xG_against": 40.3,
        "shots_per_game": 11.7,
        "shots_on_target_per_game": 4.2,
        "possession_pct": 51.3,
        "passes_per_game": 478,
        "pass_accuracy_pct": 83.7,
        "corners_per_game": 5.1,
        "set_piece_xG": 7.2,
        "clean_sheets": 8,
        "save_percent": 77.1,
        "ppda": 13.2,
        "big_chances_created": 34,
        "big_chances_missed": 29,
        "yellow_cards": 47,
        "red_cards": 2,
        "field_tilt_pct": 56.2,
        "goals_added_gplus": 4.1
      }
    },
    "fc_dallas": {
      "season_stats": {
        "matches_played": 30,
        "wins": 9,
        "draws": 10,
        "losses": 11,
        "points": 37,
        "goals_for": 45,
        "goals_against": 49,
        "goal_difference": -4,
        "xG_for": 41.0,
        "xG_against": 47.2,
        "shots_per_game": 10.6,
        "shots_on_target_per_game": 3.9,
        "possession_pct": 46.2,
        "passes_per_game": 445,
        "pass_accuracy_pct": 81.9,
        "corners_per_game": 4.8,
        "set_piece_xG": 6.5,
        "clean_sheets": 6,
        "save_percent": 59.4,
        "ppda": 14.7,
        "big_chances_created": 32,
        "big_chances_missed": 29,
        "yellow_cards": 52,
        "red_cards": 3,
        "field_tilt_pct": 48.7,
        "goals_added_gplus": -2.1
      }
    }
  },
  "players": {
    "portland_timbers": [
      {
        "name": "Antony",
        "position": "LW",
        "appearances": 24,
        "minutes": 2152,
        "goals": 7,
        "assists": 3,
        "xG": 7.7,
        "xA": 2.9,
        "shots_per_90": 2.7,
        "key_passes_per_90": 2.3,
        "big_chances_created": 8,
        "big_chances_missed": 9,
        "dribble_success_pct": 53.1,
        "progressive_runs_per_90": 4.2,
        "tackles_per_90": 1.0,
        "interceptions_per_90": 0.8,
        "gplus": 0.21,
        "field_tilt_individual": 58.5,
        "rating": 7.32
      },
      {
        "name": "David Da Costa",
        "position": "CAM",
        "appearances": 29,
        "minutes": 2450,
        "goals": 4,
        "assists": 6,
        "xG": 2.9,
        "xA": 7.3,
        "shots_per_90": 2.1,
        "key_passes_per_90": 3.1,
        "big_chances_created": 11,
        "dribble_success_pct": 61.4,
        "progressive_runs_per_90": 3.5,
        "tackles_per_90": 1.2,
        "interceptions_per_90": 1.0,
        "gplus": 0.28,
        "field_tilt_individual": 61.7,
        "rating": 7.39
      },
      {
        "name": "James Pantemis",
        "position": "GK",
        "appearances": 22,
        "minutes": 1980,
        "clean_sheets": 4,
        "save_percent": 77.1,
        "goals_conceded_per_90": 1.2,
        "saves_per_90": 4.0,
        "goals_prevented": 3.9,
        "distribution_accuracy_pct": 82.4,
        "rating": 7.11
      },
      {
        "name": "Kevin Kelsy",
        "position": "ST",
        "apps": 29,
        "goals": 7,
        "assists": 2,
        "xG": 5.6,
        "xA": 1.3,
        "shots": 32,
        "shots_on": 12,
        "minutes": 2035,
        "yellow": 3,
        "red": 0
      },
      {
        "name": "Felipe Mora",
        "position": "ST",
        "apps": 29,
        "goals": 5,
        "assists": 3,
        "xG": 6.8,
        "xA": 2.3,
        "shots": 30,
        "shots_on": 13,
        "minutes": 1920,
        "yellow": 4,
        "red": 0
      },
      {
        "name": "Santiago Moreno",
        "position": "RW",
        "apps": 22,
        "goals": 4,
        "assists": 5,
        "xG": 3.4,
        "xA": 4.6,
        "shots": 35,
        "shots_on": 16,
        "minutes": 1901,
        "yellow": 4,
        "red": 0
      }
    ],
    "fc_dallas": [
      {
        "name": "Petar Musa",
        "position": "ST",
        "appearances": 27,
        "minutes": 2160,
        "goals": 16,
        "assists": 6,
        "xG": 13.1,
        "xA": 3.4,
        "shots_per_90": 2.8,
        "key_passes_per_90": 1.1,
        "big_chances_created": 11,
        "big_chances_missed": 11,
        "dribble_success_pct": 48.7,
        "progressive_runs_per_90": 2.1,
        "tackles_per_90": 0.7,
        "interceptions_per_90": 0.6,
        "gplus": 0.16,
        "field_tilt_individual": 50.2,
        "rating": 7.41
      },
      {
        "name": "Logan Farrington",
        "position": "ST",
        "apps": 29,
        "goals": 5,
        "assists": 3,
        "xG": 3.8,
        "xA": 1.1,
        "shots": 27,
        "shots_on": 11,
        "minutes": 1970,
        "yellow": 4,
        "red": 0
      },
      {
        "name": "Shaq Moore",
        "position": "RB",
        "apps": 29,
        "goals": 3,
        "assists": 3,
        "chances_created": 34,
        "prog_passes": 38,
        "yellow": 3,
        "red": 0
      },
      {
        "name": "Patrickson Delgado",
        "position": "CM",
        "apps": 26,
        "goals": 0,
        "assists": 5,
        "prog_passes": 24,
        "chances_created": 25,
        "prog_runs": 8,
        "yellow": 2,
        "red": 0
      },
      {
        "name": "Sebastien Ibeagha",
        "position": "CB",
        "apps": 29,
        "goals": 1,
        "assists": 0,
        "tackles": 29,
        "interceptions": 21,
        "clearances": 139,
        "minutes": 2610,
        "yellow": 4,
        "red": 1
      },
      {
        "name": "Maarten Paes",
        "position": "GK",
        "apps": 22,
        "clean_sheets": 3,
        "saves": 63,
        "goals_against": 43,
        "save_pct": 59.4,
        "minutes": 1980,
        "yellow": 0,
        "red": 0
      }
    ]
  },
  "ml_predictions": {
    "win_probability": {"portland": 48, "draw": 29, "fc_dallas": 23},
    "expected_goals": {"portland": 1.6, "fc_dallas": 1.1},
    "key_factors": [
        {"factor": "Home Advantage", "weight": 0.18, "favor": "Portland", "impact": "+15%"},
        {"factor": "Recent Form", "weight": 0.22, "favor": "Portland", "impact": "+8%"},
        {"factor": "xG Performance", "weight": 0.19, "favor": "Even", "impact": "Neutral"},
        {"factor": "Big Chances Created", "weight": 0.15, "favor": "Portland", "impact": "+5%"},
        {"factor": "Defensive Solidity", "weight": 0.14, "favor": "Portland", "impact": "+6%"},
        {"factor": "Set Piece Threat", "weight": 0.12, "favor": "Portland", "impact": "+4%"}
    ],
    "confidence": 78
  },
  "trends": {
    "portland": {
      "results_last_5": ["W","L","D","W","D"],
      "goals_scored_last_5": [2,0,1,2,1],
      "xg_last_5": [1.22, 0.87, 1.02, 1.34, 1.09]
    },
    "fc_dallas": {
      "results_last_5": ["L","L","D","W","L"],
      "goals_scored_last_5": [1,0,2,3,1],
      "xg_last_5": [1.13, 0.89, 1.19, 1.45, 0.97]
    }
  },
  "style_metrics": {
    "portland": {
      "ppda": 13.2,
      "field_tilt_avg": 56.2,
      "press_regains_per_game": 4.2,
      "zone_14_entries_per_game": 10.8,
      "avg_possession": 51.3,
      "final_third_pass_pct": 29.5,
      "long_pass_ratio": 12.7,
      "crosses_per_game": 18.2,
      "chance_creation_zones": {
        "left": 0.34,
        "center": 0.32,
        "right": 0.34
      },
      "build_up_attacks_per_game": 4.8,
      "direct_attacks_per_game": 2.1
    },
    "fc_dallas": {
      "ppda": 14.7,
      "field_tilt_avg": 48.7,
      "press_regains_per_game": 3.8,
      "zone_14_entries_per_game": 9.3,
      "avg_possession": 46.2,
      "final_third_pass_pct": 25.1,
      "long_pass_ratio": 14.3,
      "crosses_per_game": 14.6,
      "chance_creation_zones": {
        "left": 0.29,
        "center": 0.40,
        "right": 0.31
      },
      "build_up_attacks_per_game": 3.4,
      "direct_attacks_per_game": 2.9
    }
  },
  "last_match_detail": {
    "date": "2025-08-09",
    "venue": "Toyota Stadium, Dallas",
    "score": "FC Dallas 2-0 Portland Timbers",
    "summary": "Dallas capitalized on two high-xG chances — Musa from open play, Abubakar from corner. Portland controlled possession (60%) and created more passes, but failed to convert final third entries or big chances.",
    "key_stats": {
      "ptfc": {
        "possession": 60.1, "passes": 574, "pass_accuracy": 84.2, "shots": 13, "shots_on": 6, "xG": 1.08, "corners": 6, "big_chances": 4, "final_third_entries": 34
      },
      "fcd": {
        "possession": 39.9, "passes": 319, "pass_accuracy": 78.8, "shots": 9, "shots_on": 5, "xG": 1.41, "corners": 5, "big_chances": 3, "final_third_entries": 23
      }
    },
    "goal_events": [
      {"minute":8, "team":"FC Dallas", "player":"Petar Musa", "type":"goal", "xG":0.44},
      {"minute":62, "team":"FC Dallas", "player":"Lalas Abubakar", "type":"goal", "xG":0.22}
    ]
  }
}
    """
    data = json.loads(data_str)

    # Re-structure data to fit original code's dictionary format for a single entry point
    team_data = {
        'portland': {
            'name': 'Portland Timbers',
            'record': {
                'wins': data['teams']['portland_timbers']['season_stats']['wins'],
                'draws': data['teams']['portland_timbers']['season_stats']['draws'],
                'losses': data['teams']['portland_timbers']['season_stats']['losses'],
                'points': data['teams']['portland_timbers']['season_stats']['points'],
                'matches': data['teams']['portland_timbers']['season_stats']['matches_played']
            },
            'position': 8, # Placeholder as position isn't in provided JSON
            'conference': 'Western', # Placeholder
            'form': data['trends']['portland']['results_last_5'],
            'goals_for': data['teams']['portland_timbers']['season_stats']['goals_for'],
            'goals_against': data['teams']['portland_timbers']['season_stats']['goals_against'],
            'goal_diff': data['teams']['portland_timbers']['season_stats']['goal_difference'],
            'xG': data['teams']['portland_timbers']['season_stats']['xG_for'],
            'xGA': data['teams']['portland_timbers']['season_stats']['xG_against'],
            'playoff_chance': 68, # Placeholder
            'possession': data['teams']['portland_timbers']['season_stats']['possession_pct'],
            'pass_accuracy': data['teams']['portland_timbers']['season_stats']['pass_accuracy_pct'],
            'shots_per_game': data['teams']['portland_timbers']['season_stats']['shots_per_game'],
            'big_chances_created': data['teams']['portland_timbers']['season_stats']['big_chances_created'],
            'big_chances_missed': data['teams']['portland_timbers']['season_stats']['big_chances_missed'],
            'clean_sheets': data['teams']['portland_timbers']['season_stats']['clean_sheets'],
            'save_percent': data['teams']['portland_timbers']['season_stats']['save_percent'],
            'ppda': data['teams']['portland_timbers']['season_stats']['ppda'],
            'field_tilt': data['teams']['portland_timbers']['season_stats']['field_tilt_pct'],
            'g_plus': data['teams']['portland_timbers']['season_stats']['goals_added_gplus'],
            'set_piece_xG': data['teams']['portland_timbers']['season_stats']['set_piece_xG']
        },
        'fc_dallas': {
            'name': 'FC Dallas',
            'record': {
                'wins': data['teams']['fc_dallas']['season_stats']['wins'],
                'draws': data['teams']['fc_dallas']['season_stats']['draws'],
                'losses': data['teams']['fc_dallas']['season_stats']['losses'],
                'points': data['teams']['fc_dallas']['season_stats']['points'],
                'matches': data['teams']['fc_dallas']['season_stats']['matches_played']
            },
            'position': 10, # Placeholder
            'conference': 'Western', # Placeholder
            'form': data['trends']['fc_dallas']['results_last_5'],
            'goals_for': data['teams']['fc_dallas']['season_stats']['goals_for'],
            'goals_against': data['teams']['fc_dallas']['season_stats']['goals_against'],
            'goal_diff': data['teams']['fc_dallas']['season_stats']['goal_difference'],
            'xG': data['teams']['fc_dallas']['season_stats']['xG_for'],
            'xGA': data['teams']['fc_dallas']['season_stats']['xG_against'],
            'playoff_chance': 32, # Placeholder
            'possession': data['teams']['fc_dallas']['season_stats']['possession_pct'],
            'pass_accuracy': data['teams']['fc_dallas']['season_stats']['pass_accuracy_pct'],
            'shots_per_game': data['teams']['fc_dallas']['season_stats']['shots_per_game'],
            'big_chances_created': data['teams']['fc_dallas']['season_stats']['big_chances_created'],
            'big_chances_missed': data['teams']['fc_dallas']['season_stats']['big_chances_missed'],
            'clean_sheets': data['teams']['fc_dallas']['season_stats']['clean_sheets'],
            'save_percent': data['teams']['fc_dallas']['season_stats']['save_percent'],
            'ppda': data['teams']['fc_dallas']['season_stats']['ppda'],
            'field_tilt': data['teams']['fc_dallas']['season_stats']['field_tilt_pct'],
            'g_plus': data['teams']['fc_dallas']['season_stats']['goals_added_gplus'],
            'set_piece_xG': data['teams']['fc_dallas']['season_stats']['set_piece_xG']
        }
    }
    
    player_data = data['players']
    ml_predictions = data['ml_predictions']
    match_data = data['last_match_detail']
    
    return team_data, player_data, ml_predictions, match_data

# --- Gemini Chatbot Class ---
# This is a placeholder. You need to replace this with your actual Gemini API
# key and the correct endpoint for your project.
class GeminiChatbot:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://your-gemini-api-endpoint"  # Replace with actual endpoint
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def get_response(self, prompt, context_data):
        # Embed the soccer data into the prompt for context
        full_prompt = f"""
        You are a soccer data analyst. Your goal is to provide a narrative of the statistics and the game for a person asking different questions about the teams or anything related to the match being analyzed.

        Here is the relevant data about the Portland Timbers and FC Dallas:
        {json.dumps(context_data, indent=2)}

        Now, answer the following question based on this data. Be concise, informative, and do not make up information that isn't in the data provided.

        Question: {prompt}
        """

        payload = {
            "model_name": "gemini-pro",
            "prompt": full_prompt,
            "temperature": 0.7
        }
        
        try:
            # This is a placeholder for a real API call.
            # You would need to set up a real endpoint.
            # response = requests.post(self.endpoint, headers=self.headers, json=payload)
            # response.raise_for_status()
            # return response.json()['text']
            
            # For demonstration, we'll return a static response.
            return "As an AI, I can tell you that Portland's attacking strengths come from their wings and set pieces, while Dallas focuses on direct attacks through the center. Portland's goalkeeper has a much higher save percentage, which could be a key factor in the match."

        except requests.exceptions.RequestException as e:
            return f"An error occurred while calling the API: {e}"

# --- Page configuration and CSS ---
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
    /* Add a class for better chat styling */
    .st-chat-message-container {
        border-radius: 15px;
        padding: 10px 15px;
        margin-bottom: 10px;
    }
    .st-chat-message-container.user {
        background-color: #e0f7fa;
        text-align: right;
    }
    .st-chat-message-container.assistant {
        background-color: #f1f1f1;
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

# --- Function Definitions for Dashboard Sections ---

def show_overview(team_data, ml_predictions):
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
        **Record:** {portland['record']['wins']}-{portland['record']['draws']}-{portland['record']['losses']} ({portland['record']['points']} points)
        
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
        **Record:** {dallas['record']['wins']}-{dallas['record']['draws']}-{dallas['record']['losses']} ({dallas['record']['points']} points)
        
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

def show_performance(team_data):
    st.header("📊 Performance Analysis")
    
    # Radar chart for team comparison
    st.subheader("Team Performance Radar")
    
    categories = ['Attack', 'Defense', 'Possession', 'Pressing', 'Set Pieces', 'Creativity']
    portland_values = [
        (team_data['portland']['xG'] / team_data['portland']['goals_for']) * 100, # Simplified metric
        (team_data['portland']['xGA'] / team_data['portland']['goals_against']) * 100, # Simplified metric
        team_data['portland']['possession'],
        100 - (team_data['portland']['ppda'] * 5), # Inverted for better visualization
        (team_data['portland']['set_piece_xG'] / team_data['portland']['xG']) * 100,
        (team_data['portland']['big_chances_created'] / team_data['portland']['shots_per_game']) * 10 # Simplified metric
    ]
    dallas_values = [
        (team_data['fc_dallas']['xG'] / team_data['fc_dallas']['goals_for']) * 100,
        (team_data['fc_dallas']['xGA'] / team_data['fc_dallas']['goals_against']) * 100,
        team_data['fc_dallas']['possession'],
        100 - (team_data['fc_dallas']['ppda'] * 5),
        (team_data['fc_dallas']['set_piece_xG'] / team_data['fc_dallas']['xG']) * 100,
        (team_data['fc_dallas']['big_chances_created'] / team_data['fc_dallas']['shots_per_game']) * 10
    ]
    
    # Normalize values for radar chart if they are outside a reasonable range
    portland_values = [min(100, max(0, v)) for v in portland_values]
    dallas_values = [min(100, max(0, v)) for v in dallas_values]

    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=portland_values + [portland_values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Portland Timbers',
        marker_color='#10B981',
        fillcolor='rgba(16, 185, 129, 0.4)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=dallas_values + [dallas_values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='FC Dallas',
        marker_color='#3B82F6',
        fillcolor='rgba(59, 130, 246, 0.4)'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Goals vs xG Plot
    st.subheader("Goals vs Expected Goals (xG) Plot")
    
    teams_df = pd.DataFrame({
        'Team': ['Portland Timbers', 'FC Dallas'],
        'Goals For': [team_data['portland']['goals_for'], team_data['fc_dallas']['goals_for']],
        'xG For': [team_data['portland']['xG'], team_data['fc_dallas']['xG']]
    })
    
    fig_xg = px.bar(
        teams_df,
        x='Team',
        y=['Goals For', 'xG For'],
        barmode='group',
        color_discrete_map={'Goals For': '#10B981', 'xG For': '#A7F3D0'},
        title='Goals Scored vs Expected Goals (xG) For'
    )
    
    st.plotly_chart(fig_xg, use_container_width=True)

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
        
    st.subheader("Zone of Attack Breakdown")
    
    fig = go.Figure()
    
    portland_zones = team_data['portland']['chance_creation_zones']
    dallas_zones = team_data['fc_dallas']['chance_creation_zones']
    
    df_zones = pd.DataFrame({
        'Team': ['Portland', 'Portland', 'Portland', 'Dallas', 'Dallas', 'Dallas'],
        'Zone': ['Left', 'Center', 'Right', 'Left', 'Center', 'Right'],
        'Percentage': [
            portland_zones['left'] * 100,
            portland_zones['center'] * 100,
            portland_zones['right'] * 100,
            dallas_zones['left'] * 100,
            dallas_zones['center'] * 100,
            dallas_zones['right'] * 100
        ]
    })
    
    fig_zones = px.bar(
        df_zones,
        x='Team',
        y='Percentage',
        color='Zone',
        barmode='group',
        title="Chance Creation by Zone"
    )
    st.plotly_chart(fig_zones, use_container_width=True)

def show_ml_prediction(ml_predictions):
    st.header("🤖 Machine Learning Match Prediction")
    
    # Win probability pie chart
    labels = ['Portland Win', 'Draw', 'Dallas Win']
    values = [
        ml_predictions['win_probability']['portland'],
        ml_predictions['win_probability']['draw'],
        ml_predictions['win_probability']['fc_dallas']
    ]
    colors = ['#10B981', '#6B7280', '#3B82F6']
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=colors)])
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Key Factors breakdown
    st.subheader("Key Factors Driving the Prediction")
    factors_df = pd.DataFrame(ml_predictions['key_factors'])
    
    fig_factors = px.bar(
        factors_df,
        x='factor',
        y='weight',
        color='favor',
        title="ML Model Prediction Factors",
        labels={'factor': 'Factor', 'weight': 'Weighting (%)'},
        color_discrete_map={
            'Portland': '#10B981',
            'Even': '#6B7280',
            'Dallas': '#3B82F6'
        }
    )
    fig_factors.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_factors, use_container_width=True)
    
def show_key_players(player_data):
    st.header("⭐ Key Players Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🟢 Portland Timbers")
        for player in player_data['portland']:
            if player.get('rating'): # Only show players with a rating
                with st.expander(f"**{player['name']}** ({player['position']})"):
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Goals", player.get('goals', 0))
                    with col_b:
                        st.metric("Assists", player.get('assists', 0))
                    with col_c:
                        st.metric("Rating", player['rating'])
    
    with col2:
        st.subheader("🔵 FC Dallas")
        for player in player_data['fc_dallas']:
            if player.get('rating'):
                with st.expander(f"**{player['name']}** ({player['position']})"):
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

def show_chatbot(team_data, player_data, ml_predictions, match_data):
    st.header("💬 Gemini Chatbot: Ask a Question")

    # Combine all data into a single context for the chatbot
    context_data = {
        "team_data": team_data,
        "player_data": player_data,
        "ml_predictions": ml_predictions,
        "last_match_detail": match_data
    }
    
    # Initialize the chatbot class
    # Replace "YOUR_GEMINI_API_KEY" with your actual key
    gemini_key = st.secrets["gemini_api_key"]
    chatbot = GeminiChatbot(gemini_key)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask about team stats, player performance, or predictions..."):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing data..."):
                response = chatbot.get_response(prompt, context_data)
                st.markdown(response)
                
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- Main app logic ---
def main():
    # Load all data
    team_data, player_data, ml_predictions, match_data = load_data()
    
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
        ["Overview", "Performance Analysis", "Tactical Intelligence", "ML Prediction", "Key Players", "Match Intelligence", "Chatbot"]
    )
    
    if tab == "Overview":
        show_overview(team_data, ml_predictions)
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
    elif tab == "Chatbot":
        show_chatbot(team_data, player_data, ml_predictions, match_data)

# Run the app
if __name__ == "__main__":
    main()
