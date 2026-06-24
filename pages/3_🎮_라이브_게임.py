import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# ── [페이지 기본 설정] ──
st.set_page_config(page_title="라이브 게임 중계", page_icon="🎮", layout="wide")

# ── [전역 상태 관리 (DB 없는 글로벌 채팅방)] ──
# @st.cache_resource를 사용하면 서버가 켜져 있는 동안 모든 접속자가 이 리스트를 공유합니다!
@st.cache_resource
def get_global_chat():
    return []

chat_history = get_global_chat()

# ── [세션 상태 관리 (개인별 상태)] ──
if 'player_auth' not in st.session_state:
    st.session_state['player_auth'] = False
if 'spectator_profile' not in st.session_state:
    st.session_state['spectator_profile'] = None

# ── [상단 헤더] ──
st.title("🎮 라이브 게임 경기장")
st.markdown("선수는 인증 코드를 입력해 경기에 참가하고, 관전자는 응원하는 선수를 선택해 채팅에 참여하세요!")
st.divider()

# ── [역할 선택 (선수 vs 관전자)] ──
mode = st.radio("당신의 역할은 무엇인가요?", ["👀 관전 및 응원 모드", "🎮 대회 선수 (인증 필요)"], horizontal=True)
st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 1. 🎮 대회 선수 모드
# ==========================================
if mode == "🎮 대회 선수 (인증 필요)":
    if not st.session_state['player_auth']:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.container(border=True):
                st.subheader("🔐 선수 전용 입장")
                st.info("💡 대회 주최자에게 발급받은 선수 인증 키를 입력해야 게임을 조작할 수 있습니다.")
                # 예시 인증키: PLAYER2026
                auth_key = st.text_input("선수 인증 키", type="password")
                
                if st.button("입장하기", type="primary", use_container_width=True):
                    if auth_key == "PLAYER2026":
                        st.session_state['player_auth'] = True
                        st.success("인증 완료! 게임 컨트롤 권한이 부여되었습니다.")
                        st.rerun()
                    else:
                        st.error("❌ 인증 키가 일치하지 않습니다.")
    else:
        st.success("✅ 선수 인증이 완료되었습니다. 아래 화면에서 방을 만들거나 참여하세요.")
        if st.button("🚪 선수 로그아웃"):
            st.session_state['player_auth'] = False
            st.rerun()
            
        # HTML 렌더링 (가운데 정렬 느낌으로 넉넉하게)
        col_space1, col_game, col_space2 = st.columns([1, 4, 1])
        with col_game:
            with st.container(border=True):
                try:
                    with open("tetris.html", "r", encoding="utf-8") as f:
                        components.html(f.read(), height=800, scrolling=False)
                except FileNotFoundError:
                    st.error("🚨 `tetris.html` 파일을 찾을 수 없습니다.")

# ==========================================
# 2. 👀 관전 및 응원 모드
# ==========================================
elif mode == "👀 관전 및 응원 모드":
    # 관전자 프로필이 없는 경우 (입장 전)
    if st.session_state['spectator_profile'] is None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.container(border=True):
                st.subheader("📣 응원석 입장하기")
                
                # 대진표 페이지에서 참가자 목록을 가져옴 (없으면 기본값)
                if 'participants' in st.session_state and st.session_state['participants']:
                    player_list = [p['닉네임'] for p in st.session_state['participants']]
                else:
                    player_list = ["테트리스장인", "고인물", "초보자"] # 테스트용 기본값
                
                nickname = st.text_input("사용할 채팅 닉네임", max_chars=10)
                support_team = st.selectbox("응원하는 선수를 선택하세요!", ["선택 안 함"] + player_list)
                
                if st.button("채팅방 입장", type="primary", use_container_width=True):
                    if not nickname:
                        st.warning("닉네임을 입력해주세요!")
                    else:
                        st.session_state['spectator_profile'] = {
                            "nickname": nickname,
                            "team": support_team
                        }
                        st.rerun()
                        
    # 관전자 프로필 설정 완료 (입장 후)
    else:
        profile = st.session_state['spectator_profile']
        st.success(f"🎉 **{profile['nickname']}**님 환영합니다! (응원 선수: **{profile['team']}**)")
        
        # 화면을 2분할: 좌측(게임 화면) 70%, 우측(채팅방) 30%
        col_game, col_chat = st.columns([2.5, 1])
        
        # [좌측] 게임 관전 화면
        with col_game:
            with st.container(border=True):
                st.caption("💡 게임 화면 내부의 `👀 관전하기` 버튼을 눌러야 플레이어들의 화면이 보입니다.")
                try:
                    with open("tetris.html", "r", encoding="utf-8") as f:
                        components.html(f.read(), height=700, scrolling=False)
                except FileNotFoundError:
                    st.error("🚨 `tetris.html` 파일을 찾을 수 없습니다.")
                    
        # [우측] 글로벌 실시간 채팅방
        with col_chat:
            st.markdown(f"### 💬 응원 채팅방")
            
            # 채팅 새로고침 버튼
            if st.button("🔄 최신 메시지 불러오기", use_container_width=True):
                st.rerun()
                
            # 채팅 내역을 보여주는 박스 (스크롤 가능하게 height 지정)
            chat_container = st.container(height=550)
            
            with chat_container:
                if not chat_history:
                    st.info("아직 채팅이 없습니다. 첫 번째 응원의 메시지를 남겨보세요!")
                else:
                    # 최신 메시지가 아래로 가도록 출력
                    for msg in chat_history:
                        # 응원하는 팀에 따라 배지(Badge) 색상 다르게 표시
                        team_badge = f"[{msg['team']}]" if msg['team'] != "선택 안 함" else ""
                        
                        # 내가 쓴 글인지 남이 쓴 글인지에 따라 아바타 다르게 적용
                        is_me = (msg['nickname'] == profile['nickname'])
                        avatar = "👤" if is_me else "💬"
                        
                        with st.chat_message("user", avatar=avatar):
                            st.markdown(f"**{team_badge} {msg['nickname']}**: {msg['text']}")
                            st.caption(msg['time'])

            # 채팅 입력창 (입력 시 자동으로 화면 리로드되며 채팅 추가됨)
            user_input = st.chat_input("응원의 메시지를 입력하세요!")
            if user_input:
                new_message = {
                    "nickname": profile['nickname'],
                    "team": profile['team'],
                    "text": user_input,
                    "time": datetime.now().strftime("%H:%M:%S")
                }
                chat_history.append(new_message)
                # 채팅창 길이 유지 (최대 50개)
                if len(chat_history) > 50:
                    chat_history.pop(0)
                st.rerun()