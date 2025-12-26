import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# 1. 극장 시스템 설정 (V75: 서울스토리씨어터 메인)
st.set_page_config(
    page_title="서울스토리씨어터",
    page_icon="🎭",
    layout="wide"
)

# 2. 로컬 스토리 DB 로드 (RAG 기초)
@st.cache_data
def load_theater_data():
    # CSV에서 지역별 설화 및 캐릭터 정보 로드
    df = pd.read_csv('seoul_data.csv')
    return df

theater_db = load_theater_data()

# 3. 세션 초기화 및 관리 로직 (기술전략팀 과제: 세션 혼동 해결)
if "theater_session" not in st.session_state:
    st.session_state.theater_session = {"user": None, "messages": []}

def reset_performance():
    """무대 배경 전환 시 대사 기록 초기화"""
    st.session_state.theater_session["messages"] = []
    st.toast("무대 장치를 교체하고 대본을 새로 배부합니다.")

# -------------------------------------------------------------------------
# [화면 구현] 인트로: 관람객 등록 (B2G 전략 반영)
# -------------------------------------------------------------------------
if st.session_state.theater_session["user"] is None:
    st.markdown("<h1 style='text-align: center; color: #D32F2F;'>🎭 서울스토리씨어터</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>지자체 아카이브 기반 로컬 스토리텔링 시스템</p>", unsafe_allow_html=True)
    
    with st.container():
        st.write("---")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.info("📜 본 서비스는 지역의 실제 설화 데이터를 기반으로 제공되는 공공 스토리 아카이브 플랫폼입니다.")
        with col2:
            st.subheader("🎟️ 관람 티켓 발권")
            name = st.text_input("성함")
            if st.button("무대 입장", type="primary"):
                if name:
                    st.session_state.theater_session["user"] = name
                    st.rerun()

# -------------------------------------------------------------------------
# [화면 구현] 메인 무대: 연극 진행
# -------------------------------------------------------------------------
else:
    user_name = st.session_state.theater_session["user"]
    
    # 사이드바: 무대 컨트롤러
    with st.sidebar:
        st.title(f"🎭 {user_name}의 관람석")
        # 지역 선택 시 데이터 무결성을 위해 리셋 함수 호출
        selected_region = st.selectbox(
            "어느 지역의 무대를 관람하시겠소?", 
            theater_db['region'].unique(), 
            on_change=reset_performance
        )
        
        # 선택된 지역의 상세 데이터 추출
        stage_info = theater_db[theater_db['region'] == selected_region].iloc[0]
        
        if st.button("🚪 극장 나가기"):
            st.session_state.theater_session["user"] = None
            st.rerun()

    # 메인 공연장 레이아웃
    st.markdown(f"## 🏛️ {selected_region} 스테이지")
    st.write(f"**현재 상연작:** {stage_info['keyword']} 기반 로컬 스토리")
    
    col_img, col_txt = st.columns([1, 1.5])
    
    with col_img:
        # 하이브리드 리소스 매칭: {지역}_{캐릭터이름}.png
        img_path = f"{selected_region}_{stage_info['name']}.png"
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.warning(f"🎭 {stage_info['visual']} 배우가 분장 중입니다.")

    with col_txt:
        st.subheader(f"주연 배우: {stage_info['name']}")
        st.write(f"**배역:** {stage_info['role']}")
        st.write(f"**성격:** {stage_info['personality']}")
        st.success(f"💬 {stage_info['name']}: \"{stage_info['welcome']}\"")

    st.write("---")
    
    # 탭 구성: 스토리 감상 및 대화 (기능 통합)
    tab1, tab2 = st.tabs(["📜 공연 보기 (Archive)", "🗣️ 배우와 대화 (Interaction)"])
    
    with tab1:
        if st.button("▶️ 막 올리기"):
            # 실제 설화 데이터를 기반으로 스토리 텔링 (RAG 적용)
            st.markdown(f"### 📖 {selected_region}의 전설")
            st.write(stage_info['story'])

    with tab2:
        # 대화형 인터페이스 (Persona 일관성 확보)
        for msg in st.session_state.theater_session["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])
            
        if prompt := st.chat_input("배우에게 질문을 던져보세요..."):
            st.session_state.theater_session["messages"].append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            # 여기서 app_story.py의 API 호출 로직을 연동합니다.
            st.info("배우가 대답을 준비 중입니다... (API 연동 대기)")
