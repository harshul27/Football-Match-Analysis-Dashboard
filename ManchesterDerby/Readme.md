# Manchester Derby Analytics Dashboard

A simple and effective Streamlit dashboard analyzing the Manchester City vs Manchester United match (September 14, 2025).

## Features

- **Match Overview**: xG timeline, key metrics, momentum analysis
- **Team Statistics**: Comprehensive comparison with visual charts
- **Player Performance**: Individual ratings and goal/assist tracking
- **Match Events**: Timeline of key moments throughout the game

## Quick Deploy to Streamlit Cloud

1. **Fork this repository** to your GitHub account
2. **Go to** [share.streamlit.io](https://share.streamlit.io)
3. **Connect your GitHub** and select this repository
4. **Deploy automatically** - it's ready to go!

## Local Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/manchester-derby-analytics.git
cd manchester-derby-analytics

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

## Dashboard Sections

### Match Overview
- Final score and key metrics
- Expected Goals (xG) timeline chart
- Match momentum by 15-minute periods

### Team Statistics  
- Complete statistical comparison table
- Interactive metric selection and visualization
- Key tactical insights for both teams

### Player Performance
- Individual player analysis with ratings
- Goals and assists breakdown
- Visual comparison charts

###  Match Events
- Chronological timeline of key events
- Goals, substitutions, and big chances
- Visual events distribution chart

## Key Match Data

**Final Result:** Manchester City 3-0 Manchester United  
**Date:** September 14, 2025  
**Venue:** Etihad Stadium  
**Attendance:** 55,017  

**Goals:**
- 18' Phil Foden (assist: Doku)
- 53' Erling Haaland (assist: Doku)  
- 78' Erling Haaland

**Expected Goals:** City 2.51 - 0.73 United

## 🛠️ Built With

- **Streamlit** - Web framework
- **Pandas** - Data manipulation
- **Matplotlib** - Visualizations
- **NumPy** - Numerical computing
- **Seaborn** - Statistical plotting

## Project Structure

```
manchester-derby-analytics/
├── streamlit_app.py    # Main application
├── requirements.txt    # Dependencies
└── README.md          # This file
```

## Dependencies

The app uses only essential Python libraries:
- `streamlit` - Dashboard framework
- `pandas` - Data handling  
- `numpy` - Mathematical operations
- `matplotlib` - Charts and graphs
- `seaborn` - Enhanced plotting

## Live Demo

Once deployed on Streamlit Cloud, your dashboard will be available at:
`https://your-app-name.streamlit.app`

## Contributing

Feel free to fork this project and submit pull requests for improvements!

## License

This project is open source and available under the [MIT License](LICENSE).

---

**Built with ❤️ for Football Analytics**
