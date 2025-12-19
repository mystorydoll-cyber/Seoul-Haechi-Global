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
        audio_tag = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
        st.markdown(audio_tag, unsafe_allow_html=True)
        st.audio(response.content, format="audio/mp3")
    except Exception as e:
        st.error(f"🔈 오디오 재생 중 오류 발생: {e}")

@st.cache_data
def load_full_database():
    csv_file = "seoul_data.csv"
    if not os.path.exists(csv_file): return {} # None 대신 빈 딕셔너리 반환
    # ... (기존 로직 동일)
    return db # (기존 로직에서 구성된 db 반환)

# 데이터 로드 및 초기화
seoul_db = load_full_database()
if "user_profile" not in st.session_state: st.session_state.user_profile = None
if "story_text" not in st.session_state: st.session_state.story_text = ""

# --- 화면 로직 시작 ---

if st.session_state.user_profile is None:
    # [화면 1] 입단 신청서 (생략: 기존 코드 유지)
    pass
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
        # ... (중략)

    # [화면 2] 메인 탐험
    # (중략: 기존 UI 로직 유지)

    t1, t2, t3, t4 = st.tabs(["📜 전설 듣기", "🗣️ 대화하기", "🎨 그림 그리기", "👑 작가 되기"])

    with t1:
        st.subheader(f"📜 {char['name']}의 전설")
        if st.button("이야기 생성! (Generate Story)"):
            if not client: 
                st.error("API Key가 필요합니다.")
            else:
                with st.spinner("해치가 기억을 떠올리고 있습니다..."):
                    prompt = f"당신은 {char['name']}. 전설 {char['story']}를 {user['language']}로 {user['age']}세 대원에게 들려주세요. 말투는 {char['tone']}입니다."
                    res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"system", "content":prompt}])
                    st.session_state.story_text = res.choices[0].message.content
        
        if st.session_state.story_text:
            st.write(st.session_state.story_text)
            if st.button("🔊 음성으로 듣기"):
                speak(client, st.session_state.story_text, user['language'])
