import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

st.set_page_config(page_title="라이브 게임 중계", page_icon="🎮", layout="wide")

from db import get_global_db
global_db = get_global_db()

if 'player_auth' not in st.session_state: st.session_state['player_auth'] = False
if 'spectator_profile' not in st.session_state: st.session_state['spectator_profile'] = None

st.title("🎮 라이브 게임 경기장")
st.divider()

mode = st.radio("당신의 역할은 무엇인가요?", ["👀 관전 및 응원 모드", "🎮 대회 선수 (인증 필요)"], horizontal=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── 🎮 [선수 모드] ──
if mode == "🎮 대회 선수 (인증 필요)":
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
        st.success("✅ 선수 인증이 완료되었습니다.")
        col_space1, col_game, col_space2 = st.columns([1, 4, 1])
        with col_game:
            with st.container(border=True):
                # 💡 핵심 수정 포인트: html 코드를 읽는 대신, static 서버의 진짜 URL을 띄워 Firebase 차단을 우회합니다!
                components.iframe("/app/static/tetris.html", height=800, scrolling=False)

# ── 👀 [관전 모드] ──
elif mode == "👀 관전 및 응원 모드":
    if st.session_state['spectator_profile'] is None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.container(border=True):
                st.subheader("📣 응원석 입장하기")
                player_list = [p['닉네임'] for p in global_db['participants']] if global_db['participants'] else ["현재 참가자 없음"]
                nickname = st.text_input("사용할 채팅 닉네임", max_chars=10)
                support_team = st.selectbox("응원 선수", ["선택 안 함"] + player_list)
                if st.button("입장", type="primary", use_container_width=True):
                    if nickname:
                        st.session_state['spectator_profile'] = {"nickname": nickname, "team": support_team}
                        st.rerun()
    else:
        profile = st.session_state['spectator_profile']
        col_info, col_game, col_chat = st.columns([1, 2, 1])
        
        with col_info:
            st.subheader("⚔️ 매치업 현황")
            @st.fragment(run_every=3)
            def realtime_bracket_view():
                with st.container(border=True):
                    if not global_db['matches']: st.caption("대진표 없음")
                    else:
                        for idx, match in enumerate(global_db['matches']):
                            st.markdown(f"**M{idx+1}:** {match[0]} VS {match[1]}")
            realtime_bracket_view()

        with col_game:
            st.caption("💡 `👀 관전하기` 버튼 클릭")
            with st.container(border=True):
                # 관전자 화면도 마찬가지로 iframe url 적용
                components.iframe("/app/static/tetris.html", height=700, scrolling=False)
                    
        with col_chat:
            st.subheader("💬 라이브 채팅")
            @st.fragment(run_every=2)
            def realtime_chat_view():
                with st.container(height=600):
                    for msg in global_db['chat_history']:
                        badge = f"[{msg['team']}] " if msg['team'] != "선택 안 함" else ""
                        icon = "👤" if msg['nickname'] == profile['nickname'] else "💬"
                        st.chat_message("user", avatar=icon).write(f"**{badge}{msg['nickname']}**: {msg['text']}")
            realtime_chat_view()
            
            user_input = st.chat_input("응원 메시지 입력")
            if user_input:
                global_db['chat_history'].append({"nickname": profile['nickname'], "team": profile['team'], "text": user_input})
                if len(global_db['chat_history']) > 100: global_db['chat_history'].pop(0)
                st.rerun()