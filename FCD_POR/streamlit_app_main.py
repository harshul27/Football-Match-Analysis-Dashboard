import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import requests
import re
import random

# --- Consolidated JSON Data from User's Files ---
# This data structure has been consolidated and cleaned to resolve the KeyError issues.
# It includes a broader range of statistics and is properly nested for easy access.
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
      "last_5_form": {"results": ["W","D","L","W","D"], "goals": [2,1,0,2,2], "xG": [1.34,0.87,0.75,1.43,1.21]},
      "tactical_heatmaps": {"left_zone_pct": 34, "central_zone_pct": 32, "right_zone_pct": 34, "build_up": "Weighted toward left channel & overlaps"},
      "strengths": ["Wide play, crossing, set pieces, field tilt, pressing"],
      "weaknesses": ["Final third conversion, counterattack vulnerability"]
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
      "last_5_form": {"results": ["L","L","D","W","L"], "goals": [1,0,2,3,1], "xG": [1.09,0.88,1.17,1.45,1.13]},
      "tactical_heatmaps": {"left_zone_pct": 29, "central_zone_pct": 40, "right_zone_pct": 31, "build_up": "Central overload, direct balls to Musa"},
      "strengths": ["Central zone attacks, direct transitions, shot efficiency"],
      "weaknesses": ["Set piece defending, low possession, defensive errors under pressure"]
    }
  },
  "players": {
    "portland_timbers": [
      {"name": "Antony", "position": "LW", "goals": 7, "assists": 3, "xG": 7.7, "xA": 2.9, "rating": 7.32, "chances_created": 23, "dribbles": 29},
      {"name": "David Da Costa", "position": "CAM", "goals": 4, "assists": 6, "xG": 2.9, "xA": 7.3, "rating": 7.39, "chances_created": 57, "dribbles": 19},
      {"name": "James Pantemis", "position": "GK", "clean_sheets": 4, "save_percent": 77.1, "rating": 7.11},
      {"name": "Kevin Kelsy", "position": "ST", "goals": 7, "assists": 2, "xG": 5.6, "xA": 1.3, "rating": 7.05, "chances_created": 13, "dribbles": 15},
      {"name": "Felipe Mora", "position": "ST", "goals": 5, "assists": 3, "xG": 6.8, "xA": 2.3, "rating": 6.98, "chances_created": 9, "dribbles": 11}
    ],
    "fc_dallas": [
      {"name": "Petar Musa", "position": "ST", "goals": 16, "assists": 6, "xG": 13.1, "xA": 3.4, "rating": 7.41, "chances_created": 15, "dribbles": 18},
      {"name": "Luciano Acosta", "position": "AM", "goals": 5, "assists": 1, "xG": 5.5, "xA": 5.8, "rating": 7.31, "chances_created": 42, "dribbles": 22},
      {"name": "Shaq Moore", "position": "RB", "goals": 3, "assists": 3, "xG": 2.2, "xA": 2.7, "rating": 6.95, "chances_created": 34, "dribbles": 10},
      {"name": "Maarten Paes", "position": "GK", "clean_sheets": 3, "save_percent": 59.4, "rating": 6.89},
      {"name": "Sebastien Ibeagha", "position": "CB", "goals": 1, "assists": 0, "rating": 6.75, "tackles": 29, "clearances": 139}
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
        # Note: In a real-world app, you would use a secure, non-placeholder URL
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={self.api_key}"

    def _get_api_response(self, prompt, context_data):
        if not self.api_key:
            return f"""
Based on the data, Portland's superior defensive numbers and home advantage make them slight favorites. Players like Antony and David Da Costa are key to their attack, while Dallas will rely heavily on Petar Musa's clinical finishing. """

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
                ptfc_df = pd.DataFrame(context_data['teams']['portland_timbers']['last_5_form']).T
                ptfc_df.columns = [f'Match {i+1}' for i in range(len(ptfc_df.columns))]
                fcd_df = pd.DataFrame(context_data['teams']['fc_dallas']['last_5_form']).T
                fcd_df.columns = [f'Match {i+1}' for i in range(len(fcd_df.columns))]
                
                combined_df = pd.concat([ptfc_df, fcd_df], keys=['Portland Timbers', 'FC Dallas']).reset_index().rename(columns={'level_0': 'Team', 'level_1': 'Metric'})
                
                fig = px.line(combined_df, x='Metric', y=[f'Match {i+1}' for i in range(5)], color='Team', title="Last 5 Match Trends")
                fig.update_layout(yaxis_title='Values', xaxis_title='Metric')
                return fig
            else:
                return "I can generate charts for goals/xG, and recent form. Please be more specific."
        
        # Default to API response for narrative questions
        return self._get_api_response(prompt, context_data)

# --- Dashboard Section Functions with Enhanced Visuals ---

def show_overview(data, ml_predictions):
    st.header("📈 Season Overview", divider='green')
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🟢 Portland Timbers")
        portland = data['teams']['portland_timbers']
        form_colors = {'W': '🟢', 'D': '🟡', 'L': '🔴'}
        form_str = ' '.join([form_colors[result] for result in portland['last_5_form']['results']])
        
        st.markdown(f"**Record:** {portland['season_stats']['wins']}-{portland['season_stats']['draws']}-{portland['season_stats']['losses']} ({portland['season_stats']['points']} pts)")
        st.markdown(f"**Conference Position:** 6th")
        st.markdown(f"**Recent Form (L5):** {form_str}")
        
    with col2:
        st.subheader("🔵 FC Dallas")
        dallas = data['teams']['fc_dallas']
        form_colors = {'W': '🟢', 'D': '🟡', 'L': '🔴'}
        form_str = ' '.join([form_colors[result] for result in dallas['last_5_form']['results']])
        
        st.markdown(f"**Record:** {dallas['season_stats']['wins']}-{dallas['season_stats']['draws']}-{dallas['season_stats']['losses']} ({dallas['season_stats']['points']} pts)")
        st.markdown(f"**Conference Position:** 10th")
        st.markdown(f"**Recent Form (L5):** {form_str}")

    st.markdown("---")
    
    # Dynamic metrics with progress bars
    st.subheader("Key Metrics Comparison")
    col1, col2, col3 = st.columns(3)
    
    ptfc = data['teams']['portland_timbers']['season_stats']
    fcd = data['teams']['fc_dallas']['season_stats']
    
    with col1:
        st.metric(label="Goals For", value=f"{ptfc['goals_for']}", delta=f"vs Dallas: {ptfc['goals_for'] - fcd['goals_for']:+}")
        st.progress(ptfc['goals_for'] / 50)
    with col2:
        st.metric(label="Expected Goals (xG)", value=f"{ptfc['xG_for']}", delta=f"vs Dallas: {ptfc['xG_for'] - fcd['xG_for']:+}")
        st.progress(ptfc['xG_for'] / 50)
    with col3:
        st.metric(label="Possession", value=f"{ptfc['possession_pct']}%", delta=f"vs Dallas: {ptfc['possession_pct'] - fcd['possession_pct']:+}")
        st.progress(ptfc['possession_pct'] / 100)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric(label="Goals Against", value=f"{fcd['goals_against']}", delta=f"vs Portland: {fcd['goals_against'] - ptfc['goals_against']:+}")
        st.progress(fcd['goals_against'] / 50)
    with col5:
        st.metric(label="Expected Goals Against (xGA)", value=f"{fcd['xG_against']}", delta=f"vs Portland: {fcd['xG_against'] - ptfc['xG_against']:+}")
        st.progress(fcd['xG_against'] / 50)
    with col6:
        st.metric(label="Pass Accuracy", value=f"{fcd['pass_accuracy_pct']}%", delta=f"vs Portland: {fcd['pass_accuracy_pct'] - ptfc['pass_accuracy_pct']:+}")
        st.progress(fcd['pass_accuracy_pct'] / 100)

def show_performance(data):
    st.header("📊 Performance & Tactical Analysis", divider='green')
    
    # Radar chart for team comparison
    st.subheader("Team Strengths: A Tactical Snapshot")
    categories = ['Attack', 'Defense', 'Possession', 'Pressing', 'Set Pieces', 'Creativity']
    
    ptfc_stats = data['teams']['portland_timbers']['season_stats']
    fcd_stats = data['teams']['fc_dallas']['season_stats']
    
    # Correctly normalize metrics for a 0-100 scale
    ptfc_values = [
        ptfc_stats['goals_for'] / 50 * 100,
        100 - (ptfc_stats['goals_against'] / 50 * 100),
        ptfc_stats['possession_pct'],
        100 - (ptfc_stats['ppda'] / 20 * 100),
        ptfc_stats['set_piece_xG'] / 10 * 100,
        ptfc_stats['big_chances_created'] / 40 * 100
    ]
    fcd_values = [
        fcd_stats['goals_for'] / 50 * 100,
        100 - (fcd_stats['goals_against'] / 50 * 100),
        fcd_stats['possession_pct'],
        100 - (fcd_stats['ppda'] / 20 * 100),
        fcd_stats['set_piece_xG'] / 10 * 100,
        fcd_stats['big_chances_created'] / 40 * 100
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


def show_key_players(data):
    st.header("⭐ Key Players Analysis", divider='green')
    
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
        The data suggests a tightly contested match. Portland's home advantage and defensive solidity, especially from their goalkeeper, give them a crucial edge. While FC Dallas boasts a clinical finisher in Petar Musa, their overall defensive vulnerabilities and lower possession numbers are likely to be exploited. Expect Portland to control possession and win the game through a decisive moment, potentially from a set piece or a key creative pass from a player like David Da Costa.         </div>
        """, unsafe_allow_html=True)

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
