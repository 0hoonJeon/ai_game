import streamlit as st
import pandas as pd
import random

# 무조건 와이드 레이아웃 적용
st.set_page_config(page_title="참가자 명단 및 대진표", page_icon="🏆", layout="wide")

st.title("🏆 대회 참가자 라인업 & 대진표 생성")
st.markdown("현재까지 등록된 사이버 듀얼 테트리스 챔피언십 참가자 명단을 확인하고, 공식 대진표를 추첨합니다.")

st.divider()

# 1. 참가자 데이터 확인 (예외 처리)
if 'participants' not in st.session_state or len(st.session_state['participants']) == 0:
    st.warning("🚨 아직 참가 신청한 선수가 없습니다. 좌측 '대회 신청' 페이지에서 먼저 참가자를 등록해주세요.")
    st.stop()

participants = st.session_state['participants']
player_names = [p['닉네임'] for p in participants]

# ── [섹션 1] 대회 참가자 전격 공개 ──
st.subheader(f"👥 공식 참가자 라인업 (총 {len(player_names)}명)")

# 와이드 레이아웃의 장점을 살려 좌측엔 표, 우측엔 티어별 통계를 배치
col_table, col_stat = st.columns([2, 1])

with col_table:
    df = pd.DataFrame(participants)
    # 연락처(이메일)는 가리고 출력
    display_df = df.drop(columns=['연락처']) if '연락처' in df.columns else df
    st.dataframe(display_df, use_container_width=True, hide_index=True)

with col_stat:
    st.markdown("**📊 티어별 참가자 분포**")
    if '티어' in df.columns:
        tier_counts = df['티어'].value_counts()
        st.bar_chart(tier_counts)
    else:
        st.info("티어 데이터가 없습니다.")

st.divider()

# ── [섹션 2] 대진표 생성 및 시각화 ──
st.subheader("🎲 공식 대진표 추첨")

# 세션 상태 초기화
if 'matches' not in st.session_state:
    st.session_state['matches'] = []

# 버튼 디자인 (와이드 화면 중앙 배치 느낌을 위해 columns 사용)
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
with btn_col2:
    if st.button("🔥 무작위 대진표 추첨 시작 🔥", use_container_width=True, type="primary"):
        if len(player_names) < 2:
            st.error("대진표를 생성하려면 최소 2명 이상의 참가자가 필요합니다.")
        else:
            shuffled_players = player_names.copy()
            random.shuffle(shuffled_players)
            
            matches = []
            for i in range(0, len(shuffled_players), 2):
                p1 = shuffled_players[i]
                p2 = shuffled_players[i+1] if i+1 < len(shuffled_players) else "부전승 (Bye)"
                matches.append((p1, p2))
                
            st.session_state['matches'] = matches
            st.success("대진표 생성이 완료되었습니다!")
            st.balloons()

# ── [섹션 3] 매치업 카드 뷰 (와이드 화면 최적화) ──
if st.session_state['matches']:
    st.markdown("### ⚔️ 공식 매치업")
    
    matches = st.session_state['matches']
    
    # 한 줄에 4개의 매치업 카드를 꽉 채워서 배치 (와이드 레이아웃 최적화)
    cols = st.columns(4)
    
    for idx, match in enumerate(matches):
        col_idx = idx % 4
        with cols[col_idx]:
            # Streamlit 컨테이너에 테두리를 주어 게임 매치업 카드 느낌 연출
            with st.container(border=True):
                st.caption(f"Match {idx + 1}")
                st.markdown(f"<h4 style='text-align: center; color: #38bdf8;'>{match[0]}</h4>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; font-weight: bold; color: #64748b;'>VS</p>", unsafe_allow_html=True)
                
                if match[1] == "부전승 (Bye)":
                    st.markdown(f"<h4 style='text-align: center; color: #64748b;'>{match[1]}</h4>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<h4 style='text-align: center; color: #f43f5e;'>{match[1]}</h4>", unsafe_allow_html=True)