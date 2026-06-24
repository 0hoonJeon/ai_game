import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 기본 설정
st.set_page_config(page_title="대회 신청 - 사이버 듀얼", page_icon="📝", layout="centered")

# 세션 상태(Session State) 초기화: 참가자 데이터를 임시 저장할 리스트 생성
if 'participants' not in st.session_state:
    st.session_state['participants'] = []

st.title("📝 제 1회 사이버 듀얼 대회 신청")
st.markdown("사이버 듀얼 테트리스 챔피언십에 오신 것을 환영합니다! 아래 폼을 작성하여 대회에 참가해 주세요.")

st.divider()

# 좌우 단을 나누어 규정과 폼을 배치
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("대회 규정 및 안내")
    st.info("""
    * **모집 기간:** 2026.06.24 ~ 2026.07.01
    * **대회 일자:** 2026.07.05 (일) 오후 2시
    * **참가 자격:** 테트리스를 사랑하는 누구나
    * **진행 방식:** 1:1 토너먼트 (단판승부)
    * **우승 상품:** 기계식 키보드 & 명예의 전당 등재
    """)
    st.warning("⚠️ 입력하신 닉네임은 대진표 및 게임 화면에 그대로 노출되니, 불쾌감을 주는 닉네임은 삼가주세요.")

with col2:
    # 폼(Form) 생성
    with st.form("registration_form"):
        st.subheader("참가 신청서 작성")
        
        nickname = st.text_input("닉네임 (게임 내 표시될 ID)", max_chars=12, placeholder="예: 테트리스장인")
        email = st.text_input("연락처 (이메일)", placeholder="example@email.com")
        tier = st.selectbox("본인의 예상 실력 (티어)", ["선택해주세요", "브론즈 (초보)", "실버 (중수)", "골드 (고수)", "마스터 (신)"])
        motto = st.text_area("대회에 임하는 각오 한마디!", max_chars=50)
        
        agree = st.checkbox("대회 규정을 확인하였으며, 이에 동의합니다.")
        
        # 제출 버튼
        submitted = st.form_submit_button("🚀 참가 신청하기", use_container_width=True)

# 제출 버튼이 눌렸을 때의 로직 처리
if submitted:
    if not nickname or not email or tier == "선택해주세요":
        st.error("필수 항목(닉네임, 이메일, 실력)을 모두 입력 및 선택해 주세요.")
    elif not agree:
        st.error("대회 규정 동의 체크박스에 체크해 주세요.")
    else:
        # 중복 닉네임 검사
        existing_nicknames = [p['닉네임'] for p in st.session_state['participants']]
        if nickname in existing_nicknames:
            st.error("이미 등록된 닉네임입니다. 다른 닉네임을 사용해 주세요.")
        else:
            # 데이터 저장
            new_participant = {
                "신청일시": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "닉네임": nickname,
                "연락처": email,
                "티어": tier,
                "각오": motto
            }
            st.session_state['participants'].append(new_participant)
            
            st.success(f"환영합니다, **{nickname}**님! 성공적으로 참가 신청이 완료되었습니다.")
            st.balloons() # 성공 시 풍선 애니메이션 효과

st.divider()

# 관리자용: 현재까지 모인 참가자 현황 보여주기 (익명화 처리 가능)
st.subheader("📊 현재 참가 현황")
if len(st.session_state['participants']) > 0:
    st.metric(label="총 참가자 수", value=f"{len(st.session_state['participants'])} 명")
    
    # 데이터프레임으로 변환하여 테이블 출력
    df = pd.DataFrame(st.session_state['participants'])
    # 개인정보(이메일) 보호를 위해 화면에 띄울 때는 이메일 열 제외
    display_df = df.drop(columns=['연락처']) 
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.write("아직 참가 신청자가 없습니다. 첫 번째 참가자가 되어보세요!")