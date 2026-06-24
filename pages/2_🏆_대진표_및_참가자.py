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
import pandas as pd
import random
import math

# 무조건 와이드 레이아웃
st.set_page_config(page_title="토너먼트 대진표", page_icon="🏆", layout="wide")

st.title("🏆 공식 토너먼트 대진표 & 진행 상황")
st.markdown("참가자 수에 맞춰 자동으로 토너먼트 트리가 생성됩니다. 각 매치에서 승자를 선택하면 다음 라운드로 진출합니다.")
st.divider()

if 'participants' not in st.session_state or len(st.session_state['participants']) == 0:
    st.warning("🚨 아직 참가 신청한 선수가 없습니다.")
    st.stop()

participants = st.session_state['participants']
player_names = [p['닉네임'] for p in participants]

# 현재 인원에 맞는 토너먼트 크기 계산 (예: 6명 -> 8강, 14명 -> 16강)
next_pow2 = 2 ** math.ceil(math.log2(len(player_names)))
if next_pow2 < 4 and len(player_names) > 2:
    next_pow2 = 4
num_byes = next_pow2 - len(player_names)

# 상단 컨트롤 패널
col1, col2 = st.columns([1, 1])
with col1:
    with st.expander(f"👥 참가자 명단 확인 (총 {len(player_names)}명)", expanded=False):
        df = pd.DataFrame(participants)
        display_df = df.drop(columns=['연락처']) if '연락처' in df.columns else df
        st.dataframe(display_df, use_container_width=True, hide_index=True)

with col2:
    if st.button("🔥 무작위 대진표 추첨 시작 🔥", use_container_width=True, type="primary"):
        # 명단 섞고 부전승(Bye) 패딩 넣기
        padded_players = player_names.copy() + ["부전승 (Bye)"] * num_byes
        random.shuffle(padded_players)
        
        # 1라운드(최초 매치) 생성
        matches = [(padded_players[i], padded_players[i+1]) for i in range(0, len(padded_players), 2)]
        st.session_state['base_matches'] = matches
        st.success(f"{next_pow2}강 대진표 추첨 완료!")
        st.rerun()

st.divider()

# ── [반응형 토너먼트 트리 시각화] ──
if 'base_matches' in st.session_state:
    total_rounds = int(math.log2(next_pow2))
    cols = st.columns(total_rounds)
    
    current_matches = st.session_state['base_matches']
    losers_for_3rd = []
    champion = "진행 전"
    third_place = "진행 전"

    for round_idx in range(total_rounds):
        is_final = (round_idx == total_rounds - 1)
        is_semi = (round_idx == total_rounds - 2)
        
        with cols[round_idx]:
            # 라운드 타이틀 (8강, 4강, 결승 등)
            round_name = "👑 결승전" if is_final else f"🏁 {2**(total_rounds - round_idx)}강"
            st.markdown(f"<h3 style='text-align:center; color:#38bdf8;'>{round_name}</h3>", unsafe_allow_html=True)
            
            next_round_players = []

            # 현재 라운드의 매치업 카드 생성
            for match_idx, match in enumerate(current_matches):
                p1, p2 = match
                with st.container(border=True):
                    st.caption(f"Match {match_idx + 1}")
                    
                    # 1. 부전승(Bye) 처리: 자동으로 상대방을 승자로 기록
                    if p1 == "부전승 (Bye)":
                        winner, loser = p2, p1
                        st.markdown(f"<h5 style='text-align:center;'>{p2} <span style='color:#64748b; font-size:14px;'>(부전승)</span></h5>", unsafe_allow_html=True)
                    elif p2 == "부전승 (Bye)":
                        winner, loser = p1, p2
                        st.markdown(f"<h5 style='text-align:center;'>{p1} <span style='color:#64748b; font-size:14px;'>(부전승)</span></h5>", unsafe_allow_html=True)
                    
                    # 2. 아직 이전 라운드가 안 끝나서 선수가 올라오지 않은 경우 (?)
                    elif p1 == "?" or p2 == "?":
                        st.markdown(f"<h5 style='text-align:center; color:#64748b;'>{p1} <span style='color:#f43f5e;'>VS</span> {p2}</h5>", unsafe_allow_html=True)
                        winner, loser = "?", "?"
                    
                    # 3. 정상적인 1:1 매치 (결과 입력 폼 표시)
                    else:
                        st.markdown(f"<h5 style='text-align:center;'>{p1} <span style='color:#f43f5e;'>VS</span> {p2}</h5>", unsafe_allow_html=True)
                        # 승자를 선택하면 즉시 화면이 리로드되며 다음 라운드(우측 컬럼)로 이름이 넘어감!
                        sel = st.selectbox("승자 선택", ["진행 전", p1, p2], key=f"win_{round_idx}_{match_idx}", label_visibility="collapsed")
                        if sel == "진행 전":
                            winner, loser = "?", "?"
                        else:
                            winner = sel
                            loser = p2 if sel == p1 else p1

                    next_round_players.append(winner)

                    # 4강전에서 진 사람은 3/4위전으로 보냄
                    if is_semi:
                        losers_for_3rd.append(loser)
                    # 결승전 승자는 챔피언!
                    if is_final:
                        champion = winner

            # ── 3·4위전 출력 (결승전이 있는 마지막 컬럼의 하단에 추가) ──
            if is_final and len(losers_for_3rd) == 2:
                st.divider()
                st.markdown(f"<h3 style='text-align:center; color:#fbbf24;'>🥉 3·4위전</h3>", unsafe_allow_html=True)
                lp1, lp2 = losers_for_3rd
                with st.container(border=True):
                    if lp1 == "?" or lp2 == "?":
                        st.markdown(f"<h5 style='text-align:center; color:#64748b;'>{lp1} <span style='color:#f43f5e;'>VS</span> {lp2}</h5>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<h5 style='text-align:center;'>{lp1} <span style='color:#f43f5e;'>VS</span> {lp2}</h5>", unsafe_allow_html=True)
                        sel_3rd = st.selectbox("3위 선택", ["진행 전", lp1, lp2], key="win_3rd", label_visibility="collapsed")
                        third_place = sel_3rd1 if sel_3rd != "진행 전" else "?"

            # 다음 라운드(우측 컬럼)를 위한 매치업 데이터 가공
            next_matches = []
            for i in range(0, len(next_round_players), 2):
                if i + 1 < len(next_round_players):
                    next_matches.append((next_round_players[i], next_round_players[i+1]))
            current_matches = next_matches

    # 최종 결과 하단 요약
    st.divider()
    res1, res2 = st.columns(2)
    res1.success(f"🏆 **최종 우승 (Champion):** {champion if champion != '?' else '진행 전'}")
    res2.info(f"🥉 **3위 (3rd Place):** {third_place if third_place != '?' else '진행 전'}")