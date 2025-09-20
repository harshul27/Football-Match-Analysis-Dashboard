# Manchester City Performance Dashboard

An interactive Streamlit application for analyzing Manchester City's season performance with comprehensive tactical insights and data visualization.

## ⚠️ Important Disclaimer

**This dashboard contains entirely fictional data for demonstration purposes.** The "2025/26 season" referenced in the code does not exist - we're currently in 2024. This is a template showing how such analysis could work with real data from sources like FBref, ESPN, or official Premier League statistics.

## Features

- **Season Overview**: Complete season statistics, points progression, and performance metrics
- **Match Analysis**: Detailed tactical breakdown of individual matches
- **Player Performance**: Individual player ratings and performance tracking
- **Season Projections**: Data-driven predictions and scenario analysis
- **Interactive Visualizations**: Charts, radars, and comparative analysis tools

## Installation & Setup

### Local Development

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

### Streamlit Cloud Deployment

1. Fork this repository to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository
5. Set the main file path to `app.py`
6. Deploy!

## Project Structure

```
manchester-city-dashboard/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── .streamlit/        # Streamlit configuration (optional)
    └── config.toml
```

## Dashboard Sections

### 1. Season Overview
- League position and points progression
- Goal statistics and clean sheet records
- Performance radar charts
- New signings impact analysis

### 2. Match Analysis
- Individual match breakdowns
- Tactical analysis by phase (attack, midfield, defense)
- Player ratings visualization
- Key moments and turning points

### 3. Player Performance
- Individual player statistics
- Performance comparison across matches
- Season averages and trends
- Impact assessment

### 4. Season Projections
- Points per game projections
- Final table predictions
- European qualification chances
- Scenario analysis (best/worst case)

## Key Technologies

- **Streamlit**: Web application framework
- **Plotly**: Interactive data visualization
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations

## Data Structure

The application uses structured dictionaries and DataFrames to organize:
- Season statistics and standings
- Individual match data and analysis
- Player performance metrics
- Historical comparisons

## Customization

To adapt this dashboard for real data:

1. Replace the fictional data in `load_season_data()` function
2. Connect to real data sources (APIs, databases, CSV files)
3. Modify metrics and calculations based on actual football statistics
4. Update team information and player details

## Real Data Integration

For real implementation, consider integrating with:
- **FBref**: Advanced football statistics
- **ESPN API**: Match results and basic stats
- **Official Premier League API**: Live data
- **Opta/StatsBomb**: Professional football data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add appropriate tests
5. Submit a pull request

## License

This project is for educational and demonstration purposes. Please ensure you have proper licensing for any real football data used.

## Contact

For questions about implementation or customization, please open an issue in the GitHub repository.

---

**Note**: This is a demonstration dashboard. For production use with real data, ensure proper data licensing, privacy compliance, and performance optimization.
