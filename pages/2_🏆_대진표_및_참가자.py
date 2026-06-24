import streamlit as st
import pandas as pd
import random
import math
from db import get_global_db

st.set_page_config(page_title="대진표 관리", page_icon="🏆", layout="wide")

global_db = get_global_db()

st.title("🏆 공식 토너먼트 대진표 & 진행 상황")
st.markdown("참가자를 확인하고 토너먼트 트리를 생성하세요. 승자를 선택하면 자동으로 다음 라운드가 갱신됩니다.")
st.divider()

# ── [섹션 1] 참가자 명단 ──
with st.expander(f"👥 현재 참가자 명단 (총 {len(global_db['participants'])}명)", expanded=False):
    if global_db['participants']:
        df = pd.DataFrame(global_db['participants'])
        st.dataframe(df.drop(columns=['연락처']), use_container_width=True, hide_index=True)
    else:
        st.info("신청자가 없습니다.")

# ── [대진표 추첨 로직] ──
if st.button("🎲 무작위 대진표 추첨/초기화", type="primary"):
    if len(global_db['participants']) < 2:
        st.error("최소 2명 이상이 필요합니다.")
    else:
        names = [p['닉네임'] for p in global_db['participants']]
        next_pow2 = 2 ** math.ceil(math.log2(len(names)))
        if next_pow2 < 4 and len(names) > 2: next_pow2 = 4
        
        # 부전승 포함 셔플
        padded = names + ["부전승 (Bye)"] * (next_pow2 - len(names))
        random.shuffle(padded)
        
        global_db['matches'] = [(padded[i], padded[i+1]) for i in range(0, len(padded), 2)]
        st.rerun()

st.divider()

# ── [토너먼트 트리 시각화 및 승자 결정] ──
if global_db['matches']:
    next_pow2 = len(global_db['matches']) * 2
    total_rounds = int(math.log2(next_pow2))
    cols = st.columns(total_rounds)
    
    current_matches = global_db['matches']
    losers_for_3rd = []
    champion = "진행 중"
    
    for round_idx in range(total_rounds):
        is_semi = (round_idx == total_rounds - 2)
        
        with cols[round_idx]:
            st.markdown(f"### {'👑 결승' if round_idx == total_rounds-1 else f'🏁 {2**(total_rounds-round_idx)}강'}")
            next_round_players = []

            for m_idx, (p1, p2) in enumerate(current_matches):
                with st.container(border=True):
                    if p1 == "부전승 (Bye)": winner = p2; st.caption(f"{p2} (부전승)"); next_round_players.append(winner)
                    elif p2 == "부전승 (Bye)": winner = p1; st.caption(f"{p1} (부전승)"); next_round_players.append(winner)
                    elif p1 == "?" or p2 == "?": st.markdown(f"{p1} VS {p2}"); next_round_players.append("?")
                    else:
                        st.markdown(f"**{p1}** VS **{p2}**")
                        sel = st.selectbox("승자 선택", ["진행 전", p1, p2], key=f"w_{round_idx}_{m_idx}")
                        winner = "?" if sel == "진행 전" else sel
                        if is_semi and winner != "?": losers_for_3rd.append(p2 if sel == p1 else p1)
                        next_round_players.append(winner)

            # 다음 라운드 매칭 생성
            if round_idx < total_rounds - 1:
                current_matches = [(next_round_players[i], next_round_players[i+1]) for i in range(0, len(next_round_players), 2)]
    
    # 3/4위전 별도 시각화
    if len(losers_for_3rd) == 2:
        st.divider()
        st.subheader("🥉 3/4위 결정전")
        cols_3rd = st.columns(3)
        with cols_3rd[1]:
            st.markdown(f"**{losers_for_3rd[0]}** VS **{losers_for_3rd[1]}**")
            st.selectbox("3위 승자", ["진행 전", losers_for_3rd[0], losers_for_3rd[1]], key="3rd_place")