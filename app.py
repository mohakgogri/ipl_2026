import streamlit as st

st.set_page_config(
    page_title="IPL 2026 Dashboard",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 IPL 2026 Dashboard")
st.write("Welcome to the IPL 2026 Dashboard. Use the sidebar to navigate to different sections.")

# Home page content
st.markdown("""
### Welcome!

This dashboard provides comprehensive information about:
- **Schedule**: View upcoming matches
- **Results**: Check match results and statistics

Navigate using the sidebar menu to explore more!
""")

