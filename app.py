import streamlit as st
from datetime import datetime, date
from data import players, schedule_data, results_data, results_by_match, matches_by_date, get_today, get_max_vote_date
import pandas as pd

st.set_page_config(
    page_title="IPL 2026 Dashboard",
    page_icon="🏏",
    layout="wide"
)

# Custom CSS for minimalistic, artistic feel
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
    .stTextInput input, .stSelectbox select {
        border-radius: 8px;
        border: 1px solid #bdc3c7;
        padding: 8px 12px;
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

st.title("We only belive in Jassi Bhai")

st.markdown("## 🏆 Latest Scoreboard")

if "guesses" not in st.session_state:
    st.session_state.guesses = {}

if "message" not in st.session_state:
    st.session_state.message = ""

# Helper functions remain the same

def get_match_by_date(date_value):
    return matches_by_date.get(date_value.strftime("%Y-%m-%d"), [])


def calculate_scoreboard():
    scores = {p: 0 for p in players}
    for date_key, date_guesses in st.session_state.guesses.items():
        for match_id, guess in date_guesses.items():
            actual = results_by_match.get(match_id)
            if not actual:
                continue
            player_winner = guess.get("winner")
            player_motm = guess.get("motm", "").strip().lower()
            actual_winner = actual.get("Winner", "")
            actual_motm = actual.get("Man of the Match", "").strip().lower()
            if player_winner == actual_winner:
                scores[guess["player"]] += 1
            if player_motm and player_motm == actual_motm:
                scores[guess["player"]] += 1
    return scores


def store_guesses(selected_date, form_data):
    date_key = selected_date.strftime("%Y-%m-%d")
    st.session_state.guesses.setdefault(date_key, {})

    for key, value in form_data.items():
        player, match_id, field = key.split("|")
        match_id = int(match_id)
        st.session_state.guesses[date_key].setdefault(match_id, {"player": player})
        st.session_state.guesses[date_key][match_id][field] = value


# Scoreboard with artistic cards
score_map = calculate_scoreboard()
col1, col2, col3 = st.columns(3)
for i, (player, points) in enumerate(sorted(score_map.items(), key=lambda x: -x[1])):
    with [col1, col2, col3][i % 3]:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{player}</h3>
            <h1>{points}</h1>
            <p>Points</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("## 🎯 Submit Guesses")

valid_min = get_today()
valid_max = get_max_vote_date()
selected_date = st.date_input(
    "Select match date", value=valid_min, min_value=valid_min, max_value=valid_max, label_visibility="collapsed"
)

matches_today = get_match_by_date(selected_date)
if not matches_today:
    st.info("🌙 No matches on this date. Choose another.")
else:
    st.markdown(f"### 📅 Matches on {selected_date.strftime('%B %d, %Y')}")
    with st.form("guess_form"):
        st.markdown("**Enter your predictions below:**")
        for player in players:
            with st.expander(f"👤 {player}'s Guesses"):
                for match in matches_today:
                    match_id = match["Match #"]
                    existing_guess = st.session_state.guesses.get(selected_date.isoformat(), {}).get(match_id, {})
                    col1, col2 = st.columns(2)
                    with col1:
                        winner = st.selectbox(
                            f"🏆 Winner: {match['Team 1']} vs {match['Team 2']}",
                            options=["", match["Team 1"], match["Team 2"]],
                            index=0 if existing_guess.get("winner") == "" else (1 if existing_guess.get("winner") == match["Team 1"] else 2),
                            key=f"{player}|{match_id}|winner"
                        )
                    with col2:
                        motm = st.text_input(
                            "⭐ Man of the Match",
                            value=existing_guess.get("motm", ""),
                            placeholder="Player name",
                            key=f"{player}|{match_id}|motm"
                        )

        submitted = st.form_submit_button("✨ Save Guesses")
        if submitted:
            form_data = {}
            for player in players:
                for match in matches_today:
                    match_id = match["Match #"]
                    winner_key = f"{player}|{match_id}|winner"
                    motm_key = f"{player}|{match_id}|motm"
                    form_data[winner_key] = st.session_state.get(winner_key, "")
                    form_data[motm_key] = st.session_state.get(motm_key, "")
            store_guesses(selected_date, form_data)
            st.success("🎉 Guesses saved successfully!")

# Overview section
st.markdown("---")
st.markdown("## 📋 Guess Overview")
if not st.session_state.guesses:
    st.info("📝 No guesses yet. Start predicting!")
else:
    overview_df = pd.DataFrame([
        {
            "Date": date_key,
            "Match": match_id,
            "Player": guess.get("player"),
            "Winner": guess.get("winner", ""),
            "MOTM": guess.get("motm", "")
        }
        for date_key, values in st.session_state.guesses.items()
        for match_id, guess in values.items()
    ])
    st.dataframe(overview_df, use_container_width=True, hide_index=True)




