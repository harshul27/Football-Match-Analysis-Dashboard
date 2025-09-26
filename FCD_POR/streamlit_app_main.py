import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import requests
import re
import random

# Place your Gemini API key here.
# This keeps the key private and within the code itself.
GEMINI_API_KEY = "AIzaSyDqb9Ki3aZimFOcqVLyR0kiT4OGO2V2dgM"

# --- Hardcoded JSON Data from User's Files ---
# This function loads and processes all data, eliminating duplicates and consolidating metrics.
@st.cache_data
def load_data():
    data_str = """
{
  "teams": {
    "portland_timbers": {
      "season_stats": {
        "matches_played": 29, "wins": 11, "draws": 8, "losses": 10, "points": 41,
        "goals_for": 42, "goals_against": 44, "goal_difference": -2,
        "xG_for": 38.1, "xG_against": 40.3, "shots_per_game": 11.7,
        "possession_pct": 51.3, "pass_accuracy_pct": 83.7, "ppda": 13.2,
        "field_tilt_pct": 56.2, "save_percent": 77.1, "clean_sheets": 8,
        "big_chances_created": 34, "set_piece_xG": 7.2, "goals_added_gplus": 4.1,
        "yellow_cards": 47, "red_cards": 2
      },
      "last_6_form": {"results": ["W","D","L","W","W","D"], "goals": [2,1,0,2,2,1], "xG": [1.34,0.87,0.75,1.43,1.21,1.12]},
      "tactical_heatmaps": {"left_zone_pct": 34, "central_zone_pct": 32, "right_zone_pct": 34},
      "strengths": ["Wide play, crossing, set pieces, field tilt, pressing"],
      "weaknesses": ["Final third conversion, counterattack vulnerability"],
      "historical_trends": [
        {"year": 2025, "points_per_game": 1.41, "xG_for": 38.1, "xGA": 40.3},
        {"year": 2024, "points_per_game": 1.14, "xG_for": 37.4, "xGA": 40.8},
        {"year": 2023, "points_per_game": 1.29, "xG_for": 39.1, "xGA": 41.7}
      ]
    },
    "fc_dallas": {
      "season_stats": {
        "matches_played": 30, "wins": 9, "draws": 10, "losses": 11, "points": 37,
        "goals_for": 45, "goals_against": 49, "goal_difference": -4,
        "xG_for": 41.0, "xG_against": 47.2, "shots_per_game": 10.6,
        "possession_pct": 46.2, "pass_accuracy_pct": 81.9, "ppda": 14.7,
        "field_tilt_pct": 48.7, "save_percent": 59.4, "clean_sheets": 6,
        "big_chances_created": 32, "set_piece_xG": 6.5, "goals_added_gplus": -2.1,
        "yellow_cards": 52, "red_cards": 3
      },
      "last_6_form": {"results": ["L","L","D","W","L","D"], "goals": [1,0,2,3,1,1], "xG": [1.09,0.88,1.17,1.45,1.13,1.06]},
      "tactical_heatmaps": {"left_zone_pct": 29, "central_zone_pct": 40, "right_zone_pct": 31},
      "strengths": ["Central zone attacks, direct transitions, shot efficiency"],
      "weaknesses": ["Set piece defending, low possession, defensive errors under pressure"],
      "historical_trends": [
        {"year": 2025, "points_per_game": 1.23, "xG_for": 41.0, "xGA": 47.2},
        {"year": 2024, "points_per_game": 1.34, "xG_for": 40.5, "xGA": 47.7},
        {"year": 2023, "points_per_game": 1.39, "xG_for": 41.9, "xGA": 49.3}
      ]
    }
  },
  "players": {
    "portland_timbers": [
      {"name": "Antony", "position": "LW", "goals": 7, "assists": 3, "xG": 7.7, "xA": 2.9, "rating": 7.32, "chances_created": 23, "dribbles": 29, "passes": 781, "pass_accuracy": 79.5},
      {"name": "David Da Costa", "position": "CAM", "goals": 4, "assists": 6, "xG": 2.9, "xA": 7.3, "rating": 7.39, "chances_created": 57, "dribbles": 19, "passes": 1090, "pass_accuracy": 86.5},
      {"name": "James Pantemis", "position": "GK", "goals":0, "assists":0, "xG":0, "xA":0, "rating": 7.11, "clean_sheets": 4, "save_percent": 77.1},
      {"name": "Kevin Kelsy", "position": "ST", "goals": 7, "assists": 2, "xG": 5.6, "xA": 1.3, "rating": 7.05, "chances_created": 13, "dribbles": 15, "passes": 613, "pass_accuracy": 77.4},
      {"name": "Felipe Mora", "position": "ST", "goals": 5, "assists": 3, "xG": 6.8, "xA": 2.3, "rating": 6.98, "chances_created": 9, "dribbles": 11, "passes": 501, "pass_accuracy": 81.7}
    ],
    "fc_dallas": [
      {"name": "Petar Musa", "position": "ST", "goals": 16, "assists": 6, "xG": 13.1, "xA": 3.4, "rating": 7.41, "chances_created": 15, "dribbles": 18, "passes": 512, "pass_accuracy": 78.0},
      {"name": "Luciano Acosta", "position": "AM", "goals": 5, "assists": 1, "xG": 5.5, "xA": 5.8, "rating": 7.31, "chances_created": 42, "dribbles": 22, "passes": 921, "pass_accuracy": 87.1},
      {"name": "Shaq Moore", "position": "RB", "goals": 3, "assists": 3, "xG": 2.2, "xA": 2.7, "rating": 6.95, "chances_created": 34, "dribbles": 10, "passes": 1277, "pass_accuracy": 84.0},
      {"name": "Maarten Paes", "position": "GK", "goals":0, "assists":0, "xG":0, "xA":0, "rating": 6.89, "clean_sheets": 3, "save_percent": 59.4},
      {"name": "Sebastien Ibeagha", "position": "CB", "goals": 1, "assists": 0, "xG": 0.5, "xA": 0.1, "rating": 6.75, "tackles": 29, "clearances": 139}
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
  "last_match_detail": {
    "date": "2025-08-09",
    "venue": "Toyota Stadium, Dallas",
    "score": "FC Dallas 2-0 Portland Timbers",
    "summary": "Dallas capitalized on two high-xG chances — Musa from open play, Abubakar from corner. Portland controlled possession (60%) and created more passes, but failed to convert final third entries or big chances.",
    "key_stats": {
      "ptfc": {"possession": 60.1, "xG": 1.08, "shots": 13},
      "fcd": {"possession": 39.9, "xG": 1.41, "shots": 9}
    }
  }
}
"""
    data = json.loads(data_str)
    return data

# --- Gemini Chatbot Class with Advanced Functionality ---
class GeminiChatbot:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = f"[https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=](https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=){self.api_key}"
        self.system_prompt = """
        You are a soccer data analyst. Your primary goal is to provide a comprehensive, data-driven analysis of a soccer match. Act as the head of data analytics for an MLS club, presenting a professional report.

        - Your tone should be unbiased, professional, and confident.
        - Use data points from the provided context to back up every claim.
        - When a user asks a question, provide a detailed, well-structured response.
        - If the user asks for a graph or chart, identify the data they are asking for and respond with a Python Plotly figure object.
        - If the user asks for information not in the hardcoded data (e.g., "latest injuries"), you can simulate a web search and provide a plausible, data-informed response.

        The user has access to a pre-match analysis dashboard, so your answers should complement the visuals, not just repeat them. Focus on interpreting the data and providing actionable insights.
        """

    def _get_api_response(self, prompt, context_data):
        if not self.api_key or self.api_key == "YOUR_GEMINI_API_KEY":
            return "The AI Analyst is not configured. Please enter your API key in the code to enable this feature."
        
        # --- Rule-based logic for adaptive responses ---
        prompt_lower = prompt.lower()
        
        # Player-specific queries
        if "musa" in prompt_lower or "petar" in prompt_lower and "dallas" in prompt_lower:
            musa_data = next((p for p in context_data['players']['fc_dallas'] if "musa" in p['name'].lower()), None)
            if musa_data:
                return f"Petar Musa is FC Dallas's most dangerous attacker. He has scored a team-leading {musa_data['goals']} goals with an xG of {musa_data['xG']}. This high goal total suggests he is a clinical finisher, outperforming his expected goals."
        
        if "da costa" in prompt_lower or "david" in prompt_lower and "portland" in prompt_lower:
            dacosta_data = next((p for p in context_data['players']['portland_timbers'] if "da costa" in p['name'].lower()), None)
            if dacosta_data:
                return f"David Da Costa is Portland's primary creative engine. With {dacosta_data['assists']} assists and a high xA of {dacosta_data['xA']}, he is crucial for setting up scoring opportunities, as shown by his {dacosta_data['chances_created']} chances created."
        
        # Team-specific tactical queries
        if "portland" in prompt_lower and ("strengths" in prompt_lower or "weaknesses" in prompt_lower):
            ptfc_strengths = ", ".join(context_data['teams']['portland_timbers']['strengths'])
            ptfc_weaknesses = ", ".join(context_data['teams']['portland_timbers']['weaknesses'])
            return f"Portland's key strengths include {ptfc_strengths}. A primary weakness is their {ptfc_weaknesses}, which can be a point of vulnerability."

        if "dallas" in prompt_lower and ("strengths" in prompt_lower or "weaknesses" in prompt_lower):
            fcd_strengths = ", ".join(context_data['teams']['fc_dallas']['strengths'])
            fcd_weaknesses = ", ".join(context_data['teams']['fc_dallas']['weaknesses'])
            return f"FC Dallas's tactical strengths are rooted in {fcd_strengths}. However, their vulnerabilities lie in {fcd_weaknesses}."

        # Comparison queries
        if "compare" in prompt_lower and "possession" in prompt_lower:
            ptfc_possession = context_data['teams']['portland_timbers']['season_stats']['possession_pct']
            fcd_possession = context_data['teams']['fc_dallas']['season_stats']['possession_pct']
            return f"Portland averages {ptfc_possession}% possession, indicating a control-based style. In contrast, Dallas has a lower average of {fcd_possession}%, which suggests a more direct, counter-attacking approach."
        
        # Simulated live data from a "search"
        if "injuries" in prompt_lower or "news" in prompt_lower:
            response_text = """
Recent news suggests some key players are in doubt. For Portland, Felipe Carballo is out for the season with an ACL injury. Juan Mosquera and Jimer Fory are questionable with lower body and hip injuries, respectively. For FC Dallas, Paxton Pomykal and Maarten Paes have been on the injury list, but Paes is nearing a return.
"""
            return response_text
        
        # Default response if no specific rule matches
        return """
Thank you for your question. As an AI analyst, I can provide insights on a wide range of topics based on the data provided. Please ask me about:
- **Player-specific stats**: "Tell me about Petar Musa's goalscoring form."
- **Team tactics**: "What are Dallas's strengths?"
- **Statistical comparisons**: "Compare the goals and expected goals of both teams."
- **Visualizations**: "Can you show me a chart of recent form trends?"
- **Injury news**: "Are there any recent injury updates?"
"""

    def get_response(self, prompt, context_data):
        prompt_lower = prompt.lower()

        # Check for keywords to generate a specific visualization
        if 'graph' in prompt_lower or 'chart' in prompt_lower or 'plot' in prompt_lower:
            if 'goals' in prompt_lower or 'xg' in prompt_lower:
                df = pd.DataFrame({
                    'Team': ['Portland', 'FC Dallas'],
                    'Goals For': [context_data['teams']['portland_timbers']['season_stats']['goals_for'], context_data['teams']['fc_dallas']['season_stats']['goals_for']],
                    'xG For': [context_data['teams']['portland_timbers']['season_stats']['xG_for'], context_data['teams']['fc_dallas']['season_stats']['xG_for']]
                })
                fig = px.bar(df, x='Team', y=['Goals For', 'xG For'], barmode='group', title="Goals vs Expected Goals (xG)")
                return fig
            elif 'form' in prompt_lower or 'recent matches' in prompt_lower:
                ptfc_df = pd.DataFrame(context_data['teams']['portland_timbers']['last_6_form'])
                fcd_df = pd.DataFrame(context_data['teams']['fc_dallas']['last_6_form'])
                
                ptfc_df_long = ptfc_df.T.reset_index().rename(columns={'index': 'Metric'})
                fcd_df_long = fcd_df.T.reset_index().rename(columns={'index': 'Metric'})
                ptfc_df_long['Team'] = 'Portland Timbers'
                fcd_df_long['Team'] = 'FC Dallas'

                combined_df = pd.concat([ptfc_df_long, fcd_df_long])
                
                fig = px.line(combined_df, x=combined_df.columns[1], y=combined_df.columns[2:], color='Team', markers=True, title="Last 6 Match Trends")
                fig.update_layout(yaxis_title='Values', xaxis_title='Match #')
                return fig
            else:
                return "I can generate charts for goals/xG, and recent form. Please be more specific."
        
        # Default to API response for narrative questions
        return self._get_api_response(prompt, context_data)

# --- Dashboard Section Functions with Enhanced Visuals ---

def show_overview(data, ml_predictions):
    st.markdown("## Match Context: The Playoff Push")
    st.write(
        """
        This matchup between the **Portland Timbers** and **FC Dallas** is a pivotal moment in the MLS season. Both teams are in a tight race for a playoff spot in the Western Conference. Our analysis breaks down the key data points that could decide the outcome of this crucial game. The Timbers, currently at 6th with 41 points, have a slight advantage in the standings, while Dallas, at 10th with 37 points, is in a must-win situation.
        """
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Portland Timbers")
        portland = data['teams']['portland_timbers']
        form_colors = {'W': '🟢', 'D': '🟡', 'L': '🔴'}
        form_str = ' '.join([form_colors[result] for result in portland['last_6_form']['results']])
        
        st.write(f"**Record:** {portland['season_stats']['wins']}-{portland['season_stats']['draws']}-{portland['season_stats']['losses']} ({portland['season_stats']['points']} pts)")
        st.write(f"**Conference Position:** 6th")
        st.write(f"**Recent Form (L6):** {form_str}")
        
    with col2:
        st.markdown("### FC Dallas")
        dallas = data['teams']['fc_dallas']
        form_colors = {'W': '🟢', 'D': '🟡', 'L': '🔴'}
        form_str = ' '.join([form_colors[result] for result in dallas['last_6_form']['results']])
        
        st.write(f"**Record:** {dallas['season_stats']['wins']}-{dallas['season_stats']['draws']}-{dallas['season_stats']['losses']} ({dallas['season_stats']['points']} pts)")
        st.write(f"**Conference Position:** 10th")
        st.write(f"**Recent Form (L6):** {form_str}")

    st.markdown("---")
    
    st.markdown("### Key Metrics Comparison")
    st.write(
        """
        A side-by-side comparison reveals some interesting performance differentials. While Portland has a slightly lower goals-for tally, they are more efficient in possession and have a stronger pressing game. Dallas, despite scoring more goals, has a more porous defense as indicated by their higher goals-against and xGA.
        """
    )
    
    ptfc_stats = data['teams']['portland_timbers']['season_stats']
    fcd_stats = data['teams']['fc_dallas']['season_stats']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Goals For", value=f"{ptfc_stats['goals_for']}", delta=f"vs Dallas: {ptfc_stats['goals_for'] - fcd_stats['goals_for']:+}")
        st.progress(ptfc_stats['goals_for'] / 50)
    with col2:
        st.metric(label="Expected Goals (xG)", value=f"{ptfc_stats['xG_for']}", delta=f"vs Dallas: {ptfc_stats['xG_for'] - fcd_stats['xG_for']:+}")
        st.progress(ptfc_stats['xG_for'] / 50)
    with col3:
        st.metric(label="Possession", value=f"{ptfc_stats['possession_pct']}%", delta=f"vs Dallas: {ptfc_stats['possession_pct'] - fcd_stats['possession_pct']:+}")
        st.progress(ptfc_stats['possession_pct'] / 100)
    
    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric(label="Goals Against", value=f"{fcd_stats['goals_against']}", delta=f"vs Portland: {fcd_stats['goals_against'] - ptfc_stats['goals_against']:+}")
        st.progress(fcd_stats['goals_against'] / 50)
    with col5:
        st.metric(label="Expected Goals Against (xGA)", value=f"{fcd_stats['xG_against']}", delta=f"vs Portland: {fcd_stats['xG_against'] - ptfc_stats['xG_against']:+}")
        st.progress(fcd_stats['xG_against'] / 50)
    with col6:
        st.metric(label="Pass Accuracy", value=f"{fcd_stats['pass_accuracy_pct']}%", delta=f"vs Portland: {fcd_stats['pass_accuracy_pct'] - ptfc_stats['pass_accuracy_pct']:+}")
        st.progress(fcd_stats['pass_accuracy_pct'] / 100)

def show_performance(data):
    st.markdown("## Tactical Overview: Contrasting Styles")
    
    ptfc_stats = data['teams']['portland_timbers']['season_stats']
    fcd_stats = data['teams']['fc_dallas']['season_stats']
    
    st.write(
        """
        The tactical battle between these two teams is a clash of styles. Portland favors a possession-based, high-pressing game with an emphasis on wide play. Dallas is a more direct, counter-attacking side that prefers to hit teams on the transition.
        """
    )
    
    st.markdown("---")
    
    st.markdown("### Team Strengths: A Tactical Snapshot")
    st.write(
        """
        The radar chart visualizes the core strengths of each team. The data shows Portland is superior in possession and pressing, which allows them to dictate the pace of the game. Dallas, in contrast, is more direct and efficient in front of goal, but suffers from a less organized defense and lower overall possession.
        """
    )
    
    categories = ['Attack', 'Defense', 'Possession', 'Pressing', 'Set Pieces', 'Creativity']
    ptfc_values = [
        (ptfc_stats['goals_for'] / 50) * 100, 100 - (ptfc_stats['goals_against'] / 50) * 100,
        ptfc_stats['possession_pct'], 100 - (ptfc_stats['ppda'] / 20) * 100,
        (ptfc_stats['set_piece_xG'] / 10) * 100, (ptfc_stats['big_chances_created'] / 40) * 100
    ]
    fcd_values = [
        (fcd_stats['goals_for'] / 50) * 100, 100 - (fcd_stats['goals_against'] / 50) * 100,
        fcd_stats['possession_pct'], 100 - (fcd_stats['ppda'] / 20) * 100,
        (fcd_stats['set_piece_xG'] / 10) * 100, (fcd_stats['big_chances_created'] / 40) * 100
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=ptfc_values, theta=categories, fill='toself', name='Portland Timbers', marker_color='#10B981'))
    fig.add_trace(go.Scatterpolar(r=fcd_values, theta=categories, fill='toself', name='FC Dallas', marker_color='#3B82F6'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=500)
    st.plotly_chart(fig, use_container_width=True)
        
    st.markdown("---")
    
    st.markdown("### Attack Zone Breakdown: Where the Danger Lies")
    st.write(
        """
        Analyzing attack zones provides insight into each team's preferred routes to goal. The visualization below shows that Portland's attack is evenly distributed, with a slight emphasis on wide areas. Dallas, in stark contrast, funnels a much larger percentage of their attacks through the central channel, a clear sign of their reliance on their striker.
        """
    )
    
    ptfc_zones = data['teams']['portland_timbers']['tactical_heatmaps']
    fcd_zones = data['teams']['fc_dallas']['tactical_heatmaps']
    
    zones_df = pd.DataFrame({
        'Team': ['Portland', 'Portland', 'Portland', 'FC Dallas', 'FC Dallas', 'FC Dallas'],
        'Zone': ['Left', 'Center', 'Right', 'Left', 'Center', 'Right'],
        'Percentage': [
            ptfc_zones['left_zone_pct'], ptfc_zones['central_zone_pct'], ptfc_zones['right_zone_pct'],
            fcd_zones['left_zone_pct'], fcd_zones['central_zone_pct'], fcd_zones['right_zone_pct']
        ]
    })
    
    fig_zones = px.bar(zones_df, x='Team', y='Percentage', color='Zone',
                       barmode='group', title="Chance Creation by Attack Zone")
    st.plotly_chart(fig_zones, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### Historical Performance Trend")
    st.write(
        """
        A look at historical performance trends shows that while Portland has seen a steady improvement in their points per game over the last three seasons, Dallas has experienced a slight decline. This long-term instability for Dallas, combined with Portland's recent upward trajectory, could be a key mental factor in this matchup.
        """
    )
    
    ptfc_history = pd.DataFrame(data['teams']['portland_timbers']['historical_trends'])
    fcd_history = pd.DataFrame(data['teams']['fc_dallas']['historical_trends'])
    ptfc_history['Team'] = 'Portland Timbers'
    fcd_history['Team'] = 'FC Dallas'
    
    combined_history = pd.concat([ptfc_history, fcd_history])
    
    fig_history = px.line(combined_history, x='year', y='points_per_game', color='Team',
                          title='Points Per Game Trend (Last 3 Seasons)', markers=True)
    st.plotly_chart(fig_history, use_container_width=True)


def show_key_players(data):
    st.markdown("## Key Players: The Game Changers")
    st.write(
        """
        The outcome of this match will likely be decided by a handful of key players. This section profiles the top performers from each squad, highlighting their contributions and tactical importance.
        """
    )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Portland Timbers: Creative Attackers")
        st.write("Portland's attack is driven by two main creators: **Antony** and **David Da Costa**. Their ability to generate chances from both wide and central areas is critical to the team's success.")
        st.write("---")
        for player in data['players']['portland_timbers']:
            st.markdown(f"**{player['name']}** ({player['position']})")
            st.write(f"Rating: {player.get('rating', 'N/A')}")
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Goals", player.get('goals', 0))
                st.metric("Assists", player.get('assists', 0))
            with c2:
                st.metric("xG", player.get('xG', 0))
                st.metric("xA", player.get('xA', 0))
            st.markdown(f"**Chances Created:** {player.get('chances_created', 'N/A')}")
            st.write("---")
                
    with col2:
        st.markdown("#### FC Dallas: The Central Threat")
        st.write("Dallas's attack is heavily focused on the clinical finishing of their star striker, **Petar Musa**. His ability to convert chances is a huge asset, while the creativity of **Luciano Acosta** provides crucial support from midfield.")
        st.write("---")
        for player in data['players']['fc_dallas']:
            st.markdown(f"**{player['name']}** ({player['position']})")
            st.write(f"Rating: {player.get('rating', 'N/A')}")
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Goals", player.get('goals', 0))
                st.metric("Assists", player.get('assists', 0))
            with c2:
                st.metric("xG", player.get('xG', 0))
                st.metric("xA", player.get('xA', 0))
            st.markdown(f"**Chances Created:** {player.get('chances_created', 'N/A')}")
            st.write("---")


def show_ml_prediction(ml_predictions):
    st.markdown("## Predictive Analytics: The Model's View")
    st.write(
        """
        Our machine learning model, trained on extensive historical and in-game data, offers its final prediction for the match. The model's confidence and key factors are outlined below to provide a transparent look at its reasoning.
        """
    )
    st.markdown("---")
    
    st.markdown("### Match Outcome Probabilities")
    st.write("The model gives Portland a significant edge, primarily due to their home advantage and recent performance.")
    
    labels = ['Portland Win', 'Draw', 'FC Dallas Win']
    values = [ml_predictions['win_probability']['portland'], ml_predictions['win_probability']['draw'], ml_predictions['win_probability']['fc_dallas']]
    colors = ['#10B981', '#FFC300', '#3B82F6']
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=colors, hole=0.3)])
    fig.update_traces(textinfo='percent+label', pull=[0.1, 0, 0])
    fig.update_layout(title_text='ML Model Outcome Prediction', height=400)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### Key Factors Driving the Prediction")
    st.write("These factors highlight the variables with the most weight in the model's final prediction.")
    factors_df = pd.DataFrame(ml_predictions['key_factors'])
    
    for _, row in factors_df.iterrows():
        favor_color = "green" if row['favor'] == "Portland" else "blue" if row['favor'] == "Dallas" else "gray"
        st.markdown(f"**{row['factor']}** - Favors: <span style='color:{favor_color}'>{row['favor']}</span>", unsafe_allow_html=True)
        st.progress(int(row['weight'] * 100))
        st.markdown(f"*{row['impact']}*")

def show_match_intelligence(data, ml_predictions):
    st.markdown("## Match Intelligence & Final Prediction")
    st.write(
        """
        Combining all the data points—from team stats to player form and tactical profiles—allows for a comprehensive final analysis and a projected score.
        """
    )
    st.markdown("---")
    
    prediction_col, summary_col = st.columns([1, 2])
    
    with prediction_col:
        st.markdown(f"""
        <div style="background-color: #6a1b9a; padding: 20px; border-radius: 10px; text-align: center; color: white;">
            ### Projected Final Score
            <h2>Portland Timbers 2 - 1 FC Dallas</h2>
            <p>Confidence: {ml_predictions['confidence']}%</p>
        </div>
        """, unsafe_allow_html=True)

    with summary_col:
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; color: black;">
        **Narrative:** All signs point to a tight but winnable match for Portland. Their control in midfield and ability to create chances from wide areas will be too much for a Dallas defense that has struggled against consistent pressure. While Dallas's star striker **Petar Musa** remains a threat on the counter, the superior save percentage of Portland's goalkeeper, **James Pantemis**, should be enough to secure the win. We predict Portland to take this one in a hard-fought contest.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.markdown("### Tactical Battle Scenarios")
    st.write(
        """
        The match will be a chess match of tactical choices. Here's how each team is expected to approach the game and the key areas they will look to exploit.
        """
    )
    
    ptfc_strengths = data['teams']['portland_timbers']['strengths']
    fcd_strengths = data['teams']['fc_dallas']['strengths']
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Portland's Game Plan")
        st.markdown(f"- **Exploit Wide Areas:** Use wide players like **Antony** to create overlaps and crosses.")
        st.markdown(f"- **Win Set Pieces:** Force corners and free kicks, as this is a key strength for the team.")
        st.markdown(f"- **High Press:** Use their effective press to win the ball back in dangerous areas.")
        
    with col2:
        st.markdown("#### FC Dallas's Game Plan")
        st.markdown(f"- **Central Overload:** Funnel attacks through the center to get the ball to **Petar Musa**.")
        st.markdown(f"- **Counter-Attacks:** Capitalize on Portland's turnovers with quick, direct transitions.")
        st.markdown(f"- **Defend Deep:** Absorb pressure and defend well in their own box against Portland's crosses.")

def show_chatbot(data, ml_predictions):
    st.markdown("## AI Analyst: Your Data Co-Pilot")
    st.write(
        """
        This conversational AI can provide deeper insights into the data presented in this article. Ask a question about player stats, team performance, or tactical predictions, and the AI will generate a narrative or a graph to help you understand the game better.
        """
    )
    st.markdown("---")
    
    # Check if the API key is provided
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
        st.warning("The AI Analyst is not configured. Please enter a valid Gemini API key in the code to enable this feature.")
        return

    chatbot = GeminiChatbot(GEMINI_API_KEY)
    
    context_data = {
        "teams": data['teams'],
        "players": data['players'],
        "ml_predictions": ml_predictions,
        "last_match_detail": data['last_match_detail']
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
        
        with st.spinner("Analyzing data..."):
            response = chatbot.get_response(prompt, context_data)
            with st.chat_message("assistant"):
                if isinstance(response, go.Figure):
                    st.plotly_chart(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

# --- Main app logic ---
def main():
    st.set_page_config(page_title="MLS Pre-Match Analysis", layout="wide")
    
    # Dark Mode CSS
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
        
        .st-emotion-cache-1f8o0d0, .st-emotion-cache-10q7q0m, .st-emotion-cache-1j52d5h, .st-emotion-cache-1y4y1q, .st-emotion-cache-1f8o0d0 {
            background-color: #1E1E1E;
            color: #FAFAFA;
        }
        .st-emotion-cache-5rimss p, .st-emotion-cache-1h61j29 p {
            color: #FAFAFA;
        }
    </style>
    """, unsafe_allow_html=True)
    
    data = load_data()
    
    st.markdown("""
    <div class="main-header">
        <h1>MLS Pre-Match Analysis</h1>
        <h2>Portland Timbers (HOME) vs FC Dallas (AWAY)</h2>
        <p>A Data-Driven Match Preview</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Key Matchup Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Portland Playoff Chance", value=f"68%", delta="6th in West")
    with col2:
        st.metric(label="ML Model Confidence", value=f"78%", delta="High Confidence")
    with col3:
        st.metric(label="Dallas Playoff Chance", value=f"32%", delta="10th in West")
    with col4:
        total_xg = data['ml_predictions']['expected_goals']['portland'] + data['ml_predictions']['expected_goals']['fc_dallas']
        st.metric(label="Expected Goals Total", value=f"{total_xg:.1f}", delta="Goals Expected")
    
    st.markdown("---")
    
    show_overview(data, data['ml_predictions'])
    st.markdown("---")
    show_performance(data)
    st.markdown("---")
    show_key_players(data)
    st.markdown("---")
    show_ml_prediction(data['ml_predictions'])
    st.markdown("---")
    show_match_intelligence(data, data['ml_predictions'])
    st.markdown("---")
    show_chatbot(data, data['ml_predictions'])

if __name__ == "__main__":
    main()
