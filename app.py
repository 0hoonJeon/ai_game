import streamlit as st
import pandas as pd
import random
from datetime import datetime

# ==========================================
# 1. 페이지 기본 설정 (가장 위에 위치해야 함)
# ==========================================
st.set_page_config(
    page_title="Cyber-Duel Tetris E-Sports",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이버펑크 느낌의 커스텀 CSS
st.markdown("""
    <style>
    .big-font { font-size: 40px !important; font-weight: 900; color: #38bdf8; }
    .neon-text { text-shadow: 0 0 10px #38bdf8, 0 0 20px #38bdf8; }
    .status-live { color: #f43f5e; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 가짜 데이터 생성 (나중에는 FastAPI에서 가져옴)
# ==========================================
def get_mock_leaderboard():
    data = {
        "순위": [1, 2, 3, 4, 5],
        "플레이어": ["Faker_Tetris", "BlockMaster", "CyberNinja", "DropIt", "NeonGhost"],
        "승점 (PT)": [1250, 1100, 950, 800, 780],
        "승률 (%)": [85.5, 78.0, 72.3, 65.1, 60.0],
        "공격 줄 수": [1420, 1100, 950, 840, 710],
        "폭탄 사용": [45, 32, 28, 15, 20]
    }
    return pd.DataFrame(data).set_index("순위")

def get_live_matches():
    return [
        {"id": "ROOM-101", "p1": "Faker_Tetris", "p2": "CyberNinja", "time": "05:12", "status": "PLAYING"},
        {"id": "ROOM-102", "p2": "BlockMaster", "p2": "DropIt", "time": "02:45", "status": "PLAYING"},
        {"id": "ROOM-103", "p1": "NeonGhost", "p2": "대기중...", "time": "-", "status": "WAITING"}
    ]

# ==========================================
# 3. 각 페이지별 함수 정의
# ==========================================

def page_home():
    st.markdown('<p class="big-font neon-text">⚡ Cyber-Duel Tetris E-Sports Portal</p>', unsafe_allow_html=True)
    st.write("사내 E-스포츠 대회 공식 포털에 오신 것을 환영합니다! 참가 등록, 실시간 랭킹 확인, 라이브 관전이 가능합니다.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("총 등록 참가자", "128 명", "+12명 (오늘)")
    col2.metric("현재 진행중인 매치", "2 개", "LIVE")
    col3.metric("누적 플레이 타임", "342 시간")
    
    st.divider()
    st.subheader("📢 주최측 공지사항")
    st.info("**[공지]** 32강 본선 대진표가 공개되었습니다. 대진표 탭을 확인해주세요! (일시: 이번주 금요일 18:00)")
    st.warning("**[안내]** 게임 접속 시 반드시 사내 이메일 계정으로 연동된 아이디를 사용해주시기 바랍니다.")

def page_live():
    st.title("📡 실시간 라이브 관전")
    st.write("현재 진행 중인 경기를 실시간으로 관전하고 응원하세요!")
    
    matches = get_live_matches()
    for match in matches:
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
            with col1:
                if match['status'] == 'PLAYING':
                    st.markdown('<span class="status-live">🔴 LIVE</span>', unsafe_allow_html=True)
                else:
                    st.write("🟢 WAITING")
            with col2:
                st.write(f"**{match['p1']}** 🆚 **{match['p2']}**")
            with col3:
                st.write(f"진행 시간: {match['time']}")
            with col4:
                if match['status'] == 'PLAYING':
                    # 버튼을 누르면 새 창에서 게임 화면(관전 모드) HTML을 띄운다고 가정
                    st.button("📺 관전하기", key=match['id'], type="primary")
            st.divider()

def page_leaderboard():
    st.title("🏆 명예의 전당 (리더보드)")
    st.write("현재 시즌의 최고 랭커들입니다. 상위 16명은 연말 챔피언십에 진출합니다.")
    
    df = get_mock_leaderboard()
    
    # 데이터프레임 시각화 (하이라이트 적용)
    st.dataframe(
        df.style.highlight_max(subset=['승점 (PT)', '승률 (%)', '공격 줄 수'], color='#10b981')
                .format({'승률 (%)': "{:.1f}%"}),
        use_container_width=True,
        height=250
    )
    
    # 통계 그래프
    st.subheader("📊 상위 5명 공격 지표")
    chart_data = df[['플레이어', '공격 줄 수', '폭탄 사용']].set_index('플레이어')
    st.bar_chart(chart_data)

def page_bracket():
    st.title("⚔️ 대회 대진표 (32강)")
    st.write("본선 진출자 대진표입니다.")
    
    # Streamlit으로 간단한 대진표 UI 구현 (Col expander 활용)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("16강")
        st.info("Match 1: Faker_Tetris vs Rookie99")
        st.info("Match 2: DropIt vs FastFingers")
        
    with col2:
        st.subheader("8강")
        st.warning("Match 17: (M1 승자) vs (M2 승자)")
        
    with col3:
        st.subheader("4강 (준결승)")
        st.error("Match 25: 대기중...")

def page_mypage():
    st.title("👤 마이페이지 & 참가 신청")
    
    tab1, tab2 = st.tabs(["내 프로필", "대회 참가 신청"])
    
    with tab1:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://api.dicebear.com/7.x/bottts/svg?seed=Faker_Tetris", width=150)
            st.subheader("Faker_Tetris")
            st.write("사속: 개발1팀")
        with col2:
            st.write("### 내 전적")
            st.metric("총 전적", "45전 30승 15패")
            st.write("최근 경기: 🟢승 🔴패 🟢승 🟢승 🟢승")
            
    with tab2:
        st.write("### E-스포츠 사내 대회 참가 신청")
        with st.form("join_form"):
            name = st.text_input("게임 닉네임")
            dept = st.selectbox("소속 부서", ["개발팀", "디자인팀", "기획팀", "경영지원팀"])
            motto = st.text_area("출사표 (한마디)")
            submit = st.form_submit_button("신청하기", type="primary")
            if submit:
                st.success(f"{name}님, 신청이 완료되었습니다! 행운을 빕니다.")

def page_admin():
    st.title("⚙️ 관리자 메뉴 (대회 운영)")
    st.write("진행 요원 및 서버 관리자 전용 메뉴입니다.")
    
    with st.expander("서버 상태 관리", expanded=True):
        st.metric("FastAPI 게임 서버 상태", "정상 가동 중 (UP)", delta="Ping: 12ms")
        col1, col2 = st.columns(2)
        col1.button("서버 재시작 (Restart)", type="primary")
        col2.button("전체 방 초기화 (Clear All)", type="secondary")
        
    with st.expander("대회 공지사항 발송"):
        notice = st.text_input("공지 내용 입력")
        if st.button("게임 내 팝업으로 전송"):
            st.success("접속 중인 모든 플레이어에게 공지사항을 전송했습니다!")

# ==========================================
# 4. 사이드바 라우팅 (메뉴 네비게이션)
# ==========================================
st.sidebar.markdown('## ⚡ E-Sports Portal')
menu = st.sidebar.radio(
    "메뉴 이동",
    ["🏠 홈", "📡 라이브 매치", "🏆 리더보드", "⚔️ 대진표", "👤 마이페이지", "⚙️ 대회 관리자"]
)

st.sidebar.divider()
st.sidebar.write("Logged in as: **Staff_01**")

# 메뉴 선택에 따라 해당 함수 실행
if menu == "🏠 홈":
    page_home()
elif menu == "📡 라이브 매치":
    page_live()
elif menu == "🏆 리더보드":
    page_leaderboard()
elif menu == "⚔️ 대진표":
    page_bracket()
elif menu == "👤 마이페이지":
    page_mypage()
elif menu == "⚙️ 대회 관리자":
    page_admin()