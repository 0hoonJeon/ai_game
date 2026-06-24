import streamlit as st
import pandas as pd
import random
import math

st.set_page_config(page_title="참가자 및 대진표", page_icon="🏆", layout="wide")

st.title("🏆 대회 참가자 라인업 & 대진표")
st.markdown("공식 참가자를 확인하고, 토너먼트 룰(부전승 포함)에 맞춘 대진표를 추첨합니다.")
st.divider()

if 'participants' not in st.session_state or len(st.session_state['participants']) == 0:
    st.warning("🚨 아직 참가 신청한 선수가 없습니다.")
    st.stop()

participants = st.session_state['participants']
player_names = [p['닉네임'] for p in participants]

# ── [섹션 1] 참가자 공개 ──
with st.expander(f"👥 공식 참가자 명단 열어보기 (총 {len(player_names)}명)", expanded=False):
    df = pd.DataFrame(participants)
    display_df = df.drop(columns=['연락처']) if '연락처' in df.columns else df
    st.dataframe(display_df, use_container_width=True, hide_index=True)

st.subheader("🎲 공식 토너먼트 대진표")

# ── [토너먼트 알고리즘 (부전승 계산)] ──
# 현재 인원보다 큰 가장 가까운 2의 제곱수 구하기 (예: 14명 -> 16강)
next_pow2 = 2 ** math.ceil(math.log2(len(player_names))) if len(player_names) > 1 else 2
num_byes = next_pow2 - len(player_names)

st.info(f"💡 **토너먼트 정보:** 총 {len(player_names)}명 참가 → **{next_pow2}강 대진표** 기준 생성 (부전승 {num_byes}명 포함)")

# 버튼을 중앙에 예쁘게 배치
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    if st.button("🔥 무작위 대진표 추첨 시작 🔥", use_container_width=True, type="primary"):
        # 참가자 명단에 부전승(Bye) 추가 후 섞기
        padded_players = player_names.copy() + ["부전승 (Bye)"] * num_byes
        random.shuffle(padded_players)
        
        # 2명씩 매칭
        matches = [(padded_players[i], padded_players[i+1]) for i in range(0, len(padded_players), 2)]
        st.session_state['matches'] = matches
        st.session_state['bracket_size'] = next_pow2
        st.success("대진표 추첨이 완료되었습니다!")
        st.balloons()

# ── [섹션 2] 트리형 대진표 시각화 (A블록 / B블록 분리) ──
if 'matches' in st.session_state and st.session_state['matches']:
    matches = st.session_state['matches']
    half_idx = len(matches) // 2
    
    # 대진표를 좌/우 블록으로 나누어 결승전으로 올라가는 구조 연출
    col_A, col_B = st.columns(2)
    
    with col_A:
        st.markdown(f"<h3 style='text-align: center; color: #38bdf8;'>🟦 A 블록 (결승 진출자 1명 배출)</h3>", unsafe_allow_html=True)
        # A블록 매치업 출력
        for idx in range(half_idx):
            match = matches[idx]
            with st.container(border=True):
                st.caption(f"🏁 {next_pow2}강 - {idx + 1}경기")
                
                # 부전승이 포함된 경기 시각적 강조
                p1_color = "#64748b" if match[0] == "부전승 (Bye)" else "#e2e8f0"
                p2_color = "#64748b" if match[1] == "부전승 (Bye)" else "#e2e8f0"
                
                st.markdown(f"""
                <div style='display: flex; justify-content: space-between; align-items: center; padding: 10px;'>
                    <div style='font-size: 18px; font-weight: bold; color: {p1_color}; width: 40%; text-align: right;'>{match[0]}</div>
                    <div style='font-size: 14px; color: #f43f5e; font-weight: 900;'>VS</div>
                    <div style='font-size: 18px; font-weight: bold; color: {p2_color}; width: 40%; text-align: left;'>{match[1]}</div>
                </div>
                """, unsafe_allow_html=True)

    with col_B:
        st.markdown(f"<h3 style='text-align: center; color: #fbbf24;'>🟨 B 블록 (결승 진출자 1명 배출)</h3>", unsafe_allow_html=True)
        # B블록 매치업 출력
        for idx in range(half_idx, len(matches)):
            match = matches[idx]
            with st.container(border=True):
                st.caption(f"🏁 {next_pow2}강 - {idx + 1}경기")
                
                p1_color = "#64748b" if match[0] == "부전승 (Bye)" else "#e2e8f0"
                p2_color = "#64748b" if match[1] == "부전승 (Bye)" else "#e2e8f0"
                
                st.markdown(f"""
                <div style='display: flex; justify-content: space-between; align-items: center; padding: 10px;'>
                    <div style='font-size: 18px; font-weight: bold; color: {p1_color}; width: 40%; text-align: right;'>{match[0]}</div>
                    <div style='font-size: 14px; color: #f43f5e; font-weight: 900;'>VS</div>
                    <div style='font-size: 18px; font-weight: bold; color: {p2_color}; width: 40%; text-align: left;'>{match[1]}</div>
                </div>
                """, unsafe_allow_html=True)
                
    st.divider()
    st.markdown("<h4 style='text-align: center;'>⚔️ A블록 우승자  VS  B블록 우승자 ⚔️</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>대망의 결승전</p>", unsafe_allow_html=True)