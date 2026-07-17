# Paris 2024 Olympics Dashboard
An interactive Streamlit dashboard for exploring Paris 2024 Olympic medal data. It lets users browse the overall medal standings, see how medals are distributed geographically on a world map, and dig into any country's performance by sport and individual athlete — turning a raw dataset into an easy, visual way to explore the Games.


## Setup
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files
- `app.py` — the Streamlit dashboard
- `data/medal_table.csv` — country-level medal leaderboard (with ISO3 codes for the map)
- `data/medals_events.csv` — one row per medal awarded (event-level)
- `data/medallists_clean.csv` — one row per athlete medal, with age at Games, team flag, etc.
- `data/country_sport_breakdown.csv` — pre-aggregated country x sport x medal-type counts (powers the drill-down bar chart)

## Features
- Sortable medal table (by gold/silver/bronze/total)
- Choropleth map of medal counts by country
- Country drill-down: medals-by-sport bar chart + full medallist list

# Interactive Olympics Dashboard

🔗 **Live app:** [interactive-olympics-dashboard.streamlit.app](https://interactive-olympics-dashboard.streamlit.app)
