import streamlit as st
from openai import OpenAI

# 1. 페이지 설정 및 디자인 (극장 컨셉 리브랜딩)
st.set_page_config(
    layout="wide",
    page_title="🎭 서울스토리씨어터",
    page_icon="🎭",
    initial_sidebar_state="expanded"
)

# 극장 느낌을 주는 커스텀 CSS
st.markdown("""
    <style>
    .main {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #e50914;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 메인 헤더
st.title("🎭 서울스토리씨어터 (Seoul Story Theater)")
st.write("당신만의 서울 이야기가 한 편의 연극으로 펼쳐지는 곳입니다.")

# 3. 사이드바 - 관람권 설정 (기존 탐험대 정보)
with st.sidebar:
    st.header("🎟️ 관람권 정보")
    user_name = st.text_input("관객 성함", value="홍길동")
    haechi_type = st.selectbox("가이드 해치 선택", ["오리지널 해치", "핑크 해치", "블루 해치", "옐로우 해치"])
    st.divider()
    st.info("설정한 정보에 따라 연극의 줄거리가 달라집니다.")

# 4. 메인 입력 섹션
st.subheader("🎟️ 스토리 극장 관람권 발권")
col1, col2 = st.columns(2)

with col1:
    location = st.text_input("방문하고 싶은 서울의 장소", placeholder="예: 북촌 한옥마을, 성수동, 한강공원")
    mood = st.select_slider("연극의 분위기", options=["잔잔한", "즐거운", "역동적인", "감동적인"])

with col2:
    companion = st.text_input("함께하는 동행", placeholder="예: 가족, 연인, 친구, 나홀로")
    special_request = st.text_area("연극에 꼭 넣고 싶은 장면", placeholder="예: 해치와 함께 떡볶이를 먹는 장면")

# 5. 연극 시작 버튼 (기존 스토리 생성 로직)
if st.button("🎭 연극 관람하기 (Story Play)"):
    if not location:
        st.warning("장소를 입력해 주셔야 막이 오릅니다!")
    else:
        with st.spinner('해치가 무대 장치를 준비 중입니다...'):
            try:
                # OpenAI 클라이언트 초기화 (Secrets 사용)
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                
                # 프롬프트 구성 (극장 컨셉에 맞게 최적화)
                prompt = f"""
                당신은 '서울스토리씨어터'의 연출가입니다. 
                관객 {user_name}님이 {companion}와 함께 {location}을(를) 방문하는 이야기를 한 편의 연극 대본처럼 써주세요.
                {haechi_type}가 안내자로 등장해야 하며, 전체적인 분위기는 {mood} 느낌입니다.
                특별히 '{special_request}' 장면을 포함해 주세요.
                한국어로 생동감 있게 작성해 주세요.
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": "당신은 매력적인 스토리텔러이자 연극 연출가입니다."},
                              {"role": "user", "content": prompt}]
                )
                
                story_result = response.choices[0].message.content
                
                # 결과 출력
                st.divider()
                st.subheader(f"🎬 오늘의 연극: {user_name}님의 {location} 나들이")
                st.markdown(story_result)
                st.balloons()
                
            except Exception as e:
                st.error(f"무대 장치에 문제가 생겼습니다: {e}")
                st.info("환경 설정(Secrets)에 API 키가 정확히 입력되어 있는지 확인해 주세요.")

# 6. 하단 정보
st.divider()
st.caption("© 2025 마이스토리돌(My Story Doll) - M-Unit 기술전략팀 제작")
