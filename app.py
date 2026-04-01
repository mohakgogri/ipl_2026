import streamlit as st
from datetime import datetime, date
from data import players, schedule_data, results_data, results_by_match, matches_by_date, get_today, get_max_vote_date
import pandas as pd

st.set_page_config(
    page_title="IPL 2026 Dashboard",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 IPL 2026 Game Guess League")

st.markdown("## 1. Latest Updated Scoreboard")

if "guesses" not in st.session_state:
    st.session_state.guesses = {}

if "message" not in st.session_state:
    st.session_state.message = ""

# helper functions

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
        # key format: player|match|type
        player, match_id, field = key.split("|")
        match_id = int(match_id)
        st.session_state.guesses[date_key].setdefault(match_id, {"player": player})
        st.session_state.guesses[date_key][match_id][field] = value


# Dashboard scoreboard
score_map = calculate_scoreboard()
score_df = pd.DataFrame(
    [
        {"Player": p, "Points": score_map[p]}
        for p in sorted(score_map, key=lambda x: -score_map[x])
    ]
)

st.dataframe(score_df, use_container_width=True, hide_index=True)

st.markdown("---")

st.markdown("## 2. Add Guesses (up to 3 days in advance)")

valid_min = get_today()
valid_max = get_max_vote_date()
selected_date = st.date_input(
    "Select match date for your guesses", value=valid_min, min_value=valid_min, max_value=valid_max
)

st.write(f"Voting window: {valid_min.isoformat()} to {valid_max.isoformat()} (inclusive)")

matches_today = get_match_by_date(selected_date)
if not matches_today:
    st.info("No IPL games scheduled for selected date. Try another date in range.")
else:
    st.markdown(f"### Matches on {selected_date.isoformat()}")
    form = st.form("guess_form")
    filled = {}

    for player in players:
        with form.expander(f"Add/update guesses for {player}"):
            for match in matches_today:
                match_id = match["Match #"]
                key_winner = f"{player}|{match_id}|winner"
                key_motm = f"{player}|{match_id}|motm"
                existing_guess = st.session_state.guesses.get(selected_date.isoformat(), {}).get(match_id, {})

                default_winner = existing_guess.get("winner", "")
                default_motm = existing_guess.get("motm", "")

                winner = st.selectbox(
                    f"{player} guesses winner for Match {match_id} ({match['Team 1']} vs {match['Team 2']})",
                    options=["", match["Team 1"], match["Team 2"]],
                    index=0 if default_winner == "" else (1 if default_winner == match["Team 1"] else 2),
                    key=f"{key_winner}-input"
                )
                motm = st.text_input(
                    f"{player} guesses Man of the Match",
                    value=default_motm,
                    placeholder="Type player name",
                    key=f"{key_motm}-input"
                )

                filled[f"{player}|{match_id}|winner"] = winner
                filled[f"{player}|{match_id}|motm"] = motm

    submit = form.form_submit_button("Save all guesses")

    if submit:
        store_guesses(selected_date, filled)
        st.session_state.message = f"Guesses saved for {selected_date.isoformat()}."
        st.success(st.session_state.message)

# Current saved guesses display
st.markdown("---")
st.subheader("Saved guesses overview")
if not st.session_state.guesses:
    st.info("No guesses submitted yet.")
else:
    overview_rows = []
    for date_key, values in st.session_state.guesses.items():
        for match_id, guess in values.items():
            overview_rows.append(
                {
                    "Date": date_key,
                    "Match #": match_id,
                    "Player": guess.get("player"),
                    "Predicted Winner": guess.get("winner", ""),
                    "Predicted MOTM": guess.get("motm", ""),
                }
            )
    st.dataframe(pd.DataFrame(overview_rows), use_container_width=True, hide_index=True)



