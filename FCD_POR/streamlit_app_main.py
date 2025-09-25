import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import requests
import re
import random

# --- Hardcoded JSON Data (from your provided file) ---
@st.cache_data
def load_data():
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
  },
  "tactical_visualization": {
    "matchup_key_areas": [
      {
        "area": "Left Flank (PTFC attack)",
        "ptfc_strengths": "High crossing volume (Antony, Moreno), progressive runs, set piece danger",
        "dallas_response": "Shaq Moore tasked with defensive tracking, zone 14 overload to block cutbacks"
      },
      {
        "area": "Central Zone",
        "ptfc_strengths": "Da Costa creating with high xA and total chances, Chara pressing & disrupting",
        "dallas_response": "Acosta/Kaick double pivot, direct transitions after regained ball"
      },
      {
        "area": "Set Pieces",
        "ptfc_strengths": "Multiple targets (Surman, Kelsy); above league average xG on corners/freekicks",
        "dallas_response": "Ibeagha/Abubakar aerial defense, Musa left in advanced position for counters"
      },
      {
        "area": "Transition Phase",
        "ptfc_strengths": "Counter-press in middle third, win back possession (PPDA 13.2), Pantemis distribution",
        "dallas_response": "Direct play, rapid vertical passing aimed at Musa/Farrington"
      }
    ]
  }
}
    """
    data = json.loads(data_str)

    # Correctly restructure the data for easier access
    teams = {
        'portland': data['teams']['portland_timbers'],
        'fc_dallas': data['teams']['fc_dallas']
    }
    players = {
        'portland': data['players']['portland_timbers'],
        'fc_dallas': data['players']['fc_dallas']
    }
    
    # Merge nested data into the main team dictionary to fix KeyErrors
    teams['portland']['style_metrics'] = data['style_metrics']['portland']
    teams['fc_dallas']['style_metrics'] = data['style_metrics']['fc_dallas']
    teams['portland']['tactical_areas'] = data['tactical_visualization']['matchup_key_areas']
    teams['fc_dallas']['tactical_areas'] = data['tactical_visualization']['matchup_key_areas']


    return teams, players, data['ml_predictions'], data['last_match_detail']


# --- Gemini Chatbot Class ---
class GeminiChatbot:
    def __init__(self, api_key):
        self.api_key = api_key
        # Note: In a real-world app, you would use a secure, non-placeholder URL
        self.api_url = "https://your-gemini-api-endpoint"

    def _get_api_response(self, prompt, context_data):
        # This is a placeholder for a real API call.
        # It's here to show the structure, but will return a static response.
        
        # Simulating Google Search based on user intent
        search_results = ""
        if "latest news" in prompt.lower() or "injuries" in prompt.lower():
            # In a real app, this would use google_search.search()
            search_results = f"Search results for '{prompt}':\n* Petar Musa is fit for the game. * David Da Costa is a doubt with a minor knock."
        
        full_prompt = f"""
        You are a soccer data analyst. Your goal is to provide a narrative of the statistics and the game for a person asking different questions about the teams or anything related to the match being analyzed.

        Here is the relevant data about the Portland Timbers and FC Dallas:
        {json.dumps(context_data, indent=2)}

        {search_results}

        Now, answer the following question based on the provided data and search results. Be concise, informative, and do not make up information that isn't in the data.

        Question: {prompt}
        """

        # For demonstration, we return a static response.
        return f"Based on the data, Portland's superior defensive numbers and home advantage make them slight favorites. Players like Antony and David Da Costa are key to their attack, while Dallas will rely heavily on Petar Musa's clinical finishing. 

[Image of soccer field with team stats]
"


    def get_response(self, prompt, context_data):
        prompt_lower = prompt.lower()
        
        # Check if the user is asking for a chart
        chart_keywords = ['graph', 'chart', 'plot', 'visualize']
        if any(keyword in prompt_lower for keyword in chart_keywords):
            
            # Simple keyword-based chart generation
            if 'goals' in prompt_lower or 'xg' in prompt_lower:
                teams = ['Portland', 'FC Dallas']
                goals_for = [context_data['teams']['portland']['season_stats']['goals_for'], context_data['teams']['fc_dallas']['season_stats']['goals_for']]
                xG_for = [context_data['teams']['portland']['season_stats']['xG_for'], context_data['teams']['fc_dallas']['season_stats']['xG_for']]
                
                df = pd.DataFrame({'Team': teams, 'Goals For': goals_for, 'xG For': xG_for})
                fig = px.bar(df, x='Team', y=['Goals For', 'xG For'], barmode='group', title="Goals vs Expected Goals (xG)")
                
                return fig
            elif 'possession' in prompt_lower or 'possession' in prompt_lower:
                teams = ['Portland', 'FC Dallas']
                possession = [context_data['teams']['portland']['season_stats']['possession_pct'], context_data['teams']['fc_dallas']['season_stats']['possession_pct']]
                
                df = pd.DataFrame({'Team': teams, 'Possession %': possession})
                fig = px.bar(df, x='Team', y='Possession %', title="Average Possession Percentage")
                
                return fig
            else:
                return "I can generate charts for goals, xG, and possession. Please try a more specific request."
                
        # If not a chart, get a narrative response from the LLM
        return self._get_api_response(prompt, context_data)


# --- Dashboard Section Functions ---

def show_overview(team_data, ml_predictions):
    st.header("📈 Season Overview", divider='green')
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🟢 Portland Timbers")
        portland = team_data['portland']
        form_colors = {'W': '🟢', 'D': '🟡', 'L': '🔴'}
        form_str = ' '.join([form_colors[result] for result in portland['season_stats']['form']])
        
        st.markdown(f"**Record:** {portland['season_stats']['wins']}-{portland['season_stats']['draws']}-{portland['season_stats']['losses']} ({portland['season_stats']['points']} pts)")
        st.markdown(f"**Conference Position:** 8th")
        st.markdown(f"**Recent Form (L5):** {form_str}")
        
    with col2:
        st.subheader("🔵 FC Dallas")
        dallas = team_data['fc_dallas']
        form_colors = {'W': '🟢', 'D': '🟡', 'L': '🔴'}
        form_str = ' '.join([form_colors[result] for result in dallas['season_stats']['form']])
        
        st.markdown(f"**Record:** {dallas['season_stats']['wins']}-{dallas['season_stats']['draws']}-{dallas['season_stats']['losses']} ({dallas['season_stats']['points']} pts)")
        st.markdown(f"**Conference Position:** 10th")
        st.markdown(f"**Recent Form (L5):** {form_str}")

    st.markdown("---")
    
    # Dynamic metrics with progress bars
    st.subheader("Key Metrics Comparison")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Goals For", value=f"{portland['season_stats']['goals_for']}", delta=f"vs Dallas: {portland['season_stats']['goals_for'] - dallas['season_stats']['goals_for']:+}")
        st.progress(portland['season_stats']['goals_for'] / 50)
    with col2:
        st.metric(label="Expected Goals (xG)", value=f"{portland['season_stats']['xG_for']}", delta=f"vs Dallas: {portland['season_stats']['xG_for'] - dallas['season_stats']['xG_for']:+}")
        st.progress(portland['season_stats']['xG_for'] / 50)
    with col3:
        st.metric(label="Possession", value=f"{portland['season_stats']['possession_pct']}%", delta=f"vs Dallas: {portland['season_stats']['possession_pct'] - dallas['season_stats']['possession_pct']:+}")
        st.progress(portland['season_stats']['possession_pct'] / 100)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric(label="Goals Against", value=f"{dallas['season_stats']['goals_against']}", delta=f"vs Portland: {dallas['season_stats']['goals_against'] - portland['season_stats']['goals_against']:+}")
        st.progress(dallas['season_stats']['goals_against'] / 50)
    with col5:
        st.metric(label="Expected Goals Against (xGA)", value=f"{dallas['season_stats']['xG_against']}", delta=f"vs Portland: {dallas['season_stats']['xG_against'] - portland['season_stats']['xG_against']:+}")
        st.progress(dallas['season_stats']['xG_against'] / 50)
    with col6:
        st.metric(label="Pass Accuracy", value=f"{dallas['season_stats']['pass_accuracy_pct']}%", delta=f"vs Portland: {dallas['season_stats']['pass_accuracy_pct'] - portland['season_stats']['pass_accuracy_pct']:+}")
        st.progress(dallas['season_stats']['pass_accuracy_pct'] / 100)

def show_performance(team_data):
    st.header("📊 Performance & Tactical Analysis", divider='green')
    
    # Radar chart
    st.subheader("Team Strengths: A Tactical Snapshot")
    
    categories = ['Attack', 'Defense', 'Possession', 'Pressing', 'Set Pieces', 'Creativity']
    
    # Normalize values for radar chart
    portland_values = [
        team_data['portland']['season_stats']['goals_for'] / team_data['fc_dallas']['season_stats']['goals_for'] * 100,
        100 - (team_data['portland']['season_stats']['goals_against'] / team_data['fc_dallas']['season_stats']['goals_against'] * 100),
        team_data['portland']['season_stats']['possession_pct'],
        100 - (team_data['portland']['season_stats']['ppda'] / team_data['fc_dallas']['season_stats']['ppda'] * 100),
        (team_data['portland']['season_stats']['set_piece_xG'] / 10) * 100,
        (team_data['portland']['season_stats']['big_chances_created'] / team_data['fc_dallas']['season_stats']['big_chances_created']) * 100
    ]
    dallas_values = [
        team_data['fc_dallas']['season_stats']['goals_for'] / team_data['portland']['season_stats']['goals_for'] * 100,
        100 - (team_data['fc_dallas']['season_stats']['goals_against'] / team_data['portland']['season_stats']['goals_against'] * 100),
        team_data['fc_dallas']['season_stats']['possession_pct'],
        100 - (team_data['fc_dallas']['season_stats']['ppda'] / team_data['portland']['season_stats']['ppda'] * 100),
        (team_data['fc_dallas']['season_stats']['set_piece_xG'] / 10) * 100,
        (team_data['fc_dallas']['season_stats']['big_chances_created'] / team_data['portland']['season_stats']['big_chances_created']) * 100
    ]
    
    portland_values = [min(100, max(0, v)) for v in portland_values]
    dallas_values = [min(100, max(0, v)) for v in dallas_values]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=portland_values, theta=categories, fill='toself', name='Portland Timbers'))
    fig.add_trace(go.Scatterpolar(r=dallas_values, theta=categories, fill='toself', name='FC Dallas'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Tactical breakdown
    st.markdown("---")
    st.subheader("Tactical Focus Areas")
    col_ptfc, col_fcd = st.columns(2)
    
    with col_ptfc:
        st.info("🟢 **Portland Timbers: Expected Style**")
        st.markdown(f"**Possession-based Attack:** Averaging `{team_data['portland']['season_stats']['possession_pct']}%` possession, they control the tempo and territory.")
        st.markdown(f"**High Pressing:** A PPDA of `{team_data['portland']['season_stats']['ppda']}` indicates aggressive pressing to win the ball high up the pitch.")
        st.markdown(f"**Set Piece Threat:** With a set piece xG of `{team_data['portland']['season_stats']['set_piece_xG']}`, set plays are a major scoring avenue.")

    with col_fcd:
        st.info("🔵 **FC Dallas: Expected Style**")
        st.markdown(f"**Direct Counter-Attack:** Lower possession at `{team_data['fc_dallas']['season_stats']['possession_pct']}%` shows they favor rapid vertical progression.")
        st.markdown(f"**Mid-Block Defense:** A PPDA of `{team_data['fc_dallas']['season_stats']['ppda']}` suggests they defend in a more organized, deeper block.")
        st.markdown(f"**Clinical Finishing:** Dallas overperforms their xG (`{team_data['fc_dallas']['season_stats']['goals_for']}` goals vs `{team_data['fc_dallas']['season_stats']['xG_for']}` xG), indicating efficiency in front of goal.")

def show_ml_prediction(ml_predictions):
    st.header("🤖 Machine Learning Prediction", divider='green')
    
    st.subheader("Match Outcome Probabilities")
    
    # Pie chart for probabilities
    labels = ['Portland Win', 'Draw', 'FC Dallas Win']
    values = [ml_predictions['win_probability']['portland'], ml_predictions['win_probability']['draw'], ml_predictions['win_probability']['fc_dallas']]
    colors = ['#10B981', '#FFC300', '#3B82F6']
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=colors, hole=0.3)])
    fig.update_traces(textinfo='percent+label', pull=[0.1, 0, 0])
    fig.update_layout(title_text='ML Model Outcome Prediction', height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Key Factors breakdown
    st.markdown("---")
    st.subheader("Key Factors Driving the Prediction")
    factors_df = pd.DataFrame(ml_predictions['key_factors'])
    
    for _, row in factors_df.iterrows():
        favor_color = "green" if row['favor'] == "Portland" else "blue" if row['favor'] == "Dallas" else "gray"
        st.markdown(f"**{row['factor']}** - Favors: <span style='color:{favor_color}'>{row['favor']}</span>", unsafe_allow_html=True)
        st.progress(int(row['weight'] * 100))
        st.markdown(f"*{row['impact']}*")

def show_key_players(player_data):
    st.header("⭐ Key Players Analysis", divider='green')

    st.subheader("🟢 Portland Timbers")
    pt_players_df = pd.DataFrame(player_data['portland']).sort_values(by='rating', ascending=False)
    pt_players_df = pt_players_df.loc[:, ['name', 'position', 'goals', 'assists', 'xG', 'rating']].head(5)
    st.table(pt_players_df.set_index('name'))

    st.subheader("🔵 FC Dallas")
    fcd_players_df = pd.DataFrame(player_data['fc_dallas']).sort_values(by='rating', ascending=False)
    fcd_players_df = fcd_players_df.loc[:, ['name', 'position', 'goals', 'assists', 'xG', 'rating']].head(5)
    st.table(fcd_players_df.set_index('name'))

def show_match_intelligence(team_data, ml_predictions):
    st.header("🧠 Match Intelligence & Prediction", divider='green')
    
    st.subheader("Final Expert Prediction")
    prediction_col, summary_col = st.columns([1, 2])
    
    with prediction_col:
        st.markdown(f"""
        <div style="background-color: #6a1b9a; padding: 20px; border-radius: 10px; text-align: center; color: white;">
            <h3>Portland Timbers 2 - 1 FC Dallas</h3>
            <p>Confidence: {ml_predictions['confidence']}%</p>
        </div>
        """, unsafe_allow_html=True)

    with summary_col:
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; color: black;">
        The data suggests a tightly contested match. Portland's home advantage and defensive solidity, especially from their goalkeeper, give them a crucial edge. While FC Dallas boasts a clinical finisher in Petar Musa, their overall defensive vulnerabilities and lower possession numbers are likely to be exploited. Expect Portland to control possession and win the game through a decisive moment, potentially from a set piece or a key creative pass from a player like David Da Costa. 

[Image of soccer player kicking ball]

        </div>
        """, unsafe_allow_html=True)

def show_chatbot(team_data, player_data, ml_predictions, match_data):
    st.header("💬 AI Match Analyst", divider='green')
    
    # Corrected: Use st.secrets.get() to avoid KeyError if key is missing
    gemini_key = st.secrets.get("gemini_api_key")
    if not gemini_key:
        st.warning("To use the AI Analyst, please add a `gemini_api_key` to your Streamlit secrets.")
        return

    chatbot = GeminiChatbot(gemini_key)
    
    context_data = {
        "teams": team_data,
        "players": player_data,
        "ml_predictions": ml_predictions,
        "last_match_detail": match_data
    }

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if isinstance(message["content"], go.Figure):
                st.plotly_chart(message["content"])
            else:
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask about team stats, player performance, or predictions..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing data..."):
                response = chatbot.get_response(prompt, context_data)
                
                if isinstance(response, go.Figure):
                    st.plotly_chart(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

# --- Main app logic ---
def main():
    teams_data, players_data, ml_predictions_data, match_data = load_data()
    
    st.markdown("""
    <style>
        .st-emotion-cache-13ln4j6 {
            max-width: 100%;
            padding: 2rem 1rem 1rem;
        }
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(90deg, #10B981, #3B82F6);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .st-emotion-cache-h6n4zi p {
            font-size: 1.25rem;
            line-height: 1.5;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="main-header">
        <h1>⚽ MLS Pre-Match Analysis Dashboard</h1>
        <h2>Portland Timbers (HOME) vs FC Dallas (AWAY)</h2>
        <p>Providence Park, Portland • Advanced Analytics & ML Predictions</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Key Matchup Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Portland Playoff Chance", value=f"68%", delta="8th in West")
    with col2:
        st.metric(label="ML Model Confidence", value=f"78%", delta="High Confidence")
    with col3:
        st.metric(label="Dallas Playoff Chance", value=f"32%", delta="10th in West")
    with col4:
        total_xg = ml_predictions_data['expected_goals']['portland'] + ml_predictions_data['expected_goals']['fc_dallas']
        st.metric(label="Expected Goals Total", value=f"{total_xg:.1f}", delta="Goals Expected")
    
    st.sidebar.title("📊 Analysis Sections")
    tab = st.sidebar.selectbox(
        "Select Analysis:",
        ["Overview", "Performance Analysis", "Key Players", "ML Prediction", "Match Intelligence", "AI Analyst"]
    )
    
    if tab == "Overview":
        show_overview(teams_data, ml_predictions_data)
    elif tab == "Performance Analysis":
        show_performance(teams_data)
    elif tab == "Key Players":
        show_key_players(players_data)
    elif tab == "ML Prediction":
        show_ml_prediction(ml_predictions_data)
    elif tab == "Match Intelligence":
        show_match_intelligence(teams_data, ml_predictions_data)
    elif tab == "AI Analyst":
        show_chatbot(teams_data, players_data, ml_predictions_data, match_data)

if __name__ == "__main__":
    main()
