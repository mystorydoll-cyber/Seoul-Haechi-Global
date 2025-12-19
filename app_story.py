import streamlit as st
import pandas as pd
import os
from openai import OpenAI
import unicodedata
import base64

# 1. [설정] UI & 다국어 초기화
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

# 2. [기능] 이미지 검색 엔진 (경로 체크 강화)
def find_image_file(region, char_name):
    try:
        current_files = os.listdir(".")
        # 1순위: 지역_이름.png (NFC 정규화 대응)
        target = f"{region}_{char_name}.png"
        for file in current_files:
            if unicodedata.normalize('NFC', file) == unicodedata.normalize('NFC', target):
                return file
        # 2순위: 지역으로 시작하는 png
        for file in current_files:
            if file.startswith(region) and file.lower().endswith(".png"):
                return file
    except: pass
    return None

# 3. [기능] TTS 스피커 기능 (OpenAI 활용)
def speak_text(client, text, voice="alloy"):
    if not client: return
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        # 오디오 데이터를 base64로 변환하여 재생
        audio_base64 = base64.b64encode(response.content).decode('utf-8')
        audio_tag = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
        st.markdown(audio_tag, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"🔈 음성 생성 오류: {e}")

# 4. [데이터 엔진] CSV 로드 (상세 컬럼 매핑)
@st.cache_data
def load_full_database():
    csv_file = "seoul_data.csv"
    if not os.path.exists(csv_file): return None
    
    for enc in ['utf-8-sig', 'cp949', 'utf-8']:
        try:
            df = pd.read_csv(csv_file, encoding=enc)
            df.columns = df.columns.str.strip()
            df = df.fillna("")
            db = {}
            for _, row in df.iterrows():
                reg = str(row.get('region', row.get('지역', ''))).strip()
                if reg:
                    c_name = name_map.get(reg, "서울해치")
                    db[reg] = {
                        "name": c_name,
                        "role": str(row.get('role', '서울의 수호신')).strip(),
                        "personality": str(row.get('tone', row.get('말투', '친절함'))).strip(),
                        "story": str(row.get('story', '')).strip(),
                        "welcome": str(row.get('welcome-msg', '반갑소!')).strip(),
                        "visual": str(row.get('visual_desc', '')).strip(),
                        "keyword": str(row.get('툭징2', reg)).strip()
                    }
            return db
        except: continue
    return None

seoul_db = load_full_database()

# 5. [UI 스타일]
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    * { font-family: 'Jua', sans-serif !important; }
    .main-title { text-align: center; font-size: 3.2rem; color: #FF4B4B; }
    .speech-bubble { background-color: #FFF3CD; border: 2px solid #FFEeba; border-radius: 20px; padding: 20px; font-size: 1.4rem; color: #856404; }
</style>
""", unsafe_allow_html=True)

# 6. [세션 관리]
if "user_profile" not in st.session_state: st.session_state.user_profile = None
if "messages" not in st.session_state: st.session_state.messages = []

# [화면 1] 인트로
if st.session_state.user_profile is None:
    st.markdown('<p class="main-title">🦁 서울 해치 탐험 : 입단 신청서</p>', unsafe_allow_html=True)
    with st.form("join"):
        col1, col2 = st.columns(2)
        with col1:
            u_name = st.text_input("이름 (Name)")
            u_age = st.slider("나이 (Age)", 5, 100, 25)
        with col2:
            u_nat = st.selectbox("국적 (Nationality)", ["대한민국", "USA", "China", "Japan", "Other"])
            u_lang = st.selectbox("대화 언어 (Language)", ["한국어", "English", "日本語", "中文"])
            
        if st.form_submit_button("해치 만나러 가기"):
            if u_name:
                st.session_state.user_profile = {"name": u_name, "age": u_age, "nationality": u_nat, "language": u_lang}
                st.rerun()

# [화면 2] 메인 탐험
else:
    user = st.session_state.user_profile
    if not seoul_db:
        st.error("🚨 데이터를 불러올 수 없습니다.")
        st.stop()
        
    with st.sidebar:
        st.title(f"🦁 {user['name']} 대원")
        api_key = st.text_input("🔑 OpenAI API Key", type="password")
        client = OpenAI(api_key=api_key) if api_key else None
        st.markdown("---")
        region = st.selectbox("📍 탐험 지역", list(seoul_db.keys()))
        char = seoul_db[region]
        if st.button("🔄 처음으로"):
            st.session_state.user_profile = None
            st.rerun()

    st.markdown(f"<h1>🗺️ {region} 탐험</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 1.2])
    with c1:
        img_f = find_image_file(region, char['name'])
        if img_f: st.image(img_f, use_container_width=True)
        else: st.info(f"📸 {char['name']} 이미지 준비중")
        
    with c2:
        st.markdown(f"<h2>{region} - {char['name']}</h2>", unsafe_allow_html=True)
        st.write(f"**역할:** {char['role']}")
        st.info(f"**해치의 성격:** {char['personality']}")
        st.markdown(f"<div class='speech-bubble'><b>{char['name']}</b>: \"{char['welcome']}\"</div>", unsafe_allow_html=True)
        if st.button("🔊 환영인사 듣기") and client:
            speak_text(client, char['welcome'])

    st.markdown("---")
    t1, t2, t3, t4 = st.tabs(["📜 전설 듣기", "🗣️ 대화하기", "🎨 그림 그리기", "👑 작가 되기"])

    with t1:
        st.subheader(f"📜 {char['name']}의 전설")
        if st.button("이야기 시작!"):
            if not client: st.error("API Key 필요")
            else:
                with st.spinner("해치가 이야기를 들려줍니다..."):
                    # 다국어 및 연령 맞춤 프롬프트
                    prompt = f"""
                    Role: {char['name']} from {region}.
                    Persona: {char['personality']}. 
                    Listener: {user['name']}, {user['age']} years old, from {user['nationality']}.
                    Language: {user['language']}.
                    
                    [Task]
                    1. Tell the story: {char['story']}
                    2. Adjust vocabulary for a {user['age']}-year-old.
                    3. Explain Korean culture kindly for foreigners.
                    4. MUST speak in the character's unique tone.
                    """
                    res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"system", "content":prompt}])
                    story_text = res.choices[0].message.content
                    st.write(story_text)
                    if st.button("🔊 이야기 음성으로 듣기"):
                        speak_text(client, story_text)

    with t2:
        st.subheader(f"🗣️ {char['name']}와 대화하기")
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.write(m["content"])
            
        if chat_p := st.chat_input("질문해보세요!"):
            if client:
                st.session_state.messages.append({"role":"user", "content":chat_p})
                with st.chat_message("user"): st.write(chat_p)
                
                with st.chat_message("assistant"):
                    sys_p = f"You are {char['name']}. Tone: {char['personality']}. Listener age: {user['age']}, Language: {user['language']}. Background: {char['story']}"
                    res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"system","content":sys_p}]+st.session_state.messages)
                    reply = res.choices[0].message.content
                    st.write(reply)
                    st.session_state.messages.append({"role":"assistant", "content":reply})
                    speak_text(client, reply)

    with t3:
        st.subheader("🎨 해치 그리기")
        if st.button("그림 생성") and client:
            with st.spinner("AI가 그리는 중..."):
                res = client.images.generate(model="dall-e-3", prompt=f"Cute 3D character, {char['visual']}, Pixar style, {region} background")
                st.image(res.data[0].url)

    with t4:
        st.subheader("👑 작가 되기")
        u_story = st.text_area("에피소드를 적어주세요.")
        if st.button("평가받기") and client:
            eval_p = f"You are {char['name']}. Tone: {char['personality']}. Read this story in {user['language']} and give warm feedback: {u_story}"
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"user", "content":eval_p}])
            feedback = res.choices[0].message.content
            st.success(feedback)
            speak_text(client, feedback)
