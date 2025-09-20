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

# Data Setup (use authentic data from previous prompts!)
# ... [reuse all dataframes: matches, signings, radar, ucl, proj_df, big6, player_stats, etc.] ...

# Custom CSS/JS
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

# ----- HEADER & CARDS -----
st.markdown("<h1 style='color:#045cc8'>Manchester City 2025/26 Results & Analytics Dashboard</h1>", unsafe_allow_html=True)

# Statistic cards row
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

# ----------- SEASON OVERVIEW TAB -------------
with tab1:
    st.markdown("<div class='sectitle'>Season Progression</div>", unsafe_allow_html=True)
    st.plotly_chart(
        px.bar(matches, x='GW', y='GF', color='Result',
        title="Goals per Matchday", text='Opponent',
        hover_data=['Poss','Shots','xG','xGA','PassAcc']),
        use_container_width=True
    )

    st.plotly_chart(
        px.line(matches, x='GW', y='Pts', color='Result', markers=True, title="Points per Gameweek"),
        use_container_width=True
    )

    st.markdown("<div class='secfact'>MCFC's slow GW start is still better than 15 PL clubs. Their pressing (PPDA) is league-best to this point.</div>", unsafe_allow_html=True)
    st.plotly_chart(px.bar(radar, x="metric", y=["City","LeagueAvg"], barmode="group", text_auto=True, 
               title="Man City vs. League Avg: Core Stats"), use_container_width=True)

# --------- MATCH ANALYSIS TAB ------------
with tab2:
    st.markdown("<div class='sectitle'>Detailed Match Cards (clickable/selectable)</div>", unsafe_allow_html=True)
    matchlist = [f"{m['GW']} - {m['Opponent']} ({m['score']})" for i, m in enumerate(matches)]
    sel = st.selectbox("Select gameweek", matchlist, index=0)
    m = matches[matchlist.index(sel)]
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Result", f"{m['score']}")
    c2.metric("Possession (%)", m['possessions'])
    c3.metric("xG", m['xG'])
    c4.metric("xGA", m['xGA'])
    c5.metric("Shots", m['shots'])
    st.info(f"Attack: {m['attack']}")
    st.info(f"Midfield: {m['midfield']}")
    st.info(f"Defense: {m['defense']}")

# --------- SIGNINGS ---------
with tab3:
    st.markdown("<div class='sectitle'>New Signings Impact Cards</div>", unsafe_allow_html=True)
    sigdf = pd.DataFrame(signings)
    cols = st.columns(len(signings))
    for idx, s in enumerate(signings):
        with cols[idx]:
            st.markdown(f"""
                <div class='signingcard'>
                    <div style='font-size:19px;font-weight:600'>{s['name']} <span style='color:gray;font-size:0.6em'>({s['pos']})</span></div>
                    <div>Fee £{s['fee']}M  | Games: {s['games']} | Rating: <b>{s['rating']}</b></div>
                    <div class='impact'>Impact: {s['impact']}</div>
                </div>
            """, unsafe_allow_html=True)
    st.dataframe(sigdf)

# ---------- DEPARTMENT ANALYTICS (Radar + mplsoccer option) -----------
with tab4:
    st.markdown("<div class='sectitle'>Department Radar (Attack–Midfield–Defense)</div>", unsafe_allow_html=True)
    # Radar plot (go)
    features = ["GF", "xG", "Poss", "PassAcc"]
    deptvals = [matches['GF'].sum(), matches['xG'].sum(), matches['Poss'].mean(), matches['PassAcc'].mean()]
    leaguevals = [7, 8.1, 58, 84.2]  # Demo data
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=deptvals, theta=features, fill='toself', name='Man City'))
    fig.add_trace(go.Scatterpolar(r=leaguevals, theta=features, fill='toself', name='League Avg'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

# ---------- BIG 6 TAB ----------
with tab5:
    st.markdown("<div class='sectitle'>Big 6 Table/Scatter</div>", unsafe_allow_html=True)
    st.dataframe(big6)
    st.plotly_chart(px.scatter(big6, x='xG', y='xGA', size='Pts', color='Team', hover_name='Team',
                               title="xG/xGA Scatter: Big 6 Performance"), use_container_width=True)

# ----------- UCL NAPOLI -------------
with tab6:
    st.markdown("<div class='sectitle'>UCL: Napoli 9/18/2025 Tactical Dashboard</div>", unsafe_allow_html=True)
    f1, f2, f3 = st.columns([2,1,2])
    f1.metric("Possession (%)", ucl.Poss)
    f2.metric("Shots", ucl.Shots)
    f3.metric("xG (Man City)", ucl.xG)
    st.metric("xGA (Napoli)", ucl.xGA)
    st.info("Haaland's brace, 74% possession—a Champions League statement.")
    # Optional: Draw pass map (mplsoccer Pitch) or similar...

# -------- MACHINE LEARNING PROJECTION ---------
with tab7:
    st.markdown("<div class='sectitle'>Advanced ML Projections (Ridge/Statsmodels)</div>", unsafe_allow_html=True)
    X = matches[["GW","Poss","Shots","PassAcc","xG","xGA"]]
    y = matches['GF']
    model = Ridge(alpha=1.0)
    model.fit(X.values, y.values)
    preds = model.predict(pd.DataFrame({
        "GW": np.arange(1,39),
        "Poss": np.repeat(matches["Poss"].mean(),38),
        "Shots": np.repeat(matches["Shots"].mean(),38),
        "PassAcc": np.repeat(matches["PassAcc"].mean(),38),
        "xG": np.repeat(matches["xG"].mean(),38),
        "xGA": np.repeat(matches["xGA"].mean(),38)
    }))
    st.plotly_chart(px.line(x=range(1,39),y=preds, title="Projected Goals per GW (ML Ridge Regression)"), use_container_width=True)
    st.success(f"Total projected league goals: {int(preds.sum())} — A top 4 pace.")
    st.info(
        "Model uses Ridge regression for stability and league mean for features. "
        "Upgrade to XGBoost or ensemble for greater accuracy with more data."
    )


