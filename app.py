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
# 3. [핵심] 이미지 교체 (CEO님이 원하시는 일러스트 느낌)
# -----------------------------------------------------------
# 입장 전: 꽉 찬 붉은 커튼 (밝은 버전)
IMG_CURTAIN = "https://img.freepik.com/free-vector/red-curtains-background_1017-38605.jpg?w=2000" 
# 입장 후: 조명 켜진 무대 (일러스트 느낌)
IMG_STAGE = "https://img.freepik.com/free-vector/stage-with-open-red-curtains_1017-32195.jpg?w=2000"

# 상태에 따른 배경 선택
current_bg = IMG_STAGE if st.session_state['entered'] else IMG_CURTAIN

# 4. CSS 스타일링 (배경 강제 적용 & UI 디자인)
st.markdown(f"""
    <style>
    /* [배경] 전체 화면을 이미지로 꽉 채우기 */
    .stApp {{
        background-image: url("{current_bg}") !important;
        background-size: cover !important; /* 화면 꽉 채움 */
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    
    /* [방해물 제거] Streamlit 기본 배경 투명화 */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}

    /* [텍스트] 하얀 글씨 + 검은 그림자 (가독성 확보) */
    h1, h3, p, label, div, span {{
        color: white !important;
        font-family: 'Gowun Batang', serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }}

    /* [티켓 박스] 우측 하단 배치 디자인 */
    .ticket-box {{
        background-color: rgba(0, 0, 0, 0.6); /* 반투명 검정 */
        border: 3px solid #FFD700; /* 금색 테두리 */
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        text-align: center;
        backdrop-filter: blur(5px); /* 배경 흐림 효과 */
    }}
    
    /* 입력창 스타일 */
    .stTextInput input {{
        background-color: #ffffff !important;
        color: #333333 !important;
        border-radius: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- [Scene 1] 입장 전: 커튼 닫힌 상태 ---
if not st.session_state['entered']:
    
    # 레이아웃: 화면 위쪽을 비워서 티켓 박스를 아래로 내림
    # (vh 단위는 화면 높이의 %를 의미합니다. 40vh = 화면의 40% 빈 공간)
    st.markdown("<div style='height: 40vh;'></div>", unsafe_allow_html=True)

    # 3단 분할 (좌측 여백 - 중간 여백 - 우측 티켓박스)
    col1, col2, col3 = st.columns([1, 1, 1.2]) 
    
    with col3:
        # 티켓 박스 시작
        st.markdown('<div class="ticket-box">', unsafe_allow_html=True)
        st.markdown('<h3>🎫 관람객 등록 (Ticket)</h3>', unsafe_allow_html=True)
        
        with st.form("ticket_form"):
            name = st.text_input("이름 (Name)", placeholder="이름을 입력하세요")
            
            c1, c2 = st.columns(2)
            with c1:
                age = st.slider("나이", 5, 100, 25)
            with c2:
                nat = st.selectbox("국적", ["대한민국", "USA", "China", "Japan"])
                
            # 버튼
            submit = st.form_submit_button("🎬 입장하기")
            
            if submit:
                if name:
                    st.session_state['entered'] = True
                    st.session_state['user_name'] = name
                    st.rerun() # 화면 새로고침 (배경 바뀜)
                else:
                    st.warning("이름을 꼭 적어주세요!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        # 티켓 박스 끝

# --- [Scene 2] 입장 후: 커튼 열린 무대 ---
else:
    # 제목 표시
    st.markdown(f"# 🎭 Seoul Story Theater: {st.session_state['user_name']}님의 무대")
    
    with st.container():
        tab1, tab2 = st.tabs(["📖 이야기", "💬 대화"])
        
        with tab1:
            c1, c2 = st.columns([1, 1.5])
            with c1:
                # 해치 이미지 (예시)
                st.image("https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Animals/Front-Facing%20Baby%20Chick.png", width=200) 
            with c2:
                st.markdown("""
                ### 📜 제1막: 전설의 시작
                **(무대 조명이 켜지며)**
                
                안녕하시오! 나는 이 구역의 이야기꾼 해치라오.
                오늘 들려줄 이야기는 아주 오래된 전설이지...
                """)
    
    # 나가기 버튼
    st.markdown("---")
    if st.button("🚪 극장 나가기"):
        st.session_state['entered'] = False
        st.rerun()
