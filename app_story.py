import streamlit as st
import os
from openai import OpenAI

# -------------------------------------------------------------------------
# [설정] V40: 서울 해치 탐험 (Greeting Highlight)
# -------------------------------------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="서울 해치 탐험",
    page_icon="🦁",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------
# [스타일] CSS (디자인 고도화 - 인사 강조)
# -------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

    .main-title {
        font-family: 'Jua', sans-serif;
        text-align: center;
        font-size: 3.8rem !important;
        color: #FF4B4B;
        margin-bottom: 0.5rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
    }
    /* 서브 타이틀 기본 스타일 */
    .sub-title {
        font-family: 'Jua', sans-serif;
        text-align: center;
        font-size: 2rem !important; /* 기본 크기도 약간 키움 */
        color: #555;
        margin-bottom: 2rem;
        line-height: 1.4; /* 줄 간격 조정 */
    }
    /* [핵심] "안녕?" 강조 스타일 */
    .greeting-highlight {
        font-size: 5rem !important; /* 훨씬 더 크게! */
        color: #00ADD8; /* 다른 색 (청량한 하늘색 포인트) */
        font-weight: bold;
        text-shadow: 3px 3px 0px #eee; /* 귀여운 입체 효과 */
        display: block; /* 줄바꿈 효과 */
        margin-bottom: 10px;
    }
    div[data-testid="stForm"] {
        background-color: #f9f9f9;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 2px solid #eee;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 20px;
        border-
