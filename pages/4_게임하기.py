from pathlib import Path
import streamlit as st

html_file = Path("static/tetris.html")

with open(html_file, "rb") as f:
    st.download_button(
        "🎮 테트리스 다운로드",
        data=f,
        file_name="tetris.html",
        mime="text/html"
    )