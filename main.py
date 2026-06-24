import streamlit as st

with st.sidebar():
    st.write('hihi')

st.set_page_config(
    page_title="내 앱",
    page_icon="📄",
    layout="wide"
)

st.title("일반 Streamlit 페이지")

st.header("섹션 제목")
st.write("여기에 내용을 작.")

name = st.text_input("이름 입력")

if st.button("확인"):
    st.success(f"안녕하세요, {name}님!")