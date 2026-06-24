import streamlit as st
import pandas as pd
import random
import math

st.set_page_config(page_title="토너먼트 대진표", page_icon="🏆", layout="wide")

from db import get_global_db
global_db = get_global_db()

st.title("🏆 공식 토너먼트 대진표 & 진행 상황")
st.divider()

if not global_db['participants']:
    st.warning("🚨 아직 참가 신청한 선수가 없습니다.")
    st.stop()

player_names = [p['닉네임'] for p in global_db['participants']]
next_pow2 = 2 ** math.ceil(math.log2(len(player_names)))
if next_pow2 < 4 and len(player_names) > 2: next_pow2 = 4
num_byes = next_pow2 - len(player_names)

col1, col2 = st.columns([1, 1])
with col1:
    with st.expander(f"👥 참가자 명단 확인 (총 {len(player_names)}명)", expanded=False):
        st.dataframe(pd.DataFrame(global_db['participants']), use_container_width=True, hide_index=True)

with col2:
    if st.button("🔥 무작위 대진표 추첨 시작 🔥", use_container_width=True, type="primary"):
        padded_players = player_names.copy() + ["부전승 (Bye)"] * num_byes
        random.shuffle(padded_players)
        # 세션이 아닌 global_db에 저장!
        global_db['matches'] = [(padded_players[i], padded_players[i+1]) for i in range(0, len(padded_players), 2)]
        st.success(f"{next_pow2}강 대진표 추첨 완료!")
        st.rerun()

st.divider()

if global_db['matches']:
    total_rounds = int(math.log2(next_pow2))
    cols = st.columns(total_rounds)
    current_matches = global_db['matches']
    
    for round_idx in range(total_rounds):
        is_final = (round_idx == total_rounds - 1)
        with cols[round_idx]:
            st.markdown(f"<h3 style='text-align:center; color:#38bdf8;'>{'👑 결승전' if is_final else f'🏁 {2**(total_rounds - round_idx)}강'}</h3>", unsafe_allow_html=True)
            next_round_players = []

            for match_idx, match in enumerate(current_matches):
                p1, p2 = match
                with st.container(border=True):
                    if p1 == "부전승 (Bye)": winner, loser = p2, p1; st.markdown(f"<h5 style='text-align:center;'>{p2} (부전승)</h5>", unsafe_allow_html=True)
                    elif p2 == "부전승 (Bye)": winner, loser = p1, p2; st.markdown(f"<h5 style='text-align:center;'>{p1} (부전승)</h5>", unsafe_allow_html=True)
                    elif p1 == "?" or p2 == "?": st.markdown(f"<h5 style='text-align:center; color:#64748b;'>{p1} VS {p2}</h5>", unsafe_allow_html=True); winner = "?"
                    else:
                        st.markdown(f"<h5 style='text-align:center;'>{p1} VS {p2}</h5>", unsafe_allow_html=True)
                        sel = st.selectbox("승자", ["진행 전", p1, p2], key=f"w_{round_idx}_{match_idx}", label_visibility="collapsed")
                        winner = "?" if sel == "진행 전" else sel
                    next_round_players.append(winner)

            next_matches = []
            for i in range(0, len(next_round_players), 2):
                if i + 1 < len(next_round_players): next_matches.append((next_round_players[i], next_round_players[i+1]))
            current_matches = next_matches