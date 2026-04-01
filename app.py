import streamlit as st
import random

st.set_page_config(
    page_title="IPL 2026 Dashboard",
    page_icon="🏏",
    layout="wide"
)

st.title("We only belive in Jassi Bhai")

fans = ["Rahul", "Manogna", "Shishir", "Ashay", "Surya", "Mohak"]
random.shuffle(fans)

st.markdown("---")
st.markdown(f"Fans : {', '.join(fans)}")


