import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from mplsoccer import Pitch, FontManager
from PIL import Image, ImageDraw, ImageFont

# ----------- DATA DEFINITIONS (CORRECTED) -----------------
matches = pd.DataFrame([
    {"GW":1,"Date":"Aug 16","Venue":"A","Opponent":"Wolves","Result":"W","GF":4,"GA":0,"Score":"4-0",
     "Poss":68,"PassAcc":91,"Shots":16,"xG":3.2,"xGA":0.8,
     "attack":"Clinical finishing - 4 goals, Haaland brace",
     "midfield":"Complete dominance with 91% pass accuracy",
     "defense":"Perfect debut for Donnarumma"},
    {"GW":2,"Date":"Aug 23","Venue":"H","Opponent":"Tottenham","Result":"L","GF":0,"GA":2,"Score":"0-2",
     "Poss":52,"PassAcc":84,"Shots":9,"xG":1.1,"xGA":2.1,
     "attack":"Wasteful finishing",
     "midfield":"Struggled without Gündogan",
     "defense":"Costly individual errors"},
    {"GW":3,"Date":"Aug 31","Venue":"A","Opponent":"Brighton","Result":"L","GF":1,"GA":2,"Score":"1-2",
     "Poss":62,"PassAcc":88,"Shots":12,"xG":1.4,"xGA":1.5,
     "attack":"Haaland's milestone but limited service",
     "midfield":"Handball penalty crucial",
     "defense":"Late transitions vulnerable"},
    {"GW":4,"Date":"Sep 14","Venue":"H","Opponent":"Man Utd","Result":"W","GF":3,"GA":0,"Score":"3-0",
     "Poss":71,"PassAcc":92,"Shots":18,"xG":2.4,"xGA":1.0,
     "attack":"Clinical return - Haaland double",
     "midfield":"Dominated possession and tempo",
     "defense":"Commanding clean sheet"}
])

# Example signings, radar, ucl, big6 etc—please add or adapt as per your earlier setup.
signings = [
    {"name":"Gianluigi Donnarumma", "pos":"GK", "from":"PSG", "fee":26, "games":4, "cleanSheets":2, "rating":7.4, "impact":"Solid, 2 clean sheets."},
    {"name":"James McAtee", "pos":"AM","from":"Sheff Utd","fee":0,"games":3,"goals":1,"assists":1,"rating":7.0,"impact":"Goal, assist; creative force."},
    {"name":"James Trafford", "pos":"GK","from":"Burnley","fee":31,"games":3,"cleanSheets":1,"rating":7.6,"impact":"Backup, strong debut."},
]
radar = pd.DataFrame([
    {"metric":"Points","City":6,"LeagueAvg":7.8},
    {"metric":"Goals For","City":7,"LeagueAvg":5.2},
    {"metric":"Possession","City":63.25,"LeagueAvg":58.3},
    {"metric":"Pass Accuracy","City":88.75,"LeagueAvg":84.2}
])

# Simulated UCL data and big6 as previously, omitted for brevity

# ---------- STREAMLIT APP LAYOUT (CORRECTED) --------------

# Custom CSS still used
st.markdown("""
<style>
.metriccard { background: linear-gradient(90deg,#0f1c39 60%,#44b0fd 130%);
              border-radius:15px; color:white;padding:18px;
              margin:8px; min-width:120px;
              font-size:21px; box-shadow:2px 7px 22px #0001;}
.tabpanel {background: #f9fafd; border-radius: 12px; padding: 22px;}
.sectitle {font-weight:700;letter-spacing:0.5px;color:#045cc8;}
.secfact {background:#eefdfe;padding:9px;border-radius:8px;font-size:16px;font-weight:bold;color:#234;}
</style>
""", unsafe_allow_html=True)


st.markdown("<h1 style='color:#045cc8'>Manchester City 2025/26 Results & Analytics Dashboard</h1>", unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
c1.markdown(f"<div class='metriccard'>Position<br><span style='font-size:30px'>{8}</span></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metriccard'>Points<br><span style='font-size:30px'>{6}</span></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metriccard'>Goals For<br><span style='font-size:30px'>{7}</span></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='metriccard'>Goals Against<br><span style='font-size:30px'>{4}</span></div>", unsafe_allow_html=True)
c5.markdown(f"<div class='metriccard'>PPG<br><span style='font-size:30px'>{1.5}</span></div>", unsafe_allow_html=True)
st.markdown("<div class='secfact'>Haaland already leads with 5 goals. Donnarumma is the first new City keeper since Hart to keep 2+ clean sheets in his first 4 league games.</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Season Overview",
    "Match Analysis",
    "Signings Impact",
    "Department Analytics",
    "Big 6 Compare",
    "UCL Napoli",
    "ML Projection"
])

with tab1:
    st.markdown("<div class='sectitle'>Season Progression</div>", unsafe_allow_html=True)
    st.write(matches.head())  # Debug: check your DF
    st.plotly_chart(
        px.bar(matches, x='GW', y='GF', color='Result',
        title="Goals per Matchday", text='Opponent',
        hover_data=['Poss','Shots','xG','xGA','PassAcc']),
        use_container_width=True
    )
    st.plotly_chart(
        px.line(matches, x='GW', y='GF', color='Result', markers=True, title="Goals For per GW"),
        use_container_width=True
    )
    st.markdown("<div class='secfact'>MCFC's slow GW start is still better than 15 PL clubs. Their pressing (PPDA) is league-best to this point.</div>", unsafe_allow_html=True)
    st.plotly_chart(px.bar(radar, x="metric", y=["City","LeagueAvg"], barmode="group", text_auto=True,
               title="Man City vs. League Avg: Core Stats"), use_container_width=True)

with tab2:
    st.markdown("<div class='sectitle'>Detailed Match Cards (clickable/selectable)</div>", unsafe_allow_html=True)
    matchlist = [f"{m.GW} - {m.Opponent} ({m.Score})" for i, m in matches.iterrows()]
    sel = st.selectbox("Select gameweek", matchlist, index=0)
    m = matches.iloc[matchlist.index(sel)]
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Result", f"{m.Score}")
    c2.metric("Possession (%)", m.Poss)
    c3.metric("xG", m.xG)
    c4.metric("xGA", m.xGA)
    c5.metric("Shots", m.Shots)
    st.info(f"Attack: {m.attack}")
    st.info(f"Midfield: {m.midfield}")
    st.info(f"Defense: {m.defense}")

# --- The rest of the tabs remain as in your original code, using DataFrames for all data sets ---

