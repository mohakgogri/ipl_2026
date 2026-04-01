import streamlit as st
import pandas as pd
from datetime import datetime
from data import schedule_data, results_data

st.set_page_config(page_title="IPL 2026 Schedule & Results", layout="wide")

st.title("🏏 IPL 2026 Schedule & Results")

# Create tabs for Schedule and Results
tab1, tab2 = st.tabs(["📅 Schedule", "📊 Results"])

with tab1:
    st.subheader("Upcoming Matches")
    schedule_df = pd.DataFrame(schedule_data)
    
    # Display schedule
    st.dataframe(schedule_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")

    # Add filters
    st.subheader("Filter Matches")
    col1, col2 = st.columns(2)

    all_teams = sorted({m["Team 1"] for m in schedule_data} | {m["Team 2"] for m in schedule_data})
    all_venues = sorted({m["Venue"] for m in schedule_data})
    
    with col1:
        selected_teams = st.multiselect(
            "Filter by Team", 
            options=all_teams,
            help="Select one or more teams to filter matches"
        )
    
    with col2:
        selected_venues = st.multiselect(
            "Filter by Venue", 
            options=all_venues,
            help="Select one or more venues to filter matches"
        )
    
    # Apply filters
    filtered_df = schedule_df.copy()
    
    if selected_teams:
        filtered_df = filtered_df[
            (filtered_df["Team 1"].isin(selected_teams)) | 
            (filtered_df["Team 2"].isin(selected_teams))
        ]
    
    if selected_venues:
        filtered_df = filtered_df[filtered_df["Venue"].isin(selected_venues)]
    
    if len(filtered_df) > 0:
        st.write(f"**Showing {len(filtered_df)} matches**")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    else:
        st.info("No matches found for the selected filters.")

with tab2:
    st.subheader("Past Matches")

    if len(results_data) > 0:
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Show statistics
        st.subheader("📈 Tournament Statistics")
        col1, col2, col3 = st.columns(3)
        
        total_matches = len(schedule_df) + len(results_df)
        matches_played = len(results_df)
        matches_remaining = len(schedule_df)
        progress = (matches_played / total_matches) * 100 if total_matches > 0 else 0
        
        with col1:
            st.metric("Matches Played", matches_played)
        with col2:
            st.metric("Matches Remaining", matches_remaining)
        with col3:
            st.metric("Tournament Progress", f"{progress:.1f}%")
        
        st.markdown("---")
        
        # Display recent results in expandable sections
        st.subheader("Recent Match Details")
        for idx, row in results_df.iterrows():
            with st.expander(f"Match {row['Match #']}: {row['Team 1']} vs {row['Team 2']} ({row['Date']})"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Winner:** {row['Winner']}")
                with col2:
                    st.write(f"**Margin:** {row['Margin']}")
                with col3:
                    st.write(f"**Man of the Match:** {row['Man of the Match']}")
    else:
        st.info("No match results yet. Check back after the first match!")
