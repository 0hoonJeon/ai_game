import streamlit as st

# 모든 접속자가 공유하는 실시간 인메모리 DB
@st.cache_resource
def get_global_db():
    return {
        "participants": [],  # 대회 신청자 명단
        "matches": [],       # 실시간 대진표 상황
        "chat_history": []   # 글로벌 채팅 내역
    }

global_db = get_global_db()
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

st.set_page_config(page_title="라이브 게임 중계", page_icon="🎮", layout="wide")

# ── [전역 글로벌 DB 불러오기] ──
@st.cache_resource
def get_global_db():
    return {
        "participants": [],
        "matches": [],
        "chat_history": []
    }
global_db = get_global_db()

if 'player_auth' not in st.session_state:
    st.session_state['player_auth'] = False
if 'spectator_profile' not in st.session_state:
    st.session_state['spectator_profile'] = None

st.title("🎮 라이브 게임 경기장")
st.divider()

mode = st.radio("당신의 역할은 무엇인가요?", ["👀 관전 및 응원 모드", "🎮 대회 선수 (인증 필요)"], horizontal=True)
st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 🎮 [선수 모드]
# ==========================================
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
                    else:
                        st.error("❌ 인증 키가 일치하지 않습니다.")
    else:
        st.success("✅ 선수 인증이 완료되었습니다.")
        col_space1, col_game, col_space2 = st.columns([1, 4, 1])
        with col_game:
            with st.container(border=True):
                try:
                    with open("tetris.html", "r", encoding="utf-8") as f:
                        components.html(f.read(), height=800, scrolling=False)
                except FileNotFoundError:
                    st.error("🚨 `tetris.html` 파일을 찾을 수 없습니다.")

# ==========================================
# 👀 [관전 및 응원 모드]
# ==========================================
elif mode == "👀 관전 및 응원 모드":
    # ── 관전자 입장 전 ──
    if st.session_state['spectator_profile'] is None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.container(border=True):
                st.subheader("📣 응원석 입장하기")
                
                # 글로벌 DB에서 참가자 목록 가져오기
                player_list = [p['닉네임'] for p in global_db['participants']] if global_db['participants'] else ["현재 참가자 없음"]
                
                nickname = st.text_input("사용할 채팅 닉네임", max_chars=10)
                support_team = st.selectbox("응원하는 선수를 선택하세요!", ["선택 안 함"] + player_list)
                
                if st.button("채팅방 입장", type="primary", use_container_width=True):
                    if not nickname:
                        st.warning("닉네임을 입력해주세요!")
                    else:
                        st.session_state['spectator_profile'] = {"nickname": nickname, "team": support_team}
                        st.rerun()
                        
    # ── 관전자 입장 후 (실시간 동기화 뷰) ──
    else:
        profile = st.session_state['spectator_profile']
        
        col_info, col_game, col_chat = st.columns([1, 2, 1])
        
        # 1️⃣ [좌측] 실시간 대진표 현황 (3초마다 자동 업데이트)
        with col_info:
            st.subheader("⚔️ 매치업 현황")
            
            @st.fragment(run_every=3) # 3초마다 이 함수 안의 UI만 갱신
            def realtime_bracket_view():
                with st.container(border=True):
                    if not global_db['matches']:
                        st.caption("아직 생성된 대진표가 없습니다.")
                    else:
                        for idx, match in enumerate(global_db['matches']):
                            st.markdown(f"**M{idx+1}:** {match[0]} VS {match[1]}")
                            
            realtime_bracket_view() # 프래그먼트 실행

        # 2️⃣ [중앙] 게임 화면
        with col_game:
            st.caption("💡 내부의 `👀 관전하기` 버튼을 눌러야 플레이어들의 화면이 보입니다.")
            with st.container(border=True):
                try:
                    with open("tetris.html", "r", encoding="utf-8") as f:
                        components.html(f.read(), height=700, scrolling=False)
                except FileNotFoundError:
                    st.error("🚨 `tetris.html` 파일을 찾을 수 없습니다.")
                    
        # 3️⃣ [우측] 실시간 채팅방 (2초마다 자동 업데이트)
        with col_chat:
            st.subheader("💬 라이브 채팅")
            
            # 채팅 출력 부분만 프래그먼트로 감싸서 입력창 포커스 증발 방지
            @st.fragment(run_every=2)
            def realtime_chat_view():
                chat_container = st.container(height=600)
                with chat_container:
                    if not global_db['chat_history']:
                        st.info("첫 메시지를 남겨보세요!")
                    else:
                        for msg in global_db['chat_history']:
                            team_badge = f"[{msg['team']}] " if msg['team'] != "선택 안 함" else ""
                            is_me = (msg['nickname'] == profile['nickname'])
                            st.chat_message("user", avatar="👤" if is_me else "💬").write(f"**{team_badge}{msg['nickname']}**: {msg['text']}")

            realtime_chat_view() # 프래그먼트 실행
            
            # 채팅 입력창 (입력 즉시 글로벌 DB에 꽂아넣고 화면을 1번 리로드)
            user_input = st.chat_input("응원 메시지 입력")
            if user_input:
                global_db['chat_history'].append({
                    "nickname": profile['nickname'],
                    "team": profile['team'],
                    "text": user_input,
                    "time": datetime.now().strftime("%H:%M:%S")
                })
                # 최대 100개까지만 유지
                if len(global_db['chat_history']) > 100:
                    global_db['chat_history'].pop(0)
                st.rerun()