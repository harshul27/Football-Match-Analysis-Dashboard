import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta

# Configure page
st.set_page_config(
    page_title="Tactical Analysis Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
    .tactical-insight {
        background-color: #f1f3f4;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Sample tactical data for Manchester Derby
@st.cache_data
def load_tactical_data():
    # xG timeline data
    xg_timeline = pd.DataFrame([
        {'minute': 0, 'city_xg': 0.0, 'united_xg': 0.0, 'event': ''},
        {'minute': 8, 'city_xg': 0.02, 'united_xg': 0.0, 'event': 'Ugarte error'},
        {'minute': 18, 'city_xg': 0.33, 'united_xg': 0.0, 'event': 'GOAL Foden'},
        {'minute': 24, 'city_xg': 0.41, 'united_xg': 0.05, 'event': 'Formation change'},
        {'minute': 38, 'city_xg': 0.56, 'united_xg': 0.12, 'event': 'Overload right'},
        {'minute': 45, 'city_xg': 0.73, 'united_xg': 0.24, 'event': 'Half-time'},
        {'minute': 53, 'city_xg': 1.34, 'united_xg': 0.24, 'event': 'GOAL Haaland'},
        {'minute': 62, 'city_xg': 1.52, 'united_xg': 0.24, 'event': 'Formation breakdown'},
        {'minute': 68, 'city_xg': 1.95, 'united_xg': 0.24, 'event': 'GOAL Haaland'},
        {'minute': 78, 'city_xg': 2.08, 'united_xg': 0.38, 'event': ''},
        {'minute': 84, 'city_xg': 2.08, 'united_xg': 0.64, 'event': 'United chance'},
        {'minute': 90, 'city_xg': 2.18, 'united_xg': 0.71, 'event': 'Full-time'}
    ])
    
    # Pressure map data by zones
    pressure_data = pd.DataFrame([
        {'zone': 'Defensive Third', 'period': '0-15min', 'city': 8, 'united': 22},
        {'zone': 'Defensive Third', 'period': '15-30min', 'city': 6, 'united': 28},
        {'zone': 'Defensive Third', 'period': '30-45min', 'city': 4, 'united': 31},
        {'zone': 'Defensive Third', 'period': '45-60min', 'city': 7, 'united': 34},
        {'zone': 'Defensive Third', 'period': '60-75min', 'city': 5, 'united': 38},
        {'zone': 'Defensive Third', 'period': '75-90min', 'city': 3, 'united': 42},
        
        {'zone': 'Middle Third', 'period': '0-15min', 'city': 24, 'united': 18},
        {'zone': 'Middle Third', 'period': '15-30min', 'city': 28, 'united': 15},
        {'zone': 'Middle Third', 'period': '30-45min', 'city': 31, 'united': 12},
        {'zone': 'Middle Third', 'period': '45-60min', 'city': 33, 'united': 9},
        {'zone': 'Middle Third', 'period': '60-75min', 'city': 29, 'united': 11},
        {'zone': 'Middle Third', 'period': '75-90min', 'city': 26, 'united': 13},
        
        {'zone': 'Attacking Third', 'period': '0-15min', 'city': 42, 'united': 6},
        {'zone': 'Attacking Third', 'period': '15-30min', 'city': 48, 'united': 4},
        {'zone': 'Attacking Third', 'period': '30-45min', 'city': 51, 'united': 3},
        {'zone': 'Attacking Third', 'period': '45-60min', 'city': 56, 'united': 2},
        {'zone': 'Attacking Third', 'period': '60-75min', 'city': 49, 'united': 5},
        {'zone': 'Attacking Third', 'period': '75-90min', 'city': 44, 'united': 7}
    ])
    
    # Player performance data
    player_data = pd.DataFrame([
        {
            'name': 'Haaland', 'team': 'City', 'position': 'ST',
            'progressive_passes': 3, 'progressive_carries': 8, 'shot_creating_actions': 4,
            'pressures': 12, 'interceptions': 1, 'pass_completion_final_third': 67,
            'xg': 1.32, 'xa': 0.05, 'goals': 2, 'assists': 0, 'rating': 9.2
        },
        {
            'name': 'Foden', 'team': 'City', 'position': 'AM',
            'progressive_passes': 12, 'progressive_carries': 15, 'shot_creating_actions': 8,
            'pressures': 18, 'interceptions': 3, 'pass_completion_final_third': 78,
            'xg': 0.31, 'xa': 0.18, 'goals': 1, 'assists': 0, 'rating': 8.8
        },
        {
            'name': 'Doku', 'team': 'City', 'position': 'RW',
            'progressive_passes': 9, 'progressive_carries': 22, 'shot_creating_actions': 11,
            'pressures': 14, 'interceptions': 2, 'pass_completion_final_third': 72,
            'xg': 0.12, 'xa': 0.94, 'goals': 0, 'assists': 2, 'rating': 8.9
        },
        {
            'name': 'Rodri', 'team': 'City', 'position': 'DM',
            'progressive_passes': 18, 'progressive_carries': 6, 'shot_creating_actions': 5,
            'pressures': 22, 'interceptions': 6, 'pass_completion_final_third': 85,
            'xg': 0.03, 'xa': 0.12, 'goals': 0, 'assists': 0, 'rating': 8.3
        },
        {
            'name': 'Bruno', 'team': 'United', 'position': 'AM',
            'progressive_passes': 8, 'progressive_carries': 4, 'shot_creating_actions': 3,
            'pressures': 16, 'interceptions': 2, 'pass_completion_final_third': 58,
            'xg': 0.08, 'xa': 0.22, 'goals': 0, 'assists': 0, 'rating': 6.4
        },
        {
            'name': 'Ugarte', 'team': 'United', 'position': 'CM',
            'progressive_passes': 3, 'progressive_carries': 2, 'shot_creating_actions': 1,
            'pressures': 24, 'interceptions': 4, 'pass_completion_final_third': 45,
            'xg': 0.02, 'xa': 0.03, 'goals': 0, 'assists': 0, 'rating': 5.8
        },
        {
            'name': 'Mbeumo', 'team': 'United', 'position': 'RAM',
            'progressive_passes': 4, 'progressive_carries': 7, 'shot_creating_actions': 2,
            'pressures': 8, 'interceptions': 1, 'pass_completion_final_third': 62,
            'xg': 0.26, 'xa': 0.14, 'goals': 0, 'assists': 0, 'rating': 6.1
        }
    ])
    
    # PPDA data by zone
    ppda_data = pd.DataFrame([
        {'zone': 'Left Wing', 'city_ppda': 6.2, 'united_ppda': 11.8, 'city_dominance': 0.73},
        {'zone': 'Left Half-Space', 'city_ppda': 4.8, 'united_ppda': 14.2, 'city_dominance': 0.89},
        {'zone': 'Central', 'city_ppda': 7.1, 'united_ppda': 9.4, 'city_dominance': 0.62},
        {'zone': 'Right Half-Space', 'city_ppda': 3.9, 'united_ppda': 16.7, 'city_dominance': 0.94},
        {'zone': 'Right Wing', 'city_ppda': 5.4, 'united_ppda': 13.1, 'city_dominance': 0.81}
    ])
    
    return xg_timeline, pressure_data, player_data, ppda_data

# Load data
xg_timeline, pressure_data, player_data, ppda_data = load_tactical_data()

# Header
st.title("🎯 Tactical Analysis Dashboard")
st.markdown("**Manchester Derby | City 3-0 United | Performance Intelligence**")

# Sidebar controls
st.sidebar.header("🎛️ Analysis Controls")

# Time period selector
time_period = st.sidebar.selectbox(
    "Match Period",
    ["Full Match", "First Half", "Second Half", "Custom Range"],
    index=0
)

if time_period == "Custom Range":
    time_range = st.sidebar.slider(
        "Select Minutes",
        min_value=0,
        max_value=90,
        value=(0, 90),
        step=1
    )
else:
    if time_period == "First Half":
        time_range = (0, 45)
    elif time_period == "Second Half":
        time_range = (45, 90)
    else:
        time_range = (0, 90)

# Team selector
team_filter = st.sidebar.selectbox(
    "Focus Team",
    ["Both Teams", "Manchester City", "Manchester United"],
    index=0
)

# Player selector
available_players = player_data['name'].tolist()
selected_player = st.sidebar.selectbox(
    "Player Focus",
    ["All Players"] + available_players,
    index=0
)

# Analysis layers
st.sidebar.subheader("📊 Analysis Layers")
show_pressure = st.sidebar.checkbox("Pressure Analysis", value=True)
show_transitions = st.sidebar.checkbox("Transition Speed", value=True)
show_ppda = st.sidebar.checkbox("PPDA Mapping", value=True)
show_player_focus = st.sidebar.checkbox("Player Deep Dive", value=False)

# Main layout - 3 columns
col1, col2, col3 = st.columns([2, 4, 2])

# Left column - Key metrics
with col1:
    st.subheader("🔢 Key Metrics")
    
    # Filter xG data based on time range
    filtered_xg = xg_timeline[
        (xg_timeline['minute'] >= time_range[0]) & 
        (xg_timeline['minute'] <= time_range[1])
    ]
    
    final_city_xg = filtered_xg['city_xg'].iloc[-1] if len(filtered_xg) > 0 else 0
    final_united_xg = filtered_xg['united_xg'].iloc[-1] if len(filtered_xg) > 0 else 0
    
    st.metric("Expected Goals", f"{final_city_xg:.2f} - {final_united_xg:.2f}", 
              delta=f"City +{final_city_xg - final_united_xg:.2f}")
    
    st.metric("Actual Score", "3 - 0", delta="City dominance")
    
    # Efficiency metrics
    city_efficiency = 3 / final_city_xg if final_city_xg > 0 else 0
    united_efficiency = 0 / final_united_xg if final_united_xg > 0 else 0
    
    st.metric("Finishing Efficiency", f"{city_efficiency:.1f}x vs {united_efficiency:.1f}x",
              delta="Clinical finishing")
    
    # Pressure differential
    city_att_pressure = pressure_data[pressure_data['zone'] == 'Attacking Third']['city'].mean()
    united_att_pressure = pressure_data[pressure_data['zone'] == 'Attacking Third']['united'].mean()
    
    st.metric("Attacking Third Pressure", f"{city_att_pressure:.0f} vs {united_att_pressure:.0f}",
              delta=f"City +{city_att_pressure - united_att_pressure:.0f}")

# Center column - Main visualizations
with col2:
    st.subheader("📈 Interactive Timeline & Analysis")
    
    # Interactive xG timeline
    fig_xg = go.Figure()
    
    fig_xg.add_trace(go.Scatter(
        x=filtered_xg['minute'],
        y=filtered_xg['city_xg'],
        mode='lines+markers',
        name='Manchester City',
        line=dict(color='#6CABDD', width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{fullData.name}</b><br>' +
                      'Minute: %{x}<br>' +
                      'xG: %{y:.2f}<br>' +
                      '<extra></extra>'
    ))
    
    fig_xg.add_trace(go.Scatter(
        x=filtered_xg['minute'],
        y=filtered_xg['united_xg'],
        mode='lines+markers',
        name='Manchester United',
        line=dict(color='#DA020E', width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{fullData.name}</b><br>' +
                      'Minute: %{x}<br>' +
                      'xG: %{y:.2f}<br>' +
                      '<extra></extra>'
    ))
    
    # Add event annotations
    for _, row in filtered_xg.iterrows():
        if row['event'] and 'GOAL' in row['event']:
            fig_xg.add_annotation(
                x=row['minute'],
                y=row['city_xg'] if 'City' in row['event'] else row['united_xg'],
                text="⚽",
                showarrow=True,
                arrowhead=2,
                arrowcolor="gold",
                font=dict(size=16)
            )
    
    fig_xg.update_layout(
        title="Expected Goals Timeline with Key Events",
        xaxis_title="Match Time (minutes)",
        yaxis_title="Cumulative Expected Goals",
        hovermode='x unified',
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig_xg.update_xaxis(gridcolor='lightgray', gridwidth=1)
    fig_xg.update_yaxis(gridcolor='lightgray', gridwidth=1)
    
    st.plotly_chart(fig_xg, use_container_width=True)
    
    # Pressure analysis heatmap
    if show_pressure:
        st.subheader("🔥 Pressure Intensity Analysis")
        
        # Create pressure heatmap
        pressure_pivot = pressure_data.pivot_table(
            index='zone', 
            columns='period', 
            values=['city', 'united'], 
            aggfunc='first'
        )
        
        fig_pressure = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Manchester City Pressure', 'Manchester United Pressure'),
            shared_yaxes=True
        )
        
        periods = ['0-15min', '15-30min', '30-45min', '45-60min', '60-75min', '75-90min']
        zones = ['Attacking Third', 'Middle Third', 'Defensive Third']
        
        # City pressure data
        city_pressure_matrix = []
        united_pressure_matrix = []
        
        for zone in zones:
            city_row = []
            united_row = []
            for period in periods:
                city_val = pressure_data[
                    (pressure_data['zone'] == zone) & 
                    (pressure_data['period'] == period)
                ]['city'].values[0]
                united_val = pressure_data[
                    (pressure_data['zone'] == zone) & 
                    (pressure_data['period'] == period)
                ]['united'].values[0]
                city_row.append(city_val)
                united_row.append(united_val)
            city_pressure_matrix.append(city_row)
            united_pressure_matrix.append(united_row)
        
        fig_pressure.add_trace(
            go.Heatmap(
                z=city_pressure_matrix,
                x=periods,
                y=zones,
                colorscale='Blues',
                showscale=False,
                hovertemplate='Period: %{x}<br>Zone: %{y}<br>Pressures: %{z}<extra></extra>'
            ),
            row=1, col=1
        )
        
        fig_pressure.add_trace(
            go.Heatmap(
                z=united_pressure_matrix,
                x=periods,
                y=zones,
                colorscale='Reds',
                showscale=False,
                hovertemplate='Period: %{x}<br>Zone: %{y}<br>Pressures: %{z}<extra></extra>'
            ),
            row=1, col=2
        )
        
        fig_pressure.update_layout(
            title="Pressure Distribution by Zone & Time Period",
            height=300
        )
        
        st.plotly_chart(fig_pressure, use_container_width=True)
        
        st.markdown("""
        <div class="tactical-insight">
        <strong>Tactical Insight:</strong> City maintained consistent high pressure in attacking third (42-56 pressures per period), 
        while United's pressure concentrated in defensive third, indicating territorial retreat and loss of midfield control.
        </div>
        """, unsafe_allow_html=True)
    
    # PPDA Analysis
    if show_ppda:
        st.subheader("⚡ PPDA & Zone Dominance")
        
        fig_ppda = go.Figure()
        
        fig_ppda.add_trace(go.Bar(
            x=ppda_data['zone'],
            y=ppda_data['city_ppda'],
            name='City PPDA',
            marker_color='#6CABDD',
            hovertemplate='Zone: %{x}<br>PPDA: %{y:.1f}<br>(Lower = Better Press)<extra></extra>'
        ))
        
        fig_ppda.add_trace(go.Bar(
            x=ppda_data['zone'],
            y=ppda_data['united_ppda'],
            name='United PPDA',
            marker_color='#DA020E',
            hovertemplate='Zone: %{x}<br>PPDA: %{y:.1f}<br>(Lower = Better Press)<extra></extra>'
        ))
        
        fig_ppda.update_layout(
            title="PPDA by Zone (Passes Per Defensive Action - Lower = Better)",
            xaxis_title="Field Zones",
            yaxis_title="PPDA Value",
            height=350,
            barmode='group'
        )
        
        st.plotly_chart(fig_ppda, use_container_width=True)

# Right column - Player analysis and insights
with col3:
    st.subheader("👤 Player Analysis")
    
    if selected_player != "All Players":
        # Individual player focus
        player_info = player_data[player_data['name'] == selected_player].iloc[0]
        
        st.markdown(f"**{player_info['name']}** ({player_info['position']})")
        st.markdown(f"Team: {player_info['team']}")
        st.metric("Match Rating", f"{player_info['rating']}/10")
        
        # Player radar chart
        categories = [
            'Progressive Passes', 'Progressive Carries', 'Shot Creating Actions',
            'Pressures', 'Interceptions', 'Final Third Completion'
        ]
        
        values = [
            player_info['progressive_passes'],
            player_info['progressive_carries'],
            player_info['shot_creating_actions'],
            player_info['pressures'],
            player_info['interceptions'],
            player_info['pass_completion_final_third']
        ]
        
        # Normalize values for radar (0-100 scale)
        max_values = [20, 25, 15, 30, 10, 100]  # Reasonable max values for normalization
        normalized_values = [min(100, (v / max_v) * 100) for v, max_v in zip(values, max_values)]
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=normalized_values + [normalized_values[0]],  # Close the shape
            theta=categories + [categories[0]],
            fill='toself',
            name=player_info['name'],
            line_color='#6CABDD' if player_info['team'] == 'City' else '#DA020E',
            fillcolor=('#6CABDD' if player_info['team'] == 'City' else '#DA020E') + '40'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False,
            height=350,
            title=f"{player_info['name']} Performance Profile"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Key stats
        st.markdown("**Key Statistics:**")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("xG", f"{player_info['xg']:.2f}")
            st.metric("xA", f"{player_info['xa']:.2f}")
        with col_b:
            st.metric("Goals", int(player_info['goals']))
            st.metric("Assists", int(player_info['assists']))
    
    else:
        # Team comparison
        st.subheader("🏆 Top Performers")
        
        top_city = player_data[player_data['team'] == 'City'].nlargest(3, 'rating')
        top_united = player_data[player_data['team'] == 'United'].nlargest(3, 'rating')
        
        st.markdown("**Manchester City:**")
        for _, player in top_city.iterrows():
            st.markdown(f"• {player['name']} ({player['position']}) - {player['rating']}/10")
        
        st.markdown("**Manchester United:**")
        for _, player in top_united.iterrows():
            st.markdown(f"• {player['name']} ({player['position']}) - {player['rating']}/10")
        
        # Performance comparison chart
        fig_comparison = go.Figure()
        
        city_players = player_data[player_data['team'] == 'City']
        united_players = player_data[player_data['team'] == 'United']
        
        fig_comparison.add_trace(go.Scatter(
            x=city_players['shot_creating_actions'],
            y=city_players['progressive_carries'],
            mode='markers+text',
            text=city_players['name'],
            textposition="top center",
            marker=dict(size=city_players['rating']*3, color='#6CABDD', opacity=0.7),
            name='City Players',
            hovertemplate='<b>%{text}</b><br>' +
                          'Shot Creating Actions: %{x}<br>' +
                          'Progressive Carries: %{y}<br>' +
                          'Rating: %{marker.size:.0f}/30<extra></extra>'
        ))
        
        fig_comparison.add_trace(go.Scatter(
            x=united_players['shot_creating_actions'],
            y=united_players['progressive_carries'],
            mode='markers+text',
            text=united_players['name'],
            textposition="top center",
            marker=dict(size=united_players['rating']*3, color='#DA020E', opacity=0.7),
            name='United Players',
            hovertemplate='<b>%{text}</b><br>' +
                          'Shot Creating Actions: %{x}<br>' +
                          'Progressive Carries: %{y}<br>' +
                          'Rating: %{marker.size:.0f}/30<extra></extra>'
        ))
        
        fig_comparison.update_layout(
            title="Player Impact Matrix",
            xaxis_title="Shot Creating Actions",
            yaxis_title="Progressive Carries",
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)

# Footer with tactical insights
st.markdown("---")
st.subheader("🎯 Tactical Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🔴 Key Weaknesses Exposed:**
    - United's right half-space vulnerability (3.9 vs 16.7 PPDA)
    - Progressive retreat pattern (defensive pressure 35→42)
    - Formation breakdown after 60th minute
    """)

with col2:
    st.markdown("""
    **🔵 City's Tactical Success:**
    - Sustained attacking third pressure (48+ per period)
    - Clinical finishing (3 goals from 2.18 xG)
    - Half-space dominance creation
    """)

with col3:
    st.markdown("""
    **📊 Data-Backed Insights:**
    - Ugarte's errors directly led to 1.06 xG
    - Doku's isolation tactics created 0.94 xA
    - Formation change correlation with xG spikes
    """)

# Export functionality
if st.button("📊 Export Analysis Report"):
    st.success("Analysis exported! (In production, this would generate a downloadable PDF report)")

st.markdown("""
---
*Tactical Analysis Dashboard v2.1 | Performance Intelligence System*  
*Data Sources: Event Data Analysis, Positional Tracking, Advanced Metrics*
""")
