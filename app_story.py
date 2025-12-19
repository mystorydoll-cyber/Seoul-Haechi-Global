import streamlit as st
import pandas as pd
import os
from openai import OpenAI
import unicodedata
import base64

# 1. [설정] UI 유지 및 초기화
st.set_page_config(layout="wide", page_title="서울 해치 탐험", page_icon="🦁")

# [데이터] 구별 고유 해치 이름 매칭
name_map = {
    "종로구": "초롱해치", "중구": "쇼퍼해치", "용산구": "어텐션해치", "성동구": "뚝해치", 
    "광진구": "광나루해치", "동대문구": "한약해치", "중랑구": "장미해치", "성북구": "선잠해치", 
    "강북구": "북수해치", "도봉구": "호랑해치", "노원구": "태해치", "은평구": "진관해치", 
    "서대문구": "홍지해치", "마포구": "가수해치", "양천구": "배움해치", "강서구": "강초해치", 
    "구로구": "디지털해치", "금천구": "봉제해치", "영등포구": "등포해치", "동작구": "현충해치", 
    "관악구": "낙성해치", "서초구": "법조해치", "강남구": "패션해치", "송파구": "몽촌해치", "강동구": "암사해치"
}

# [기능] 이미지/음성 관련 함수
def find_image_file(region, char_name):
    try:
        current_files = os.listdir(".")
        target = f"{region}_{char_name}.png"
        for file in current_files:
            if unicodedata.normalize('NFC', file) == unicodedata.normalize('NFC', target):
                return file
    except: pass
    return None

def speak(client, text, lang="한국어"):
    if not client or not text: return
    try:
        voice_model = "alloy" if lang == "English" else "shimmer"
        response = client.audio.speech.create(model="tts-1", voice=voice_model, input=text)
        audio_base64 = base64.b64encode(response.content).decode('utf-8')
        # HTML 태그를 이용한 자동 재생 시도 및 컨트롤러 노출
        audio_tag = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
        st.markdown(audio_tag, unsafe_allow_html=True)
        st.audio(response.content, format="audio/mp3")
    except Exception as e:
        st.error(f"🔈 오디오 재생 중 오류 발생: {e}")

# 2. [데이터 엔진] NameError 해결 및 데이터 로드 로직 복구
@st.cache_data
def load_full_database():
    csv_file = "seoul_data.csv"
    if not os.path.exists(csv_file): 
        return {} 
    
    # 인코딩 순차 시도
    for enc in ['utf-8-sig', 'cp949', 'utf-8']:
        try:
            df = pd.read_csv(csv_file, encoding=enc)
            df.columns = df.columns.str.strip()
            df = df.fillna("")
            
            # db 변수 생성 및 데이터 구조화
            db = {str(row.get('region', row.get('지역', ''))).strip(): {
                "name": name_map.get(str(row.get('region', row.get('지역', ''))).strip(), "서울해치"),
                "role": str(row.get('role', '서울의 수호신')).strip(),
                "personality": str(row.get('personality', row.get('성격', '친절함'))).strip(),
                "tone": str(row.get('tone', row.get('말투', '부드러움'))).strip(),
                "story": str(row.get('story', row.get('전설', ''))).strip(),
                "welcome": str(row.get('welcome-msg', '반갑소!')).strip(),
                "visual": str(row.get('visual_desc', ''))
            } for _, row in df.iterrows() if str(row.get('region', row.get('지역', ''))).strip()}
            
            return db # 정상적으로 처리된 db 반환
        except:
            continue
    return {}

# 데이터 로드 및 세션 초기화
seoul_db = load_full_database()
if "user_profile" not in st.session_state: st.session_state.user_profile = None
if "story_text" not in st.session_state: st.session_state.story_text = ""

# --- 화면 로직 시작 ---

# CSS 스타일 정의
st.markdown("""
<style>
    .speech-bubble { background-color: #FFF3CD; border-radius: 15px; padding: 15px; margin-bottom: 10px; border-left: 5px solid #FF4B4B; }
</style>
""", unsafe_allow_html=True)

if st.session_state.user_profile is None:
    # [화면 1] 인트로 및 입단 신청서
    st.title("🦁 서울 해치 탐험")
    with st.form("join_form"):
        u_name = st.text_input("이름", placeholder="탐험대원 이름")
        u_lang = st.selectbox("언어", ["한국어", "English", "日本語"])
        u_age = st.slider("나이", 5, 100, 25)
        if st.form_submit_button("탐험 시작"):
            if u_name:
                st.session_state.user_profile = {"name": u_name, "language": u_lang, "age": u_age}
                st.rerun()
else:
    user = st.session_state.user_profile
    with st.sidebar:
        st.title(f"🦁 {user['name']} 대원")
        api_key = st.text_input("🔑 OpenAI API Key", type="password")
        client = OpenAI(api_key=api_key) if api_key else None
        
        if not seoul_db:
            st.error("데이터를 불러올 수 없습니다. CSV 파일을 확인하세요.")
            st.stop()
            
        region_list = list(seoul_db.keys())
        region = st.selectbox("📍 탐험 지역 선택", region_list)
        char = seoul_db[region]
        
        if st.button("🔄 처음으로"):
            st.session_state.user_profile = None
            st.session_state.story_text = ""
            st.rerun()

    # [화면 2] 메인 탐험 영역
    st.header(f"🗺️ {region} 탐험: {char['name']}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        img_f = find_image_file(region, char['name'])
        if img_f: st.image(img_f, use_container_width=True)
        else: st.info("캐릭터 이미지를 찾고 있습니다.")

    with col2:
        st.markdown(f"**🛡️ 역할:** {char['role']}")
        st.markdown(f"**💬 말투:** {char['tone']}")
        st.markdown(f"<div class='speech-bubble'><b>{char['name']}</b>: {char['welcome']}</div>", unsafe_allow_html=True)

    st.markdown("---")
    t1, t2, t3, t4 = st.tabs(["📜 전설 듣기", "🗣️ 대화하기", "🎨 그림 그리기", "👑 작가 되기"])

    with t1:
        st.subheader(f"📜 {char['name']}의 전설")
        if st.button("이야기 생성! (Generate Story)"):
            if not client: 
                st.error("API Key가 필요합니다.")
            else:
                with st.spinner("해치가 기억을 떠올리는 중..."):
                    prompt = f"당신은 {char['name']}. 전설 {char['story']}를 {user['language']}로 {user['age']}세 대원에게 들려주세요. 말투는 {char['tone']}입니다."
                    res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"system", "content":prompt}])
                    st.session_state.story_text = res.choices[0].message.content
        
        if st.session_state.story_text:
            st.info(st.session_state.story_text)
            if st.button("🔊 음성으로 듣기"):
                speak(client, st.session_state.story_text, user['language'])
