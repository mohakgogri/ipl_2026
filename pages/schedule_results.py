import streamlit as st
import pandas as pd
from datetime import datetime
from data import schedule_data, results_data

st.set_page_config(page_title="IPL 2026 Schedule & Results", layout="wide")

# Custom CSS for consistency
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stTitle {
        color: #2c3e50;
        text-align: center;
        font-weight: 300;
        margin-bottom: 2rem;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #34495e;
        font-weight: 300;
    }
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button {
        background: linear-gradient(45deg, #3498db, #2980b9);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .stExpander {
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏏 IPL 2026 Schedule & Results")

tab1, tab2 = st.tabs(["📅 Schedule", "📊 Results"])

with tab1:
    st.markdown("### 🌟 Upcoming Matches")
    schedule_df = pd.DataFrame(schedule_data)
    st.dataframe(schedule_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 🔍 Filter Matches")
    col1, col2 = st.columns(2)

    all_teams = sorted({m["Team 1"] for m in schedule_data} | {m["Team 2"] for m in schedule_data})
    all_venues = sorted({m["Venue"] for m in schedule_data})

    with col1:
        selected_teams = st.multiselect("🏆 Teams", options=all_teams, help="Select teams")

    with col2:
        selected_venues = st.multiselect("📍 Venues", options=all_venues, help="Select venues")

    filtered_df = schedule_df.copy()
    if selected_teams:
        filtered_df = filtered_df[
            (filtered_df["Team 1"].isin(selected_teams)) |
            (filtered_df["Team 2"].isin(selected_teams))
        ]
    if selected_venues:
        filtered_df = filtered_df[filtered_df["Venue"].isin(selected_venues)]

    if len(filtered_df) > 0:
        st.markdown(f"**Showing {len(filtered_df)} matches**")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    else:
        st.info("🌙 No matches match your filters.")

with tab2:
    st.markdown("### 🏅 Past Matches")
    if len(results_data) > 0:
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### 📈 Tournament Stats")
        col1, col2, col3 = st.columns(3)

        total_matches = len(schedule_data) + len(results_data)
        matches_played = len(results_data)
        matches_remaining = len(schedule_data)
        progress = (matches_played / total_matches) * 100 if total_matches > 0 else 0

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Played</h3>
                <h1>{matches_played}</h1>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Remaining</h3>
                <h1>{matches_remaining}</h1>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Progress</h3>
                <h1>{progress:.1f}%</h1>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📋 Match Details")
        for idx, row in results_df.iterrows():
            with st.expander(f"🏏 Match {row['Match #']}: {row['Team 1']} vs {row['Team 2']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**🏆 Winner:** {row['Winner']}")
                with col2:
                    st.write(f"**📊 Margin:** {row['Margin']}")
                with col3:
                    st.write(f"**⭐ MOTM:** {row['Man of the Match']}")
    else:
        st.info("📝 No results yet. Check back soon!")
