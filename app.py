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

# -----------------------------------------------------------
# 3. [긴급 수정] 이미지 주소 교체 (안정적인 위키미디어 소스)
# -----------------------------------------------------------
# 입장 전: 밝은 빨간색 벡터 커튼 (Wikipedia Commons)
IMG_CURTAIN = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Red_curtain_02.svg/2560px-Red_curtain_02.svg.png"

# 입장 후: 무대 배경 (안정적인 소스)
IMG_STAGE = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Empty_Starry_Sky_background.png/1280px-Empty_Starry_Sky_background.png" 

# 상태에 따른 배경 선택
current_bg = IMG_STAGE if st.session_state['entered'] else IMG_CURTAIN

# 4. CSS 스타일링 (배경 강제 적용)
st.markdown(f"""
    <style>
    /* [배경] 전체 화면 꽉 채우기 */
    .stApp {{
        background-image: url("{current_bg}") !important;
        background-size: cover !important;
        background-position: center bottom !important; /* 커튼 바닥 기준 정렬 */
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    
    /* [투명화] 방해되는 흰색 배경 제거 */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}

    /* [텍스트] 가독성 확보 */
    h1, h3, p, label, div, span {{
        color: white !important;
        font-family: 'Gowun Batang', serif;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.9);
    }}

    /* [티켓 박스] 디자인 수정 */
    .ticket-box {{
        background-color: rgba(20, 0, 0, 0.7); /* 붉은기 도는 검정 반투명 */
        border: 4px solid #FFD700; /* 굵은 금색 테두리 */
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        text-align: center;
        backdrop-filter: blur(5px);
    }}
    
    /* 입력창 스타일 */
    .stTextInput input {{
        background-color: #ffffff !important;
        color: #333333 !important;
        border-radius: 8px;
    }}
    
    /* 입장 버튼 스타일 */
    div.stButton > button {{
        background-color: #FFD700 !important;
        color: #8B0000 !important;
        font-weight: bold !important;
        border: none !important;
        width: 100%;
        padding: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- [Scene 1] 입장 전: 커튼 닫힌 상태 ---
if not st.session_state['entered']:
    
    # 상단 여백 (커튼 중앙에 로고 배치 느낌)
    st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
    
    # 극장 간판 느낌의 타이틀
    st.markdown("<h1 style='text-align: center; font-size: 80px;'>🎪 SEOUL STORY THEATER</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #FFD700 !important;'>해치가 들려주는 서울 이야기</h3>", unsafe_allow_html=True)

    st.markdown("<div style='height: 20vh;'></div>", unsafe_allow_html=True)

    # 레이아웃 분할
    col1, col2, col3 = st.columns([1, 1, 1.2]) 
    
    with col3:
        st.markdown('<div class="ticket-box">', unsafe_allow_html=True)
        st.markdown('<h3>🎫 관람객 등록 (Ticket)</h3>', unsafe_allow_html=True)
        
        with st.form("ticket_form"):
            name = st.text_input("이름 (Name)", placeholder="이름을 입력하세요")
            
            c1, c2 = st.columns(2)
            with c1:
                age = st.slider("나이", 5, 100, 25)
            with c2:
                nat = st.selectbox("국적", ["대한민국", "USA", "China", "Japan"])
                
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("🎬 입장하기")
            
            if submit:
                if name:
                    st.session_state['entered'] = True
                    st.session_state['user_name'] = name
                    st.rerun()
                else:
                    st.warning("이름을 입력해주세요.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- [Scene 2] 입장 후: 무대 ---
else:
    st.markdown(f"# 🎭 환영합니다, {st.session_state['user_name']}님!")
    
    with st.container():
        tab1, tab2 = st.tabs(["📖 이야기", "💬 대화"])
        
        with tab1:
            c1, c2 = st.columns([1, 2])
            with c1:
                # 해치 이미지 (투명 배경)
                st.image("https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Animals/Front-Facing%20Baby%20Chick.png", width=250)
            with c2:
                st.markdown("""
                ### 📜 제1막: 전설의 시작
                **(무대 조명이 켜지며)**
                
                "반갑소! 나는 서울의 이야기를 수호하는 해치라오."
                
                오늘 밤, 당신에게만 들려줄 특별한 전설이 있소.
                준비가 되었다면 아래 버튼을 눌러보시오.
                """)
    
    st.markdown("---")
    if st.button("🚪 극장 나가기"):
        st.session_state['entered'] = False
        st.rerun()
