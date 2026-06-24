import streamlit as st
import streamlit.components.v1 as components

# 무조건 와이드 레이아웃
st.set_page_config(page_title="라이브 게임 중계", page_icon="🎮", layout="wide")

st.title("🎮 라이브 게임 경기장")
st.markdown("선수들은 방을 만들어 경기를 진행하고, 관전자는 진행 중인 방에 들어가 실시간으로 경기를 지켜볼 수 있습니다.")
st.divider()

# 와이드 화면을 2개의 단으로 분리 (좌측: 정보 패널 / 우측: 실제 게임 화면)
col_info, col_game = st.columns([1, 2.5])

# ── [좌측 패널: 대회 정보 및 조작법] ──
with col_info:
    # 1. 조작법 및 팁 안내
    with st.container(border=True):
        st.subheader("🕹️ 게임 가이드")
        st.info("💡 **중요:** 게임 방향키가 작동하지 않으면, **게임 화면 빈 공간을 한 번 클릭**해서 포커스를 맞춰주세요!")
        st.markdown("""
        * **이동:** 방향키 ⬅️ ➡️ ⬇️
        * **회전:** 방향키 ⬆️
        * **하드 드롭:** 스페이스바 (단번에 내리기)
        * **관전 모드:** 진행 중인 방의 `👀 관전하기` 버튼 클릭
        """)
    
    # 2. 현재 대회 진행 상황 연동 (대진표 페이지 데이터)
    with st.container(border=True):
        st.subheader("⚔️ 오늘의 매치업 현황")
        if 'base_matches' in st.session_state and st.session_state['base_matches']:
            st.write("대기 중인 매치업 리스트입니다.")
            for idx, match in enumerate(st.session_state['base_matches']):
                # 부전승 매치는 흐리게 처리
                if "부전승 (Bye)" in match:
                    st.caption(f"Match {idx+1}: {match[0]} vs {match[1]} (자동 진출)")
                else:
                    st.markdown(f"**Match {idx+1}:** 🔵 {match[0]} **VS** 🔴 {match[1]}")
        elif 'participants' in st.session_state and st.session_state['participants']:
            st.write(f"현재 등록된 대기 선수: **{len(st.session_state['participants'])}명**")
            st.caption("아직 대진표가 추첨되지 않았습니다.")
        else:
            st.warning("진행 중인 공식 대회가 없습니다.")

# ── [우측 패널: 테트리스 HTML 렌더링] ──
with col_game:
    with st.container(border=True):
        try:
            # 절대 HTML을 수정하지 않고, 기존에 저장된 파일을 그대로 읽어옵니다.
            with open("tetris.html", "r", encoding="utf-8") as f:
                tetris_html = f.read()
            
            # height를 800 정도로 넉넉하게 주어 스크롤 바운스 없이 쾌적하게 렌더링
            components.html(tetris_html, height=800, scrolling=False)
            
        except FileNotFoundError:
            st.error("🚨 `tetris.html` 파일을 찾을 수 없습니다. 파이썬 코드와 같은 폴더에 파일이 있는지 확인해 주세요.")