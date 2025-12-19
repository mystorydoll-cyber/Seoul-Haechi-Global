import streamlit as st
import pandas as pd
import os
from openai import OpenAI
import unicodedata

# 1. [설정] V85: 어떤 오류에도 굴하지 않는 CTO 스페셜 버전
st.set_page_config(layout="wide", page_title="서울 해치 탐험", page_icon="🦁")

# 2. [데이터 엔진] 유연한 컬럼 매칭 로직 (스마트 로드)
@st.cache_data
def load_and_clean_data():
    csv_file = "seoul_data.csv"
    if not os.path.exists(csv_file):
        return None, "파일을 찾을 수 없습니다."
    
    try:
        # 한글 인코딩 자동 대응 (utf-8 or cp949)
        try:
            df = pd.read_csv(csv_file, encoding='utf-8-sig')
        except:
            df = pd.read_csv(csv_file, encoding='cp949')
        
        # [핵심] 컬럼명의 모든 공백 제거 (role , tone  등의 오류 차단)
        df.columns = [c.strip() for c in df.columns]
        df = df.fillna("")
        
        db = {}
        for _, row in df.iterrows():
            reg = str(row.get('region', '')).strip()
            if reg:
                db[reg] = {
                    "name": str(row.get('mascot', '해치')).strip(),
                    "role": str(row.get('role', '서울의 수호신')).strip(),
                    "personality": str(row.get('tone', '친절함')).strip(),
                    "story": str(row.get('story', '')).strip(),
                    "welcome": str(row.get('welcome-msg', '반갑소!')).strip(),
                    "visual": str(row.get('visual_desc', '')).strip(),
                    "keyword": str(row.get('툭징2', reg)).strip() # 오타 대비
                }
        return db, None
    except Exception as e:
        return None, str(e)

# 3. [사이드바] 관리자 설정
with st.sidebar:
    st.title("🦁 서울 해치 관리실")
    api_key = st.text_input("OpenAI API Key", type="password")
    client = OpenAI(api_key=api_key) if api_key else None
    
    st.markdown("---")
    seoul_db, error_info = load_and_clean_data()
    
    if error_info:
        st.error(f"❌ 데이터 로드 오류: {error_info}")
        st.stop()
    
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = None

    if st.session_state.user_profile:
        st.write(f"👋 {st.session_state.user_profile['name']} 대원님")
        region = st.selectbox("📍 탐험 구역 선택", list(seoul_db.keys()))
        if st.button("처음으로 돌아가기"):
            st.session_state.user_profile = None
            st.rerun()

# 4. [메인 UI] 인트로 및 탐험 로직
if st.session_state.user_profile is None:
    st.markdown("<h1 style='text-align:center; color:#FF4B4B;'>🦁 서울 해치 탐험대 신청</h1>", unsafe_allow_html=True)
    st.markdown("---")
    c1, c2 = st.columns([1.5, 1])
    with c1:
        if os.path.exists("intro/main.mp4"): st.video("intro/main.mp4", autoplay=True, loop=True)
        else: st.info("🦁 서울의 25개 해치를 만나러 갈 준비가 되셨나요?")
    with c2:
        with st.form("join"):
            name = st.text_input("이름")
            nat = st.selectbox("국적", ["대한민국", "USA", "China", "Japan", "Other"])
            if st.form_submit_button("탐험 시작", use_container_width=True):
                if name:
                    st.session_state.user_profile = {"name": name, "nationality": nat}
                    st.rerun()
else:
    # 탐험 화면
    char = seoul_db[region]
    st.markdown(f"<h1 style='color:#FF4B4B;'>🗺️ {region} 수호신 : {char['name']}</h1>", unsafe_allow_html=True)
    
    col_img, col_info = st.columns([1, 1.2])
    with col_img:
        # 이미지 매칭 (지역_이름.png)
        img_name = f"{region}_{char['name']}.png"
        if os.path.exists(img_name): st.image(img_name, width=450)
        else: st.warning(f"📸 {char['name']} 이미지를 찾고 있습니다.")

    with col_info:
        st.markdown(f"### 🦁 캐릭터 도감")
        st.success(f"**역할:** {char['role']}")
        st.info(f"**성격:** {char['personality']}")
        st.markdown(f"<div style='background-color:#FFF3CD; padding:15px; border-radius:15px; border:1px solid #FFEeba; color:#856404;'><b>{char['name']}:</b> \"{char['welcome']}\"</div>", unsafe_allow_html=True)

    st.markdown("---")
    t1, t2, t3, t4 = st.tabs(["📜 숨겨진 전설", "🗣️ 대화하기", "🎨 그림 그리기", "👑 작가 되기"])

    with t1:
        if st.button("전체 스토리 보기"):
            if not client: st.error("API Key를 넣어주세요.")
            else:
                with st.spinner("해치가 기록을 읽어주고 있습니다..."):
                    prompt = f"너는 {char['name']}야. 말투: {char['personality']}. 아래 원본 이야기를 그대로 생생하게 들려줘: {char['story']}"
                    res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"system","content":prompt}])
                    st.write(res.choices[0].message.content)

    with t2:
        if "chat_history" not in st.session_state: st.session_state.chat_history = []
        for m in st.session_state.chat_history:
            with st.chat_message(m["role"]): st.write(m["content"])
        if chat_in := st.chat_input("해치에게 궁금한 점을 물어보세요!"):
            if not client: st.error("API Key 필요")
            else:
                st.session_state.chat_history.append({"role":"user", "content":chat_in})
                with st.chat_message("user"): st.write(chat_in)
                with st.chat_message("assistant"):
                    sys_p = f"너는 {char['name']}야. 배경스토리: {char['story']}. {char['personality']} 말투로 대답해."
                    res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"system","content":sys_p}]+st.session_state.chat_history)
                    reply = res.choices[0].message.content
                    st.write(reply)
                    st.session_state.chat_history.append({"role":"assistant", "content":reply})

    with t3:
        prompt_draw = st.text_input("어떤 해치의 모습을 그릴까요?", value=f"{region}의 특징이 담긴 {char['name']}")
        if st.button("AI 그림 생성"):
            if not client: st.error("API Key 필요")
            else:
                with st.spinner("DALL-E가 붓을 들었습니다..."):
                    res = client.images.generate(model="dall-e-3", prompt=f"Cute 3D character, {char['visual']}, {prompt_draw}")
                    st.image(res.data[0].url)

    with t4:
        user_story = st.text_area("해치와 함께한 새로운 에피소드를 기록해보세요.")
        if st.button("해치의 평가 받기"):
            if not client: st.error("API Key 필요")
            else:
                res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"user", "content":f"{char['name']} 말투로 이 이야기에 대해 감상평해줘: {user_story}"}])
                st.success(res.choices[0].message.content)

# 글로벌 폰트 적용
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    * { font-family: 'Jua', sans-serif; }
</style>
""", unsafe_allow_html=True)
