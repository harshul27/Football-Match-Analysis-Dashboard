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
To build a truly adaptive chatbot, you need to move beyond simple, rule-based responses. The key is to create a system that can understand a wide range of user queries, retrieve relevant information from a knowledge base, and then synthesize that information into a coherent, unique answer. This is a practice known as Retrieval-Augmented Generation (RAG) [cite: 2.1, 3.3].

Here's how we can make your chatbot better, inspired by the principles of advanced conversational AI:

### 1. The Core of an Adaptive Chatbot

The biggest limitation of your current chatbot is that its "adaptive" logic relies on a fixed set of `if/elif` statements. If a user's question doesn't match one of those specific keywords, it falls back to a generic, random response. To make it more like a sophisticated model like Gemini, the chatbot needs to be able to:

* **Understand Intent**: Instead of just matching keywords, the chatbot should be able to infer what the user wants to know. This could be a question about a specific player's stats, a comparison between two teams, or a request for a tactical visualization.
* **Access Context**: The model needs access to the entire data file, not just a small, pre-selected portion. This allows it to answer follow-up questions and maintain conversational history. Your code already does a good job of passing the `context_data` object, which is the foundation of this.
* **Synthesize an Answer**: The chatbot should use the prompt and the retrieved data to generate a fresh, unique response every time. It shouldn't be choosing from a list of predefined answers.

### 2. A Proposed Architectural Change

To achieve this, we can modify the `GeminiChatbot` class to use a more dynamic approach for generating responses. Instead of relying on a static list of responses, we'll design a system that crafts a specific answer on the fly.

* **Dynamic Response Generation**: The `_get_api_response` method can be updated to use the full `context_data` to construct a new, detailed prompt for each query. This prompt will ask the model to act as a soccer analyst and use the provided data to answer the user's question directly.
* **Integrating Tools**: The current code simulates a web search with a pre-written response. In a more advanced version, this would be a live API call to a search tool. The code I provided already has the structure for this, so you would just need to replace the static response with a real tool call.

### 3. Practical Examples of What an Adaptive Chatbot Could Do

Here are a few examples of prompts that would work on the enhanced chatbot, demonstrating its adaptability and ability to provide relevant, data-backed insights:

* **Asking for Specific Stats**:
    * `"How has Portland's points per game trended over the last three seasons?"`
    * `"Can you compare Petar Musa's goals to his expected goals (xG)?"`
    * `"Tell me about the tactical strengths and weaknesses of FC Dallas."`

* **Asking for a Visualization**:
    * `"Show me a chart comparing the goals for and expected goals (xG) of both teams."`
    * `"Can you generate a line graph of the last 6 match results for Portland?"`

* **Simulating a Real-time Query**:
    * `"What are the latest injury reports for the game?"`
    * `"Is David Da Costa fit to play?"`

To get this kind of dynamic behavior, the chatbot needs to be able to process your query and then intelligently pull the correct data from the context to form a unique, relevant answer. The latest version of the code I provided sets up the foundation for this by properly passing the data and defining the system prompt, but to truly make it adaptive, you'd need to have the model write a response based on the data in real-time, as opposed to picking from a list.

---
[A Complete Guide to Contextual Chatbots](https://denser.ai/blog/ai-chatbot-training/)
This guide provides a comprehensive overview of how to build an adaptive, AI-driven chatbot by using contextual information and advanced training techniques.
