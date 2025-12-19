import streamlit as st
import pandas as pd
import os
from openai import OpenAI
import unicodedata

# 1. [설정] M-CTO 정석 버전: GitHub 파일 직결 연동
st.set_page_config(
    layout="wide", 
    page_title="서울 해치 탐험", 
    page_icon="🦁",
    initial_sidebar_state="expanded"
)

# 2. [기능] 이미지 파일 매칭
def find_image_file(region, char_name):
    try:
        current_files = os.listdir(".")
        target = f"{region}_{char_name}.png"
        for file in current_files:
            if unicodedata.normalize('NFC', file) == unicodedata.normalize('NFC', target):
                return file
    except: pass
    return None

# 3. [데이터 엔진] 깃허브의 seoul_data.csv 직접 로드
@st.cache_data
def load_seoul_db():
    csv_file = "seoul_data.csv"
    if not os.path.exists(csv_file):
        return None
    
    try:
        df = pd.read_csv(csv_file)
        # 중요: 컬럼명 끝에 붙은 공백 제거 (예: 'role ' -> 'role')
        df.columns = df.columns.str.strip()
        df = df.fillna("")
        
        db = {}
        for _, row in df.iterrows():
            reg = str(row.get('region', '')).strip()
            if reg:
                db[reg] = {
                    "name": str(row.get('mascot', '해치')).strip(),
                    "role": str(row.get('role', '서울의 수호신')).strip(),
                    "personality": str(row.get('tone', '친절함')).strip(),
                    "speech": str(row.get('tone', '친절한 말투')).strip(),
                    "story": str(row.get('story', '')).strip(),
                    "welcome": str(row.get('welcome-msg', '반갑소!')).strip(),
                    "visual": str(row.get('visual_desc', '')).strip(),
                    "keyword": str(row.get('툭징2', reg)).strip()
                }
        return db
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return None

# 데이터 로드
seoul_db = load_seoul_db()

# 4. [UI] CSS 스타일
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    * { font-family: 'Jua', sans-serif !important; }
    .main-title { text-align: center; font-size: 3.5rem !important; color: #FF4B4B; margin-bottom: 0.5rem; }
    .info-box { background-color: #e8f4f8; padding: 25px; border-radius: 15px; border-left: 6px solid #FF4B4B; }
    .char-title { font-size: 3.5rem !important; color: #FF4B4B; margin-bottom: 10px; }
    .char-role { font-size: 1.6rem !important; color: #555; border-bottom: 3px solid #FFD700; display: inline-block; }
    .speech-bubble { background-color: #FFF3CD; border: 2px solid #FFEeba; border-radius: 20px; padding: 15px; font-size: 1.3rem; color: #856404; }
    .stButton>button { width: 100%; border-radius: 10px; font-size: 1.2rem; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# [로직] 앱 메인 실행부
# -------------------------------------------------------------------------
if not seoul_db:
    st.error("🚨 'seoul_data.csv' 파일을 찾을 수 없습니다. 깃허브 업로드 상태를 확인해주세요.")
    st.stop()

if "user_profile" not in st.session_state:
    st.session_state.user_profile = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# A. 입단 신청서 (Profile None)
if st.session_state.user_profile is None:
    st.markdown('<p class="main-title">🦁 서울 해치 탐험 : 입단 신청</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    col_v, col_f = st.columns([1.5, 1], gap="large")
    with col_v:
        intro_path = "intro/main.mp4"
        if os.path.exists(intro_path): st.video(intro_path, autoplay=True, loop=True)
        else: st.info("🦁 탐험 준비 완료! 아래 양식을 작성해주세요.")
        
        st.markdown('<div class="info-box"><h4>💡 해치 군단에 오신 것을 환영합니다!</h4>25개 구의 수호신들이 대원님을 기다리고 있습니다.</div>', unsafe_allow_html=True)

    with col_f:
        st.markdown("#### 🎫 대원 등록")
        with st.form("join"):
            name = st.text_input("이름")
            nat = st.selectbox("국적", ["대한민국", "USA", "China", "Japan", "Other"])
            if st.form_submit_button("입단하기", type="primary"):
                if name:
                    st.session_state.user_profile = {"name": name, "nationality": nat}
                    st.rerun()

# B. 메인 탐험 (Profile Active)
else:
    user = st.session_state.user_profile
    
    with st.sidebar:
        st.title(f"🦁 {user['name']} 대원")
        api_key = st.text_input("OpenAI API Key", type="password")
        client = OpenAI(api_key=api_key) if api_key else None
        
        st.markdown("---")
        region = st.selectbox("📍 탐험 지역", list(seoul_db.keys()))
        char = seoul_db[region]
        
        if st.button("🔄 처음으로 돌아가기"):
            st.session_state.user_profile = None
            st.session_state.chat_history = []
            st.rerun()

    # 메인 콘텐츠 레이아웃
    st.markdown(f"<h1 style='color:#FF4B4B;'>🗺️ {region} : {char['name']}</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 1.2])
    with c1:
        img = find_image_file(region, char['name'])
        if img: st.image(img, width=400)
        else: st.info(f"📸 {char['name']} 이미지를 찾을 수 없습니다.")
        
    with c2:
        st.markdown(f"<p class='char-title'>{char['name']}</p>", unsafe_allow_html=True)
        st.markdown(f"<span class='char-role'>{char['role']}</span>", unsafe_allow_html=True)
        st.markdown(f"<div style='background-color:#fff; border:2px solid #eee; border-radius:15px; padding:20px; margin:20px 0;'><b>💡 성격:</b> {char['personality']}<br><br><b>🗣️ 말투:</b> {char['speech']}<br><br><b>🔑 키워드:</b> {char['keyword']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='speech-bubble'><b>{char['name']}</b>: \"{char['welcome']}\"</div>", unsafe_allow_html=True)

    st.markdown("---")
    t1, t2, t3, t4 = st.tabs(["📜 원본 전설", "🗣️ 대화하기", "🎨 그림 그리기", "👑 작가 되기"])

    # 탭 1: 전설 듣기 (CSV 원본 스토리 100% 반영)
    with t1:
        st.subheader(f"📜 {char['name']}의 원본 스토리")
        if st.button("전설 읽어줘!"):
            if not client: st.error("API Key를 입력해주세요.")
            else:
                with st.spinner("이야기를 들려주는 중..."):
                    prompt = f"너는 {char['name']}야. 말투: {char['speech']}. 아래 스토리를 절대 생략하지 말고 생생하게 들려줘: {char['story']}"
                    res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"system", "content":prompt}])
                    st.info(res.choices[0].message.content)

    # 탭 2: 대화하기
    with t2:
        for m in st.session_state.chat_history:
            with st.chat_message(m["role"]): st.write(m["content"])
        
        if chat_p := st.chat_input("해치에게 물어보세요!"):
            if not client: st.error("API Key 필요")
            else:
                st.session_state.chat_history.append({"role":"user", "content":chat_p})
                with st.chat_message("user"): st.write(chat_p)
                with st.chat_message("assistant"):
                    sys_p = f"너는 {char['name']}야. 스토리: {char['story']}. 말투: {char['speech']}."
                    res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"system","content":sys_p}]+st.session_state.chat_history)
                    reply = res.choices[0].message.content
                    st.write(reply)
                    st.session_state.chat_history.append({"role":"assistant", "content":reply})

    # 탭 3: 그림 그리기
    with t3:
        st.subheader("🎨 AI 그림 생성")
        draw_p = st.text_input("어떤 장면을 그릴까요?", value=f"{region}을 수호하는 {char['name']}")
        if st.button("그림 생성"):
            if not client: st.error("API Key 필요")
            else:
                with st.spinner("DALL-E가 그리는 중..."):
                    final_p = f"Cute 3D style character, {char['visual']}, {draw_p}"
                    res = client.images.generate(model="dall-e-3", prompt=final_p)
                    st.image(res.data[0].url)

    # 탭 4: 작가 되기
    with t4:
        st.subheader("👑 나의 에피소드")
        u_story = st.text_area("해치와 함께하는 새로운 이야기를 써주세요.")
        if st.button("평가받기"):
            if not client: st.error("API Key 필요")
            else:
                res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"user", "content":f"{char['name']} 말투로 감상평해줘: {u_story}"}])
                st.success(res.choices[0].message.content)
