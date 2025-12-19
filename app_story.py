import streamlit as st
import pandas as pd
import os
import unicodedata
import base64
from openai import OpenAI

# ------------------------------------------------------------------
# 1. 페이지 설정
# ------------------------------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="서울 해치 탐험",
    page_icon="🦁",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------------
# 2. 해치 이름 매핑
# ------------------------------------------------------------------
name_map = {
    "종로구": "초롱해치", "중구": "쇼퍼해치", "용산구": "어텐션해치",
    "성동구": "뚝해치", "광진구": "광나루해치", "동대문구": "한약해치",
    "중랑구": "장미해치", "성북구": "선잠해치", "강북구": "북수해치",
    "도봉구": "호랑해치", "노원구": "태해치", "은평구": "진관해치",
    "서대문구": "홍지해치", "마포구": "가수해치", "양천구": "배움해치",
    "강서구": "강초해치", "구로구": "디지털해치", "금천구": "봉제해치",
    "영등포구": "등포해치", "동작구": "현충해치", "관악구": "낙성해치",
    "서초구": "법조해치", "강남구": "패션해치", "송파구": "몽촌해치",
    "강동구": "암사해치"
}

# ------------------------------------------------------------------
# 3. 유틸
# ------------------------------------------------------------------
def find_image_file(region, char_name):
    try:
        for f in os.listdir("."):
            target = f"{region}_{char_name}.png"
            if unicodedata.normalize("NFC", f) == unicodedata.normalize("NFC", target):
                return f
    except:
        pass
    return None


def speak(client, text, lang):
    if not client or not text:
        return
    try:
        voice = "alloy" if lang == "English" else "shimmer"
        res = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=text
        )
        audio_base64 = base64.b64encode(res.content).decode()
        st.markdown(
            f'<audio autoplay src="data:audio/mp3;base64,{audio_base64}"></audio>',
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"TTS 오류: {e}")

# ------------------------------------------------------------------
# 4. 데이터 로딩
# ------------------------------------------------------------------
@st.cache_data
def load_database():
    csv = "seoul_data.csv"
    if not os.path.exists(csv):
        return None

    for enc in ["utf-8-sig", "cp949", "utf-8"]:
        try:
            df = pd.read_csv(csv, encoding=enc).fillna("")
            db = {}
            for _, r in df.iterrows():
                region = str(r.get("region", r.get("지역", ""))).strip()
                if not region:
                    continue
                db[region] = {
                    "name": name_map.get(region, "서울해치"),
                    "role": r.get("role", "서울의 수호신"),
                    "personality": r.get("personality", "친절함"),
                    "tone": r.get("tone", "부드러움"),
                    "story": r.get("story", ""),
                    "welcome": r.get("welcome-msg", "반갑소!"),
                }
            return db
        except:
            continue
    return None


seoul_db = load_database()
if not seoul_db:
    st.error("서울 데이터(seoul_data.csv) 로딩 실패")
    st.stop()

# ------------------------------------------------------------------
# 5. 세션 상태
# ------------------------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "welcome_text" not in st.session_state:
    st.session_state.welcome_text = ""

# ------------------------------------------------------------------
# 6. 인트로 화면
# ------------------------------------------------------------------
if st.session_state.user is None:
    st.markdown("<h1 style='text-align:center;color:#FF4B4B;'>🦁 서울 해치 탐험</h1>", unsafe_allow_html=True)

    with st.form("join"):
        name = st.text_input("이름")
        age = st.slider("나이", 5, 100, 25)
        lang = st.selectbox("언어", ["한국어", "English", "日本語", "中文"])
        if st.form_submit_button("시작"):
            if name:
                st.session_state.user = {"name": name, "age": age, "lang": lang}
                st.rerun()

# ------------------------------------------------------------------
# 7. 메인 화면
# ------------------------------------------------------------------
else:
    user = st.session_state.user

    with st.sidebar:
        api_key = st.text_input("OpenAI API Key", type="password")
        client = OpenAI(api_key=api_key) if api_key else None
        region = st.selectbox("지역 선택", list(seoul_db.keys()))
        if st.button("처음으로"):
            st.session_state.user = None
            st.rerun()

    char = seoul_db[region]
    st.markdown(f"<h2>🗺️ {region} - {char['name']}</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.3])
    with col1:
        img = find_image_file(region, char["name"])
        if img:
            st.image(img, use_container_width=True)

    with col2:
        if client and not st.session_state.welcome_text:
            prompt = (
                f"너는 서울의 해치 '{char['name']}'다.\n"
                f"성격: {char['tone']}\n"
                f"전설 핵심: {char['story']}\n"
                f"사용자 이름은 {user['name']}.\n"
                f"한 문장으로 따뜻하게 환영해라.\n"
                f"언어: {user['lang']}"
            )
            res = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )
            st.session_state.welcome_text = res.output_text

        welcome = st.session_state.welcome_text or char["welcome"]

        st.info(f"🛡️ 역할: {char['role']}\n\n🧬 성격: {char['personality']}")
        st.markdown(
            f"<div style='background:#FFF3CD;padding:20px;border-radius:15px;'>"
            f"<b>{char['name']}</b>: {welcome}</div>",
            unsafe_allow_html=True
        )

        if st.button("🔊 인사 듣기") and client:
            speak(client, welcome, user["lang"])
