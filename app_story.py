import streamlit as st
import pandas as pd
import os
from openai import OpenAI
import unicodedata
import base64

# 1. [설정] UI 유지 및 초기화
st.set_page_config(
    layout="wide", 
    page_title="서울 해치 탐험", 
    page_icon="🦁",
    initial_sidebar_state="expanded"
)

# [데이터] 구별 고유 해치 이름 매칭
name_map = {
    "종로구": "초롱해치", "중구": "쇼퍼해치", "용산구": "어텐션해치", "성동구": "뚝해치", 
    "광진구": "광나루해치", "동대문구": "한약해치", "중랑구": "장미해치", "성북구": "선잠해치", 
    "강북구": "북수해치", "도봉구": "호랑해치", "노원구": "태해치", "은평구": "진관해치", 
    "서대문구": "홍지해치", "마포구": "가수해치", "양천구": "배움해치", "강서구": "강초해치", 
    "구로구": "디지털해치", "금천구": "봉제해치", "영등포구": "등포해치", "동작구": "현충해치", 
    "관악구": "낙성해치", "서초구": "법조해치", "강남구": "패션해치", "송파구": "몽촌해치", "강동구": "암사해치"
}

# 2. [기능] 이미지 엔진 및 TTS 스피커
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
        # 다국어 대응 보이스 설정
        v_model = "alloy" if lang == "English" else "shimmer"
        response = client.audio.speech.create(model="tts-1", voice=v_model, input=text)
        audio_base64 = base64.b64encode(response.content).decode('utf-8')
        audio_tag = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
        st.markdown(audio_tag, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"🔈 오디오 오류: {e}")

# 3. [데이터 엔진] 원본 데이터 유지
@st.cache_data
def load_full_database():
    csv_file = "seoul_data.csv"
    if not os.path.exists(csv_file): return None
    for enc in ['utf-8-sig', 'cp949', 'utf-8']:
        try:
            df = pd.read_csv(csv_file, encoding=enc)
            df.columns = df.columns.str.strip()
            df = df.fillna("")
            db = {str(row.get('region', row.get('지역', ''))).strip(): {
                "name": name_map.get(str(row.get('region', row.get('지역', ''))).strip(), "서울해치"),
                "role": str(row.get('role', '서울의 수호신')).strip(),
                "personality": str(row.get('personality', row.get('성격', '친절함'))).strip(),
                "tone": str(row.get('tone', row.get('말투', '부드러움'))).strip(),
                "story": str(row.get('story', row.get('전설', ''))).strip(),
                "welcome": str(row.get('welcome-msg', '반갑소!')).strip(),
                "visual": str(row.get('visual_desc', ''))
            } for _, row in df.iterrows() if str(row.get('region', row.get('지역', ''))).strip()}
            return db
        except: continue
    return None

seoul_db = load_full_database()

# 4. [UI 스타일] 기존 스타일 엄격 유지
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    * { font-family: 'Jua', sans-serif !important; }
    .main-title { font-size: 3.5rem !important; color: #FF4B4B; text-align: center; }
    .info-box { background-color: #e8f4f8; padding: 25px; border-radius: 15px; border-left: 6px solid #FF4B4B; margin-bottom: 20px;}
    .speech-bubble { background-color: #FFF3CD; border: 2px solid #FFEeba; border-radius: 20px; padding: 20px; font-size: 1.5rem; color: #856404; margin-bottom: 10px; }
    .credit-text { font-size: 0.8rem; color: gray; text-align: right; border-top: 1px dashed #ccc; padding-top: 10px; }
</style>
""", unsafe_allow_html=True)

if "user_profile" not in st.session_state: st.session_state.user_profile = None
if "messages" not in st.session_state: st.session_state.messages = []

# -------------------------------------------------------------------------
# [화면 1] 인트로 : 영상 및 크레딧 100% 유지
# -------------------------------------------------------------------------
if st.session_state.user_profile is None:
    st.markdown('<p class="main-title">🦁 서울 해치 탐험 : 입단 신청서</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.8rem;">"안녕? 우리는 서울을 지키는 해치 군단이야!"</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    col_v, col_f = st.columns([1.5, 1], gap="large")
    with col_v:
        if os.path.exists("intro/main.mp4"): st.video("intro/main.mp4", autoplay=True, loop=True)
        st.markdown("""<div class="info-box"><h4>💡 해치(Haechi)는 어떤 친구인가요?</h4><div style="margin-top:10px;"><strong>🐣 탄생의 비밀</strong><br>선과 악을 구별하고 재앙을 막는 서울의 수호신이에요.</div><div class="credit-text">© 2025 My Story Doll & Seoul Haechi.</div></div>""", unsafe_allow_html=True)

    with col_f:
        with st.form("join"):
            u_name = st.text_input("이름 (Name)")
            u_age = st.slider("나이 (Age)", 5, 100, 25)
            u_nat = st.selectbox("국적 (Nationality)", ["대한민국", "Japan", "USA", "China", "Other"])
            u_lang = st.selectbox("대화 언어 (Language)", ["한국어", "English", "日本語", "中文"])
            if st.form_submit_button("해치 만나러 가기 (Start)", type="primary", use_container_width=True):
                if u_name:
                    st.session_state.user_profile = {"name": u_name, "age": u_age, "nationality": u_nat, "language": u_lang}
                    st.rerun()

# -------------------------------------------------------------------------
# [화면 2] 메인 탐험 : 스피커 복원 및 스토리 기반 인사말 수정
# -------------------------------------------------------------------------
else:
    user = st.session_state.user_profile
    with st.sidebar:
        st.title(f"🦁 {user['name']} 대원")
        api_key = st.text_input("🔑 OpenAI API Key", type="password")
        client = OpenAI(api_key=api_key) if api_key else None
        st.markdown("---")
        # [내비게이션 픽스] 원본 키값(Korean)을 리스트로 유지하여 다른 언어에서도 동작 보장
        region_list = list(seoul_db.keys())
        region = st.selectbox("📍 탐험 지역 선택", region_list)
        char = seoul_db[region]
        if st.button("🔄 처음으로"):
            st.session_state.user_profile = None
            st.rerun()

    st.markdown(f"<h1 style='color:#FF4B4B;'>🗺️ {region} - {char['name']}</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.2])
    
    with c1:
        img_f = find_image_file(region, char['name'])
        if img_f: st.image(img_f, use_container_width=True)

    with c2:
        # [수정] 단순 인사가 아닌 '스토리 기반 지능형 인사말' 생성
        if client:
            welcome_p = f"너는 {char['name']}야. 말투: {char['tone']}. 사용자는 {user['name']}야. 너의 전설({char['story']})의 핵심 내용을 딱 한 문장 섞어서 사용자를 환영해줘. 언어는 {user['language']}로 해줘."
            res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":welcome_p}])
            display_welcome = res.choices[0].message.content
        else:
            display_welcome = f"{char['welcome']} (OpenAI Key를 입력하면 풍성한 이야기가 시작됩니다!)"

        st.markdown(f"### ✨ {char['name']} 상세 정보")
        st.info(f"🛡️ 역할: {char['role']}\n\n🧬 성격: {char['personality']}")
        st.markdown(f"<div class='speech-bubble'><b>{char['name']}</b>: \"{display_welcome}\"</div>", unsafe_allow_html=True)
        
        # [복원] 스피커 버튼
        if st.button(f"🔊 {user['language']}로 인사 듣기") and client:
            speak(client, display_welcome, user['language'])

    st.markdown("---")
    t1, t2, t3, t4 = st.tabs(["📜 전설 듣기", "🗣️ 대화하기", "🎨 그림 그리기", "👑 작가 되기"])
    # (이하 탭 콘텐츠는 원본 유지)
    with t1:
        st.subheader(f"📜 {char['name']}의 전설")
        if st.button("이야기 시작!") and client:
            with st.spinner("이야기 중..."):
                p = f"Role: {char['name']}. Story: {char['story']}. Language: {user['language']}. Tone: {char['tone']}. Listener age: {user['age']}."
                res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"system", "content":p}])
                st.write(res.choices[0].message.content)
