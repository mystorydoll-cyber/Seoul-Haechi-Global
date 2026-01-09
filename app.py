import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(
    page_title="서울 스토리 씨어터",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 세션 상태 초기화
if 'entered' not in st.session_state:
    st.session_state['entered'] = False

# 3. 이미지 URL (커튼 & 무대)
IMG_CURTAIN = "https://images.unsplash.com/photo-1514306191717-452ec28c7f42?q=80&w=2070&auto=format&fit=crop"
IMG_STAGE = "https://images.unsplash.com/photo-1503095392269-41a979922c00?q=80&w=2070&auto=format&fit=crop"

# 현재 상태에 따른 배경 선택
current_bg = IMG_STAGE if st.session_state['entered'] else IMG_CURTAIN

# 4. CSS 스타일링 (강제 적용 !important 추가)
st.markdown(f"""
    <style>
    /* 전체 앱 배경 강제 적용 */
    .stApp {{
        background-image: url("{current_bg}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    
    /* 헤더 투명화 */
    header {{
        background-color: rgba(0,0,0,0) !important;
    }}
    
    /* 텍스트 가독성 (흰색 글씨 + 그림자) */
    h1, h2, h3, p, label, span, .stMarkdown {{
        color: white !important;
        text-shadow: 2px 2px 4px #000000;
        font-family: 'Gowun Batang', serif;
    }}
    
    /* 입력창 라벨 색상 강제 */
    .stTextInput > label {{
        color: #FFD700 !important; /* 금색 */
    }}

    /* 티켓 박스 스타일 (우측 하단) */
    .ticket-container {{
        background-color: rgba(0, 0, 0, 0.85);
        padding: 30px;
        border-radius: 15px;
        border: 3px solid #FFD700;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
        text-align: center;
        margin-top: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- [Scene 1] 입장 전: 닫힌 커튼 ---
if not st.session_state['entered']:
    
    # 레이아웃: 위쪽 여백을 줘서 박스를 아래로 내림
    st.markdown("<div style='height: 40vh;'></div>", unsafe_allow_html=True)

    # 3단 분할: [빈 공간] - [빈 공간] - [티켓 박스]
    col1, col2, col3 = st.columns([1, 1, 1.3]) 
    
    with col3:
        st.markdown("<div class='ticket-container'><h3>🎟️ 관람객 등록 (Ticket)</h3>", unsafe_allow_html=True)
        
        with st.form("ticket_form"):
            name = st.text_input("관람객 이름", placeholder="이름을 입력하세요")
            
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                age = st.slider("나이", 5, 100, 25)
            with sub_col2:
                nationality = st.selectbox("국적", ["대한민국", "USA", "Japan", "China"])
            
            # 버튼 클릭 시 리런
            submitted = st.form_submit_button("🎬 입장하기 (Enter)")
            
            if submitted:
                if name:
                    st.session_state['entered'] = True
                    st.session_state['user_name'] = name
                    st.rerun()
                else:
                    st.warning("이름을 입력해주세요.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- [Scene 2] 입장 후: 열린 무대 ---
else:
    st.markdown(f"# 🎭 Seoul Story Theater: {st.session_state['user_name']}님의 무대")
    
    # 탭 메뉴 컨테이너
    with st.container():
        tab1, tab2, tab3 = st.tabs(["📖 전설의 이야기", "💬 해치와 대화", "🎨 캐릭터 생성"])
        
        with tab1:
            col_a, col_b = st.columns([1, 1])
            with col_a:
                # 예시 이미지
                st.image("https://images.unsplash.com/photo-1596485044893-97c27599c158", use_container_width=True)
            with col_b:
                st.markdown("""
                ### 📜 제1막: 경복궁의 수호신
                **해치:** "어서 오시오! 내 그대를 기다리고 있었소."
                """)

        with tab2:
            st.info("해치와의 대화 기능 준비 중...")

        with tab3:
            st.info("나만의 해치 만들기 준비 중...")

    st.markdown("---")
    if st.button("🚪 극장 나가기"):
        st.session_state['entered'] = False
        st.rerun()
