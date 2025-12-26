import streamlit as st
from openai import OpenAI
import time

# 1. 페이지 설정 (디자인 요소 강화)
st.set_page_config(
    layout="wide",
    page_title="🎭 서울스토리씨어터",
    page_icon="🎭"
)

# 2. 극장 테마 커스텀 CSS (검토안 요청사항 반영)
# 레드 벨벳 커튼과 어두운 극장 분위기 연출 [cite: 61]
st.markdown("""
    <style>
    /* 전체 배경을 어두운 극장 톤으로 설정 */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    /* 티켓/키오스크 느낌의 입력창 디자인  */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #1A1C24;
        color: white;
        border: 1px solid #E50914;
    }
    /* 연극 입장 버튼 (강렬한 레드 컬러)  */
    .stButton>button {
        background: linear-gradient(135deg, #E50914 0%, #B20710 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 50px;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(229, 9, 20, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 인트로: 커튼이 열리는 연출 (검토안 요청사항 반영) [cite: 61]
if 'curtain_opened' not in st.session_state:
    with st.container():
        st.markdown("<h1 style='text-align: center; color: #E50914;'>🎭 서울스토리씨어터</h1>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1503095396549-807039a30687?q=80&w=2070&auto=format&fit=crop", caption="막이 오르기 전입니다...")
        if st.button("입장하기 (Enter Theater)"):
            st.session_state.curtain_opened = True
            st.rerun()
    st.stop()

# 4. 메인 화면 (커튼 오픈 후)
st.title("🎭 서울스토리씨어터 (Seoul Story Theater)")
st.markdown("#### **해치가 들려주는 생생한 서울 이야기**") # 부제 반영 [cite: 57]

st.divider()

# 5. 사용자 등록 정보 - 티켓 디자인 섹션 
col1, col2 = st.columns([1, 1.5])

with col1:
    st.image("https://images.unsplash.com/photo-1514306191717-452ec28c7814?q=80&w=2070&auto=format&fit=crop", caption="오늘의 화자: 해치")
    
with col2:
    st.subheader("🎟️ 관람객 정보 등록") # 용어 변경 
    u_name = st.text_input("성함 (Name)", placeholder="관객님의 성함을 입력해주세요.")
    
    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        u_loc = st.selectbox("어느 지역의 이야기를 상연할까요?", 
                            ["종로구", "도봉구", "강서구", "강남구", "마포구"]) # 지역 선택 [cite: 69]
    with col_sub2:
        u_mood = st.select_slider("연극의 분위기", options=["잔잔한", "즐거운", "역동적인", "감동적인"])

    u_request = st.text_area("연극에 꼭 넣고 싶은 장면 (Special Request)", 
                             placeholder="예: 해치와 함께 광화문 광장을 걷는 장면")

# 6. 연극 상연 버튼
if st.button("입장하기 (Show Time)"): # 버튼 용어 변경 
    if not u_name:
        st.warning("관객 성함을 입력하셔야 관람권이 발권됩니다!")
    else:
        with st.spinner('📢 극장 안내방송: 곧 연극이 시작됩니다. 잠시만 기다려주세요...'):
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                
                # 검토안 의견 반영: 이야기꾼(만담꾼) 컨셉의 프롬프트 [cite: 48, 59]
                prompt = f"""
                당신은 '서울스토리씨어터'의 노련한 이야기 만담꾼입니다. [cite: 48]
                {u_loc}의 실제 전설이나 고유 설화를 바탕으로[cite: 20], 
                관객 {u_name}님이 주인공으로 등장하는 {u_mood} 분위기의 연극 대본을 써주세요.
                해치가 안내자로 등장하며, 특별 요청사항인 '{u_request}'를 포함해야 합니다.
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": "매력적인 스토리텔링 연출가"},
                              {"role": "user", "content": prompt}]
                )
                
                story_result = response.choices[0].message.content
                
                st.balloons()
                st.markdown(f"### 🎬 제 1막: {u_name}님의 {u_loc} 연대기")
                st.markdown(story_result)
                
            except Exception as e:
                st.error(f"무대 장치 오류: {e}")

# 7. 푸터
st.divider()
st.caption("© 2025 마이스토리돌(My Story Doll) - M-Unit 디자인/기술전략팀")
