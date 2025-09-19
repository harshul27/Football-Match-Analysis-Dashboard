# ⚽ Manchester Derby Analytics Dashboard

A comprehensive football analytics dashboard built with Streamlit, providing in-depth tactical analysis of the Manchester City vs Manchester United match (September 14, 2025).

![Dashboard Preview](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)

## 🌟 Features

### 📊 **Comprehensive Match Analysis**
- **xG Timeline**: Real-time expected goals progression
- **Team Statistics**: 15+ advanced metrics comparison  
- **Pressing Intensity**: PPDA analysis by match periods
- **Field Territory Control**: Zone-based possession analysis

### 👤 **Individual Player Performance**
- **Performance Radars**: 6-dimensional skill analysis
- **Heat Maps**: Position-based activity visualization
- **Advanced Metrics**: xG, xA, progressive actions, sprint data
- **Match Impact**: Key moments and contribution analysis

### 🏗️ **Tactical Insights**
- **Formation Analysis**: 3D pitch visualizations with player positions
- **Pass Networks**: Connection intensity between players
- **Strategic Recommendations**: Data-driven coaching insights
- **Vulnerability Assessment**: Tactical weaknesses identification

### 🔮 **Predictive Analytics**
- **AI-Powered Predictions**: Next 5 matches win probability
- **Form Projections**: Player confidence and performance trends
- **Injury Risk Assessment**: Load-based fatigue analysis
- **Transfer Market Impact**: Performance-based value predictions

## 🚀 **Live Demo**

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

## 📁 **Project Structure**

```
manchester-derby-analytics/
│
├── streamlit_app.py              # Main dashboard application
├── requirements.txt              # Python dependencies
├── README.md                    # Project documentation
├── .streamlit/
│   └── config.toml              # Streamlit configuration
├── data/
│   ├── match_data.json          # Match statistics and events
│   ├── player_data.json         # Individual player metrics
│   └── tactical_data.json       # Formation and tactical analysis
├── utils/
│   ├── __init__.py
│   ├── data_processor.py        # Data processing utilities
│   ├── visualizations.py       # Custom chart functions
│   └── metrics_calculator.py   # Advanced metrics computation
├── assets/
│   ├── team_logos/             # Team logos and graphics
│   └── pitch_templates/        # Pitch visualization templates
└── tests/
    ├── __init__.py
    ├── test_data_processing.py
    └── test_visualizations.py
```

## 🛠️ **Installation & Setup**

### **Local Development**

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/manchester-derby-analytics.git
   cd manchester-derby-analytics
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open your browser**
   ```
   http://localhost:8501
   ```

### **Streamlit Cloud Deployment**

1. **Fork this repository** to your GitHub account

2. **Connect to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select this repository

3. **Deploy automatically** - Streamlit Cloud will handle the rest!

## 📊 **Data Sources**

- **FotMob API**: Real-time match statistics and player data
- **ESPN Stats**: Advanced tactical metrics and formations
- **Opta Sports**: Expected goals and advanced analytics
- **Custom Calculations**: Innovative metrics like PPDA, field tilt, player impact scores

## 🎯 **Key Metrics Explained**

| Metric | Description | Interpretation |
|--------|-------------|----------------|
| **xG** | Expected Goals | Quality of scoring chances |
| **xA** | Expected Assists | Quality of assist opportunities |
| **PPDA** | Passes per Defensive Action | Pressing intensity (lower = more intense) |
| **Field Tilt** | % of play in opponent's half | Territorial dominance |
| **Progressive Passes** | Forward passes advancing play | Attacking contribution |
| **Impact Score** | Overall match influence | Combined performance rating |

## 🔧 **Advanced Features**

### **Interactive Visualizations**
- **Plotly Charts**: Responsive, interactive graphs
- **MPL Soccer**: Professional pitch visualizations
- **Custom Heat Maps**: Player positioning analysis
- **3D Formation Views**: Tactical setup visualization

### **Machine Learning Components**
- **Performance Prediction**: Next match probability models
- **Form Analysis**: Trend identification algorithms  
- **Risk Assessment**: Injury probability calculations
- **Market Value Modeling**: Performance-based valuations

### **Real-time Updates**
- **Live Data Integration**: API connections for current matches
- **Automatic Refresh**: Real-time metric updates
- **Event Notifications**: Goal and substitution alerts
- **Social Media Integration**: Match moment sharing

## 🤝 **Contributing**

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open Pull Request**

### **Areas for Contribution**
- 📊 New visualization types
- 🤖 Machine learning models
- 📱 Mobile optimization
- 🌍 Multi-language support
- ⚽ Additional leagues/matches
- 🔧 Performance optimizations

## 📈 **Roadmap**

### **Version 2.0 (Q4 2025)**
- [ ] Live match integration with real-time data
- [ ] Multiple match comparison tools
- [ ] Season-long performance tracking
- [ ] Advanced ML prediction models
- [ ] Mobile-responsive design improvements

### **Version 3.0 (Q1 2026)**
- [ ] Multi-league support (Premier League, La Liga, Serie A)
- [ ] Historical match database
- [ ] Custom report generation
- [ ] API for third-party integrations
- [ ] Video highlight synchronization

## 🏆 **Key Insights from This Match**

### **Manchester City Dominance**
- **Tactical Superiority**: 4-3-3 → 3-2-5 fluid formation
- **Pressing Excellence**: 8.2 PPDA shows intense pressure
- **Creative Partnerships**: Doku-Foden chemistry (2 assists)
- **Clinical Finishing**: 3 goals from 2.51 xG

### **Manchester United Struggles**
- **Formation Issues**: 3-5-2 exposed in midfield
- **Possession Problems**: Only 40% ball retention
- **Press Vulnerability**: 78% pass accuracy under pressure
- **Creative Drought**: Limited final third penetration

## 📚 **Technical Documentation**

### **Data Processing Pipeline**
```python
# Example: Advanced metrics calculation
def calculate_ppda(team_data):
    """Calculate Passes per Defensive Action"""
    opponent_passes = team_data['opponent_passes']
    defensive_actions = (team_data['tackles'] + 
                        team_data['interceptions'] + 
                        team_data['fouls'])
    return opponent_passes / defensive_actions

def field_tilt_analysis(events):
    """Calculate territorial dominance"""
    final_third_events = filter_events_by_zone(events, 'final_third')
    return len(final_third_events) / len(events) * 100
```

### **Visualization Components**
```python
# Custom pitch visualization
from mplsoccer import Pitch
import matplotlib.pyplot as plt

def create_player_heatmap(player_data, team_color):
    """Generate player position heat map"""
    pitch = Pitch(pitch_color='#0d1421', line_color='white')
    fig, ax = pitch.draw(figsize=(12, 8))
    
    for x, y, intensity in player_data['positions']:
        ax.scatter(x, y, s=intensity*50, c=team_color, alpha=0.7)
    
    return fig
```

## 🧪 **Testing**

Run the test suite:
```bash
python -m pytest tests/ -v
```

### **Test Coverage**
- ✅ Data processing functions
- ✅ Visualization rendering
- ✅ Metric calculations
- ✅ API integrations
- ✅ User interface components

## 🔐 **Security & Privacy**

- **Data Protection**: No personal user data collected
- **API Security**: Secure connections to data sources
- **Privacy Compliance**: GDPR compliant data handling
- **Open Source**: Full transparency in data processing

## 📞 **Support & Contact**

- **Issues**: [GitHub Issues](https://github.com/yourusername/manchester-derby-analytics/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/manchester-derby-analytics/discussions)
- **Email**: football.analytics@example.com
- **Twitter**: [@FootballAnalytics](https://twitter.com/footballanalytics)

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Streamlit Team**: For the amazing framework
- **Plotly**: For interactive visualizations
- **MPL Soccer**: For professional pitch graphics
- **Football Data Providers**: FotMob, ESPN, Opta
- **Community Contributors**: Everyone who helped improve this project

## 🌟 **Star History**

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/manchester-derby-analytics&type=Date)](https://star-history.com/#yourusername/manchester-derby-analytics&Date)

---

<div align="center">

**Built with ❤️ for Football Analytics**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/manchester-derby-analytics?style=social)](https://github.com/yourusername/manchester-derby-analytics/stargazers)
[![Twitter Follow](https://img.shields.io/twitter/follow/footballanalytics?style=social)](https://twitter.com/footballanalytics)

*If you found this project useful, please consider giving it a ⭐!*

</div>