import streamlit as st
from openai import OpenAI
import time

# 1. 극장 전용 페이지 설정
st.set_page_config(
    layout="wide",
    page_title="🎭 서울스토리씨어터",
    page_icon="🎭"
)

# 2. 극장 디자인 (검토안 요청: 극장 연상 디자인, 키오스크 요소) [cite: 61, 67]
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: #f1f1f1;
    }
    /* 티켓박스/키오스크 느낌의 사이드바  */
    [data-testid="stSidebar"] {
        background-color: #1e1e1e;
        border-right: 2px solid #E50914;
    }
    /* 연극 입장 버튼 (레드 카펫 테마) */
    .stButton>button {
        background: linear-gradient(135deg, #E50914 0%, #8B0000 100%);
        color: gold;
        border: 2px solid gold;
        padding: 20px;
        font-size: 24px;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 인트로: 커튼이 열리는 연출 
if 'theater_entered' not in st.session_state:
    st.markdown("<h1 style='text-align: center; font-size: 60px;'>🎭</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #E50914;'>서울스토리씨어터</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>해치가 들려주는 서울 이야기가 곧 상연됩니다.</p>", unsafe_allow_html=True)
    
    # 극장 커튼 이미지 (Unsplash 무료 이미지 활용)
    st.image("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2070&auto=format&fit=crop", 
             caption="[안내] 잠시 후 막이 오릅니다.")
    
    if st.button("🎭 티켓 제시하고 입장하기"):
        st.session_state.theater_entered = True
        st.rerun()
    st.stop()

# 4. 메인 무대 시작
st.title("🎭 서울스토리씨어터")
st.markdown("#### **“서울의 숨겨진 이야기를 들려주는 해치 만담꾼의 무대”**") [cite: 57, 48]

st.divider()

# 5. 티켓 정보 입력 (검토안 요청: 관람객 정보 등록으로 용어 변경) 
col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://images.unsplash.com/photo-1518834107812-67b0b7c58434?q=80&w=1935&auto=format&fit=crop", 
             caption="전통과 현대가 공존하는 무대, 서울")

with col2:
    st.subheader("🎟️ 관람객 정보 등록 (Kiosk)")
    u_name = st.text_input("관객 성함", placeholder="홍길동")
    
    c1, c2 = st.columns(2)
    with c1:
        u_loc = st.selectbox("이야기 무대 선택", ["종로구", "도봉구", "강서구", "강남구", "마포구"]) [cite: 71]
    with c2:
        u_mood = st.select_slider("연극 분위기", options=["잔잔한", "즐거운", "역동적인", "감동적인"])

    u_request = st.text_area("연극에 꼭 넣고 싶은 장면", placeholder="예: 해치와 함께 야경을 보는 장면")

# 6. 연극 상연 (AI 만담꾼 로직) 
if st.button("🎭 연극 상연 시작 (Show Time)"):
    if not u_name:
        st.error("관람객 성함을 입력해 주세요!")
    else:
        with st.spinner('📢 만담꾼 해치가 무대 뒤에서 의상을 갈아입고 있습니다...'):
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                
                # 검토안 의견 반영: 단순 창작이 아닌 실제 지역 이야기를 기반으로 하는 만담꾼 프롬프트 [cite: 75, 76]
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
