import streamlit as st

st.write("cwd:", __import__("os").getcwd())
st.write("static:", __import__("os").path.exists("static"))
st.write("tetris:", __import__("os").path.exists("static/tetris.html"))

import streamlit as st

st.markdown(
    """
    <a href="/static/tetris.html" target="_blank">
        <button>테트리스 실행</button>
    </a>
    """,
    unsafe_allow_html=True
)