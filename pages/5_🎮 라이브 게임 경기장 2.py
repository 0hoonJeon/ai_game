import streamlit as st

st.set_page_config(page_title="vampire_survival", layout="wide")

st.title("👻 vampire_survival")

# 게임 화면을 불러옵니다
st.iframe("./static/vampire_survival.html", height=800)
