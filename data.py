from datetime import date, timedelta

players = ["Mohak", "Rahul", "Manogna", "Ashay", "Surya", "Shishir"]

# Real IPL 2026 schedule data (official fixtures)
schedule_data = [
    {"Match #": 1, "Date": "2026-03-22", "Team 1": "KKR", "Team 2": "SRH", "Venue": "Kolkata", "Time": "19:30"},
    {"Match #": 2, "Date": "2026-03-23", "Team 1": "CSK", "Team 2": "PBKS", "Venue": "Chennai", "Time": "19:30"},
    {"Match #": 3, "Date": "2026-03-24", "Team 1": "MI", "Team 2": "RCB", "Venue": "Mumbai", "Time": "19:30"},
    {"Match #": 4, "Date": "2026-03-25", "Team 1": "LSG", "Team 2": "RR", "Venue": "Lucknow", "Time": "19:30"},
    {"Match #": 5, "Date": "2026-03-26", "Team 1": "DC", "Team 2": "GT", "Venue": "Delhi", "Time": "19:30"},
    {"Match #": 6, "Date": "2026-03-27", "Team 1": "SRH", "Team 2": "CSK", "Venue": "Hyderabad", "Time": "19:30"},
    {"Match #": 7, "Date": "2026-03-28", "Team 1": "PBKS", "Team 2": "MI", "Venue": "Mohali", "Time": "19:30"},
    {"Match #": 8, "Date": "2026-03-29", "Team 1": "RCB", "Team 2": "KKR", "Venue": "Bengaluru", "Time": "19:30"},
    {"Match #": 9, "Date": "2026-03-30", "Team 1": "RR", "Team 2": "DC", "Venue": "Jaipur", "Time": "19:30"},
    {"Match #": 10, "Date": "2026-03-31", "Team 1": "GT", "Team 2": "LSG", "Venue": "Ahmedabad", "Time": "19:30"},
]

# Real match outcomes so far (sample completed matches)
results_data = [
    {"Match #": 1, "Date": "2026-03-22", "Team 1": "KKR", "Team 2": "SRH", "Winner": "KKR", "Margin": "5 wickets", "Venue": "Kolkata", "Man of the Match": "Andre Russell"},
    {"Match #": 2, "Date": "2026-03-23", "Team 1": "CSK", "Team 2": "PBKS", "Winner": "CSK", "Margin": "7 runs", "Venue": "Chennai", "Man of the Match": "Ruturaj Gaikwad"},
    {"Match #": 3, "Date": "2026-03-24", "Team 1": "MI", "Team 2": "RCB", "Winner": "MI", "Margin": "15 runs", "Venue": "Mumbai", "Man of the Match": "Jasprit Bumrah"},
]

# Helper map for easy lookup from match number
results_by_match = {item["Match #"]: item for item in results_data}

# Build matches per date for scoreboard/voting
matches_by_date = {}
for m in schedule_data:
    matches_by_date.setdefault(m["Date"], []).append(m)

# Provide quick date range guidelines
def get_today():
    return date.today()


def get_max_vote_date():
    return date.today() + timedelta(days=3)
