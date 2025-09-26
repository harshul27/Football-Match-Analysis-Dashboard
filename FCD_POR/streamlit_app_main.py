import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import requests
import re
import random

# --- Consolidated JSON Data from User's Files ---
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
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={self.api_key}"

    def _get_api_response(self, prompt, context_data):
        if not self.api_key:
            return "Based on the data, Portland's superior defensive numbers and home advantage make them slight favorites. Players like Antony and David Da Costa are key to their attack, while Dallas will rely heavily on Petar Musa's clinical finishing. "
        
        # Simulating live data from a "search"
        if "latest injuries" in prompt.lower() or "latest news" in prompt.lower():
            # This is a mock response from a tool call to google_search
            response_text = """
Recent news suggests some key players are in doubt. For Portland, Felipe Carballo is out for the season with an ACL injury. Juan Mosquera and Jimer Fory are questionable with lower body and hip injuries, respectively. For FC Dallas, Paxton Pomykal and Maarten Paes have been on the injury list, but Paes is nearing a return.
"""
            return response_text
        
        full_prompt = f"""
        You are a soccer data analyst. Your goal is to provide a narrative of the statistics and the game for a person asking different questions about the teams or anything related to the match being analyzed.

        Here is the relevant data about the Portland Timbers and FC Dallas:
        {json.dumps(context_data, indent=2)}

        Now, answer the following question based on the provided data. Be concise, informative, and do not make up information that isn't in the data.

        Question: {prompt}
        """

        # For demonstration, we return a static, but now more descriptive, response.
        return f"""
Based on the data, Portland's superior defensive numbers and home advantage make them slight favorites. Players like Antony and David Da Costa are key to their attack, while Dallas will rely heavily on Petar Musa's clinical finishing. Portland's goalkeeper has a much higher save percentage, which could be a key factor in the match.
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
                ptfc_df = pd.DataFrame(context_data['teams']['portland_timbers']['last_6_form']).T
                ptfc_df.columns = [f'Match {i+1}' for i in range(len(ptfc_df.columns))]
                fcd_df = pd.DataFrame(context_data['teams']['fc_dallas']['last_6_form']).T
                fcd_df.columns = [f'Match {i+1}' for i in range(len(fcd_df.columns))]
                
                combined_df = pd.concat([ptfc_df, fcd_df], keys=['Portland Timbers', 'FC Dallas']).reset_index().rename(columns={'level_0': 'Team', 'level_1': 'Metric'})
                
                fig = px.line(combined_df, x='Metric', y=[f'Match {i+1}' for i in range(len(ptfc_df.columns))], color='Team', title="Last 6 Match Trends")
                fig.update_layout(yaxis_title='Values', xaxis_title='Metric')
                return fig
            else:
                return "I can generate charts for goals/xG, and recent form. Please be more specific."
        
        # Default to API response for narrative questions
        return self._get_api_response(prompt, context_data)

# --- Dashboard Section Functions with Enhanced Visuals ---

def show_overview(data, ml_predictions):
    st.header("📈 Season Overview & Narrative", divider='green')
    
    st.markdown(
        f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        As the season progresses, both teams find themselves in a tight race for a playoff spot. **Portland Timbers** currently sit 6th with 41 points from 29 games, while **FC Dallas** are 10th with 37 points from 30 games. This matchup is crucial for Dallas, who must secure a win to keep their playoff hopes alive. Both teams have a negative goal difference, indicating defensive struggles throughout the season. However, the Timbers have shown more stability at home and in recent form, which could give them a crucial advantage in this fixture.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🟢 Portland Timbers")
        portland = data['teams']['portland_timbers']
        form_colors = {'W': '🟢', 'D': '🟡', 'L': '🔴'}
        form_str = ' '.join([form_colors[result] for result in portland['last_6_form']['results']])
        
        st.markdown(f"**Record:** {portland['season_stats']['wins']}-{portland['season_stats']['draws']}-{portland['season_stats']['losses']} ({portland['season_stats']['points']} pts)")
        st.markdown(f"**Conference Position:** 6th")
        st.markdown(f"**Recent Form (L6):** {form_str}")
        
    with col2:
        st.subheader("🔵 FC Dallas")
        dallas = data['teams']['fc_dallas']
        form_colors = {'W': '🟢', 'D': '🟡', 'L': '🔴'}
        form_str = ' '.join([form_colors[result] for result in dallas['last_6_form']['results']])
        
        st.markdown(f"**Record:** {dallas['season_stats']['wins']}-{dallas['season_stats']['draws']}-{dallas['season_stats']['losses']} ({dallas['season_stats']['points']} pts)")
        st.markdown(f"**Conference Position:** 10th")
        st.markdown(f"**Recent Form (L6):** {form_str}")

    st.markdown("---")
    
    # Dynamic metrics with progress bars
    st.subheader("Key Metrics Comparison")
    
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
    
    st.markdown("<br>", unsafe_allow_html=True)
    
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
    st.header("📊 Performance & Tactical Analysis", divider='green')
    
    ptfc_stats = data['teams']['portland_timbers']['season_stats']
    fcd_stats = data['teams']['fc_dallas']['season_stats']
    
    st.markdown(
        f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        **Narrative:** The radar chart below visualizes the core strengths and weaknesses of each team. **Portland** excels in areas like possession and pressing, which allows them to dictate the pace of the game. They are also a major threat from set pieces. **Dallas**, on the other hand, is a more direct, counter-attacking side that relies on being clinical in front of goal despite having lower overall possession. The battle for midfield control and converting chances will be key.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Radar chart for team comparison
    st.subheader("Team Strengths: A Tactical Snapshot")
    categories = ['Attack', 'Defense', 'Possession', 'Pressing', 'Set Pieces', 'Creativity']
    
    # Correctly normalize metrics for a 0-100 scale
    ptfc_values = [
        (ptfc_stats['goals_for'] / 50) * 100,
        100 - (ptfc_stats['goals_against'] / 50) * 100,
        ptfc_stats['possession_pct'],
        100 - (ptfc_stats['ppda'] / 20) * 100,
        (ptfc_stats['set_piece_xG'] / 10) * 100,
        (ptfc_stats['big_chances_created'] / 40) * 100
    ]
    fcd_values = [
        (fcd_stats['goals_for'] / 50) * 100,
        100 - (fcd_stats['goals_against'] / 50) * 100,
        fcd_stats['possession_pct'],
        100 - (fcd_stats['ppda'] / 20) * 100,
        (fcd_stats['set_piece_xG'] / 10) * 100,
        (fcd_stats['big_chances_created'] / 40) * 100
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=ptfc_values, theta=categories, fill='toself', name='Portland Timbers', marker_color='#10B981'))
    fig.add_trace(go.Scatterpolar(r=fcd_values, theta=categories, fill='toself', name='FC Dallas', marker_color='#3B82F6'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=500)
    st.plotly_chart(fig, use_container_width=True)
        
    # --- New: Tactical Heatmap Visualization ---
    st.markdown("---")
    st.subheader("Attack Zone Breakdown")
    
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
    
    st.markdown(
        f"""
        **Narrative:** The heatmap analysis highlights key tactical differences. **Portland** distributes their attack evenly across the field, but their wide play is their primary strength. **Dallas**, however, shows a clear preference for a central overload, relying on players like Petar Musa to create and convert chances from the middle of the pitch.
        """,
        unsafe_allow_html=True
    )
    
    # --- New: Historical Trend Chart ---
    st.markdown("---")
    st.subheader("Historical Performance Trend")
    
    ptfc_history = pd.DataFrame(data['teams']['portland_timbers']['historical_trends'])
    fcd_history = pd.DataFrame(data['teams']['fc_dallas']['historical_trends'])
    ptfc_history['Team'] = 'Portland Timbers'
    fcd_history['Team'] = 'FC Dallas'
    
    combined_history = pd.concat([ptfc_history, fcd_history])
    
    fig_history = px.line(combined_history, x='year', y='points_per_game', color='Team',
                          title='Points Per Game Trend (Last 3 Seasons)', markers=True)
    st.plotly_chart(fig_history, use_container_width=True)
    
    st.markdown(
        f"""
        **Narrative:** A quick look at the last three seasons reveals some interesting trends. **Portland** has shown a gradual improvement in their points per game, suggesting a team that is finding its footing. **Dallas**, on the other hand, has seen a slight decline, indicating potential inconsistency. This trend makes Portland's current form and home advantage even more significant.
        """
    )


def show_key_players(data):
    st.header("⭐ Key Players Analysis", divider='green')
    
    st.markdown(
        f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        **Narrative:** This section provides a detailed look at each team's key players. Their statistics reveal their roles in the team's tactics. For Portland, the creative forces of **Antony** and **David Da Costa** on the wings and in the center are crucial. For Dallas, the focus is squarely on their star striker, **Petar Musa**, who is responsible for a significant portion of their goals and xG.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    
    # Player cards for Portland
    with col1:
        st.subheader("🟢 Portland Timbers - Top Performers")
        for player in data['players']['portland']:
            with st.expander(f"**{player['name']}** ({player['position']}) - Rating: {player.get('rating', 'N/A')}"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Goals", player.get('goals', 0))
                with c2:
                    st.metric("Assists", player.get('assists', 0))
                with c3:
                    st.metric("xG", player.get('xG', 0))
                st.markdown("---")
                st.markdown("**Performance Insights**")
                st.markdown(f"**Chances Created:** {player.get('chances_created', 'N/A')}")
                st.markdown(f"**Dribbles:** {player.get('dribbles', 'N/A')}")
                
    # Player cards for FC Dallas
    with col2:
        st.subheader("🔵 FC Dallas - Top Performers")
        for player in data['players']['fc_dallas']:
            with st.expander(f"**{player['name']}** ({player['position']}) - Rating: {player.get('rating', 'N/A')}"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Goals", player.get('goals', 0))
                with c2:
                    st.metric("Assists", player.get('assists', 0))
                with c3:
                    st.metric("xG", player.get('xG', 0))
                st.markdown("---")
                st.markdown("**Performance Insights**")
                st.markdown(f"**Chances Created:** {player.get('chances_created', 'N/A')}")
                st.markdown(f"**Dribbles:** {player.get('dribbles', 'N/A')}")


def show_ml_prediction(ml_predictions):
    st.header("🤖 Machine Learning Prediction", divider='green')
    
    st.subheader("Match Outcome Probabilities")
    labels = ['Portland Win', 'Draw', 'FC Dallas Win']
    values = [ml_predictions['win_probability']['portland'], ml_predictions['win_probability']['draw'], ml_predictions['win_probability']['fc_dallas']]
    colors = ['#10B981', '#FFC300', '#3B82F6']
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=colors, hole=0.3)])
    fig.update_traces(textinfo='percent+label', pull=[0.1, 0, 0])
    fig.update_layout(title_text='ML Model Outcome Prediction', height=400)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Key Factors Driving the Prediction")
    factors_df = pd.DataFrame(ml_predictions['key_factors'])
    
    for _, row in factors_df.iterrows():
        favor_color = "green" if row['favor'] == "Portland" else "blue" if row['favor'] == "Dallas" else "gray"
        st.markdown(f"**{row['factor']}** - Favors: <span style='color:{favor_color}'>{row['favor']}</span>", unsafe_allow_html=True)
        st.progress(int(row['weight'] * 100))
        st.markdown(f"*{row['impact']}*")

def show_match_intelligence(data, ml_predictions):
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
        **Narrative:** The data suggests a tightly contested match. **Portland's home advantage** and defensive solidity, especially from their goalkeeper **James Pantemis** (77.1% save rate), give them a crucial edge. While FC Dallas boasts a clinical finisher in **Petar Musa** (16 goals), their overall defensive vulnerabilities and lower possession numbers are likely to be exploited. Expect Portland to control possession and win the game through a decisive moment, potentially from a set piece or a key creative pass from a player like David Da Costa. 
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.subheader("Tactical Battle Scenarios")
    
    ptfc_strengths = data['teams']['portland_timbers']['strengths']
    ptfc_weaknesses = data['teams']['portland_timbers']['weaknesses']
    fcd_strengths = data['teams']['fc_dallas']['strengths']
    fcd_weaknesses = data['teams']['fc_dallas']['weaknesses']
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("**Portland's Game Plan**")
        st.markdown("- **Exploit Wide Areas:** Use wide players like Antony and Da Costa to create overlaps and crosses.")
        st.markdown("- **Win Set Pieces:** Force corners and free kicks, as this is a key strength for the team.")
        st.markdown("- **High Press:** Use their effective press to win the ball back in dangerous areas.")
        
    with col2:
        st.info("**FC Dallas' Game Plan**")
        st.markdown("- **Central Overload:** Funnel attacks through the center to get the ball to Petar Musa.")
        st.markdown("- **Counter-Attacks:** Capitalize on Portland's turnovers with quick, direct transitions.")
        st.markdown("- **Defend Deep:** Absorb pressure and defend well in their own box against Portland's crosses and set pieces.")

def show_chatbot(data, ml_predictions):
    st.header("💬 AI Match Analyst", divider='green')
    
    gemini_key = st.secrets.get("gemini_api_key")
    if not gemini_key:
        st.warning("To use the AI Analyst, please add a `gemini_api_key` to your Streamlit secrets.")
        return

    chatbot = GeminiChatbot(gemini_key)
    
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
    data = load_data()
    
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
        total_xg = data['ml_predictions']['expected_goals']['portland'] + data['ml_predictions']['expected_goals']['fc_dallas']
        st.metric(label="Expected Goals Total", value=f"{total_xg:.1f}", delta="Goals Expected")
    
    st.sidebar.title("📊 Analysis Sections")
    tab = st.sidebar.selectbox(
        "Select Analysis:",
        ["Overview", "Performance Analysis", "Key Players", "ML Prediction", "Match Intelligence", "AI Analyst"]
    )
    
    if tab == "Overview":
        show_overview(data, data['ml_predictions'])
    elif tab == "Performance Analysis":
        show_performance(data)
    elif tab == "Key Players":
        show_key_players(data)
    elif tab == "ML Prediction":
        show_ml_prediction(data['ml_predictions'])
    elif tab == "Match Intelligence":
        show_match_intelligence(data, data['ml_predictions'])
    elif tab == "AI Analyst":
        show_chatbot(data, data['ml_predictions'])

if __name__ == "__main__":
    main()
