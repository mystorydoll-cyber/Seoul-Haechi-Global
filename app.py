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

# 3. CSS 스타일링 (강력한 배경 적용 버전)
# 배경 이미지 URL
IMG_CURTAIN = "https://images.unsplash.com/photo-1514306191717-452ec28c7f42?q=80&w=2070&auto=format&fit=crop" # 닫힌 커튼
IMG_STAGE = "https://images.unsplash.com/photo-1503095392269-41a979922c00?q=80&w=2070&auto=format&fit=crop"   # 어두운 무대

# 현재 상태에 따른 배경 선택
current_bg = IMG_STAGE if st.session_state['entered'] else IMG_CURTAIN

st.markdown(f"""
    <style>
    /* 1. 전체 배경 강제 적용 (가장 중요) */
    [data-testid="stAppViewContainer"] {{
        background-image: url("{current_bg}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* 2. 상단 헤더 투명화 (이미지 가리지 않게) */
    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0);
    }}
    
    /* 3. 텍스트 스타일 */
    h1, h2, h3, p, label, .stMarkdown {{
        color: white !important;
        text-shadow: 2px 2px 4px #000000;
        font-family: 'Gowun Batang', serif;
    }}

    /* 4. 입장권 박스 디자인 (우측 하단) */
    .ticket-container {{
        background-color: rgba(0, 0, 0, 0.8); /* 더 진한 검정 */
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #FFD700; /* 금색 테두리 */
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
        text-align: center;
    }}
    
    /* 입력 필드 스타일 조정 */
    .stTextInput input {{
        color: black !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- [Scene 1] 입장 전: 닫힌 커튼과 매표소 ---
if not st.session_state['entered']:
    
    # 레이아웃: 화면을 위/아래로 나누는 빈 공간
    st.markdown("<div style='height: 45vh;'></div>", unsafe_allow_html=True) # 높이 조절

    # 좌우 레이아웃: [빈 공간] - [빈 공간] - [티켓 박스]
    col1, col2, col3 = st.columns([1, 1, 1.3]) 
    
    with col3: # 오른쪽 하단
        st.markdown("<div class='ticket-container'><h3>🎟️ 관람객 등록 (Ticket)</h3>", unsafe_allow_html=True)
        
        with st.form("ticket_form"):
            name = st.text_input("이름 (Name)", placeholder="관람객 이름을 적어주세요")
            
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
                    st.success(f"{name}님, 극장으로 모십니다.")
                    time.sleep(1.0)
                    st.rerun()
                else:
                    st.warning("입장권을 위해 이름을 입력해주세요.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- [Scene 2] 입장 후: 열린 무대 ---
else:
    st.markdown(f"# 🎭 Seoul Story Theater: {st.session_state['user_name']}님의 무대")
    
    # 탭 메뉴 뒷배경도 어둡게 처리
    with st.container():
        tab1, tab2, tab3 = st.tabs(["📖 전설의 이야기", "💬 해치와 대화", "🎨 캐릭터 생성"])
        
        with tab1:
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.image("https://images.unsplash.com/photo-1596485044893-97c27599c158", caption="경복궁 근정전", use_container_width=True)
            with col_b:
                st.markdown("""
                ### 📜 제1막: 경복궁의 수호신
                
                (조명이 켜지며)
                
                **해치:** "어서 오시오! 내 그대를 기다리고 있었소."
                
                한양 도성에는 화재와 재앙을 막아주는 신비한 동물 해치가 살고 있었습니다...
                """)

        with tab2:
            st.info("준비 중입니다.")

        with tab3:
            st.info("준비 중입니다.")

    st.markdown("---")
    if st.button("🚪 극장 나가기 (Exit)"):
        st.session_state['entered'] = False
        st.rerun()
