import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(
    page_title="서울 스토리 씨어터",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed" # 몰입감을 위해 사이드바 기본 닫힘
)

# 2. 세션 상태 초기화
if 'entered' not in st.session_state:
    st.session_state['entered'] = False

# 3. CSS 스타일링 (배경 및 배치 마법)
# 배경 이미지 URL (무료 이미지 소스 활용)
IMG_CURTAIN = "https://images.unsplash.com/photo-1514306191717-452ec28c7f42?q=80&w=2070&auto=format&fit=crop" # 닫힌 커튼 느낌
IMG_STAGE = "https://images.unsplash.com/photo-1503095392269-41a979922c00?q=80&w=2070&auto=format&fit=crop"   # 어두운 조명 무대

# 현재 상태에 따른 배경 선택
current_bg = IMG_STAGE if st.session_state['entered'] else IMG_CURTAIN

st.markdown(f"""
    <style>
    /* 전체 배경 이미지 적용 */
    .stApp {{
        background-image: url("{current_bg}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        transition: background-image 1s ease-in-out; /* 부드러운 전환 효과 */
    }}
    
    /* 텍스트 가독성을 위한 그림자 처리 */
    h1, h2, h3, p, label, .stMarkdown {{
        color: white !important;
        text-shadow: 2px 2px 4px #000000;
        font-family: 'Gowun Batang', serif;
    }}

    /* 입장권 박스 디자인 (우측 하단 배치용 스타일) */
    .ticket-container {{
        background-color: rgba(0, 0, 0, 0.7); /* 반투명 검정 배경 */
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #FFD700; /* 금색 테두리 */
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.5); /* 금색 빛 */
    }}
    
    /* 입력 필드 스타일 */
    .stTextInput input {{
        background-color: rgba(255, 255, 255, 0.9);
        color: black !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- [Scene 1] 입장 전: 닫힌 커튼과 매표소 ---
if not st.session_state['entered']:
    
    # 레이아웃: 빈 공간을 만들어 티켓 박스를 아래로 밈
    # (Streamlit은 위에서 아래로 쌓이는 구조라 '빈 공간(Spacer)'을 둡니다)
    st.markdown("<div style='height: 40vh;'></div>", unsafe_allow_html=True) # 화면의 40%만큼 빈 공간

    # 3단 컬럼: [빈 공간] - [빈 공간] - [티켓 박스]
    col1, col2, col3 = st.columns([1, 1, 1.2]) 
    
    with col3: # 오른쪽 하단 위치
        st.markdown("<div class='ticket-container'><h3>🎟️ 관람객 등록 (Ticket)</h3>", unsafe_allow_html=True)
        
        with st.form("ticket_form"):
            name = st.text_input("이름 (Name)", placeholder="관람객 이름을 적어주세요")
            
            # 폼 내부 레이아웃
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                age = st.slider("나이", 5, 100, 25)
            with sub_col2:
                nationality = st.selectbox("국적", ["대한민국", "USA", "Japan", "China"])
            
            submitted = st.form_submit_button("🎬 입장하기 (Enter Stage)")
            
            if submitted:
                if name:
                    st.session_state['entered'] = True
                    st.session_state['user_name'] = name
                    st.success(f"{name}님, 극장으로 안내합니다...")
                    time.sleep(1.0) # 전환 딜레이
                    st.rerun()
                else:
                    st.warning("입장권을 위해 이름을 입력해주세요.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- [Scene 2] 입장 후: 열린 무대 (메인 콘텐츠) ---
else:
    # 상단 타이틀
    st.markdown(f"# 🎭 Seoul Story Theater: {st.session_state['user_name']}님의 무대")
    
    # 탭 메뉴 (반투명 컨테이너로 감싸기)
    with st.container():
        tab1, tab2, tab3 = st.tabs(["📖 전설의 이야기", "💬 해치와 대화", "🎨 캐릭터 생성"])
        
        with tab1:
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.image("https://images.unsplash.com/photo-1596485044893-97c27599c158", caption="배경: 경복궁 근정전", use_container_width=True)
            with col_b:
                st.markdown("""
                ### 📜 제1막: 경복궁의 수호신
                
                (무대 조명이 켜지며)
                
                **해치:** "어서 오시오! 내 그대를 기다리고 있었소."
                
                옛날 옛적, 한양 도성에는 화재와 재앙을 막아주는 신비한 동물 해치가 살고 있었습니다...
                """)
                st.audio("https://samplelib.com/lib/preview/mp3/sample-3s.mp3") 

        with tab2:
            st.info("준비 중: 해치와의 실시간 대화 기능이 곧 연결됩니다.")

        with tab3:
            st.info("준비 중: 나만의 해치 만들기 기능")

    # 나가기 버튼 (왼쪽 하단)
    st.markdown("---")
    if st.button("🚪 극장 나가기 (Exit)"):
        st.session_state['entered'] = False
        st.rerun()
