import streamlit as st

st.write("cwd:", __import__("os").getcwd())
st.write("static:", __import__("os").path.exists("static"))
st.write("tetris:", __import__("os").path.exists("static/tetris.html"))

import streamlit.components.v1 as components

with open("static/tetris.html", encoding="utf-8") as f:
    html = f.read()

components.html(
    html,
    height=1000,
    scrolling=True,
)