import streamlit as st
import random

st.title("🎮 1~100 숫자 맞추기 (Up & Down)")

# 1. 게임 상태(session_state) 초기화
# 코드가 재실행되어도 정답과 시도 횟수가 초기화되지 않도록 설정합니다.
if 'target_number' not in st.session_state:
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False

# 2. 게임 재시작 함수
def reset_game():
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False

st.write("컴퓨터가 1부터 100 사이의 숫자를 하나 골랐습니다. 맞춰보세요!")

# 3. 사용자 입력 받기
guess = st.number_input("숫자를 입력하세요:", min_value=1, max_value=100, step=1)

# 4. 게임 로직 처리
# 버튼을 누르면 정답인지 확인합니다.
if st.button("정답 확인") and not st.session_state.game_over:
    st.session_state.attempts += 1 # 시도 횟수 1 증가
    
    if guess < st.session_state.target_number:
        st.warning(f"⬆️ **UP!** {guess}보다 더 큰 숫자입니다. (현재 시도: {st.session_state.attempts}회)")
    elif guess > st.session_state.target_number:
        st.warning(f"⬇️ **DOWN!** {guess}보다 더 작은 숫자입니다. (현재 시도: {st.session_state.attempts}회)")
    else:
        st.success(f"🎉 **정답입니다!** {st.session_state.attempts}번만에 맞추셨습니다!")
        st.balloons() # 정답을 맞추면 풍선 이펙트!
        st.session_state.game_over = True

# 5. 게임 종료 시 재시작 버튼 표시
if st.session_state.game_over:
    st.button("새 게임 시작하기", on_click=reset_game)