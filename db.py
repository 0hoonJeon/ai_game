# db.py
import streamlit as st

# @st.cache_resource는 서버가 재시작되지 않는 한, 
# 이 데이터(딕셔너리)를 전역 변수처럼 서버 메모리에 고정합니다.
@st.cache_resource
def get_global_db():
    return {
        "participants": [],  # 대회 신청자 명단
        "matches": [],       # 실시간 대진표 (리스트 형태)
        "chat_history": []   # 채팅 로그 (최대 100개 제한 등)
    }