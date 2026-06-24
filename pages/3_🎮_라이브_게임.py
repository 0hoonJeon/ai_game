import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정 (게임을 넓게 보기 위해 wide 레이아웃 사용)
st.set_page_config(page_title="라이브 게임 - 사이버 듀얼 테트리스", layout="wide")

st.title("🎮 라이브 게임 중계: 사이버 듀얼 테트리스")
st.markdown("방을 만들거나 참가하여 상대방과 실시간으로 대결하세요!")

st.divider()

# tetris.html 파일을 읽어와서 화면에 렌더링
try:
    with open("tetris.html", "r", encoding="utf-8") as f:
        tetris_code = f.read()
    
    # height를 넉넉하게 주어 스크롤 없이 게임을 즐길 수 있게 설정
    components.html(tetris_code, height=900, scrolling=True)
    
except FileNotFoundError:
    st.error("⚠️ 'tetris.html' 파일을 찾을 수 없습니다. 경로를 다시 확인해주세요.")