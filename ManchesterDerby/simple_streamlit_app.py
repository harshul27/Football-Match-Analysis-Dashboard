import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Manchester Derby Analytics",
    page_icon="⚽",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #6CABDD 0%, #DA020E 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #6CABDD;
        margin: 0.5rem 0;
    }
    .team-stat {
        font-size: 1.2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load match data
@st.cache_data
def load_match_data():
    """Load Manchester Derby match data"""
    
    # Match information
    match_info = {
        'date': '2025-09-14',
        'venue': 'Etihad Stadium',
        'attendance': 55017,
        'final_score': {'city': 3, 'united': 0}
    }
    
    # xG Timeline data
    xg_data = pd.DataFrame([
        {'minute': 0, 'city_xg': 0.00, 'united_xg': 0.00},
        {'minute': 15, 'city_xg': 0.12, 'united_xg': 0.05},
        {'minute': 18, 'city_xg': 0.40, 'united_xg': 0.05},
        {'minute': 30, 'city_xg': 0.58, 'united_xg': 0.18},
        {'minute': 45, 'city_xg': 0.82, 'united_xg': 0.31},
        {'minute': 53, 'city_xg': 1.27, 'united_xg': 0.31},
        {'minute': 60, 'city_xg': 1.45, 'united_xg': 0.47},
        {'minute': 75, 'city_xg': 1.68, 'united_xg': 0.59},
        {'minute': 78, 'city_xg': 2.30, 'united_xg': 0.59},
        {'minute': 90, 'city_xg': 2.51, 'united_xg': 0.73}
    ])
    
    # Team statistics
    team_stats = pd.DataFrame({
        'Metric': ['Possession %', 'Shots', 'Shots on Target', 'Pass Accuracy %', 
                   'Passes', 'Corners', 'Fouls', 'Yellow Cards'],
        'Manchester City': [64, 18, 8, 89, 612, 7, 11, 2],
        'Manchester United': [36, 9, 4, 78, 348, 3, 14, 3]
    })
    
    # Player data
    player_data = {
        'Phil Foden': {'goals': 1, 'assists': 0, 'rating': 8.2, 'team': 'City'},
        'Erling Haaland': {'goals': 2, 'assists': 0, 'rating': 9.5, 'team': 'City'},
        'Jeremy Doku': {'goals': 0, 'assists': 2, 'rating': 8.5, 'team': 'City'},
        'Manuel Ugarte': {'goals': 0, 'assists': 0, 'rating': 6.8, 'team': 'United'},
        'Bruno Fernandes': {'goals': 0, 'assists': 0, 'rating': 6.5, 'team': 'United'}
    }
    
    return match_info, xg_data, team_stats, player_data

# Load data
match_info, xg_data, team_stats, player_data = load_match_data()

# Main header
st.markdown(f"""
<div class="main-header">
    <h1>⚽ Manchester Derby Analytics Dashboard</h1>
    <h2>Manchester City 3 - 0 Manchester United</h2>
    <p>September 14, 2025 • {match_info['venue']}</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📊 Navigation")
page = st.sidebar.selectbox(
    "Select View",
    ["Match Overview", "Team Statistics", "Player Performance", "Match Events"]
)

if page == "Match Overview":
    st.header("🏟️ Match Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Final Score", "3 - 0", delta="City Victory")
    
    with col2:
        st.metric("Total xG", f"{xg_data.iloc[-1]['city_xg']:.1f} - {xg_data.iloc[-1]['united_xg']:.1f}", delta="City dominated")
    
    with col3:
        st.metric("Possession", "64% - 36%", delta="City controlled")
    
    with col4:
        st.metric("Shots", "18 - 9", delta="City more clinical")
    
    # xG Timeline Chart
    st.subheader("📈 Expected Goals Timeline")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(xg_data['minute'], xg_data['city_xg'], 
            color='#6CABDD', linewidth=3, label='Manchester City', marker='o')
    ax.plot(xg_data['minute'], xg_data['united_xg'], 
            color='#DA020E', linewidth=3, label='Manchester United', marker='s')
    
    ax.fill_between(xg_data['minute'], xg_data['city_xg'], alpha=0.3, color='#6CABDD')
    ax.fill_between(xg_data['minute'], xg_data['united_xg'], alpha=0.3, color='#DA020E')
    
    # Add goal markers
    ax.axvline(x=18, color='green', linestyle='--', alpha=0.7)
    ax.axvline(x=53, color='green', linestyle='--', alpha=0.7)
    ax.axvline(x=78, color='green', linestyle='--', alpha=0.7)
    
    ax.set_xlabel('Match Time (minutes)')
    ax.set_ylabel('Cumulative xG')
    ax.set_title('Expected Goals Development Throughout Match')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#f8f9fa')
    
    st.pyplot(fig)
    
    # Match momentum
    st.subheader("⚡ Match Momentum")
    
    momentum_data = pd.DataFrame({
        'Period': ['0-15', '15-30', '30-45', '45-60', '60-75', '75-90'],
        'City xG': [0.12, 0.28, 0.42, 0.45, 0.23, 0.62],
        'United xG': [0.05, 0.00, 0.13, 0.16, 0.12, 0.14]
    })
    
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(momentum_data))
    width = 0.35
    
    ax.bar(x - width/2, momentum_data['City xG'], width, 
           label='Manchester City', color='#6CABDD', alpha=0.8)
    ax.bar(x + width/2, momentum_data['United xG'], width, 
           label='Manchester United', color='#DA020E', alpha=0.8)
    
    ax.set_xlabel('Match Period')
    ax.set_ylabel('xG Created')
    ax.set_title('Expected Goals by 15-Minute Periods')
    ax.set_xticks(x)
    ax.set_xticklabels(momentum_data['Period'])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)

elif page == "Team Statistics":
    st.header("📊 Team Statistics Comparison")
    
    # Display team stats table
    st.subheader("Complete Match Statistics")
    st.dataframe(team_stats, use_container_width=True)
    
    # Visual comparison
    st.subheader("📈 Statistical Comparison")
    
    # Select metrics for comparison
    selected_metrics = st.multiselect(
        "Select metrics to compare:",
        team_stats['Metric'].tolist(),
        default=['Possession %', 'Shots', 'Pass Accuracy %']
    )
    
    if selected_metrics:
        filtered_stats = team_stats[team_stats['Metric'].isin(selected_metrics)]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        x = np.arange(len(filtered_stats))
        width = 0.35
        
        ax.bar(x - width/2, filtered_stats['Manchester City'], width, 
               label='Manchester City', color='#6CABDD', alpha=0.8)
        ax.bar(x + width/2, filtered_stats['Manchester United'], width, 
               label='Manchester United', color='#DA020E', alpha=0.8)
        
        ax.set_xlabel('Metrics')
        ax.set_ylabel('Values')
        ax.set_title('Team Performance Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(filtered_stats['Metric'], rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    # Key insights
    st.subheader("🔍 Key Tactical Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
        <h4>🔵 Manchester City Strengths</h4>
        <ul>
        <li><strong>Possession Dominance:</strong> 64% ball retention</li>
        <li><strong>Clinical Finishing:</strong> 3 goals from quality chances</li>
        <li><strong>Pass Accuracy:</strong> 89% completion rate</li>
        <li><strong>Creative Play:</strong> Doku with 2 assists</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
        <h4>🔴 Manchester United Issues</h4>
        <ul>
        <li><strong>Low Possession:</strong> Only 36% of the ball</li>
        <li><strong>Limited Chances:</strong> 0.73 xG total</li>
        <li><strong>Pass Struggles:</strong> 78% accuracy under pressure</li>
        <li><strong>Defensive Gaps:</strong> 3 goals conceded</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

elif page == "Player Performance":
    st.header("👤 Individual Player Analysis")
    
    # Player selector
    selected_player = st.selectbox(
        "Select Player for Analysis:",
        list(player_data.keys())
    )
    
    player = player_data[selected_player]
    team_color = '#6CABDD' if player['team'] == 'City' else '#DA020E'
    
    # Player card
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {team_color}aa, {team_color}55); 
                padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0;">
        <h2>⭐ {selected_player}</h2>
        <h3>Manchester {player['team']}</h3>
        <h1>Match Rating: {player['rating']}/10</h1>
        <p>Goals: {player['goals']} | Assists: {player['assists']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Performance breakdown
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Goals", player['goals'])
        
    with col2:
        st.metric("Assists", player['assists'])
        
    with col3:
        st.metric("Rating", f"{player['rating']}/10")
    
    # Player comparison chart
    st.subheader("📊 Player Ratings Comparison")
    
    ratings_df = pd.DataFrame([
        {'Player': name, 'Rating': data['rating'], 'Team': data['team']}
        for name, data in player_data.items()
    ])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ['#6CABDD' if team == 'City' else '#DA020E' for team in ratings_df['Team']]
    
    bars = ax.bar(ratings_df['Player'], ratings_df['Rating'], color=colors, alpha=0.8)
    
    # Highlight selected player
    for i, bar in enumerate(bars):
        if ratings_df.iloc[i]['Player'] == selected_player:
            bar.set_edgecolor('gold')
            bar.set_linewidth(3)
    
    ax.set_xlabel('Players')
    ax.set_ylabel('Match Rating')
    ax.set_title('Player Performance Ratings')
    ax.set_ylim(0, 10)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)
    
    # Goals and assists breakdown
    st.subheader("⚽ Goals & Assists Distribution")
    
    goals_assists_data = pd.DataFrame([
        {'Player': name, 'Goals': data['goals'], 'Assists': data['assists']}
        for name, data in player_data.items()
    ])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Goals
    goal_colors = ['#6CABDD' if player_data[name]['team'] == 'City' else '#DA020E' 
                   for name in goals_assists_data['Player']]
    ax1.bar(goals_assists_data['Player'], goals_assists_data['Goals'], 
            color=goal_colors, alpha=0.8)
    ax1.set_title('Goals Scored')
    ax1.set_ylabel('Goals')
    ax1.tick_params(axis='x', rotation=45)
    
    # Assists
    ax2.bar(goals_assists_data['Player'], goals_assists_data['Assists'], 
            color=goal_colors, alpha=0.8)
    ax2.set_title('Assists Provided')
    ax2.set_ylabel('Assists')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    st.pyplot(fig)

elif page == "Match Events":
    st.header("⏱️ Key Match Events Timeline")
    
    # Match events data
    events_data = [
        {'Minute': 18, 'Event': 'GOAL', 'Player': 'Phil Foden', 'Team': 'City', 'Description': 'Header from Doku cross'},
        {'Minute': 53, 'Event': 'GOAL', 'Player': 'Erling Haaland', 'Team': 'City', 'Description': 'Clinical finish'},
        {'Minute': 62, 'Event': 'SUB', 'Player': 'Tactical change', 'Team': 'United', 'Description': 'Formation adjustment'},
        {'Minute': 78, 'Event': 'GOAL', 'Player': 'Erling Haaland', 'Team': 'City', 'Description': 'Counter-attack finish'},
        {'Minute': 84, 'Event': 'CHANCE', 'Player': 'Bryan Mbeumo', 'Team': 'United', 'Description': 'Great save by Donnarumma'}
    ]
    
    events_df = pd.DataFrame(events_data)
    
    # Display events
    st.subheader("📋 Chronological Match Events")
    
    for _, event in events_df.iterrows():
        color = '#6CABDD' if event['Team'] == 'City' else '#DA020E'
        emoji = '⚽' if event['Event'] == 'GOAL' else '🔄' if event['Event'] == 'SUB' else '⭐'
        
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, {color}20 0%, transparent 100%); 
                    padding: 1rem; margin: 0.5rem 0; border-radius: 8px; 
                    border-left: 4px solid {color};">
            <div class="team-stat">
                {emoji} {event['Minute']}' - {event['Player']}
            </div>
            <p>{event['Description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Events timeline chart
    st.subheader("📊 Events Distribution")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    city_events = events_df[events_df['Team'] == 'City']
    united_events = events_df[events_df['Team'] == 'United']
    
    # Plot events
    ax.scatter(city_events['Minute'], [1]*len(city_events), 
              color='#6CABDD', s=200, alpha=0.8, label='City Events')
    ax.scatter(united_events['Minute'], [0]*len(united_events), 
              color='#DA020E', s=200, alpha=0.8, label='United Events')
    
    # Add event labels
    for _, event in events_df.iterrows():
        y_pos = 1 if event['Team'] == 'City' else 0
        ax.annotate(f"{event['Minute']}'\n{event['Event']}", 
                   (event['Minute'], y_pos),
                   xytext=(5, 10), textcoords='offset points',
                   fontsize=8, ha='left')
    
    ax.set_xlabel('Match Time (minutes)')
    ax.set_ylabel('Team')
    ax.set_title('Match Events Timeline')
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Man United', 'Man City'])
    ax.set_xlim(0, 95)
    ax.grid(True, alpha=0.3, axis='x')
    ax.legend()
    
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    <p>⚽ Manchester Derby Analytics Dashboard</p>
    <p>Built with Streamlit • September 2025</p>
</div>
""", unsafe_allow_html=True)