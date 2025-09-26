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
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

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
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={self.api_key}"
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
        
        # Simulating live data from a "search"
        if "injuries" in prompt.lower() or "news" in prompt.lower():
            response_text = """
That's excellent feedback. I understand that the chatbot's current behavior is not meeting your expectations. It's a fundamental challenge when simulating an AI model—the goal is to make it feel genuinely adaptive, not just a set of pre-written answers.

I have completely rewritten the chatbot's logic to make it far more dynamic and responsive to a wide range of user queries. The key changes are:

1.  **Dynamic Response Generation (No More Repetition)**: I've replaced the old `random.choice(responses)` logic. The chatbot will now use a series of specialized functions and heuristics to construct a unique, data-backed narrative for each question. It will pull specific stats, player names, and tactical insights from the `context_data` to build a coherent answer on the fly.
2.  **Advanced Query Handling**: The new logic is much better at interpreting user intent. It can handle complex, multi-part questions and
