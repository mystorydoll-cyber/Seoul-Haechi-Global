import streamlit as st
from openai import OpenAI
import time

# 1. 극장 전용 페이지 설정
st.set_page_config(
    layout="wide",
    page_title="🎭 서울스토리씨어터",
    page_icon="🎭"
)

# 2. 극장 디자인 (화려한 무대 배경 및 키오스크 요소)
st.markdown("""
    <style>
    /* 전체 배경을 화려한 무대 커튼 이미지로 설정 */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1514306191717-452ec28c7814?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    /* 텍스트 가독성을 위한 반투명 배경 박스 */
    .stMarkdown, .stTitle, .stSubheader, .stCaption, .stTextInput, .stSelectbox, .stSlider, .stTextArea {
        background-color: rgba(0, 0, 0, 0.7); /* 검은색 반투명 */
        padding: 20px;
        border-radius: 15px;
        color: #f1f1f1;
    }
    /* 티켓박스/키오스크 느낌의 사이드바 */
    [data-testid="stSidebar"] {
        background-color: rgba(30, 30, 30, 0.9);
        border-right: 2px solid #E50914;
    }
    /* 연극 입장 버튼 (골드 & 레드 테마) */
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #E50914 100%);
        color: #ffffff;
        border: 2px solid #FFD700;
        padding: 20px;
        font-size: 24px;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.5);
    }
    /* 입력 필드 내부 글씨색 하얗게 */
    input, select, textarea {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 인트로: 커튼이 열리는 연출
if 'theater_entered' not in st.session_state:
    st.markdown("<h1 style='text-align: center; font-size: 60px;'>🎭</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #FFD700;'>서울스토리씨어터</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>해치가 들려주는 빛나는 서울 이야기가 곧 상연됩니다.</p>", unsafe_allow_html=True)
    
    if st.button("🎭 티켓 제시하고 입장하기 (Enter)"):
        st.session_state.theater_entered = True
        st.rerun()
    st.stop()

# 4. 메인 무대 시작
st.title("🎭 서울스토리씨어터")
st.markdown("#### **“서울의 숨겨진 이야기를 들려주는 해치 만담꾼의 무대”**")

st.divider()

# 5. 티켓 정보 입력 (Kiosk)
col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://images.unsplash.com/photo-1543050760-456452075563?q=80&w=1974&auto=format&fit=crop", 
             caption="오늘의 무대, 당신의 서울")

with col2:
    st.subheader("🎟️ 관람객 정보 등록 (Kiosk)")
    u_name = st.text_input("관객 성함", placeholder="홍길동")
    
    c1, c2 = st.columns(2)
    with c1:
        u_loc = st.selectbox("이야기 무대 선택", ["종로구", "도봉구", "강서구", "강남구", "마포구"])
    with c2:
        u_mood = st.select_slider("연극 분위기", options=["잔잔한", "즐거운", "역동적인", "감동적인"])

    u_request = st.text_area("연극에 꼭 넣고 싶은 장면", placeholder="예: 해치와 함께 야경을 보는 장면")

# 6. 연극 상연 (AI 만담꾼 로직)
if st.button("✨ 연극 상연 시작 (Show Time)"):
    if not u_name:
        st.error("관람객 성함을 입력해 주세요!")
    else:
        with st.spinner('📢 만담꾼 해치가 무대 조명을 켜고 있습니다...'):
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                
                # 만담꾼 프롬프트
                prompt = f"""
                당신은 '서울스토리씨어터'의 노련한 이야기 만담꾼입니다.
                {u_loc} 지역의 실제 설화나 전통적인 소재를 바탕으로,
                관객 {u_name}님을 주인공으로 한 {u_mood} 분위기의 짧은 연극 대본을 써주세요.
                {u_loc}의 대표적인 장소를 언급해야 하며, "{u_request}" 장면을 아주 재미있게 녹여내세요.
                말투는 '~하오', '~다오' 같은 정겨운 만담꾼 말투를 사용하세요.
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": "매력적인 로컬 스토리 만담꾼"},
                              {"role": "user", "content": prompt}]
                )
                
                story_content = response.choices[0].message.content
                
                st.divider()
                st.subheader(f"🎬 제 1막: {u_name}님의 {u_loc} 이야기")
                st.markdown(story_content)
                st.balloons()
                
            except Exception as e:
                st.error(f"무대 장치 오류: {e}")

# 7. 푸터
st.divider()
st.caption("© 2025 마이스토리돌(My Story Doll) - M-Unit 기술전략팀 제작")
