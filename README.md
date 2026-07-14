# Paris 2024 Olympics Dashboard

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

## Ideas to extend
- Add a "medals per capita" or "medals per GDP" toggle (needs a population/GDP lookup table)
- Add an athlete search box across all countries
- Add a timeline slider using `medal_date` to replay the Games day by day
- Deploy for free on Streamlit Community Cloud so you can share a live link
