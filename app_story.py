import streamlit as st
import pandas as pd
import os
import unicodedata
from openai import OpenAI

# 1. 극장 시스템 설정 및 테마 적용
st.set_page_config(
    layout="wide",
    page_title="서울스토리씨어터",
    page_icon="🎭",
    initial_sidebar_state="expanded"
)

# [스타일] 연극 무대 느낌의 CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    h1, h2, h3, h4, .stMarkdown, p, div, span, button, input, label {
        font-family: 'Jua', sans-serif !important;
    }
    .main-title { text-align: center; font-size: 3.5rem !important; color: #D32F2F; margin-bottom: 0.5rem; }
    .theater-box { background-color: #fffaf0; padding: 20px; border-radius: 15px; border-left: 6px solid #D32F2F; color: #333; }
    .speech-bubble { background-color: #fdf2f2; border: 2px solid #D32F2F; border-radius: 15px; padding: 15px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# 2. 데이터 및 이미지 핸들링 기능
@st.cache_data
def load_archive():
    # 지자체 설화 DB 로드
    return pd.read_csv('seoul_data.csv').set_index('region').to_dict('index')

seoul_db = load_archive()

def find_character_image(region, name):
    # 하이브리드 리소스 매칭 (구_이름.png)
    target = f"{region}_{name}.png"
    try:
        for file in os.listdir("."):
            if unicodedata.normalize('NFC', file) == unicodedata.normalize('NFC', target):
                return file
    except: pass
    return None

# 3. OpenAI API 클라이언트 설정
# Streamlit Secrets 또는 직접 입력을 지원합니다.
api_key = st.secrets.get("OPENAI_API_KEY") or st.sidebar.text_input("OpenAI API Key", type="password")
client = OpenAI(api_key=api_key) if api_key else None

# -------------------------------------------------------------------------
# [화면 로직] 관람객 등록 및 무대 전환
# -------------------------------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "msgs" not in st.session_state:
    st.session_state.msgs = []

if st.session_state.user is None:
    st.markdown('<p class="main-title">🎭 서울스토리씨어터</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>지역의 진짜 이야기를 상연합니다.</p>", unsafe_allow_html=True)
    with st.form("entry"):
        name = st.text_input("관람객 성함")
        if st.form_submit_button("무대 입장"):
            if name: 
                st.session_state.user = name
                st.rerun()
else:
    # 사이드바 설정
    with st.sidebar:
        st.title(f"🎟️ {st.session_state.user}의 티켓")
        if st.button("🚪 극장 퇴장"):
            st.session_state.user = None
            st.rerun()
        
        st.write("---")
        # 지역 변경 시 세션 초기화 (데이터 무결성 확보)
        region = st.selectbox("무대 선택", list(seoul_db.keys()), on_change=lambda: st.session_state.update(msgs=[]))
        char = seoul_db[region] #

    # 메인 무대 레이아웃
    st.markdown(f"## 🏛️ {region} 스테이지")
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        img = find_character_image(region, char['name'])
        if img: st.image(img, use_container_width=True)
        else: st.info(f"🎭 {char['visual']}가 등장 준비 중이오.")
        
    with col2:
        st.markdown(f"### 배우: {char['name']}")
        st.write(f"**역할:** {char['role']}")
        st.write(f"**성격:** {char['personality']}")
        st.markdown(f"<div class='speech-bubble'><b>{char['name']}</b>: \"{char['welcome']}\"</div>", unsafe_allow_html=True)

    st.write("---")
    tab1, tab2 = st.tabs(["📜 아카이브 전설", "🗣️ 배우와 만담"])

    # [RAG 기능 1] 실제 설화 기반 스토리텔링
    with tab1:
        if st.button("▶️ 공연 시작", type="primary"):
            if not client: st.error("API Key를 입력해주시오.")
            else:
                with st.spinner("대본 구성 중..."):
                    # 실제 설화(story) 데이터를 주입하여 환각 방지
                    prompt = f"""
                    너는 {region}의 수호신 {char['name']} 배우다. 
                    아래 [지역 설화]의 내용을 관객 {st.session_state.user}에게 재미있게 들려줘.
                    사극 말투(~하오, ~소)를 사용하고, 절대 AI라고 말하지 마라.
                    [지역 설화]: {char['story']}
                    """
                    res = client.chat.completions.create(model="gpt-4", messages=[{"role":"user", "content":prompt}]).choices[0].message.content
                    st.write(res)

    # [RAG 기능 2] 페르소나 일관성 대화
    with tab2:
        for m in st.session_state.msgs:
            st.chat_message(m["role"]).write(m["content"])
            
        if q := st.chat_input("질문이나 만담을 건네보시오..."):
            st.session_state.msgs.append({"role": "user", "content": q})
            st.chat_message("user").write(q)
            
            if client:
                # 시스템 프롬프트에 캐릭터 정체성 및 설화 지식 주입
                sys_prompt = f"""
                당신은 {region}의 {char['name']}입니다. 성격은 {char['personality']}이며 {char['role']}입니다.
                절대 AI라고 밝히지 말고, 아래 [공인 데이터]의 내용에 근거해서만 답변하십시오.
                말투는 {char['welcome']}의 톤을 따르십시오.
                [공인 데이터]: {char['story']}
                """
                rsp = client.chat.completions.create(
                    model="gpt-4", 
                    messages=[{"role": "system", "content": sys_prompt}] + st.session_state.msgs
                ).choices[0].message.content
                st.session_state.msgs.append({"role": "assistant", "content": rsp})
                st.chat_message("assistant").write(rsp)
