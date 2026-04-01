import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="IPL 2026 Schedule & Results", layout="wide")

st.title("🏏 IPL 2026 Schedule & Results")

# Create tabs for Schedule and Results
tab1, tab2 = st.tabs(["📅 Schedule", "📊 Results"])

# Sample data - Replace with actual IPL 2026 data
schedule_data = {
    "Match #": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Date": ["2026-03-28", "2026-03-29", "2026-03-30", "2026-03-31", "2026-04-01", 
             "2026-04-02", "2026-04-03", "2026-04-04", "2026-04-05", "2026-04-06"],
    "Team 1": ["CSK", "MI", "RCB", "KKR", "DC", "SRH", "GT", "LSG", "PBKS", "RR"],
    "Team 2": ["RR", "SRH", "GT", "LSG", "PBKS", "CSK", "MI", "RCB", "KKR", "DC"],
    "Venue": ["Chennai", "Mumbai", "Bangalore", "Kolkata", "Delhi", 
              "Hyderabad", "Ahmedabad", "Lucknow", "Mohali", "Jaipur"],
    "Time": ["19:30", "19:30", "19:30", "19:30", "19:30", "19:30", "19:30", "19:30", "19:30", "19:30"]
}

results_data = {
    "Match #": [1, 2],
    "Date": ["2026-03-28", "2026-03-29"],
    "Team 1": ["CSK", "MI"],
    "Team 2": ["RR", "SRH"],
    "Winner": ["CSK", "MI"],
    "Margin": ["6 wickets", "4 runs"],
    "Venue": ["Chennai", "Mumbai"],
    "Man of the Match": ["Du Plessis", "Hardik Pandya"]
}

with tab1:
    st.subheader("Upcoming Matches")
    schedule_df = pd.DataFrame(schedule_data)
    
    # Display schedule
    st.dataframe(schedule_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Add filters
    st.subheader("Filter Matches")
    col1, col2 = st.columns(2)
    
    all_teams = sorted(set(schedule_data["Team 1"] + schedule_data["Team 2"]))
    all_venues = sorted(set(schedule_data["Venue"]))
    
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
    
    if len(results_data["Match #"]) > 0:
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
