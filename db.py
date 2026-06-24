# db.py
import streamlit as st

@st.cache_resource
def get_global_db():
    # 서버가 켜져 있는 동안 이 딕셔너리 하나를 모든 페이지와 유저가 공유합니다.
    return {
        "participants": [],
        "matches": [],
        "chat_history": []
    }