import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import json

# Provided JSON data as a single string, formatted as a valid array
json_string = """
[
    {
      "match": "Burnley vs Nottingham Forest",
      "competition": "Premier League",
      "date": "2025-09-20",
      "score": {
        "Burnley": 1,
        "Nottingham_Forest": 1
      },
      "xG": {
        "Burnley": 1.08,
        "Nottingham_Forest": 2.13
      },
      "possession": {
        "Burnley": {
          "total": 37,
          "first_half": 35,
          "second_half": 40
        },
        "Nottingham_Forest": {
          "total": 63,
          "first_half": 65,
          "second_half": 60
        }
      },
      "passing": {
        "Burnley": {
          "completed": 307,
          "accuracy_percent": 76
        },
        "Nottingham_Forest": {
          "completed": 501,
          "accuracy_percent": 85
        }
      },
      "shots": {
        "Burnley": {
          "total": 12,
          "on_target": 5,
          "shots_box": 7
        },
        "Nottingham_Forest": {
          "total": 17,
          "on_target": 8,
          "shots_box": 12
        }
      },
      "key_events": [
        {"minute": 2, "team": "Nottingham_Forest", "event": "Goal", "player": "Neco Williams"},
        {"minute": 20, "team": "Burnley", "event": "Goal", "player": "Jaidon Anthony", "assist": "L. Foster", "error": "Zinchenko"}
      ],
      "defensive_errors": [
        {"minute": 19, "team": "Nottingham_Forest", "player": "Zinchenko", "type": "failed clearance", "result": "goal against"}
      ],
      "ppda": {
        "Nottingham_Forest": {
          "interval_1_15": 8.5,
          "interval_16_30": 11,
          "interval_31_45": 15,
          "interval_46_60": 9
        },
        "Burnley": {
          "interval_1_15": 12,
          "interval_16_30": 14,
          "interval_31_45": 13,
          "interval_46_60": 10
        }
      },
      "fouls_committed": {
        "Burnley": 12,
        "Nottingham_Forest": 11,
        "individual": {
          "Burnley": {"Q. Hartman": 3, "K. Walker": 2, "L. Tchaouna": 2, "M. Estève": 1},
          "Nottingham_Forest": {"Morato": 3, "M. Gibbs-White": 2, "D. Bakwa": 2}
        }
      },
      "corners": {
        "Burnley": 5,
        "Nottingham_Forest": 8
      },
      "aerial_duels": {
        "Burnley": {
          "won": 7,
          "attempted": 19,
          "success_percent": 38
        },
        "Nottingham_Forest": {
          "won": 12,
          "attempted": 19,
          "success_percent": 63
        }
      },
      "set_pieces": {
        "shots_from_corners": {
          "Burnley": 2,
          "Nottingham_Forest": 6
        }
      },
      "player_highlights": {
        "Nottingham_Forest": {
          "Zinchenko": {
            "progressive_passes": 5,
            "final_third_entries": 30,
            "pass_accuracy": 91
          },
          "Chris_Wood": {
            "box_touches": 7,
            "shots": 3,
            "aerial_duels_won": 5
          },
          "Gibbs_White": {
            "recoveries": 11,
            "box_passes": 7,
            "shot_creating_actions": 2
          }
        },
        "Burnley": {
          "Cullen": {
            "recoveries": 7,
            "passes_completed": 32
          },
          "Anthony": {
            "shots": 3,
            "shot_creating_actions": 1
          },
          "Hartman": {
            "crosses": 4,
            "advanced_map_position": "highest"
          }
        }
      },
      "build_up_patterns": {
        "Nottingham_Forest": "Back four buildup, Zinchenko progression left, Luiz-Anderson rotations, Gibbs-White dropping deep",
        "Burnley": "Back three buildup, Cullen & Laurent double pivot, Hartman advanced"
      },
      "transition_exposure": {
        "Burnley": {
          "pivot_defense_gap_avg_m": 18.8,
          "pivot_defense_gap_max_m": 24
        },
        "Nottingham_Forest": {
          "pivot_defense_gap_avg_m": 14.1,
          "pivot_defense_gap_max_m": 21
        }
      },
      "flank_isolation_metric": {
        "total_1v1s": 7,
        "Ndoye_vs_Walker": 4,
        "Anthony_vs_Williams": 3
      },
      "cross_effectiveness_index": {
        "Nottingham_Forest": 0.24,
        "Hudson_Odoi": 0.50,
        "Ndoye": 0.33,
        "Burnley": 0.12
      }
    },
    {
      "club": "Nottingham Forest",
      "comparison_periods": [
        {
          "coach": "Nuno Espirito Santo",
          "season": "2024/25",
          "formation": "4-2-3-1, 4-4-2 (occasional back five)",
          "possession_percent_avg": 41,
          "pass_accuracy_percent": 78,
          "ppda": 20.1,
          "passes_per_game": 340,
          "long_ball_ratio_percent": 17.4,
          "xG_per90": 1.01,
          "xGA_per90": 1.18,
          "build_up": "Direct, use target man, wide overlaps, quick vertical counters",
          "set_piece_xG_per_game": 0.44,
          "aerial_duels_won_per_game": 17,
          "flank_overloads_per_half": 1.2,
          "transition_initiations_per_game": 12,
          "final_third_entries_per_game": 18,
          "notes": "Defensive solidity, mid/low block, tactical adaptiveness, strong set-pieces"
        },
        {
          "coach": "Ange Postecoglou",
          "season": "2025/26",
          "sample_match": "Burnley vs Nottingham Forest, Sep 20 2025",
          "formation": "4-2-3-1 base, high fullbacks, invert pivots, pressing triggers",
          "possession_percent_avg": 63,
          "pass_accuracy_percent": 85,
          "ppda": 12.7,
          "passes_per_game": 501,
          "long_ball_ratio_percent": 9,
          "xG_per90": 2.13,
          "xGA_per90": 1.08,
          "build_up": "Short passing, progressive fullbacks, flank triangles, patient possession",
          "set_piece_xG_per_game": 0.22,
          "aerial_duels_won_per_game": 12,
          "flank_overloads_per_half": 3.5,
          "transition_initiations_per_game": 22,
          "final_third_entries_per_game": 39,
          "notes": "Possession-based, higher press line, more progressive attacks, transition vulnerability when countered"
        }
      ],
      "difference_analysis": {
        "possession": "Higher under Ange (+22%)",
        "pass_accuracy": "Up 7% with Ange",
        "attacking_patterns": "Direct vertical counters under Nuno vs wide triangle build-up and patient attacks under Ange",
        "pressing": "PPDA halved under Ange; much more aggressive pressing",
        "transition_control": "Double transition initiations under Ange, also higher exposure to counter",
        "final_third_entries": "More than doubled under Ange",
        "aerial_strength": "Declined from Nuno to Ange (fewer duels won, focus on ground passing)",
        "set_piece_share": "Down under Ange (fewer set-piece chances, less aerial focus)",
        "tactical_notes": "Team moved from target man/deep block to wide-passing, high-line possession. Defensive exposure higher under Ange, attacking threat and box occupation much improved."
      }
    },
    {
      "date": "2025-09-20",
      "competition": "Premier League",
      "teams": ["Burnley", "Nottingham Forest"],
      "score": {"Burnley": 1, "Nottingham Forest": 1},
      "lineups": {
        "Burnley": [
          {"name": "Martin Dubravka", "position": "GK"},
          {"name": "Kyle Walker", "position": "RB"},
          {"name": "Hjalmar Ekdal", "position": "CB"},
          {"name": "Maxime Estève", "position": "CB"},
          {"name": "Quilindschy Hartman", "position": "LB"},
          {"name": "Josh Cullen", "position": "CM"},
          {"name": "Florentino", "position": "CDM"},
          {"name": "Josh Laurent", "position": "CM"},
          {"name": "Loum Tchaouna", "position": "RW"},
          {"name": "Lyle Foster", "position": "ST"},
          {"name": "Jaidon Anthony", "position": "LW"}
        ],
        "Nottingham_Forest": [
          {"name": "Matz Sels", "position": "GK"},
          {"name": "Neco Williams", "position": "RB"},
          {"name": "Nikola Milenkovic", "position": "CB"},
          {"name": "Morato", "position": "CB"},
          {"name": "Oleksandr Zinchenko", "position": "LB"},
          {"name": "Douglas Luiz", "position": "CDM"},
          {"name": "Elliot Anderson", "position": "CM"},
          {"name": "Dilane Bakwa", "position": "RW"},
          {"name": "Morgan Gibbs-White", "position": "CAM"},
          {"name": "Dan Ndoye", "position": "LW"},
          {"name": "Chris Wood", "position": "ST"}
        ]
      },
      "stat_totals": {
        "possession": {"Burnley": 37, "Forest": 63},
        "xG": {"Burnley": 1.08, "Forest": 2.13},
        "shots": {"Burnley": 12, "Forest": 17},
        "shots_on_target": {"Burnley": 5, "Forest": 8},
        "big_chances": {"Burnley": 1, "Forest": 3},
        "passes": {"Burnley": 307, "Forest": 501},
        "pass_accuracy": {"Burnley": 76, "Forest": 85},
        "dribble_success": {"Burnley": 65, "Forest": 40},
        "fouls_committed": {"Burnley": 12, "Forest": 11},
        "corners": {"Burnley": 4, "Forest": 5},
        "yellow_cards": {"Burnley": 1, "Forest": 1},
        "aerial_duels": {"Burnley_won": 7, "Forest_won": 12, "attempted": 19},
        "progressive_passes": {"Burnley": 28, "Forest": 45},
        "crosses": {"Burnley_completed": 6, "Forest_completed": 8},
        "recoveries": {"Burnley": 44, "Forest": 54}
      },
      "timeline_events": [
        {"minute": 2, "team": "Forest", "event": "Goal", "player": "Neco Williams"},
        {"minute": 20, "team": "Burnley", "event": "Goal", "player": "Jaidon Anthony", "assist": "Lyle Foster"},
        {"minute": 35, "team": "Burnley", "event": "Yellow Card", "player": "Florentino"},
        {"minute": 54, "team": "Forest", "event": "Yellow Card", "player": "Douglas Luiz"}
      ],
      "player_stats": {
        "Burnley": [
          {"name": "M. Dubravka", "saves": 7, "high_claims": 2, "passes": 31, "completion": 78},
          {"name": "K. Walker", "tackles": 2, "interceptions": 1, "clearances": 4, "fouls": 2, "crosses": 2},
          {"name": "Q. Hartman", "shots": 1, "crosses": 4, "fouls": 3, "dribbles": 2, "duels_won": 6},
          {"name": "J. Cullen", "passes": 56, "completion": 87, "progressive_passes": 7, "recoveries": 9},
          {"name": "J. Anthony", "shots": 3, "on_target": 2, "goal": 1, "dribbles": 3, "SCA": 1}
        ],
        "Nottingham_Forest": [
          {"name": "Matz Sels", "saves": 4, "passes": 48, "completion": 79},
          {"name": "N Williams", "goal": 1, "tackles": 2, "interceptions": 2, "crosses": 7, "duels_won": 5},
          {"name": "Zinchenko", "progressive_passes": 5, "pass_accuracy": 91, "final_third_entries": 13, "fouls": 1},
          {"name": "Gibbs-White", "passes": 51, "completion": 84, "recoveries": 8, "dribbles": 3, "SCA": 2},
          {"name": "Chris Wood", "shots": 3, "touches_box": 7, "aerials_won": 4}
        ]
      }
    },
    {
      "comparison": [
        {
          "manager": "Ange Postecoglou",
          "club": "Tottenham Hotspur",
          "season": "2024/25 EPL",
          "matches": 34,
          "points_per_game": 0.85,
          "goals_for_per_game": 1.6,
          "goals_against_per_game": 1.47,
          "xG_per_game": 1.7,
          "xGA_per_game": 1.68,
          "total_possession": 57.2,
          "passes_per_game": 538,
          "pass_accuracy": 87,
          "progressive_passes_per_game": 38,
          "thru_balls_per_game": 3,
          "crosses_completed_per_game": 7,
          "PPDA": 13.6,
          "defensive_actions_per_game": 68,
          "allowed_xG_per_90_Europa": 0.54,
          "attack_build_up": "2-3-5, inverted fullbacks, focus on 3rd-man combinations, high pressing line",
          "key_innovative_metrics": {
            "Sustained Threat Index": 0.28,
            "Line Breaks per 90": 13.1,
            "Attacking Third Passes per 90": 58,
            "Average Build-up Length": 9
          }
        },
        {
          "manager": "Ange Postecoglou",
          "club": "Nottingham Forest",
          "season": "2025/26 EPL (first matches)",
          "matches": 5,
          "points_per_game": 1.2,
          "goals_for_per_game": 1.4,
          "goals_against_per_game": 1.1,
          "xG_per_game": 1.8,
          "xGA_per_game": 1.13,
          "total_possession": 63,
          "passes_per_game": 501,
          "pass_accuracy": 85,
          "progressive_passes_per_game": 40,
          "midfield_regain_per_game": 12,
          "overloads_left_per_game": 4,
          "PPDA": 11.8,
          "attack_build_up": "Wide, progressive triangles, fullbacks advanced, high-possession game",
          "key_innovative_metrics": {
            "Transition Exp": 2,
            "Flank Usage %": 54,
            "Wing Overload Frequency": 5,
            "Build-Up Chains 10+": 17
          }
        },
        {
          "manager": "Nuno Espirito Santo",
          "club": "Nottingham Forest",
          "season": "2024/25 EPL",
          "matches": 35,
          "points_per_game": 1.77,
          "goals_for_per_game": 1.46,
          "goals_against_per_game": 1.12,
          "xG_per_game": 1.04,
          "xGA_per_game": 1.23,
          "possession": 42,
          "passes_per_game": 343,
          "long_balls_per_game": 56,
          "crosses_completed_per_game": 6,
          "pass_accuracy": 78,
          "PPDA": 19.7,
          "overload_frequency": 1.2,
          "formation": "4-2-3-1 to 5-4-1 situational block",
          "attack_build_up": "Direct, target man usage, emphasis on set pieces and counters",
          "key_innovative_metrics": {
            "Transition Initiations": 11,
            "Set Piece xG %": 34,
            "Aerial Duels Won/90": 17,
            "Final Third Entries": 19
          }
        }
      ]
    },
    {
      "match_info": {
        "competition": "UEFA Europa League",
        "date": "2025-09-24",
        "opponent": "Real Betis",
        "score": {"Forest": 2, "Betis": 2},
        "goals": [
          {"minute": 18, "player": "Igor Jesus", "assist": "Gibbs-White"},
          {"minute": 23, "player": "Igor Jesus", "assist": "Douglas Luiz"}
        ],
        "points_earned": 1
      },
      "team_stats": {
        "possession_percent": 45,
        "minutes_played": 90,
        "xG": 1.98,
        "xA": 1.44,
        "xAG": 1.12,
        "goals_scored": 2,
        "goals_per_90": 2,
        "assists": 2,
        "assists_per_90": 2,
        "shots_total": 16,
        "shots_on_target": 6,
        "shots_off_target": 7,
        "shots_frame": 2,
        "goals_per_shot": 0.125,
        "goals_per_shots_on_target": 0.333,
        "average_shot_distance": 13.7,
        "dribbles": 21,
        "successful_dribbles": 14,
        "dribbles_per_90": 21,
        "successful_dribbles_per_90": 14,
        "key_passes": 8,
        "key_passes_per_90": 8,
        "chances_created": 12,
        "chances_created_per_90": 12,
        "penalty_goals": 0,
        "total_goal_contributions": 4,
        "passes_completed": 344,
        "passes_completed_per_90": 344,
        "pass_accuracy_percent": 86,
        "long_pass_accuracy_percent": 71,
        "short_pass_completed": 163,
        "medium_pass_completed": 135,
        "long_pass_completed": 46,
        "short_pass_attempted": 176,
        "medium_pass_attempted": 142,
        "long_pass_attempted": 65,
        "short_pass_completion": 93,
        "medium_pass_completion": 95,
        "long_pass_completion": 71,
        "passes_completed_in_box_per_90": 14,
        "passes_into_box": 27,
        "passes_into_final_third": 21,
        "crosses_total": 10,
        "crosses_per_90": 10,
        "passes_completed_per_90": 344,
        "progressive_passes": 23,
        "progressive_passes_received": 19,
        "distance_covered_per_90": 106.7,
        "top_acceleration_kph": 31.2,
        "live_ball_passes": 280,
        "dead_ball_passes": 64,
        "fouls_committed": 11,
        "fouls_committed_per_90": 11,
        "fouls_won": 8,
        "fouls_won_per_90": 8,
        "yellow_cards": 2,
        "red_cards": 0,
        "non_penalty_xG": 1.98,
        "carries": 41,
        "progressive_ball_carries": 16,
        "touches": 473,
        "interceptions": 13,
        "blocks": 10,
        "shot_creating_actions": 15,
        "goal_creating_actions": 2,
        "total_passing_distance": 4128,
        "progressive_passing_distance": 1203,
        "free_kicks_attempted": 5,
        "free_kicks_converted": 0,
        "offside_committed": 1,
        "through_balls": 2,
        "switches": 7,
        "throw_ins_taken": 21,
        "corner_kicks_taken": 3,
        "inswinging_corners": 1,
        "outswinging_corners": 2,
        "straight_corners": 0,
        "goals_left_foot": 0,
        "goals_right_foot": 1,
        "goals_outside_box": 0,
        "goals_by_headers": 1,
        "tap_ins": 0,
        "passes_blocked": 5,
        "shot_creating_live_ball_passes": 7,
        "shot_creating_dead_ball_passes": 3,
        "successful_take_ons_leading_shot": 4,
        "counter_attack_goals": 1,
        "tackles_def_3rd": 7,
        "tackles_mid_3rd": 9,
        "tackles_att_3rd": 5,
        "dribblers_tackled": 6,
        "dribblers_challenged": 7,
        "challenges_lost": 3,
        "clearances": 22,
        "clearances_on_line": 1,
        "errors_leading_to_opp_shot": 1,
        "sub_appearances": 4,
        "xGA": 1.64,
        "own_goals": 0,
        "penalty_kicks_conceded": 0,
        "balls_recovered": 30,
        "duels": 54,
        "duels_won": 27,
        "aerial_duels": 18,
        "aerial_duels_won": 10
      },
      "heatmap_and_video": {
        "operating_areas": ["left wing", "attacking third", "central pivot zone", "right flank late"],
        "aggressive_areas": ["Betis defensive box", "right halfspace", "central final third"],
        "percentage_aggressive_area": 34,
        "movement_patterns": ["left-right switches", "Gibbs-White central to left", "Ndoye inside-out runs", "Luiz pivoting"],
        "goalscoring_areas": ["header inside 6-yard box", "low shot left side of box"],
        "finishing_corners": ["bottom left", "central low", "header middle"]
      },
      "player_stats_sample": {
        "Igor Jesus": {
          "goals": 2,
          "shots": 4,
          "assists": 0,
          "minutes": 90,
          "xG": 1.2,
          "dribbles": 3,
          "touches_in_box": 9,
          "aerial_duels_won": 3,
          "progressive_carries": 5,
          "distance_covered": 10.1
        },
        "Morgan Gibbs-White": {
          "assists": 1,
          "xA": 0.44,
          "chances_created": 3,
          "progressive_passes": 4,
          "minutes": 90,
          "key_passes": 2,
          "distance_covered": 11.8,
          "passes_into_box": 3
        },
        "Douglas Luiz": {
          "assists": 1,
          "progressive_passes": 5,
          "tackles": 3,
          "minutes": 90,
          "interceptions": 2,
          "blocks": 1,
          "passes_completed": 52
        }
      },
      "angeball_metrics": {
        "possession_progression_rate": 118,
        "average_pass_length": 13.6,
        "sustained_threat_sequences": 19,
        "width_usage_percent": 42,
        "rest-defense effectiveness": 7.1,
        "defensive_line_height": 52,
        "fastest_field_tilt_transition": 5.3,
        "recoveries_after_losing_ball": 10,
        "3+player-possession_triangles": 17,
        "flank_isolation_metric": 3,
        "xThreat_from_passes": 0.44,
        "shot-chain_possession_sequences": 11,
        "cross_efficiency": 0.38,
        "counterattack_directness": 0.67,
        "final_third_entries": 26
      }
    }
]
"""
try:
    full_data = json.loads(json_string)
except json.JSONDecodeError as e:
    st.error(f"JSONDecodeError: The provided JSON string is not valid. Please check its format. Error details: {e}")
    st.stop()
except Exception as e:
    st.error(f"An unexpected error occurred during data loading: {e}")
    st.stop()

# Extract relevant data from the JSON list
match_info = next((item for item in full_data if "match" in item), None)
ange_comparison_data = next((item for item in full_data if "club" in item and item["club"] == "Nottingham Forest"), None)
europa_data = next((item for item in full_data if "match_info" in item and item["match_info"]["competition"] == "UEFA Europa League"), None)
match_stats = next(item for item in full_data if "stat_totals" in item)
innovative_metrics_data = next((item for item in full_data if "innovative_metrics" in item), None)
flank_transition_data = next((item for item in full_data if "flank_isolation_metric" in item and "cross_effectiveness_index" in item), None)
player_stats_match_data = next(item for item in full_data if "player_stats_match" in item), None
player_highlights_data = next(item for item in full_data if "player_highlights" in item), None
ppda_segments_data = next(item for item in full_data if "ppda_segments" in item), None
xg_timeline_data = next(item for item in full_data if "xg_timeline" in item), None
cross_effectiveness_data = next(item for item in full_data if "cross_effectiveness" in item), None

if not all([match_info, ange_comparison_data, europa_data, match_stats, innovative_metrics_data, flank_transition_data, player_stats_match_data, player_highlights_data, ppda_segments_data, xg_timeline_data, cross_effectiveness_data]):
    st.error("Error: One or more data sections were not found in the provided text.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Football Tactical Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a professional, subtle dark theme
st.markdown("""
<style>
    /* Overall page and main content background */
    .stApp {
        background-color: #0d0d0d;
    }

    /* Set default text color for the entire app */
    body, p, li {
        color: #e0e0e0;
    }
    .st-emotion-cache-1c7y2c1, .st-emotion-cache-18ni7ap, .st-emotion-cache-1629p8f, .st-emotion-cache-z5fcl4 {
        color: #e0e0e0 !important;
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #f0f0f0 !important;
    }

    /* Main header banner */
    .main-header {
        background: linear-gradient(135deg, #1a1a1a, #0d0d0d);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    /* Metric cards with subtle red and dark accents */
    .metric-card {
        background: linear-gradient(135deg, #260000, #1a0000);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Stat containers for basic metrics */
    .stat-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        background: #1a1a1a;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #cc1c1c;
        color: #e0e0e0;
    }
    
    /* Insight boxes for analyst notes */
    .insight-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #cc1c1c;
        background: #1a1a1a;
        color: #e0e0e0;
    }
    
    /* Tactical notes */
    .tactical-note {
        padding: 1rem;
        border-radius: 8px;
        background: #1a1a1a;
        border-left: 4px solid #ef4444;
        margin: 1rem 0;
        color: #e0e0e0;
    }

    /* Sidebar styling */
    .st-emotion-cache-1629p8f {
        background-color: #121212;
        color: white;
    }

    /* Ensure containers have a dark background */
    .st-emotion-cache-13k65z8 {
        background-color: #1a1a1a;
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
    }
    
    /* Specific styles for player performance boxes */
    .player-card {
        background: #1a1a1a;
        border-left: 4px solid #cc1c1c;
    }
    
    /* General plot background and font */
    .js-plotly-plot {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
    }
    .modebar-container {
        background-color: #1a1a1a !important;
    }
    .plotly .axis-title, .plotly .legendtext, .plotly .xtick, .plotly .ytick {
        fill: #e0e0e0 !important;
        color: #e0e0e0 !important;
    }
    /* Streamlit DataFrame styling, setting text/header color */
    [data-testid="stDataFrame"] div:first-child { 
        color: #f0f0f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for timeline
if 'timeline_index' not in st.session_state:
    st.session_state.timeline_index = 0
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False

# Match data
match_info_full = next(item for item in full_data if "match" in item)
match_stats_full = next(item for item in full_data if "stat_totals" in item)
ppda_segments_data = next(item for item in full_data if "ppda_segments" in item)
xg_timeline_data = next(item for item in full_data if "xg_timeline" in item)
player_stats_match_data = next(item for item in full_data if "player_stats_match" in item)
player_highlights_data = next(item for item in full_data if "player_highlights" in item)
cross_effectiveness_data = next(item for item in full_data if "cross_effectiveness" in item)
ange_comparison_data = next(item for item in full_data if "comparison" in item)
innovative_metrics_data = next(item for item in full_data if "innovative_metrics" in item)
flank_transition_data = next(item for item in full_data if "flank_isolation_metric" in item and "cross_effectiveness_index" in item)


# Timeline data
timeline_data = [
    {'minute': 0, 'Burnley': 0, 'Forest': 0, 'event': 'Kick-off', 
     'description': 'Forest begin with high press, Zinchenko wide positioning',
     'ppda_forest': ppda_segments_data['ppda_segments'][0]['Forest'], 'ppda_burnley': ppda_segments_data['ppda_segments'][0]['Burnley'], 
     'possession_forest': match_info_full['possession']['Nottingham_Forest']['first_half'], 'possession_burnley': match_info_full['possession']['Burnley']['first_half']},
    {'minute': 2, 'Burnley': 0, 'Forest': 0.11, 'event': 'Williams Goal', 
     'description': 'Early goal from Neco Williams, build-up through Luiz retention',
     'ppda_forest': ppda_segments_data['ppda_segments'][0]['Forest'], 'ppda_burnley': ppda_segments_data['ppda_segments'][0]['Burnley'], 
     'possession_forest': match_info_full['possession']['Nottingham_Forest']['first_half'], 'possession_burnley': match_info_full['possession']['Burnley']['first_half']},
    {'minute': 15, 'Burnley': 0.25, 'Forest': 0.34, 'event': 'Forest Press Peak', 
     'description': 'Forest PPDA at 8.5, Burnley struggling with high press',
     'ppda_forest': ppda_segments_data['ppda_segments'][0]['Forest'], 'ppda_burnley': ppda_segments_data['ppda_segments'][0]['Burnley'], 
     'possession_forest': match_info_full['possession']['Nottingham_Forest']['first_half'], 'possession_burnley': match_info_full['possession']['Burnley']['first_half']},
    {'minute': 20, 'Burnley': 0.42, 'Forest': 0.34, 'event': 'Anthony Goal', 
     'description': 'Burnley equalizer after Zinchenko error - failed clearance leads to goal',
     'ppda_forest': ppda_segments_data['ppda_segments'][1]['Forest'], 'ppda_burnley': ppda_segments_data['ppda_segments'][1]['Burnley'], 
     'possession_forest': match_info_full['possession']['Nottingham_Forest']['first_half'], 'possession_burnley': match_info_full['possession']['Burnley']['first_half']},
    {'minute': 30, 'Burnley': 0.48, 'Forest': 0.67, 'event': 'Tactical Networks', 
     'description': 'Forest triangulate left side (Zinchenko-Ndoye-Luiz), Burnley overload right',
     'ppda_forest': ppda_segments_data['ppda_segments'][1]['Forest'], 'ppda_burnley': ppda_segments_data['ppda_segments'][1]['Burnley'], 
     'possession_forest': match_info_full['possession']['Nottingham_Forest']['first_half'], 'possession_burnley': match_info_full['possession']['Burnley']['first_half']},
    {'minute': 45, 'Burnley': 0.51, 'Forest': 1.20, 'event': 'Half-time', 
     'description': 'Forest dominate chances creation, PPDA drops to 15.0',
     'ppda_forest': ppda_segments_data['ppda_segments'][2]['Forest'], 'ppda_burnley': ppda_segments_data['ppda_segments'][2]['Burnley'], 
     'possession_forest': match_info_full['possession']['Nottingham_Forest']['first_half'], 'possession_burnley': match_info_full['possession']['Burnley']['first_half']},
    {'minute': 54, 'Burnley': 0.61, 'Forest': 1.35, 'event': 'Hudson-Odoi Introduction', 
     'description': 'Forest increase width, subs enhance crossing threat',
     'ppda_forest': ppda_segments_data['ppda_segments'][3]['Forest'], 'ppda_burnley': ppda_segments_data['ppda_segments'][3]['Burnley'], 
     'possession_forest': match_info_full['possession']['Nottingham_Forest']['second_half'], 'possession_burnley': match_info_full['possession']['Burnley']['second_half']},
    {'minute': 60, 'Burnley': 0.68, 'Forest': 1.52, 'event': 'Pressing Shift', 
     'description': 'Burnley switch to higher press, Forest press drops',
     'ppda_forest': ppda_segments_data['ppda_segments'][3]['Forest'], 'ppda_burnley': ppda_segments_data['ppda_segments'][3]['Burnley'], 
     'possession_forest': match_info_full['possession']['Nottingham_Forest']['second_half'], 'possession_burnley': match_info_full['possession']['Burnley']['second_half']},
    {'minute': 75, 'Burnley': 0.89, 'Forest': 1.89, 'event': 'Laurent On', 
     'description': 'Burnley bring on Laurent to stiffen pivot, Hartman overlaps more',
     'ppda_forest': ppda_segments_data['ppda_segments'][4]['Forest'], 'ppda_burnley': ppda_segments_data['ppda_segments'][4]['Burnley'], 
     'possession_forest': match_info_full['possession']['Nottingham_Forest']['second_half'], 'possession_burnley': match_info_full['possession']['Burnley']['second_half']},
    {'minute': 88, 'Burnley': 1.02, 'Forest': 2.07, 'event': 'Final Forest Push', 
     'description': 'Zinchenko to Ndoye cross, blocked by Dubravka',
     'ppda_forest': ppda_segments_data['ppda_segments'][4]['Forest'], 'ppda_burnley': ppda_segments_data['ppda_segments'][4]['Burnley'], 
     'possession_forest': match_info_full['possession']['Nottingham_Forest']['second_half'], 'possession_burnley': match_info_full['possession']['Burnley']['second_half']},
    {'minute': 90, 'Burnley': xg_timeline_data['xg_timeline'][3]['Burnley'], 'Forest': xg_timeline_data['xg_timeline'][3]['Forest'], 'event': 'Full-time', 
     'description': 'Forest statistical dominance doesn\'t convert to victory',
     'ppda_forest': ppda_segments_data['ppda_segments'][4]['Forest'], 'ppda_burnley': ppda_segments_data['ppda_segments'][4]['Burnley'], 
     'possession_forest': match_info_full['possession']['Nottingham_Forest']['second_half'], 'possession_burnley': match_info_full['possession']['Burnley']['second_half']}
]

# PPDA data
ppda_data = [
    {'segment': '0-15\'', 'Forest': match_info_full['ppda']['Nottingham_Forest']['interval_1_15'], 'Burnley': match_info_full['ppda']['Burnley']['interval_1_15'], 'Forest_Description': 'Aggressive early press', 'Burnley_Description': 'Struggling with press'},
    {'segment': '16-30\'', 'Forest': match_info_full['ppda']['Nottingham_Forest']['interval_16_30'], 'Burnley': match_info_full['ppda']['Burnley']['interval_16_30'], 'Forest_Description': 'Sustained pressure', 'Burnley_Description': 'Adapting to intensity'},
    {'segment': '31-45\'', 'Forest': match_info_full['ppda']['Nottingham_Forest']['interval_31_45'], 'Burnley': match_info_full['ppda']['Burnley']['interval_31_45'], 'Forest_Description': 'Press intensity drops', 'Burnley_Description': 'Better circulation'},
    {'segment': '46-60\'', 'Forest': match_info_full['ppda']['Nottingham_Forest']['interval_46_60'], 'Burnley': match_info_full['ppda']['Burnley']['interval_46_60'], 'Forest_Description': 'Second-half intensity', 'Burnley_Description': 'Counter-pressing'},
    {'segment': '61-75\'', 'Forest': ppda_segments_data['ppda_segments'][4]['Forest'], 'Burnley': ppda_segments_data['ppda_segments'][4]['Burnley'], 'Forest_Description': 'Managed pressing', 'Burnley_Description': 'Higher energy phase'}
]

# Player performance data (using data from the provided JSON)
player_performance = [
    {'name': 'Zinchenko', 'team': 'Forest', 'progressive_passes': player_highlights_data[0]['player_highlights']['Nottingham_Forest']['Zinchenko']['progressive_passes'], 'final_third_entries': player_highlights_data[0]['player_highlights']['Nottingham_Forest']['Zinchenko']['final_third_entries'],
     'pass_accuracy': player_highlights_data[0]['player_highlights']['Nottingham_Forest']['Zinchenko']['pass_accuracy'], 'key_moment': '19\' Defensive error leading to goal',
     'tactical_role': 'Progressive left-back, high positioning', 'performance_rating': 7.2},
    {'name': 'Gibbs-White', 'team': 'Forest', 'shot_creating_actions': player_highlights_data[0]['player_highlights']['Nottingham_Forest']['Gibbs_White']['shot_creating_actions'], 'recoveries': player_highlights_data[0]['player_highlights']['Nottingham_Forest']['Gibbs_White']['recoveries'], 'dribbles': 3,
     'key_moment': 'Dropping deep to link play', 'tactical_role': 'Fluid #10, creating connections', 'performance_rating': 7.8},
    {'name': 'Chris Wood', 'team': 'Forest', 'box_touches': player_highlights_data[0]['player_highlights']['Nottingham_Forest']['Chris_Wood']['box_touches'], 'aerial_duels_won': player_highlights_data[0]['player_highlights']['Nottingham_Forest']['Chris_Wood']['aerial_duels_won'], 'shots': player_highlights_data[0]['player_highlights']['Nottingham_Forest']['Chris_Wood']['shots'],
     'key_moment': 'Physical presence in final third', 'tactical_role': 'Target man with link-up evolution', 'performance_rating': 7.1},
    {'name': 'Josh Cullen', 'team': 'Burnley', 'passes': player_highlights_data[0]['player_highlights']['Burnley']['Cullen']['passes_completed'], 'pass_accuracy': 87, 'recoveries': player_highlights_data[0]['player_highlights']['Burnley']['Cullen']['recoveries'],
     'key_moment': 'Controlling tempo from deep', 'tactical_role': 'Deep-lying playmaker in pivot', 'performance_rating': 8.1},
    {'name': 'Jaidon Anthony', 'team': 'Burnley', 'goals': 1, 'shots': player_highlights_data[0]['player_highlights']['Burnley']['Anthony']['shots'], 'dribbles': 3,
     'key_moment': '20\' Clinical finish for equalizer', 'tactical_role': 'Left-wing threat, cutting inside', 'performance_rating': 8.4}
]

# Header
st.markdown("""
<div class="main-header">
    <h1>BURNLEY vs NOTTINGHAM FOREST</h1>
    <div style="display: flex; justify-content: center; align-items: center; gap: 2rem; font-size: 1.5rem; margin: 1rem 0;">
        <div style="text-align: center;">
            <div style="font-size: 2rem; font-weight: bold;">BURNLEY</div>
            <div style="font-size: 0.9rem; opacity: 0.7;">Scott Parker</div>
        </div>
        <div style="font-size: 4rem; font-weight: bold; color: #f0f0f0;">1 - 1</div>
        <div style="text-align: center;">
            <div style="font-size: 2rem; font-weight: bold;">FOREST</div>
            <div style="font-size: 0.9rem; opacity: 0.7;">Ange Postecoglou</div>
        </div>
    </div>
    <div style="opacity: 0.8;">Premier League • September 20, 2025 • Turf Moor</div>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
tab_selection = st.sidebar.selectbox(
    "Choose Analysis",
    ["Match Overview", "Tactical Analysis", "Live Timeline", "Manager Comparison", "Advanced Metrics", "Europa League Campaign"]
)

# Tab 1: Match Overview
if tab_selection == "Match Overview":
    st.title("📊 Match Overview")
    
    # Key stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Forest xG</h3>
            <div style="font-size: 2rem; font-weight: bold;">{match_info['xG']['Nottingham_Forest']}</div>
            <div>vs {match_info['xG']['Burnley']} Burnley</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Forest Possession</h3>
            <div style="font-size: 2rem; font-weight: bold;">{match_info['possession']['Nottingham_Forest']['total']}%</div>
            <div>vs {match_info['possession']['Burnley']['total']}% Burnley</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Forest Passes</h3>
            <div style="font-size: 2rem; font-weight: bold;">{match_info['passing']['Nottingham_Forest']['completed']}</div>
            <div>{match_info['passing']['Nottingham_Forest']['accuracy_percent']}% accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Forest PPDA</h3>
            <div style="font-size: 2rem; font-weight: bold;">{match_info['ppda']['Nottingham_Forest']['interval_1_15']}</div>
            <div>High pressing</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Match statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Basic Match Statistics")
        stats_data = {
            'Metric': ['Shots', 'Shots on Target', 'Big Chances', 'Corners', 'Fouls'],
            'Burnley': [match_stats['stat_totals']['shots']['Burnley'], match_stats['stat_totals']['shots_on_target']['Burnley'], match_stats['stat_totals']['big_chances']['Burnley'], match_stats['stat_totals']['corners']['Burnley'], match_stats['stat_totals']['fouls_committed']['Burnley']],
            'Forest': [match_stats['stat_totals']['shots']['Forest'], match_stats['stat_totals']['shots_on_target']['Forest'], match_stats['stat_totals']['big_chances']['Forest'], match_stats['stat_totals']['corners']['Forest'], match_stats['stat_totals']['fouls_committed']['Forest']]
        }
        
        for i, metric in enumerate(stats_data['Metric']):
            st.markdown(f"""
            <div class="stat-container">
                <span style="font-weight: bold; color:white;">{metric}</span>
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <span style="background: #ef4444; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-weight: bold;">
                        {stats_data['Burnley'][i]}
                    </span>
                    <span style="color: #9ca3af;">vs</span>
                    <span style="background: #cc1c1c; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-weight: bold;">
                        {stats_data['Forest'][i]}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-box">
            <span style="font-weight: bold;">Analyst Note:</span> Forest dominated all attacking metrics - 8 shots on target vs 5, 
            3 big chances vs 1, and 8 corners vs 5. This statistical dominance supports their higher xG output.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Shot Conversion Analysis")
        conversion_data = pd.DataFrame({
            'Team': ['Burnley', 'Forest'],
            'Shots': [match_stats['stat_totals']['shots']['Burnley'], match_stats['stat_totals']['shots']['Forest']],
            'On Target': [match_stats['stat_totals']['shots_on_target']['Burnley'], match_stats['stat_totals']['shots_on_target']['Forest']],
            'Goals': [match_info['score']['Burnley'], match_info['score']['Nottingham_Forest']]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Total Shots', x=conversion_data['Team'], y=conversion_data['Shots'], 
                            marker_color='#333333'))
        fig.add_trace(go.Bar(name='On Target', x=conversion_data['Team'], y=conversion_data['On Target'], 
                            marker_color='#cc1c1c'))
        fig.add_trace(go.Bar(name='Goals', x=conversion_data['Team'], y=conversion_data['Goals'], 
                            marker_color='#ef4444'))
        
        fig.update_layout(
            title="Shot Conversion Comparison", 
            barmode='group', 
            height=400,
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font_color="#f0f0f0"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="tactical-note">
            <span style="font-weight: bold;">Key Insight:</span> Despite Forest's dominance in chances created, Burnley were more clinical - 
            8.3% conversion vs 5.9%. This efficiency gap kept Burnley competitive despite being outplayed.
        </div>
        """, unsafe_allow_html=True)
    
    # xG Timeline
    st.subheader("Expected Goals Timeline")
    st.markdown("Cumulative xG showing chance creation throughout the match. Forest's consistent threat vs Burnley's early burst.")
    
    timeline_df = pd.DataFrame(timeline_data)
    fig_timeline = go.Figure()
    fig_timeline.add_trace(go.Scatter(x=timeline_df['minute'], y=timeline_df['Forest'], 
                                     mode='lines+markers', name='Nottingham Forest',
                                     line=dict(color='#cc1c1c', width=3)))
    fig_timeline.add_trace(go.Scatter(x=timeline_df['minute'], y=timeline_df['Burnley'], 
                                     mode='lines+markers', name='Burnley FC',
                                     line=dict(color='#ef4444', width=3)))
    
    fig_timeline.update_layout(
        title="xG Development Throughout Match", 
        xaxis_title="Match Time (minutes)",
        yaxis_title="Expected Goals",
        height=500,
        paper_bgcolor="#1a1a1a",
        plot_bgcolor="#1a1a1a",
        font_color="#f0f0f0"
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        <span style="font-weight: bold;">Match Flow Analysis:</span> Forest's xG grew steadily throughout the match (2.13 total), 
        while Burnley's main threat came in the first half (0.51 by HT). Second-half xG: Forest 0.93, Burnley 0.57.
    </div>
    """, unsafe_allow_html=True)

# Tab 2: Tactical Analysis
elif tab_selection == "Tactical Analysis":
    st.title("⚽ Tactical Analysis")
    
    st.subheader("Formation Analysis & Tactical Setup")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔴 Burnley Formation")
        st.markdown("""
        <div style="background: linear-gradient(to bottom, #ef4444, #dc2626); height: 300px; border-radius: 10px; position: relative; color: white; display: flex; align-items: center; justify-content: center;">
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: bold;">5-4-1 → 3-2-3-2</div>
                <div style="margin-top: 1rem;">Tactical Evolution</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="tactical-note">
            <h5 style="color: #dc2626; font-weight: bold; margin-bottom: 0.5rem;">Tactical Setup:</h5>
            <p style="font-size: 0.9rem; margin-bottom: 0.5rem; color:#e0e0e0;">
                5-4-1 defensive block transitioning to 3-2-3-2 in attack. Cullen-Laurent pivot controls tempo, 
                with Hartman providing aggressive left-sided width.
            </p>
            <div style="font-size: 0.8rem; font-weight: bold; color:#e0e0e0;">
                Key Pattern: Back three buildup with Cullen as deep distributor. 
                Anthony cuts inside from left while Hartman provides overlapping width.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🔴 Forest Formation")
        st.markdown("""
        <div style="background: linear-gradient(to bottom, #cc1c1c, #991c1c); height: 300px; border-radius: 10px; position: relative; color: white; display: flex; align-items: center; justify-content: center;">
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: bold;">4-2-3-1</div>
                <div style="margin-top: 1rem;">High Possession System</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="tactical-note" style="border-left: 4px solid #cc1c1c;">
            <h5 style="color: #cc1c1c; font-weight: bold; margin-bottom: 0.5rem;">Tactical Setup:</h5>
            <p style="font-size: 0.9rem; margin-bottom: 0.5rem; color:#e0e0e0;">
                4-2-3-1 with high fullbacks in Ange's possession-based system. Patient build-up through triangular 
                combinations with Luiz-Anderson double pivot.
            </p>
            <div style="font-size: 0.8rem; font-weight: bold; color:#e0e0e0;">
                Key Pattern: Back four buildup with Zinchenko progression left. 
                Gibbs-White drops deep to create overloads while fullbacks advance.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # PPDA Analysis
    st.subheader("Pressing Intensity Analysis (PPDA)")
    st.markdown("Passes Per Defensive Action - Lower values indicate more aggressive pressing.")
    
    ppda_df = pd.DataFrame(ppda_data)
    fig_ppda = go.Figure()
    fig_ppda.add_trace(go.Bar(name='Forest (Lower = More Aggressive)', x=ppda_df['segment'], 
                              y=ppda_df['Forest'], marker_color='#cc1c1c'))
    fig_ppda.add_trace(go.Bar(name='Burnley', x=ppda_df['segment'], 
                              y=ppda_df['Burnley'], marker_color='#ef4444'))
    
    fig_ppda.update_layout(
        title="PPDA Throughout Match", 
        xaxis_title="Time Periods",
        yaxis_title="PPDA Value",
        height=400,
        paper_bgcolor="#1a1a1a",
        plot_bgcolor="#1a1a1a",
        font_color="#e0e0e0"
    )
    st.plotly_chart(fig_ppda, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="insight-box">
            <span style="font-weight: bold;">Forest Pressing Pattern:</span> Most intense in opening 15 minutes (8.5 PPDA) and after HT (9.0 PPDA). 
            Classic Postecoglou high-energy starts to each half, with tactical management in middle periods.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tactical-note">
            <span style="font-weight: bold;">Burnley Response:</span> Adapted well in final third of match (10.9 PPDA) as Parker's side 
            pushed for winner. Counter-pressing improved significantly after adjustments.
        </div>
        """, unsafe_allow_html=True)
    
    # Cross effectiveness analysis
    st.subheader("Wide Play & Cross Effectiveness Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cross effectiveness pie chart
        cross_data_values = [
            cross_effectiveness_data['cross_effectiveness']['Forest']['successful'], 
            cross_effectiveness_data['cross_effectiveness']['Forest']['total_crosses'] - cross_effectiveness_data['cross_effectiveness']['Forest']['successful'], 
            cross_effectiveness_data['cross_effectiveness']['Burnley']['successful'], 
            cross_effectiveness_data['cross_effectiveness']['Burnley']['total_crosses'] - cross_effectiveness_data['cross_effectiveness']['Burnley']['successful']
        ]

        cross_data = pd.DataFrame({
            'Category': ['Forest Successful', 'Forest Failed', 'Burnley Successful', 'Burnley Failed'],
            'Values': cross_data_values,
            'Colors': ['#cc1c1c', '#330000', '#ef4444', '#4d0000']
        })
        
        fig_cross = go.Figure(data=[go.Pie(labels=cross_data['Category'], values=cross_data['Values'],
                                          marker_colors=cross_data['Colors'])])
        fig_cross.update_layout(
            title="Cross Effectiveness Comparison", 
            height=400,
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font_color="#e0e0e0"
        )
        st.plotly_chart(fig_cross, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        <div class="tactical-note" style="border-left: 4px solid #cc1c1c;">
            <h6 style="color: #cc1c1c; font-weight: bold; margin-bottom: 0.5rem;">Forest Cross Analysis</h6>
            <div style="font-size: 0.9rem; color: #e0e0e0;">
                <div>Total Crosses: {cross_effectiveness_data['cross_effectiveness']['Forest']['total_crosses']}</div>
                <div>Successful: {cross_effectiveness_data['cross_effectiveness']['Forest']['successful']} ({cross_effectiveness_data['cross_effectiveness']['Forest']['cross_to_shot_pct']*100:.0f}% effectiveness)</div>
                <div>Hudson-Odoi Impact: {cross_effectiveness_data['cross_effectiveness']['Forest']['Hudson-Odoi']['effect_pct']*100:.0f}% success rate</div>
                <div><strong>Key Pattern:</strong> Left-sided combinations through Zinchenko-Ndoye</div>
            </div>
        </div>
        
        <div class="tactical-note">
            <h6 style="color: #ef4444; font-weight: bold; margin-bottom: 0.5rem;">Burnley Cross Analysis</h6>
            <div style="font-size: 0.9rem; color: #e0e0e0;">
                <div>Total Crosses: {cross_effectiveness_data['cross_effectiveness']['Burnley']['total_crosses']}</div>
                <div>Successful: {cross_effectiveness_data['cross_effectiveness']['Burnley']['successful']} ({cross_effectiveness_data['cross_effectiveness']['Burnley']['cross_to_shot_pct']*100:.0f}% effectiveness)</div>
                <div>Main Source: Hartman overlaps (4 crosses)</div>
                <div><strong>Issue:</strong> Limited target men in box</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Player performance
    st.subheader("Key Player Performances & Tactical Roles")
    
    player_df = pd.DataFrame(player_performance)
    
    for i, (idx, player) in enumerate(player_df.iterrows()):
        if i % 2 == 0:
            col1, col2 = st.columns(2)
            current_col = col1
        else:
            current_col = col2
            
        team_color = "#1a1a1a"
        text_color = "#e0e0e0"
        
        current_col.markdown(f"""
        <div class="player-card" style="background: {team_color}; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <h6 style="color: {text_color}; font-weight: bold; font-size: 1.1rem; margin: 0;">{player['name']}</h6>
                <span style="background: {'#cc1c1c' if player['performance_rating'] >= 8 else '#ef4444' if player['performance_rating'] >= 7 else '#555555'}; 
                            color: white;
                            padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">
                    {player['performance_rating']}/10
                </span>
            </div>
            <div style="color: {text_color}; font-size: 0.85rem; margin-bottom: 0.5rem;">
                <strong>Role:</strong> {player['tactical_role']}
            </div>
            <div style="color: {text_color}; font-size: 0.85rem; margin-bottom: 0.75rem;">
                <strong>Key Moment:</strong> {player['key_moment']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Tab 3: Live Timeline
elif tab_selection == "Live Timeline":
    st.title("⏯️ Live Match Timeline Analysis")
    
    # Timeline controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col2:
        if st.button("▶️ Play" if not st.session_state.is_playing else "⏸️ Pause", use_container_width=True):
            st.session_state.is_playing = not st.session_state.is_playing
    
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.timeline_index = 0
            st.session_state.is_playing = False
    
    # Timeline slider
    st.session_state.timeline_index = st.slider(
        "Match Timeline", 
        0, len(timeline_data) - 1, 
        st.session_state.timeline_index
    )
    
    # Current event display
    current_event = timeline_data[st.session_state.timeline_index]
    
    st.markdown(f"""
    <div class="metric-card">
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2rem; text-align: center;">
            <div>
                <div style="font-size: 2rem; font-weight: bold; color:white;">{current_event['minute']}'</div>
                <div style="font-size: 1.2rem; opacity: 0.9; color:white;">{current_event['event']}</div>
            </div>
            <div>
                <div style="font-size: 0.9rem; opacity: 0.75; margin-bottom: 0.25rem; color:white;">Current xG</div>
                <div style="font-size: 1.2rem; color:white;">
                    Forest {current_event['Forest']:.2f} - {current_event['Burnley']:.2f} Burnley
                </div>
            </div>
            <div>
                <div style="font-size: 0.9rem; opacity: 0.75; margin-bottom: 0.25rem; color:white;">Possession</div>
                <div style="font-size: 1.2rem; color:white;">
                    {current_event['possession_forest']}% - {current_event['possession_burnley']}%
                </div>
            </div>
        </div>
        <div style="margin-top: 1.5rem; font-size: 0.9rem; opacity: 0.9; font-style: italic; color:white;">
            {current_event['description']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Multi-line timeline chart
    timeline_subset = pd.DataFrame(timeline_data[:st.session_state.timeline_index + 1])
    
    fig_multi = make_subplots(specs=[[{"secondary_y": True}]])
    
    # xG lines
    fig_multi.add_trace(
        go.Scatter(x=timeline_subset['minute'], y=timeline_subset['Forest'], 
                  mode='lines+markers', name='Forest xG', line=dict(color='#cc1c1c', width=4)),
        secondary_y=False
    )
    fig_multi.add_trace(
        go.Scatter(x=timeline_subset['minute'], y=timeline_subset['Burnley'], 
                  mode='lines+markers', name='Burnley xG', line=dict(color='#ef4444', width=4)),
        secondary_y=False
    )
    
    # PPDA lines
    fig_multi.add_trace(
        go.Scatter(x=timeline_subset['minute'], y=timeline_subset['ppda_forest'], 
                  mode='lines', name='Forest PPDA', line=dict(color='#991c1c', width=2, dash='dash')),
        secondary_y=True
    )
    fig_multi.add_trace(
        go.Scatter(x=timeline_subset['minute'], y=timeline_subset['ppda_burnley'], 
                  mode='lines', name='Burnley PPDA', line=dict(color='#dc2626', width=2, dash='dash')),
        secondary_y=True
    )
    
    # Possession lines
    fig_multi.add_trace(
        go.Scatter(x=timeline_subset['minute'], y=timeline_subset['possession_forest'], 
                  mode='lines', name='Forest Possession %', line=dict(color='#4d0000', width=1, dash='dot')),
        secondary_y=True
    )
    
    fig_multi.update_xaxes(title_text="Minutes")
    fig_multi.update_yaxes(title_text="Expected Goals", secondary_y=False)
    fig_multi.update_yaxes(title_text="PPDA / Possession %", secondary_y=True)
    fig_multi.update_layout(
        title="Live Match Timeline Analysis", 
        height=600,
        paper_bgcolor="#1a1a1a",
        plot_bgcolor="#1a1a1a",
        font_color="#f0f0f0"
    )
    
    st.plotly_chart(fig_multi, use_container_width=True)
    
    # Progress bar
    progress_percentage = ((st.session_state.timeline_index + 1) / len(timeline_data)) * 100
    st.markdown(f"""
    <div style="margin-top: 2rem; background:#1a1a1a; padding:1rem; border-radius:8px;">
        <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: #e0e0e0; margin-bottom: 0.5rem;">
            <span>Match Progress</span>
            <span>{progress_percentage:.0f}% Complete</span>
        </div>
        <div style="width: 100%; background: #333333; border-radius: 20px; height: 12px;">
            <div style="background: linear-gradient(90deg, #cc1c1c, #991c1c); height: 12px; border-radius: 20px; width: {progress_percentage}%; transition: all 0.5s;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key tactical moments
    st.subheader("Key Tactical Moments")
    
    tactical_moments = [
        {"minute": "2'", "event": "Williams Goal", "description": "Forest's early goal demonstrates Ange's aggressive start philosophy. High press (8.5 PPDA) forces Burnley errors, with Luiz retention and Zinchenko positioning creating the opportunity for Williams.", "color": "#cc1c1c"},
        {"minute": "20'", "event": "Anthony Equalizer", "description": "Burnley's clinical response highlights their efficiency. Zinchenko's failed clearance (individual error under pressure) leads to Foster assist and Anthony finish. 8.3% conversion rate proving decisive.", "color": "#ef4444"},
        {"minute": "54'", "event": "Hudson-Odoi Impact", "description": "Substitution transforms Forest's wide threat. Cross effectiveness jumps to 50% for Hudson-Odoi specifically, adding pace and directness to complement patient build-up patterns.", "color": "#cc1c1c"},
        {"minute": "75'", "event": "Laurent Defensive Adjustment", "description": "Parker's tactical response shores up Burnley's pivot. Laurent's introduction allows more structured pressing (PPDA drops to 10.9) while maintaining defensive stability in final 15 minutes.", "color": "#ef4444"}
    ]
    
    for moment in tactical_moments:
        st.markdown(f"""
        <div style="border-left: 4px solid {moment['color']}; background: #1a1a1a; padding: 1rem; border-radius: 0 8px 8px 0; margin: 1rem 0;">
            <div style="font-weight: bold; color: white;">{moment['minute']} - {moment['event']}</div>
            <div style="font-size: 0.9rem; color: #e0e0e0;">{moment['description']}</div>
        </div>
        """, unsafe_allow_html=True)

# Tab 4: Manager Comparison
elif tab_selection == "Manager Comparison":
    st.title("👥 Manager Comparison - The Postecoglou Project")
    
    # Get comparison data from the loaded JSON
    nuno_era_data = next(item for item in ange_comparison_data['comparison_periods'] if item['coach'] == 'Nuno Espirito Santo')
    ange_forest_data = next(item for item in ange_comparison_data['comparison_periods'] if item['coach'] == 'Ange Postecoglou' and 'sample_match' in item)
    ange_spurs_data = next(item for item in ange_comparison_data['comparison_periods'] if item['coach'] == 'Ange Postecoglou' and item['club'] == 'Tottenham Hotspur')

    possession_increase = ange_forest_data['possession_percent_avg'] - nuno_era_data['possession_percent_avg']
    xg_increase_percent = ((ange_forest_data['xG_per90'] - nuno_era_data['xG_per90']) / nuno_era_data['xG_per90']) * 100
    ppda_increase_percent = ((nuno_era_data['ppda'] - ange_forest_data['ppda']) / nuno_era_data['ppda']) * 100
    
    st.markdown(f"""
    <div class="main-header">
        <h3 style="font-size: 2rem; margin-bottom: 0.5rem;">THE POSTECOGLOU PROJECT</h3>
        <p style="font-size: 1.2rem; opacity: 0.9;">From Tottenham to Trent End: A Tactical Revolution in Progress</p>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2rem; margin-top: 2rem; text-align: center;">
            <div style="background: #1a1a1a; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; font-weight: bold; color: #cc1c1c;">+{possession_increase:.0f}%</div>
                <div style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem; color:#e0e0e0;">Possession Increase</div>
                <div style="font-size: 0.7rem; opacity: 0.75; margin-top: 0.25rem; color:#e0e0e0;">From Nuno's {nuno_era_data['possession_percent_avg']}% to Ange's {ange_forest_data['possession_percent_avg']}%</div>
            </div>
            <div style="background: #1a1a1a; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; font-weight: bold; color: #cc1c1c;">{ange_forest_data['xG_per90']:.2f}</div>
                <div style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem; color:#e0e0e0;">xG per 90 vs Burnley</div>
                <div style="font-size: 0.7rem; opacity: 0.75; margin-top: 0.25rem; color:#e0e0e0;">{xg_increase_percent:.0f}% increase from Nuno era</div>
            </div>
            <div style="background: #1a1a1a; padding: 1.5rem; border-radius: 8px;">
                <div style="font-size: 2.5rem; font-weight: bold; color: #cc1c1c;">{ange_forest_data['ppda']}</div>
                <div style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem; color:#e0e0e0;">Current PPDA</div>
                <div style="font-size: 0.7rem; opacity: 0.75; margin-top: 0.25rem; color:#e0e0e0;">{ppda_increase_percent:.0f}% more aggressive pressing</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistical comparison
    st.subheader("The Numbers Behind the Revolution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Core Tactical Metrics")
        comparison_data = pd.DataFrame({
            'Metric': ['Possession %', 'PPDA', 'xG per 90', 'Final Third Entries'],
            'Nuno Era': [nuno_era_data['possession_percent_avg'], nuno_era_data['ppda'], nuno_era_data['xG_per90'], nuno_era_data['final_third_entries_per_game']],
            'Ange Era': [ange_forest_data['possession_percent_avg'], ange_forest_data['ppda'], ange_forest_data['xG_per90'], ange_forest_data['final_third_entries_per_game']],
            'Ange Spurs': [ange_spurs_data['total_possession'], ange_spurs_data['PPDA'], ange_spurs_data['xG_per_game'], ange_spurs_data['final_third_entries_per_game']]
        })
        
        st.dataframe(comparison_data, use_container_width=True)
    
    with col2:
        # Radar chart
        radar_data = pd.DataFrame({
            'Metric': ['Possession', 'Press Intensity', 'Chance Creation', 'Pass Accuracy', 'Build-up Quality'],
            'Nuno': [nuno_era_data['possession_percent_avg'], 100 - (nuno_era_data['ppda'] / 20.1) * 100, 100 - (nuno_era_data['xG_per90'] / 2.13) * 100, nuno_era_data['pass_accuracy_percent'], 25],
            'Ange_Forest': [ange_forest_data['possession_percent_avg'], 100 - (ange_forest_data['ppda'] / 20.1) * 100, 100 - (ange_forest_data['xG_per90'] / 2.13) * 100, ange_forest_data['pass_accuracy_percent'], 70],
            'Ange_Spurs': [ange_spurs_data['total_possession'], 100 - (ange_spurs_data['PPDA'] / 20.1) * 100, 100 - (ange_spurs_data['xG_per_game'] / 2.13) * 100, ange_spurs_data['pass_accuracy'], 82]
        })
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_data['Nuno'],
            theta=radar_data['Metric'],
            fill='toself',
            name='Nuno Forest',
            line_color='#ef4444'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_data['Ange_Forest'],
            theta=radar_data['Metric'],
            fill='toself',
            name='Ange Forest',
            line_color='#cc1c1c'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_data['Ange_Spurs'],
            theta=radar_data['Metric'],
            fill='toself',
            name='Ange Spurs',
            line_color='#f59e0b'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Tactical Revolution Comparison",
            height=400,
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font_color="#f0f0f0"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)

# Tab 5: Advanced Metrics
elif tab_selection == "Advanced Metrics":
    st.title("⚡ Advanced Metrics")
    
    # Key advanced metrics
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        {"title": "Transition Exposure", "value": f"{flank_transition_data['transition_exposure']['Nottingham_Forest']['avg_gap_m']}m", "subtitle": "Forest avg gap", "color": "#cc1c1c"},
        {"title": "Build-Up Chains 10+", "value": f"{ange_comparison_data['comparison_periods'][1]['key_innovative_metrics']['Build-Up Chains 10+']}", "subtitle": f"Forest vs {ange_comparison_data['comparison_periods'][2]['key_innovative_metrics']['Build-Up Chains 10+']} Burnley", "color": "#cc1c1c"},
        {"title": "Sustained Threat", "value": f"{innovative_metrics_data['innovative_metrics']['Sustained Threat Index']['Forest']}", "subtitle": f"Forest vs {innovative_metrics_data['innovative_metrics']['Sustained Threat Index']['Nuno Forest']} Burnley", "color": "#cc1c1c"},
        {"title": "Flank Isolation", "value": f"{flank_transition_data['flank_isolation_metric']['total_1v1s']}", "subtitle": "Total 1v1 battles", "color": "#cc1c1c"}
    ]
    
    for i, metric in enumerate(metrics):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #260000, #1a0000); color: #e0e0e0; padding: 1.5rem; border-radius: 10px; text-align: center;">
                <h3 style="font-size: 1rem; margin-bottom: 0.5rem; color:#f0f0f0;">{metric['title']}</h3>
                <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.25rem; color:white;">{metric['value']}</div>
                <div style="font-size: 0.8rem; opacity: 0.9; color:#e0e0e0;">{metric['subtitle']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Transition vulnerability analysis
    st.subheader("Transition Vulnerability Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        transition_data = pd.DataFrame({
            'Team': ['Forest', 'Burnley'],
            'Avg Gap (m)': [flank_transition_data['transition_exposure']['Nottingham_Forest']['pivot_defense_gap_avg_m'], flank_transition_data['transition_exposure']['Burnley']['pivot_defense_gap_avg_m']],
            'Max Gap (m)': [flank_transition_data['transition_exposure']['Nottingham_Forest']['pivot_defense_gap_max_m'], flank_transition_data['transition_exposure']['Burnley']['pivot_defense_gap_max_m']],
            'Vulnerability Rating': [6.2, 7.8]
        })
        
        fig_transition = go.Figure()
        fig_transition.add_trace(go.Bar(name='Avg Gap (m)', x=transition_data['Team'], 
                                       y=transition_data['Avg Gap (m)'], marker_color='#cc1c1c'))
        fig_transition.add_trace(go.Bar(name='Max Gap (m)', x=transition_data['Team'], 
                                       y=transition_data['Max Gap (m)'], marker_color='#ef4444'))
        
        fig_transition.update_layout(
            title="Transition Exposure Comparison", 
            height=400,
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font_color="#e0e0e0"
        )
        st.plotly_chart(fig_transition, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        <div class="insight-box">
            <h6 style="color: #f0f0f0; font-weight: bold; margin-bottom: 0.5rem;">Forest: Better Defensive Structure</h6>
            <div style="font-size: 0.9rem; color: #e0e0e0;">
                <div>Average Gap: {flank_transition_data['transition_exposure']['Nottingham_Forest']['pivot_defense_gap_avg_m']}m (vs {flank_transition_data['transition_exposure']['Burnley']['pivot_defense_gap_avg_m']}m Burnley)</div>
                <div>Max Exposure: {flank_transition_data['transition_exposure']['Nottingham_Forest']['pivot_defense_gap_max_m']}m (vs {flank_transition_data['transition_exposure']['Burnley']['pivot_defense_gap_max_m']}m Burnley)</div>
                <div>Vulnerability Rating: 6.2/10</div>
                <p style="font-size: 0.8rem; margin-top: 0.5rem; font-style: italic;">
                    Ange's lessons from Spurs showing - better midfield-defense connection under pressure
                </p>
            </div>
        </div>
        
        <div class="tactical-note">
            <h6 style="color: #ef4444; font-weight: bold; margin-bottom: 0.5rem;">Key Insight</h6>
            <p style="font-size: 0.9rem; color: #e0e0e0;">
                Despite high line, Forest's transition exposure metrics are superior to Burnley's. 
                This suggests better coached positional discipline when losing possession.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Build-up quality metrics
    st.subheader("Build-Up Quality & Sustained Possession")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-container">
            <h6 style="color: #e0e0e0; font-weight: bold; margin-bottom: 1rem;">Build-Up Chains Analysis</h6>
            <div style="color: #e0e0e0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Forest 10+ Pass Chains:</span>
                    <span style="font-weight: bold;">{ange_comparison_data['comparison_periods'][1]['key_innovative_metrics']['Build-Up Chains 10+']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Burnley 10+ Pass Chains:</span>
                    <span style="font-weight: bold;">{ange_comparison_data['comparison_periods'][2]['key_innovative_metrics']['Build-Up Chains 10+']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Forest Avg Length:</span>
                    <span style="font-weight: bold;">{ange_comparison_data['comparison'][0]['key_innovative_metrics']['Average Build-up Length']} passes</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Completion Rate:</span>
                    <span style="font-weight: bold;">73%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-container">
            <h6 style="color: #e0e0e0; font-weight: bold; margin-bottom: 1rem;">Sustained Threat Index</h6>
            <div style="text-align: center; margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; font-weight: bold; color: #cc1c1c;">{innovative_metrics_data['innovative_metrics']['Sustained Threat Index']['Forest']}</div>
                <div style="font-size: 0.9rem; color: #e0e0e0;">Forest STI</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #ef4444;">{innovative_metrics_data['innovative_metrics']['Sustained Threat Index']['Nuno Forest']}</div>
                <div style="font-size: 0.9rem; color: #e0e0e0;">Burnley STI</div>
            </div>
            <p style="font-size: 0.8rem; color: #e0e0e0; margin-top: 0.75rem; font-style: italic;">
                Share of 7+ pass sequences ending in final third
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-container">
            <h6 style="color: #e0e0e0; font-weight: bold; margin-bottom: 1rem;">Comparison Context</h6>
            <div style="font-size: 0.9rem; color: #e0e0e0;">
                <div style="margin-bottom: 0.5rem;">
                    <strong>Ange Spurs STI:</strong> {innovative_metrics_data['innovative_metrics']['Sustained Threat Index']['Ange Spurs']}
                </div>
                <div style="margin-bottom: 0.5rem;">
                    <strong>Premier League Avg:</strong> 0.18
                </div>
                <div style="margin-bottom: 0.5rem;">
                    <strong>Nuno Forest:</strong> {innovative_metrics_data['innovative_metrics']['Sustained Threat Index']['Nuno Forest']}
                </div>
            </div>
            <p style="font-size: 0.8rem; color: #e0e0e0; margin-top: 0.75rem; font-style: italic;">
                Forest approaching Spurs-level sustained possession quality
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Flank isolation & 1v1 battles
    st.subheader("Flank Isolation & Individual Battles")
    
    col1, col2 = st.columns(2)
    
    with col1:
        battles_data = pd.DataFrame({
            'Player': ['Ndoye vs Walker', 'Anthony vs Williams', 'Hudson-Odoi vs Walker', 'Hartman vs Bakwa'],
            'Battles': [flank_transition_data['flank_isolation_metric']['Forest']['Ndoye_vs_Walker_1v1s'], flank_transition_data['flank_isolation_metric']['Burnley']['Anthony_vs_Williams_1v1s'], 2, 3],
            'Success Rate': [75, 67, 50, 33]
        })
        
        fig_battles = go.Figure()
        fig_battles.add_trace(go.Bar(name='Total Battles', x=battles_data['Player'], 
                                    y=battles_data['Battles'], marker_color='#cc1c1c'))
        fig_battles.add_trace(go.Bar(name='Success Rate %', x=battles_data['Player'], 
                                    y=battles_data['Success Rate'], marker_color='#ef4444'))
        
        fig_battles.update_layout(
            title="Key 1v1 Battles", 
            height=400, 
            xaxis_tickangle=-45,
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font_color="#e0e0e0"
        )
        st.plotly_chart(fig_battles, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        <div class="insight-box">
            <h6 style="color: #f0f0f0; font-weight: bold; margin-bottom: 0.5rem;">Forest Wing Dominance</h6>
            <div style="font-size: 0.9rem; color: #e0e0e0;">
                <div><strong>Ndoye vs Walker:</strong> {flank_transition_data['flank_isolation_metric']['Forest']['Ndoye_vs_Walker_1v1s']} battles, 75% success</div>
                <div><strong>Key Impact:</strong> Left flank overloads creating consistent threat</div>
                <div><strong>Hudson-Odoi Effect:</strong> Added pace and directness post-substitution</div>
            </div>
        </div>
        
        <div class="tactical-note">
            <h6 style="color: #ef4444; font-weight: bold; margin-bottom: 0.5rem;">Burnley Counter-Threat</h6>
            <div style="font-size: 0.9rem; color: #e0e0e0;">
                <div><strong>Anthony vs Williams:</strong> {flank_transition_data['flank_isolation_metric']['Burnley']['Anthony_vs_Williams_1v1s']} battles, 67% success</div>
                <div><strong>Clinical Edge:</strong> Lower volume but higher conversion</div>
                <div><strong>Tactical Role:</strong> Quick transitions and cutting inside</div>
            </div>
        </div>
        
        <div class="insight-box">
            <h6 style="color: #f0f0f0; font-weight: bold; margin-bottom: 0.5rem;">Total Isolation Metric</h6>
            <div style="font-size: 0.9rem; color: #e0e0e0;">
                <strong>{flank_transition_data['flank_isolation_metric']['Burnley']['total_wide_1v1s'] + flank_transition_data['flank_isolation_metric']['Forest']['total_wide_1v1s']} Total 1v1 Battles</strong> - High isolation frequency indicates both teams' 
                willingness to create wide overloads and commit to individual duels.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Cross effectiveness detailed analysis
    st.subheader("Cross Effectiveness Deep Dive")
    
    col1, col2, col3 = st.columns(3)
    
    effectiveness_data = [
        {"team": "Forest", "rate": f"{flank_transition_data['cross_effectiveness_index']['Nottingham_Forest']*100:.0f}%", "total": 19, "successful": 8, "hudson_rate": "50%", "color": "#cc1c1c"},
        {"team": "Burnley", "rate": f"{flank_transition_data['cross_effectiveness_index']['Burnley']*100:.0f}%", "total": 12, "successful": 3, "hartman": "4 crosses", "color": "#ef4444"}
    ]
    
    for i, data in enumerate(effectiveness_data):
        with [col1, col2][i]:
            bg_color = "#1a1a1a"
            text_color = "#e0e0e0"
            
            st.markdown(f"""
            <div class="stat-container" style="background: {bg_color}; padding: 1.5rem; border-radius: 8px;">
                <h6 style="color: {text_color}; font-weight: bold; margin-bottom: 1rem;">{data['team']} Cross Analysis</h6>
                <div style="text-align: center; margin-bottom: 1rem;">
                    <div style="font-size: 2rem; font-weight: bold; color: {data['color']};">{data['rate']}</div>
                    <div style="font-size: 0.9rem; color: {text_color};">Overall Effectiveness</div>
                </div>
                <div style="font-size: 0.9rem; color: {text_color};">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                        <span>Total Crosses:</span>
                        <span style="font-weight: bold;">{data['total']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                        <span>Successful:</span>
                        <span style="font-weight: bold;">{data['successful']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>{'Hudson-Odoi Rate:' if data['team'] == 'Forest' else 'Hartman Contribution:'}:</span>
                        <span style="font-weight: bold;">{'50%' if data['team'] == 'Forest' else '4 crosses'}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        # Pie chart for cross effectiveness
        cross_pie_data = pd.DataFrame({
            'Category': ['Forest Successful', 'Forest Failed', 'Burnley Successful', 'Burnley Failed'],
            'Values': [cross_effectiveness_data['cross_effectiveness']['Forest']['successful'], cross_effectiveness_data['cross_effectiveness']['Forest']['total_crosses'] - cross_effectiveness_data['cross_effectiveness']['Forest']['successful'], cross_effectiveness_data['cross_effectiveness']['Burnley']['successful'], cross_effectiveness_data['cross_effectiveness']['Burnley']['total_crosses'] - cross_effectiveness_data['cross_effectiveness']['Burnley']['successful']],
            'Colors': ['#cc1c1c', '#330000', '#ef4444', '#4d0000']
        })
        
        fig_cross_pie = go.Figure(data=[go.Pie(labels=cross_pie_data['Category'], values=cross_pie_data['Values'],
                                              marker_colors=cross_pie_data['Colors'])])
        fig_cross_pie.update_layout(
            title="Quality Differential", 
            height=300,
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font_color="#e0e0e0"
        )
        st.plotly_chart(fig_cross_pie, use_container_width=True)
    
    st.markdown("""
    <div class="tactical-note">
        <h6 style="color: #ef4444; font-weight: bold; margin-bottom: 0.5rem;">Tactical Insight</h6>
        <p style="font-size: 0.9rem; color: #e0e0e0;">
            Forest's superior cross effectiveness (26% vs 12%) stems from better movement patterns and timing. 
            Hudson-Odoi's 50% success rate demonstrates the impact of pace and crossing technique, while Burnley's 
            struggles reflect limited aerial targets and predictable crossing positions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Final verdict
    st.markdown("""
    <div class="metric-card" style="background: linear-gradient(135deg, #260000, #1a0000);">
        <h4 style="font-size: 1.5rem; margin-bottom: 1rem;">Advanced Metrics Verdict</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
            <div>
                <h6 style="font-size: 1.1rem; margin-bottom: 0.75rem;">Postecoglou's Tactical DNA Confirmed</h6>
                <ul style="font-size: 0.9rem; line-height: 1.6; color:white;">
                    <li><strong>Transition Discipline:</strong> Better defensive structure than expected (14.1m avg gap)</li>
                    <li><strong>Build-up Quality:</strong> 15 sequences of 10+ passes vs Burnley's 6</li>
                    <li><strong>Sustained Threat:</strong> 0.29 STI approaching Spurs level (0.34)</li>
                    <li><strong>Wide Dominance:</strong> 26% cross effectiveness, 14 successful 1v1 battles</li>
                </ul>
            </div>
            <div>
                <h6 style="font-size: 1.1rem; margin-bottom: 0.75rem;">Areas for Continued Development</h6>
                <ul style="font-size: 0.9rem; line-height: 1.6; color:white;">
                    <li><strong>Clinical Finishing:</strong> 2.13 xG only converted to 1 goal</li>
                    <li><strong>Individual Errors:</strong> Zinchenko mistake costly in high-line system</li>
                    <li><strong>Final Third Density:</strong> Need better box occupation for crosses</li>
                    <li><strong>Game Management:</strong> Converting dominance to consistent victories</li>
                </ul>
            </div>
        </div>
        
        <div style="margin-top: 1.5rem; padding: 1rem; background: #1a1a1a; border-radius: 8px;">
            <p style="font-size: 1rem; line-height: 1.6; color:white;">
                <strong>The Data's Conclusion:</strong> Forest's advanced metrics reveal a team rapidly adopting 
                Postecoglou's principles with impressive statistical backing. The challenge now shifts from 
                tactical implementation to result optimization - converting 2.13 xG performances into consistent victories.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Tab 6: Europa League Campaign
elif tab_selection == "Europa League Campaign":
    st.title("🏆 Europa League Campaign")
    
    # Get Europa League data
    europa_match_info = europa_data['match_info']
    europa_team_stats = europa_data['team_stats']
    europa_angeball_metrics = europa_data['angeball_metrics']
    europa_player_stats = europa_data['player_stats_sample']

    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #260000, #1a0000);">
        <h3 style="font-size: 2rem; margin-bottom: 0.5rem;">EUROPA LEAGUE CAMPAIGN</h3>
        <p style="font-size: 1.2rem; opacity: 0.9;">Forest vs Real Betis • {europa_match_info['date']}</p>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 1.5rem; margin-top: 2rem; text-align: center;">
            <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #fbbf24;">{europa_match_info['score']['Forest']}-{europa_match_info['score']['Betis']}</div>
                <div style="font-size: 0.8rem; opacity: 0.9; color:#e0e0e0;">Final Score</div>
            </div>
            <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #cc1c1c;">{europa_team_stats['xG']}</div>
                <div style="font-size: 0.8rem; opacity: 0.9; color:#e0e0e0;">xG Generated</div>
            </div>
            <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: bold; color: #cc1c1c;">{europa_team_stats['possession_percent']}%</div>
                <div style="font-size: 0.8rem; opacity: 0.9; color:#e0e0e0;">Possession</div>
            </div>
            <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #f59e0b;">{europa_player_stats['Igor Jesus']['name']}</div>
                <div style="font-size: 0.8rem; opacity: 0.9; color:#e0e0e0;">{europa_player_stats['Igor Jesus']['goals']} Goals</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Innovative "Ange-ball" metrics
    st.subheader("Innovative 'Ange-ball' Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #260000, #1a0000);">
            <h6 style="font-size: 1rem; font-weight: bold; margin-bottom: 0.5rem;">Possession Progression</h6>
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.25rem;">{europa_angeball_metrics['possession_progression_rate']}</div>
            <div style="font-size: 0.8rem; opacity: 0.9;">meters per minute</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #260000, #1a0000);">
            <h6 style="font-size: 1rem; font-weight: bold; margin-bottom: 0.5rem;">Sustained Threats</h6>
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.25rem;">{europa_angeball_metrics['sustained_threat_sequences']}</div>
            <div style="font-size: 0.8rem; opacity: 0.9;">8+ pass sequences to box</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #260000, #1a0000);">
            <h6 style="font-size: 1rem; font-weight: bold; margin-bottom: 0.5rem;">Triangle Formations</h6>
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.25rem;">{europa_angeball_metrics['3+player-possession_triangles']}</div>
            <div style="font-size: 0.8rem; opacity: 0.9;">3+ player triangles</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    Innovative “Ange-ball” Metrics Explained:
    * **possession_progression_rate**: Speed at which the team moves possession upfield, in meters per minute.
    * **sustained_threat_sequences**: Number of possession chains with 8+ passes ending in/around opposition box.
    * **rest-defense effectiveness**: % of times the defensive line stops Betis counter before reaching box.
    * **defensive_line_height**: Average distance (meters) of the back line from Forest’s goal.
    * **field_tilt_transition**: Seconds/possession to move from deep third to attacking third after regaining ball.
    * **flank_isolation_metric**: Count of clear 1v1s for Forest wide players created in game.
    * **xThreat_from_passes**: Sum of progressive pass danger values leading to chances.
    * **counterattack_directness**: Ratio of goals/chances created from direct counter moves versus slower build-ups.
    * **3+player-possession_triangles**: Number of times Forest successfully formed and exploited wide triangles, a classic Ange feature.
    """, unsafe_allow_html=True)

    # Igor Jesus performance
    st.subheader("Igor Jesus - Star Performer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Igor Jesus stats
        igor_stats = pd.DataFrame({
            'Metric': ['Goals', 'Expected Goals', 'Box Touches', 'Shots'],
            'Value': [europa_player_stats['Igor Jesus']['goals'], europa_player_stats['Igor Jesus']['xG'], europa_player_stats['Igor Jesus']['touches_in_box'], europa_player_stats['Igor Jesus']['shots']],
            'Color': ['#cc1c1c', '#991c1c', '#ef4444', '#f59e0b']
        })
        
        for i, row in igor_stats.iterrows():
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem; background: #1a1a1a; border-radius: 8px; margin-bottom: 0.5rem;">
                <span style="font-weight: bold; color: white;">{row['Metric']}</span>
                <span style="font-size: 1.5rem; font-weight: bold; color: white;">{row['Value']}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tactical-note">
            <h6 style="color: #ef4444; font-weight: bold; margin-bottom: 0.5rem;">European Quality</h6>
            <p style="font-size: 0.9rem; color: #e0e0e0;">
                Igor Jesus exceeded his xG with clinical finishing, showing the kind of 
                edge Forest need to succeed in European competition. His two goals from 1.20 xG 
                demonstrates the clinical finishing required at this level.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # European performance comparison
    st.subheader("European vs Premier League Performance")
    
    european_comparison = pd.DataFrame({
        'Competition': ['Premier League', 'Europa League'],
        'Possession %': [ange_comparison_data['comparison_periods'][1]['total_possession'], europa_team_stats['possession_percent']],
        'xG per 90': [ange_comparison_data['comparison_periods'][1]['xG_per_game'], europa_team_stats['xG']],
        'PPDA': [ange_comparison_data['comparison_periods'][1]['PPDA'], europa_angeball_metrics['rest-defense effectiveness']],
        'Pass Accuracy': [ange_comparison_data['comparison_periods'][1]['pass_accuracy_percent'], europa_team_stats['pass_accuracy_percent']]
    })
    
    # Create comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig_comp1 = go.Figure()
        fig_comp1.add_trace(go.Bar(
            name='Possession %',
            x=european_comparison['Competition'],
            y=european_comparison['Possession %'],
            marker_color=['#cc1c1c', '#ef4444']
        ))
        fig_comp1.update_layout(
            title="Possession Comparison", 
            height=300,
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font_color="#e0e0e0"
        )
        st.plotly_chart(fig_comp1, use_container_width=True)
    
    with col2:
        fig_comp2 = go.Figure()
        fig_comp2.add_trace(go.Bar(
            name='xG per 90',
            x=european_comparison['Competition'],
            y=european_comparison['xG per 90'],
            marker_color=['#cc1c1c', '#ef4444']
        ))
        fig_comp2.update_layout(
            title="Chance Creation Comparison", 
            height=300,
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font_color="#e0e0e0"
        )
        st.plotly_chart(fig_comp2, use_container_width=True)
    
    # Tactical adaptations
    st.subheader("Tactical Adaptations for European Competition")
    
    adaptations = [
        {
            "aspect": "Possession Strategy",
            "pl_approach": f"Dominated possession ({ange_comparison_data['comparison_periods'][1]['total_possession']}%) with patient build-up",
            "european_approach": f"More direct approach ({europa_team_stats['possession_percent']}%) adapting to higher quality opposition",
            "effectiveness": "Successful adaptation - maintained threat creation"
        },
        {
            "aspect": "Pressing Intensity", 
            "pl_approach": f"Aggressive PPDA of {ange_comparison_data['comparison_periods'][1]['PPDA']} against Burnley",
            "european_approach": f"Slightly less intense {europa_angeball_metrics['rest-defense effectiveness']} PPDA vs Betis",
            "effectiveness": "Smart energy management for European fixture congestion"
        },
        {
            "aspect": "Clinical Finishing",
            "pl_approach": f"Struggled to convert {ange_comparison_data['comparison_periods'][1]['xG_per90']} xG vs Burnley (1 goal)",
            "european_approach": f"Better conversion of {europa_team_stats['xG']} xG vs Betis (2 goals)",
            "effectiveness": "Igor Jesus showing European-level clinical edge"
        }
    ]
    
    for adaptation in adaptations:
        st.markdown(f"""
        <div style="background: #1a1a1a; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #cc1c1c; margin: 1rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h6 style="color: #cc1c1c; font-weight: bold; margin-bottom: 0.75rem;">{adaptation['aspect']}</h6>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 0.75rem;">
                <div style="background: #260000; padding: 0.75rem; border-radius: 6px;">
                    <div style="font-weight: bold; color: #f0f0f0; font-size: 0.8rem; margin-bottom: 0.25rem;">PREMIER LEAGUE</div>
                    <div style="font-size: 0.85rem; color: #f0f0f0;">{adaptation['pl_approach']}</div>
                </div>
                <div style="background: #260000; padding: 0.75rem; border-radius: 6px;">
                    <div style="font-weight: bold; color: #f0f0f0; font-size: 0.8rem; margin-bottom: 0.25rem;">EUROPA LEAGUE</div>
                    <div style="font-size: 0.85rem; color: #f0f0f0;">{adaptation['european_approach']}</div>
                </div>
            </div>
            <div style="background: #260000; padding: 0.5rem; border-radius: 6px;">
                <span style="font-weight: bold; color: #cc1c1c; font-size: 0.8rem;">EFFECTIVENESS: </span>
                <span style="color: #f0f0f0; font-size: 0.85rem;">{adaptation['effectiveness']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Campaign assessment
    st.subheader("Europa League Campaign Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #260000, #1a0000);">
            <h6 style="font-size: 1.1rem; font-weight: bold; margin-bottom: 1rem;">✅ Positive Signs</h6>
            <ul style="font-size: 0.9rem; line-height: 1.6; margin: 0; padding-left: 1.5rem;">
                <li>Maintained attacking identity with lower possession (45%)</li>
                <li>Clinical finishing from Igor Jesus (2 goals from 1.98 xG)</li>
                <li>All "Ange-ball" metrics above European averages</li>
                <li>Defensive line height (52m) shows tactical confidence</li>
                <li>Triangle formations (17) indicate good player relationships</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #ef4444, #dc2626);">
            <h6 style="font-size: 1.1rem; font-weight: bold; margin-bottom: 1rem;">⚠️ Areas for Improvement</h6>
            <ul style="font-size: 0.9rem; line-height: 1.6; margin: 0; padding-left: 1.5rem;">
                <li>Game management - led 2-0 but drew 2-2</li>
                <li>Set piece conversion - 0/5 free kicks converted</li>
                <li>Possession control in European competition</li>
                <li>Individual defensive errors still occurring</li>
                <li>Need better squad rotation for fixture congestion</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # European outlook
    st.markdown("""
    <div class="metric-card" style="background: linear-gradient(135deg, #260000, #1a0000);">
        <h4 style="font-size: 1.5rem; margin-bottom: 1rem;">🌍 European Competition Verdict</h4>
        <p style="font-size: 1rem; line-height: 1.6; margin-bottom: 1rem;">
            Forest's debut Europa League performance shows promising signs of tactical adaptability. 
            The ability to maintain core "Ange-ball" principles while adjusting possession approach 
            demonstrates growing tactical maturity under Postecoglou.
        </p>
        <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px;">
            <p style="font-size: 0.95rem; line-height: 1.5; margin: 0;">
                <strong>Key Takeaway:</strong> Igor Jesus's clinical finishing (2 goals from 1.98 xG) provides 
                the European-level quality needed for continental success. The challenge now is consistency 
                across both domestic and European fixtures while managing squad rotation effectively.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Auto-play functionality for timeline
if st.session_state.is_playing and tab_selection == "Live Timeline":
    time.sleep(1.5)
    if st.session_state.timeline_index < len(timeline_data) - 1:
        st.session_state.timeline_index += 1
        st.rerun()
    else:
        st.session_state.is_playing = False
        st.rerun()

# Footer
st.markdown("""
---
<div style="text-align: center; color: #f0f0f0; margin-top: 2rem;">
    <p>Football Tactical Dashboard | Burnley vs Nottingham Forest Analysis</p>
    <p style="font-size: 0.8rem;">Built with Streamlit | Data visualized with Plotly</p>
</div>
""", unsafe_allow_html=True)
