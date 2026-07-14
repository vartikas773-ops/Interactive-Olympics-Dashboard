"""
Paris 2024 Olympics — Interactive Medal Dashboard
Run with: streamlit run app.py
"""
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Paris 2024 Olympics Dashboard", layout="wide", page_icon="🏅")

# ---------------------------------------------------------------
# Data loading (cached so filters don't reload from disk each time)
# ---------------------------------------------------------------
@st.cache_data
def load_data():
    medal_table = pd.read_csv("data/medal_table.csv")
    medals_events = pd.read_csv("data/medals_events.csv", parse_dates=["medal_date"])
    medallists = pd.read_csv("data/medallists_clean.csv", parse_dates=["medal_date"])
    country_sport = pd.read_csv("data/country_sport_breakdown.csv")
    return medal_table, medals_events, medallists, country_sport

medal_table, medals_events, medallists, country_sport = load_data()

st.title("🏅 Paris 2024 Olympics — Medal Dashboard")
st.caption("Explore medal standings, country breakdowns, and athlete-level results from the Paris 2024 Summer Olympics.")

# =================================================================
# SECTION 1 — Sortable medal table + choropleth map
# =================================================================
col_table, col_map = st.columns([1, 1])

with col_table:
    st.subheader("Medal Table")
    sort_by = st.selectbox("Sort by", ["gold", "silver", "bronze", "total"], index=3)
    sorted_table = medal_table.sort_values(sort_by, ascending=False).reset_index(drop=True)
    sorted_table.index = sorted_table.index + 1  # 1-based rank display
    st.dataframe(
        sorted_table[["country", "gold", "silver", "bronze", "total"]],
        use_container_width=True,
        height=520,
    )

with col_map:
    st.subheader("Medal Map")
    map_metric = st.selectbox("Map metric", ["total", "gold", "silver", "bronze"], index=0, key="map_metric")
    fig_map = px.choropleth(
        medal_table,
        locations="iso3",
        color=map_metric,
        hover_name="country",
        hover_data={"gold": True, "silver": True, "bronze": True, "total": True, "iso3": False},
        color_continuous_scale="YlOrRd",
        projection="natural earth",
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=500)
    st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# =================================================================
# SECTION 2 — Country drill-down
# =================================================================
st.subheader("Country Drill-Down")

country_list = sorted(medal_table["country"].unique())
default_idx = country_list.index("United States") if "United States" in country_list else 0
selected_country = st.selectbox("Choose a country", country_list, index=default_idx)

country_row = medal_table[medal_table["country"] == selected_country].iloc[0]
m1, m2, m3, m4 = st.columns(4)
m1.metric("🥇 Gold", int(country_row["gold"]))
m2.metric("🥈 Silver", int(country_row["silver"]))
m3.metric("🥉 Bronze", int(country_row["bronze"]))
m4.metric("Total", int(country_row["total"]))

drill_left, drill_right = st.columns([1, 1.4])

with drill_left:
    st.markdown("**Medals by Sport**")
    cs = country_sport[country_sport["country"] == selected_country]
    if len(cs):
        cs_pivot = cs.pivot_table(
            index="sport", columns="medal_type", values="count", aggfunc="sum", fill_value=0
        )
        for col in ["Gold Medal", "Silver Medal", "Bronze Medal"]:
            if col not in cs_pivot.columns:
                cs_pivot[col] = 0
        cs_pivot["total"] = cs_pivot[["Gold Medal", "Silver Medal", "Bronze Medal"]].sum(axis=1)
        cs_pivot = cs_pivot.sort_values("total", ascending=True)

        fig_bar = px.bar(
            cs_pivot,
            x=["Gold Medal", "Silver Medal", "Bronze Medal"],
            y=cs_pivot.index,
            orientation="h",
            color_discrete_map={
                "Gold Medal": "#FFD700",
                "Silver Medal": "#C0C0C0",
                "Bronze Medal": "#CD7F32",
            },
        )
        fig_bar.update_layout(
            barmode="stack", legend_title="", xaxis_title="Medals", yaxis_title="",
            height=max(300, 28 * len(cs_pivot)),
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No medals recorded for this country.")

with drill_right:
    st.markdown("**Medallists**")
    country_medallists = medallists[medallists["country"] == selected_country][
        ["name", "gender", "sport", "event", "medal_type", "age_at_games"]
    ].sort_values("medal_type")
    st.dataframe(country_medallists, use_container_width=True, height=420, hide_index=True)

st.divider()

st.caption("Data: Paris 2024 Olympic Summer Games dataset (Kaggle).")
