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
from datetime import datetime

st.set_page_config(page_title="대회 신청 - 사이버 듀얼", page_icon="📝", layout="wide")

st.title("📝 제 1회 사이버 듀얼 대회 신청")
st.markdown("대회 커뮤니티 소속 확인 및 자동 가입 방지를 통과해야 신청 폼이 활성화됩니다.")
st.divider()

# ── [섹션 0] 세션 상태 초기화 및 정답 설정 ──
if 'participants' not in st.session_state:
    st.session_state['participants'] = []
if 'is_authenticated' not in st.session_state:
    st.session_state['is_authenticated'] = False

# 주최자가 설정하는 비밀 코드와 퀴즈 정답 (이 파일 안에서만 관리하면 됨)
SECRET_INVITE_CODE = "CYBER2026"
QUIZ_ANSWER = "테트리스"

# ── [섹션 1] 커뮤니티 인증 구역 ──
col_auth, col_form = st.columns([1, 1.5])

with col_auth:
    st.subheader("1단계: 참가 자격 인증")
    
    if st.session_state['is_authenticated']:
        st.success("✅ 인증 완료! 우측의 참가 신청서를 작성해 주세요.")
    else:
        with st.container(border=True):
            st.markdown("**🔒 커뮤니티 초대 코드**")
            user_code = st.text_input("디스코드/카톡방에서 안내받은 코드를 입력하세요.", type="password")
            
            st.markdown("**🤖 봇 방지 퀴즈**")
            user_quiz = st.text_input("Q. 테트리스에서 긴 일자(I) 블록으로 한 번에 4줄을 지우는 기술은?", placeholder="단답형 4글자")
            
            if st.button("인증하기", type="primary", use_container_width=True):
                # 공백 제거나 대소문자 무시 등 유연하게 검사
                if user_code.strip().upper() == SECRET_INVITE_CODE and user_quiz.strip() == QUIZ_ANSWER:
                    st.session_state['is_authenticated'] = True
                    st.rerun()
                else:
                    st.error("❌ 초대 코드 또는 퀴즈 정답이 틀렸습니다.")

# ── [섹션 2] 참가 신청서 구역 (인증 완료 시 활성화) ──
with col_form:
    st.subheader("2단계: 참가 신청서 작성")
    
    if not st.session_state['is_authenticated']:
        st.info("👈 좌측에서 자격 인증을 먼저 완료해야 폼이 활성화됩니다.")
    else:
        with st.form("registration_form"):
            nickname = st.text_input("닉네임 (게임 내 표시될 ID)", max_chars=12, placeholder="예: 테트리스장인")
            # 이메일은 이제 단순 연락망 용도로만 수집 (인증 X)
            contact = st.text_input("연락처 (이메일 또는 디스코드 ID)", placeholder="우승 상품 수령 및 연락용")
            tier = st.selectbox("본인의 예상 실력 (티어)", ["선택해주세요", "브론즈", "실버", "골드", "마스터"])
            motto = st.text_area("대회에 임하는 각오 한마디!", max_chars=50)
            
            agree = st.checkbox("대회 규정을 확인하였으며, 이에 동의합니다.")
            
            submitted = st.form_submit_button("🚀 최종 참가 신청하기", use_container_width=True)
            
        if submitted:
            if not nickname or not contact or tier == "선택해주세요" or not agree:
                st.error("모든 필수 항목을 입력하고 규정에 동의해 주세요.")
            else:
                existing_nicknames = [p['닉네임'] for p in st.session_state['participants']]
                
                # 중복 닉네임 방지
                if nickname in existing_nicknames:
                    st.error("이미 등록된 닉네임입니다. 다른 닉네임을 사용해 주세요.")
                else:
                    new_participant = {
                        "신청일시": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "닉네임": nickname,
                        "연락처": contact,
                        "티어": tier,
                        "각오": motto
                    }
                    st.session_state['participants'].append(new_participant)
                    st.success(f"🎉 환영합니다, **{nickname}**님! 대회 신청이 확정되었습니다.")
                    st.balloons()