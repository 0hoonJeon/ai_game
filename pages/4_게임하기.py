import streamlit as st

st.set_page_config(page_title="실시간 숨바꼭질", layout="wide")

st.title("👻 실시간 3D 숨바꼭질")

# 게임 화면을 불러옵니다
st.iframe("./static/hide_and_seek.html", height=600)

st.markdown("""
### 🎮 게임 안내
* **3D 시점:** 현재 플레이어의 시점에서 맵을 바라봅니다.
* **실시간 동기화:** 조만간 Firebase를 연동하여 술래와 숨는 자의 위치를 실시간으로 뿌릴 예정입니다.
""")