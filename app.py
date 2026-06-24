import streamlit as st
import time
from datetime import datetime
from db import get_global_db

st.set_page_config(page_title="사이버 듀얼 토너먼트", page_icon="🏆", layout="wide")

global_db = get_global_db()

# ── [상단 헤더] ──
st.title("⚡ Cyber-Duel Tetris Tournament")
st.markdown("### 제 1회 공식 테트리스 챔피언십에 오신 것을 환영합니다!")
st.divider()

# ── [메인 레이아웃: 대시보드] ──
col1, col2, col3 = st.columns([1, 1, 1])

# 1. 대회 카운트다운
with col1:
    st.subheader("⏳ 대회까지 남은 시간")
    target_date = datetime(2026, 7, 5, 14, 0, 0)
    now = datetime.now()
    delta = target_date - now
    
    if delta.total_seconds() > 0:
        days = delta.days
        hours = delta.seconds // 3600
        mins = (delta.seconds % 3600) // 60
        st.metric("D-Day 카운트다운", f"{days}일 {hours}시간 {mins}분")
    else:
        st.success("🎉 대회가 지금 진행 중입니다!")

# 2. 실시간 상황 요약
with col2:
    st.subheader("📊 대회 현황 요약")
    st.metric("총 참가 선수", f"{len(global_db['participants'])} 명")
    st.metric("진행 중인 매치", f"{len(global_db['matches'])} 개")

# 3. 대회 공지사항
with col3:
    st.subheader("📢 주요 공지")
    st.markdown("""
    * **선수 인증:** 입장 시 `PLAYER2026` 코드 필수
    * **매너 규정:** 채팅창 욕설 금지 (적발 시 실격)
    * **결승전:** 우승자에게는 공식 트로피 수여
    """)

st.divider()

# ── [하단: 메인 컨텐츠 바로가기] ──
st.subheader("🚀 대회 센터 바로가기")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("📝 대회 참가 신청하기", use_container_width=True):
        st.switch_page("pages/1_📝_대회_신청.py")
with c2:
    if st.button("🏆 대진표 및 결과 확인", use_container_width=True):
        st.switch_page("pages/2_🏆_대진표_및_참가자.py")
with c3:
    if st.button("🎮 라이브 게임 경기장 입장", use_container_width=True):
        st.switch_page("pages/3_🎮_라이브_게임.py")

# ── [바닥글] ──
st.divider()
st.caption("© 2026 Cyber-Duel Tournament Platform | Powered by Streamlit")