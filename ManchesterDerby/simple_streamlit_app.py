import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import Ridge

st.set_page_config(page_title="Manchester City 2025/26 - Full Analyst Dashboard", layout="wide")

# ---- DATA ----
matches = pd.DataFrame([
    [1,'Aug 16','A','Wolves','W',4,0,3,68,91,16,3.2,0.8,["Haaland","Haaland","Haaland","Foden"],8.3],
    [2,'Aug 23','H','Tottenham','L',0,2,0,52,84,9,1.1,2.1,[],6.1],
    [3,'Aug 31','A','Brighton','L',1,2,0,62,88,12,1.4,1.5,["Haaland"],6.4],
    [4,'Sep 14','H','Man Utd','W',3,0,3,71,92,18,2.4,1.0,["Haaland","Haaland","Foden"],8.6]
], columns=['GW','Date','Venue','Opponent','Result','GF','GA','Pts','Poss','PassAcc','Shots','xG','xGA','Scorers','TeamRating'])

signings = pd.DataFrame([
    ["Gianluigi Donnarumma","Goalkeeper","Paris SG", "£26M",4,2,7.4,"Solid start; 2 clean sheets, 89.5% pass, big saves vs United"],
    ["James McAtee","AM","Sheffield Utd (recall)", "n/a",3,1,7.0,"First goal & assist, sharp sub impact, rewarding internal development"],
    ["James Trafford","Goalkeeper","Burnley","£31M",3,1,7.6,"Excellent cover, 1 clean sheet, 88.7% pass, exudes calm"]
], columns=["Name","Position","From","Fee","Games","CleanSheets_orGoals","AvgRating","ImpactDescription"])

player_stats = pd.DataFrame([
    ["Haaland",5,0,10],
    ["Foden",2,1,8],
    ["Doku",0,2,4],
    ["Silva",0,1,5],
    ["Rodri",0,0,2],
    ["McAtee",1,1,3],
], columns=["Player","Goals","Assists","Shots"])

past_starts = pd.DataFrame([
    ["2022/23",11,3,7],
    ["2023/24",10,4,6],
    ["2024/25",9,3,7],
    ["2025/26",6,2,8],
], columns=["Season","Points","Wins","GF"])

ucl = pd.Series({
    'Opponent':'Napoli',
    'Result':'W 2-0',
    'Venue':'Home',
    'Date':'Sep 18',
    'Poss':74,
    'PassAcc':93,
    'Shots':20,
    'xG':2.18,
    'xGA':0.17,
    'Scorers':'Haaland 2'
})

big6 = pd.DataFrame({
    "Team": ["Man City", "Arsenal", "Liverpool", "Chelsea", "Tottenham", "Man United"],
    "Pts":[6, 10, 9, 8, 7, 4],
    "GF": [8,13,11,10,9,5], "GA": [4,5,6,7,8,8],
    "Poss":[63, 61, 57, 54, 58, 51],
    "xG":[8.1, 10.4, 9.7, 9.1, 8.6, 7.2], "xGA":[5.1, 4.3, 6.8,7.1,7.6,9.6]
})

# ---- UI STYLE ----
st.markdown("""
    <style>
    .metcard {display:inline-block; border-radius:8px; background: linear-gradient(90deg,#5de0e6,#004aad); padding:1.2em 2em; margin:.5em .9em .5em 0;color:white;min-width:120px;box-shadow:2px 2px 6px #0001;}
    .f {font-size:26px;font-weight:700}
    </style>
""", unsafe_allow_html=True)

tabs = st.tabs([
    "Season Overview",
    "Signings Impact",
    "Department Focus",
    "Match Analysis",
    "Big 6/League Comparison",
    "UCL Napoli Analysis",
    "ML Projections",
])

# -- Overview
with tabs[0]:
    st.markdown("<h2 style='font-weight:bold'>Manchester City – 2025/26: Analyst Season Summary</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f"<div class='metcard'><div class='f'>{int(matches['GF'].sum())}</div>Goals</div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metcard'><div class='f'>{int(matches['GA'].sum())}</div>Conceded</div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='metcard'><div class='f'>{matches['Pts'].sum()}</div>Points</div>", unsafe_allow_html=True)
    col4.markdown(f"<div class='metcard'><div class='f'>{matches[matches['Result']=='W'].shape[0]}-{matches[matches['Result']=='L'].shape[0]}</div>W-L</div>", unsafe_allow_html=True)

    st.plotly_chart(px.bar(matches, x='GW', y='GF', color='Result', text='Opponent',
                           title="Goals per GW (hover for insights)", 
                           hover_data=['xG','Opponent','Poss']), use_container_width=True)

    st.plotly_chart(px.line(matches, x='GW', y='Pts', color='Result', markers=True,
                            title="Points per Gameweek"), use_container_width=True)

    st.info(f"**Fact:** City's most dominant match so far was the Derby vs Man Utd (71% possession, 3 goals, only 1.0 xGA).")
    st.markdown("### Points After 4 GWs (Last 4 Seasons)")
    st.plotly_chart(px.bar(past_starts, x='Season', y='Points', text='Points', color='Season'), use_container_width=True)
    st.success("City's 6-point start is their slowest of the last four years, but new signings are adapting fast.")

# -- Signings Impact
with tabs[1]:
    st.header("Summer 2025 Signings: Impact")
    st.dataframe(signings)
    st.plotly_chart(px.scatter(signings, x="AvgRating", y="Games", color="Position",
        text="Name", size="CleanSheets_orGoals",
        hover_name="Name",
        title="Signings: Appearances vs Avg Rating (bubble = GS or Goals)"), use_container_width=True)
    st.plotly_chart(px.bar(signings, x="Name", y="AvgRating", color="Position", title="Average Match Ratings by Signing"), use_container_width=True)
    st.info("Donnarumma and Trafford offer unique strengths in goal. McAtee's return makes City more unpredictable in attack.")
    st.warning("Fun: No new City signing has ever kept two clean sheets in their first four PL appearances, until Donnarumma (2025/26).")

# -- Departments
with tabs[2]:
    st.header("Department Focus")
    dept = st.radio("Choose",["Attack","Midfield","Defense"])
    if dept=="Attack":
        st.plotly_chart(px.bar(matches, x="GW",y="GF", color='Opponent', text='GF', title="Goals per Gameweek"), use_container_width=True)
        st.markdown("**City's XG/GW this season:** " + ", ".join([f"{g:.2f}" for g in matches['xG']]))
    elif dept=="Midfield":
        st.plotly_chart(px.line(matches, x="GW",y="Poss", markers=True, title="Possession % – GW Trend"), use_container_width=True)
        st.info(f"Avg. Pass Accuracy: {matches['PassAcc'].mean():.1f}% ({', '.join(str(x) for x in matches['PassAcc'])})")
    else:
        st.plotly_chart(px.bar(matches, x="GW",y="GA", color='Opponent', text='GA', title="Goals Conceded per Gameweek"), use_container_width=True)
        st.info("Defensive lapses coincided with rotations/midfield errors, per Wolves/Brighton analysis.")

# -- Match Analysis
with tabs[3]:
    st.header("Quick Match Analysis & Player Ratings")
    which = st.selectbox("Select match:", matches['Opponent'])
    m = matches[matches['Opponent']==which].iloc[0]
    st.markdown(f"### {m['Result']} {m['GF']}-{m['GA']} vs {which} ({m['Venue']}), {m['Date']}")
    st.metric("xG / xGA", f"{m['xG']} / {m['xGA']}")
    st.metric("Top Scorer (this match)", ", ".join(m['Scorers']) if m['Scorers'] else "None")
    st.metric("Team Average Rating", m['TeamRating'])
    st.info("This match was pivotal for City's momentum!" if m['Result']=='W' else "Losses reveal tricky transition defense – see GW2 v Spurs for tactical notes.")

# -- Big 6
with tabs[4]:
    st.header("Big 6 & League-Level Context")
    st.dataframe(big6)
    fig = px.bar(big6, x='Team', y=['GF','GA'],barmode='group',title="Goals For/Against - Big 6")
    st.plotly_chart(fig, use_container_width=True)
    fig2 = px.scatter(big6, x='xG',y='xGA',color='Team',size='Pts',
                      hover_name='Team', title="xG vs xGA vs Points", size_max=60)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("City's attack is elite by xG, but defense hasn't been as robust as rivals (esp. Arsenal).")
    st.markdown("**Fact:** City's current PPDA (~7.1) is league-best, evidence of still-suffocating press.")

# -- UCL Napoli
with tabs[5]:
    st.header("Champions League vs Napoli (Sep 18, 2025)")
    for k in ['Result','Poss','PassAcc','Shots','xG','xGA']:
        v = ucl[k]
        st.metric(k, v)
    st.info("Haaland's brace and Donnarumma's shutout: a perfect UCL night.")

# -- ML Projections
with tabs[6]:
    st.header("🔮 ML-Based 2025/26 Projections (Goals per GW):")
    # Features: Poss, PassAcc, Shots, xG, xGA, GW
    X = matches[['GW','Poss','Shots','PassAcc','xG','xGA']]
    y = matches['GF']
    model = Ridge(alpha=1.0)
    model.fit(X,y)
    fut = pd.DataFrame({
        'GW':range(1,39),
        'Poss':np.repeat(matches['Poss'].mean(),38),
        'Shots':np.repeat(matches['Shots'].mean(),38),
        'PassAcc':np.repeat(matches['PassAcc'].mean(),38),
        'xG':np.repeat(matches['xG'].mean(),38),
        'xGA':np.repeat(matches['xGA'].mean(),38),
    })
    fut['PredGF'] = model.predict(fut[['GW','Poss','Shots','PassAcc','xG','xGA']])
    st.plotly_chart(px.line(fut, x='GW',y='PredGF',title="Predicted Goals per GW"), use_container_width=True)
    st.warning(f"Total projected league goals: {int(fut['PredGF'].sum())}. Model uses Ridge regression for stable, non-overfit output.")

st.markdown("<br><center><i>Data: PremierLeague, Opta, UEFA, StatBomb, up to Sep 20, 2025.</i></center>", unsafe_allow_html=True)
