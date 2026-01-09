import streamlit as st
import time

# 1. 페이지 설정 (반드시 가장 윗부분에 위치)
st.set_page_config(
    page_title="서울 스토리 씨어터",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 스타일 커스텀 (CSS) - 극장 분위기 연출 (어두운 배경, 붉은 커튼 톤)
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117; /* 짙은 남색 배경 */
        color: #FAFAFA;
    }
    .theater-header {
        text-align: center;
        font-family: 'Gowun Batang', serif;
        color: #FF4B4B; /* 포인트 컬러 */
        padding-bottom: 20px;
        border-bottom: 2px solid #FF4B4B;
        margin-bottom: 30px;
    }
    .ticket-box {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border: 2px dashed #FF4B4B; /* 티켓 절취선 느낌 */
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 세션 상태 초기화 (입장 여부 확인)
if 'entered' not in st.session_state:
    st.session_state['entered'] = False

# --- 사이드바 (언어 설정 등) ---
with st.sidebar:
    st.header("⚙️ 극장 안내소")
    language = st.selectbox("언어 (Language)", ["한국어", "English", "日本語", "中文"])
    st.info("💡 Tip: F11을 눌러 전체화면으로 보시면 더 실감납니다.")

# --- 메인 로직 ---

# [Scene 1] 입장 전: 매표소 (Ticket Booth)
if not st.session_state['entered']:
    # 타이틀 섹션
    st.markdown("<h1 class='theater-header'>🎪 서울 스토리 씨어터 🎪<br><span style='font-size:20px; color:white'>해치가 들려주는 서울 이야기</span></h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class='ticket-box'>
            <h3>🎫 관람객 정보 등록 (Ticket)</h3>
            <p>공연 입장을 위해 티켓 정보를 입력해주세요.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 입력 폼
        with st.form("ticket_form"):
            name = st.text_input("관람객 이름 (Name)", placeholder="예: 김동이")
            age = st.slider("나이 (Age)", 5, 100, 25)
            nationality = st.selectbox("국적 (Nationality)", ["대한민국", "USA", "Japan", "China", "Others"])
            
            submitted = st.form_submit_button("🎬 입장하기 (Enter)")
            
            if submitted:
                if name:
                    st.session_state['entered'] = True
                    st.session_state['user_name'] = name
                    st.success(f"환영합니다, {name}님! 곧 막이 오릅니다...")
                    time.sleep(1.5) # 극장 문 열리는 연출 시간
                    st.rerun()
                else:
                    st.error("이름을 입력해야 입장할 수 있습니다.")

# [Scene 2] 입장 후: 메인 무대 (Main Stage)
else:
    # 상단 네비게이션
    st.markdown(f"### 🎭 현재 상영 중: **{st.session_state['user_name']}님의 서울 탐험**")
    
    # 탭 메뉴 구성 (기획안 반영)
    tab1, tab2, tab3 = st.tabs(["📖 전설의 무대 (Story)", "💬 배우와 대화 (Chat)", "🎨 나만의 해치 (Make)"])
    
    with tab1:
        st.markdown("### 📜 오늘의 이야기: 경복궁의 수호신")
        st.image("https://images.unsplash.com/photo-1596485044893-97c27599c158", caption="무대 위: 경복궁 근정전", use_container_width=True)
        st.write("옛날 옛적, 한양 도성에는 궁궐을 지키는 신비한 동물 '해치'가 살고 있었습니다...")
        st.audio("https://samplelib.com/lib/preview/mp3/sample-3s.mp3") # 임시 오디오

    with tab2:
        st.markdown("### 💬 해치 배우와의 만남")
        # 채팅 UI 예시
        messages = st.container(height=300)
        messages.chat_message("assistant", avatar="🦁").write(f"반갑소! 나는 종로구를 지키는 선비 해치라오. {st.session_state['user_name']} 대협은 어디서 오셨소?")
        user_input = st.chat_input("해치에게 말을 걸어보세요...")
        if user_input:
            messages.chat_message("user").write(user_input)
            messages.chat_message("assistant", avatar="🦁").write("허허, 참으로 재미있는 말이구려! (아직 대본 연습 중입니다)")

    with tab3:
        st.markdown("### 🎨 나만의 배우 캐스팅")
        st.info("준비 중입니다. 곧 나만의 해치 캐릭터를 만들 수 있습니다!")
        
    # 나가기 버튼
    if st.button("🚪 극장 나가기 (Exit)"):
        st.session_state['entered'] = False
        st.rerun()
