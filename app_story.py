import streamlit as st
import os
import unicodedata
import pandas as pd # 데이터 분석용 추가
from openai import OpenAI

# -------------------------------------------------------------------------
# [설정] V70: 서울스토리씨어터 전략적 피벗 반영
# -------------------------------------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="서울스토리씨어터",
    page_icon="🎭",
    initial_sidebar_state="expanded"
)

# [RAG 데이터 엔진] CSV 아카이브 연동
@st.cache_data
def load_seoul_archive():
    df = pd.read_csv('seoul_data.csv')
    # region 컬럼을 인덱스로 설정하여 조회 최적화
    return df.set_index('region').to_dict('index')

seoul_db = load_seoul_archive()

# -------------------------------------------------------------------------
# [기능] 스마트 이미지 찾기 (하이브리드 제작 방식)
# -------------------------------------------------------------------------
def find_image_file(region, char_name):
    # '강남구_패션해치.png' 형식 매칭
    target_name = f"{region}_{char_name}.png"
    try:
        current_files = os.listdir(".")
    except:
        return None
    for file in current_files:
        norm_file = unicodedata.normalize('NFC', file)
        norm_target = unicodedata.normalize('NFC', target_name)
        if norm_file == norm_target:
            return file
    return None

# -------------------------------------------------------------------------
# [스타일] CSS (극장/연극 컨셉으로 고도화)
# -------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    h1, h2, h3, h4, .stMarkdown, p, div, span, button, input, label {
        font-family: 'Jua', sans-serif !important;
    }
    .main-title {
        text-align: center; font-size: 3.5rem !important; color: #D32F2F; 
        margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-title {
        text-align: center; font-size: 1.8rem !important; color: #555; margin-bottom: 2rem;
    }
    .theater-box {
        background-color: #fffaf0; padding: 25px; border-radius: 15px; margin-top: 20px;
        border-left: 6px solid #D32F2F; box-shadow: 0 2px 10px rgba(0,0,0,0.05); color: #333;
    }
    .app-header {
        font-size: 2.8rem !important; color: #D32F2F; text-shadow: 2px 2px 0px #eee; margin-bottom: 20px;
    }
    .char-title {
        font-size: 3.5rem !important; color: #D32F2F; margin-bottom: 10px; line-height: 1.2;
    }
    .speech-bubble {
        background-color: #fdf2f2; border: 2px solid #D32F2F; border-radius: 20px; padding: 15px; font-size: 1.3rem; color: #333;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# [로직] 인트로 + 메인 앱
# -------------------------------------------------------------------------
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None

if st.session_state.user_profile is None:
    st.markdown('<p class="main-title">🎭 서울스토리씨어터 : 관람 등록</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">"지역의 잠든 데이터를 깨우는 진짜 이야기가 시작됩니다."</p>', unsafe_allow_html=True)
    st.markdown("---")
    col1, col2 = st.columns([1.5, 1], gap="large")
    with col1:
        intro_dir = "intro"
        if os.path.exists(intro_dir) and "main.mp4" in os.listdir(intro_dir):
            st.video(os.path.join(intro_dir, "main.mp4"), autoplay=True, loop=True, muted=True)
        else:
            st.info("🎭 서막 영상을 준비 중입니다.")
        
        st.markdown("""
        <div class="theater-box">
            <h4>📜 공연 기획 의도</h4>
            <p>본 시스템은 지자체의 <b>로컬 스토리 DB</b>를 기반으로 작동하는 공공 솔루션입니다. AI의 환각을 제어하고, 실제 기록된 설화만을 바탕으로 공연을 진행합니다.</p>
            <div class="copyright">© 2025 M-Unit Seoul Story Theater.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🎟️ 관람 티켓 등록")
        with st.form("intro_form"):
            name = st.text_input("관람객 성함 (Name)", placeholder="예: 홍길동")
            nationality = st.selectbox("언어권", ["대한민국", "USA", "China", "Japan"])
            st.markdown("---")
            if st.form_submit_button("무대 입장하기", type="primary", use_container_width=True):
                if name:
                    st.session_state.user_profile = {"name": name, "nationality": nationality}
                    st.rerun()
                else: st.error("성함을 입력해주세요!")

else:
    user = st.session_state.user_profile
    with st.sidebar:
        st.title(f"🎭 {user['name']}님 환영하오!")
        if st.button("🔄 극장 나가기"):
            st.session_state.user_profile = None
            st.rerun()
        st.markdown("---")
        
        # 무대 변경 시 대화 기록 초기화 함수
        def reset_stage():
            st.session_state.msgs = []
            st.toast("대본을 새로 준비 중입니다...")

        st.markdown("### 📍 무대 배경 선택")
        region = st.selectbox("어느 지역의 이야기를 보시겠소?", list(seoul_db.keys()), on_change=reset_stage)
        char = seoul_db[region] #

        api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else st.text_input("OpenAI API Key", type="password")
        client = OpenAI(api_key=api_key) if api_key else None

    # [메인 화면 구성] 
    st.markdown(f"<div class='app-header'>🏛️ {region} 스테이지</div>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1], gap="medium")
    
    with c1:
        # 하이브리드 리소스 매칭
        img_file = find_image_file(region, char['name'])
        if img_file: st.image(img_file, use_container_width=True)
        else: st.info(f"📸 {char['visual']} (이미지 준비중)")
        
    with c2:
        st.markdown(f"<p class='char-title'>{char['name']}</p>", unsafe_allow_html=True)
        st.markdown(f"<span class='char-role'>{char['role']}</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='desc-box'><b>💡 성격:</b> {char['personality']}<br><br><b>🔑 키워드:</b> {char['keyword']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='speech-bubble'><b>{char['name']}</b>: \"{char['welcome']}\"</div>", unsafe_allow_html=True)

    st.markdown("---")
    t1, t2, t3 = st.tabs(["📜 전설 보기 (Archive)", "🗣️ 만담 나누기 (Persona)", "🎭 무대 이벤트"])

    with t1:
        if st.button("▶️ 전설 들려주기", type="primary"):
            if not client: st.error("API Key 필요")
            else:
                with st.spinner("대본 읽는 중..."):
                    # RAG: 실제 story 데이터 기반 각색
                    p = f"너는 {char['name']} 배우다. 아래 설화 내용을 {user['name']}님에게 연극하듯 들려줘. 말투는 {char['welcome']}의 톤을 유지해. [내용]: {char['story']}"
                    s = client.chat.completions.create(model="gpt-4", messages=[{"role":"user", "content":p}]).choices[0].message.content
                    st.write(s)

    with t2:
        if "msgs" not in st.session_state: st.session_state.msgs = []
        for m in st.session_state.msgs: st.chat_message(m["role"]).write(m["content"])
        if q := st.chat_input("배우에게 말 걸기..."):
            st.session_state.msgs.append({"role":"user", "content":q})
            st.chat_message("user").write(q)
            if client:
                # 페르소나 교정 및 지식 제한
                system_p = f"""
                당신은 {region}의 {char['name']}입니다. 
                - 절대 AI라고 말하지 마시오. 
                - 제공된 [지식] 외에 지어내지 마시오.
                - 말투: {char['welcome']} 분위기의 사극 만담 톤.
                [지식]: {char['story']}
                """
                rsp = client.chat.completions.create(model="gpt-4", messages=[{"role":"system", "content":system_p}]+st.session_state.msgs).choices[0].message.content
                st.session_state.msgs.append({"role":"assistant", "content":rsp})
                st.chat_message("assistant").write(rsp)

    with t3:
        # '작가 되기'와 '그림 그리기'를 이벤트로 통합
        kw = st.text_input("공연에 추가할 소품이나 소재를 말해달라!")
        if st.button("무대 연출") and client:
            with st.spinner("연출 중..."):
                u = client.images.generate(model="dall-e-3", prompt=f"Character {char['name']} in {region} theater stage, with {kw}", size="1024x1024").data[0].url
                st.image(u)
