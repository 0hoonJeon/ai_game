import streamlit.components.v1 as components

with open("static/tetris.html", encoding="utf-8") as f:
    html = f.read()

components.html(
    html,
    height=1000,
    scrolling=True,
)