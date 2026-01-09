import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(
    page_title="서울 스토리 씨어터",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 세션 초기화
if 'entered' not in st.session_state:
    st.session_state['entered'] = False

# 3. 이미지 URL (커튼 & 무대)
IMG_CURTAIN = "https://images.unsplash.com/photo-1514306191717-452ec28c7f42?q=80&w=2070&auto=format&fit=crop"
IMG_STAGE = "https://images.unsplash.com/photo-1503095392269-41a979922c00?q=80&w=2070&auto=format&fit=crop"

current_bg = IMG_STAGE if st.session_state['entered'] else IMG_CURTAIN

# 4. CSS 스타일링 (투명화 패치 적용)
st.markdown(f"""
    <style>
    /* [1] 가장 바깥쪽 배경에 이미지 적용 */
    .stApp {{
        background-image: url("{current_bg}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}

    /* [2] 검은색으로 덮인 내부 컨테이너들을 전부 '투명'하게 변경 */
    [data-testid="stAppViewContainer"] {{
        background-color: transparent !important;
    }}
    
    [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}
    
    [data-testid="stToolbar"] {{
        right: 2rem;
    }}

    /* [3] 텍스트 및 UI 디자인 */
    h1, h2, h3, p, div, span, label {{
        color: white !important;
        text-shadow: 2px 2px 5px black;
        font-family: 'Gowun Batang', serif;
    }}

    /* 입력창 내부 글씨는 검게 */
    .stTextInput input {{
        color: black !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
    }}
    
    /* [4] 티켓 박스 디자인 (우측 하단) */
    .ticket-box {{
        background-color: rgba(0, 0, 0, 0.7); /* 반투명 검정 */
        border: 2px solid #FFD700;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 15px #FFD700;
        text-align: center;
        margin-top: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- [Scene 1] 입장 전 ---
if not st.session_state['entered']:
    
    # 상단 타이틀 (멋지게 추가)
    st.markdown("<h1 style='text-align: center; font-size: 60px; margin-top: 50px;'>🎪 서울 스토리 씨어터 🎪</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>해치가 들려주는 서울 이야기</h3>", unsafe_allow_html=True)

    # 레이아웃 조정 (박스를 우측 하단으로)
    st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True) # 여백

    col1, col2, col3 = st.columns([1, 0.5, 1])
    
    with col3:
        st.markdown('<div class="ticket-box"><h3>🎟️ 관람객 등록 (Ticket)</h3>', unsafe_allow_html=True)
        
        with st.form("ticket_form"):
            name = st.text_input("관람객 이름", placeholder="이름을 입력하세요")
            
            c1, c2 = st.columns(2)
            with c1:
                age = st.slider("나이", 5, 100, 25)
            with c2:
                nat = st.selectbox("국적", ["대한민국", "USA", "China", "Japan"])
                
            submit = st.form_submit_button("🎬 입장하기")
            
            if submit:
                if name:
                    st.session_state['entered'] = True
                    st.session_state['user_name'] = name
                    st.rerun()
                else:
                    st.warning("이름을 입력해주세요.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- [Scene 2] 입장 후 ---
else:
    st.markdown(f"# 🎭 Seoul Story Theater: {st.session_state['user_name']}님의 무대")
    
    with st.container():
        tab1, tab2 = st.tabs(["📖 이야기", "💬 대화"])
        
        with tab1:
            c_a, c_b = st.columns(2)
            with c_a:
                 st.image("https://images.unsplash.com/photo-1596485044893-97c27599c158", use_container_width=True)
            with c_b:
                st.markdown("### 📜 제1막: 경복궁의 해치\n\n(조명이 켜지며 이야기 시작...)")

    if st.button("🚪 나가기"):
        st.session_state['entered'] = False
        st.rerun()
