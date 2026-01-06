import streamlit as st
import os
from openai import OpenAI
import time

# -------------------------------------------------------------------------
# [설정] 통합 버전: 서울 해치 유니버스 (사용자용 + 관리자용)
# -------------------------------------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="서울 해치 유니버스",
    page_icon="🦁",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------
# [스타일] CSS (디자인 고도화)
# -------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    
    /* 전체 폰트 적용 */
    html, body, [class*="css"] {
        font-family: 'Jua', sans-serif !important;
    }
    
    /* 타이틀 스타일 */
    .main-title {
        font-size: 3rem !important;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 관리자 모드 전용 박스 스타일 */
    .admin-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4B8BBE;
        margin-bottom: 20px;
        font-family: 'Malgun Gothic', sans-serif; /* 관리자는 가독성 폰트 */
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# [데이터] 14년 축적 로컬 데이터 자산 (공통 DB)
# -------------------------------------------------------------------------
seoul_db = {
    "종로구": {
        "name": "초롱해치",
        "role": "전통과 역사를 지키는 해치",
        "personality": "진지하고 사려 깊음, 예의 바름",
        "speech": "사극 톤 (~하오, ~다오)",
        "keyword": "경복궁, 창덕궁, 전통차, 한복",
        "visual_desc": "Traditional Korean hat (Gat), holding a lantern, pink color haechi character"
    },
    "중구": {
        "name": "쇼퍼해치",
        "role": "쇼핑 도우미 도깨비",
        "personality": "활기차고 트렌디함, 열정적",
        "speech": "쇼호스트 톤 (~거든요!, ~신상이에요!)",
        "keyword": "명동, 쇼핑, 패션, 남대문시장",
        "visual_desc": "Wearing sunglasses, carrying colorful shopping bags, trendy fashion haechi character"
    },
    "용산구": {
        "name": "어텐션해치",
        "role": "다양성 존중 힙합 도깨비",
        "personality": "쿨하고 자유로움, 개방적",
        "speech": "교포 힙합 톤 (Yo!, Respect!)",
        "keyword": "이태원, 세계 음식, 다양성, 뮤직",
        "visual_desc": "Wearing headphones and hoodie, hip-hop style haechi character"
    },
    "성동구": {
        "name": "뚝해치",
        "role": "과거와 현재를 잇는 감성 해치",
        "personality": "감성적이고 차분함, 낭만적",
        "speech": "동화 구연가 톤 (~했답니다, ~군요)",
        "keyword": "성수동 카페거리, 살곶이다리, 팝업스토어",
        "visual_desc": "Sitting in a cafe, holding a coffee cup, emotional atmosphere haechi character"
    },
    "광진구": {
        "name": "광나루해치",
        "role": "미식가 해치",
        "personality": "먹는 것을 좋아함, 미식가",
        "speech": "미식가 톤 (음~!, 캬~!)",
        "keyword": "한강, 뚝섬유원지, 맛집, 야경",
        "visual_desc": "Eating delicious food, happy face haechi character"
    }
}

# -------------------------------------------------------------------------
# [사이드바] 모드 선택 (핵심 기능)
# -------------------------------------------------------------------------
with st.sidebar:
    st.title("🦁 해치 유니버스")
    st.caption("AI Based Local Story Platform")
    
    st.markdown("---")
    
    # 여기서 모드를 선택합니다
    app_mode = st.radio(
        "모드 선택 (Mode Switch)", 
        ["🙋‍♂️ 해치 탐험 (사용자용)", "🛠️ 콘텐츠 스튜디오 (관리자용)"],
        index=0
    )
    
    st.markdown("---")
    
    # API 키 입력
    if "OPENAI_API_KEY" in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
    else:
        api_key = st.text_input("OpenAI API Key", type="password")
    
    client = None
    if api_key:
        try: client = OpenAI(api_key=api_key)
        except: pass

# =========================================================================
# [MODE 1] 사용자 모드: 해치 탐험 (B2C Chatbot)
# =========================================================================
if app_mode == "🙋‍♂️ 해치 탐험 (사용자용)":
    
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = None

    # 1-1. 인트로 화면 (로그인)
    if st.session_state.user_profile is None:
        st.markdown('<p class="main-title">🦁 서울 해치 탐험대</p>', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>안녕? 나는 서울을 지키는 해치야!</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            with st.form("intro_form"):
                st.write("너에 대해 알려주면 딱 맞는 친구를 소개해줄게!")
                name = st.text_input("이름이 뭐야?")
                age = st.slider("나이는?", 5, 100, 20)
                submitted = st.form_submit_button("탐험 시작하기!", use_container_width=True)
                
                if submitted and name:
                    st.session_state.user_profile = {"name": name, "age": age}
                    st.rerun()

    # 1-2. 메인 탐험 화면 (채팅)
    else:
        user = st.session_state.user_profile
        
        # 지역 선택
        region = st.selectbox("어느 지역으로 떠날까?", list(seoul_db.keys()))
        char = seoul_db[region]
        
        col1, col2 = st.columns([1, 2])
        with col1:
            # 캐릭터 이미지 (플레이스홀더)
            st.info(f"📸 {char['visual_desc']}")
            
        with col2:
            st.subheader(f"👋 안녕! 나는 {region}의 '{char['name']}'야!")
            st.write(f"**성격:** {char['personality']}")
            st.write(f"**특징:** {char['keyword']}")
            st.success(f
