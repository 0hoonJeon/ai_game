import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from db import get_global_db
from pathlib import Path

# 페이지 설정
st.set_page_config(page_title="라이브 게임 중계", page_icon="🎮", layout="wide")

global_db = get_global_db()

# 세션 상태 초기화
if 'player_auth' not in st.session_state: st.session_state['player_auth'] = False
if 'spectator_profile' not in st.session_state: st.session_state['spectator_profile'] = None

st.title("🎮 라이브 게임 경기장")
st.markdown("선수는 인증 후 파일을 다운로드하여 경기를 진행하고, 관전자는 실시간 채팅으로 응원하세요!")
st.divider()

mode = st.radio("역할 선택:", ["👀 관전 및 응원 모드", "🎮 대회 선수 (인증 필요)"], horizontal=True)

# ── [1. 선수 모드] ──
# if mode == "🎮 대회 선수 (인증 필요)":
if not st.session_state['player_auth']:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.subheader("🔐 선수 전용 입장")
            auth_key = st.text_input("선수 인증 키", type="password")
            if st.button("입장하기", type="primary", use_container_width=True):
                if auth_key == "PLAYER2026":
                    st.session_state['player_auth'] = True
                    st.rerun()
                else: st.error("❌ 인증 키가 일치하지 않습니다.")
else:
    st.success("✅ 선수 인증 완료! 아래 버튼을 눌러 게임 파일을 다운로드하세요.")
    
    # 파일 경로 확인
    html_path = Path("static/cyber_duel_tetris_multi_v7.html")
    if html_path.exists():
        with open(html_path, "rb") as f:
            st.download_button(
                label="🎮 테트리스 게임 다운로드 (실행용)",
                data=f,
                file_name="tetris.html",
                mime="text/html",
                type="primary"
            )
    else:
        st.error(f"🚨 게임 파일을 찾을 수 없습니다: {html_path}")

# ── [2. 관전 및 채팅 모드] ──
# elif mode == "👀 관전 및 응원 모드":
if st.session_state['spectator_profile'] is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.subheader("📣 응원석 입장")
            player_list = [p['닉네임'] for p in global_db['participants']]
            nickname = st.text_input("사용할 채팅 닉네임", max_chars=10)
            support_team = st.selectbox("응원 선수", ["선택 안 함"] + player_list)
            if st.button("입장", type="primary", use_container_width=True):
                if nickname:
                    st.session_state['spectator_profile'] = {"nickname": nickname, "team": support_team}
                    st.rerun()
else:
    profile = st.session_state['spectator_profile']
    col_game, col_chat = st.columns([3, 1])
    
    with col_game:
        st.caption("💡 게임 화면 내부의 버튼을 눌러 관전하세요.")
        # 경로 수정: static 파일을 정확히 가리킴
        st.iframe("./static/cyber_duel_tetris_multi_v7.html", height=800)
                
    with col_chat:
        st.subheader("💬 라이브 채팅")
        
        @st.fragment(run_every=2)
        def chat_display():
            with st.container(height=600):
                for msg in global_db['chat_history']:
                    badge = f"[{msg['team']}] " if msg['team'] != "선택 안 함" else ""
                    icon = "👤" if msg['nickname'] == profile['nickname'] else "💬"
                    st.chat_message("user", avatar=icon).write(f"**{badge}{msg['nickname']}**: {msg['text']}")
        
        chat_display()
        
        user_input = st.chat_input("응원 메시지 입력")
        if user_input:
            global_db['chat_history'].append({
                "nickname": profile['nickname'], 
                "team": profile['team'], 
                "text": user_input
            })
            if len(global_db['chat_history']) > 100: global_db['chat_history'].pop(0)
            st.rerun()