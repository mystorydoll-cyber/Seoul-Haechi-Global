import streamlit as st
import pandas as pd
import os
from openai import OpenAI
import unicodedata
import base64

# 1. [설정] UI 및 페이지 테마
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

# 2. [기능] 이미지 검색 엔진 (정규화 강화)
def find_image_file(region, char_name):
    try:
        current_files = os.listdir(".")
        target = f"{region}_{char_name}.png"
        # NFC 정규화 비교
        for file in current_files:
            if unicodedata.normalize('NFC', file) == unicodedata.normalize('NFC', target):
                return file
        # 보조: 지역명으로 시작하는 png 찾기
        for file in current_files:
            if file.startswith(region) and file.lower().endswith(".png"):
                return file
    except: pass
    return None

# 3. [기능] OpenAI TTS 스피커 엔진
def speak(client, text, lang="한국어"):
    if not client or not text: return
    try:
        # 언어별 적절한 보이스 선택 (영어는 alloy, 그 외는 shimmer 등)
        voice_model = "alloy" if lang == "English" else "shimmer"
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice_model,
            input=text
        )
        audio_base64 = base64.b64encode(response.content).decode('utf-8')
        audio_tag = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
        st.markdown(audio_tag, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"🔈 음성 오류: {e}")

# 4. [기능] 다국어 지원을 위한 실시간 번역기 (UI용)
def translate_info(client, text, target_lang):
    if target_lang == "한국어" or not client or not text: return text
    try:
        # 간단한 정보 번역에는 속도가 빠른 mini 모델 사용
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": f"Translate the following text to {target_lang}. Keep the tone natural."},
                      {"role": "user", "content": text}]
        )
        return res.choices[0].message.content
    except: return text

# 5. [데이터 엔진] CSV 로드 (상세 데이터 추출 및 인코딩 방어)
@st.cache_data
def load_full_database():
    csv_file = "seoul_data.csv"
    if not os.path.exists(csv_file): return None
    for enc in ['utf-8-sig', 'cp949', 'utf-8', 'euc-kr']:
        try:
            df = pd.read_csv(csv_file, encoding=enc)
            df.columns = df.columns.str.strip() # 컬럼명 공백 제거
            df = df.fillna("") # 결측치 처리
            db = {}
            for _, row in df.iterrows():
                # 지역명 컬럼 유연하게 찾기
                reg = str(row.get('region', row.get('지역', ''))).strip()
                if reg:
                    c_name = name_map.get(reg, "서울해치")
                    # CSV 데이터 상세 매핑
                    db[reg] = {
                        "name": c_name,
                        "role": str(row.get('role', row.get('역할', '서울의 수호신'))).strip(),
                        "personality": str(row.get('personality', row.get('성격', '친절하고 따뜻함'))).strip(),
                        "tone": str(row.get('tone', row.get('말투', '정중하고 부드러운 말투'))).strip(),
                        "story": str(row.get('story', row.get('전설', ''))).strip(),
                        # [핵심 수정] 단순 인사가 아닌 CSV의 상세 환영인사 로드
                        "welcome": str(row.get('welcome-msg', row.get('환영인사', '반갑소! 대원님!'))).strip(),
                        "visual": str(row.get('visual_desc', ''))
                    }
            return db
        except: continue
    return None

seoul_db = load_full_database()

# 6. [UI 스타일]
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    * { font-family: 'Jua', sans-serif !important; }
    .main-title { font-size: 3.5rem !important; color: #FF4B4B; margin-bottom: 20px; font-weight: bold; text-align: center; }
    .sub-title { font-size: 2.5rem !important; color: #FF4B4B; margin-bottom: 10px; }
    .info-box { background-color: #e8f4f8; padding: 25px; border-radius: 15px; border-left: 6px solid #FF4B4B; margin-bottom: 20px;}
    .info-card { background-color: #f8f9fa; border-radius: 15px; padding: 20px; border-left: 8px solid #FFD700; margin: 15px 0; }
    .speech-bubble { background-color: #FFF3CD; border-radius: 20px; padding: 25px; font-size: 1.6rem; color: #856404; border: 3px solid #FFEeba; position: relative; margin-bottom: 10px;}
    .credit-text { font-size: 0.8rem; color: gray; margin-top: 30px; text-align: right; border-top: 1px dashed #ccc; padding-top: 10px; }
</style>
""", unsafe_allow_html=True)

# 7. [세션 관리]
if "user_profile" not in st.session_state: st.session_state.user_profile = None
if "messages" not in st.session_state: st.session_state.messages = []

# -------------------------------------------------------------------------
# [화면 1] 인트로 : 입단 신청서 (영상/크레딧 복구 + 다국어 선택 추가)
# -------------------------------------------------------------------------
if st.session_state.user_profile is None:
    st.markdown('<p class="main-title">🦁 서울 해치 탐험 : 입단 신청서</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.8rem; color: #555;">"안녕? 우리는 서울을 지키는 해치 군단이야!"</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # [복구] 좌측 영상/정보, 우측 폼 구조 유지
    col_v, col_f = st.columns([1.5, 1], gap="large")
    
    with col_v:
        # [복구] 인트로 영상
        if os.path.exists("intro/main.mp4"): st.video("intro/main.mp4", autoplay=True, loop=True)
        else: st.info("🦁 서울의 25개 구 수호신들을 만나보세요! (intro/main.mp4 파일을 넣어주세요)")
        
        # [복구] 설명 박스 & 크레딧
        st.markdown("""
        <div class="info-box">
            <h4>💡 해치(Haechi)는 어떤 친구인가요?</h4>
            <div style="margin-top:10px;"><strong>🐣 탄생의 비밀</strong><br>선과 악을 구별하고 재앙을 막는 서울의 수호신이에요.</div>
            <div style="margin-top:10px;"><strong>🦁 매력 포인트</strong><br>25개 구마다 다른 개성을 가진 해치가 살고 있어요.</div>
            <div class="credit-text">
            © 2025 My Story Doll & Seoul Haechi. Powered by M-Unit AI Technology.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_f:
        st.markdown("#### 🎫 탐험대원 등록 카드")
        with st.form("join_form"):
            u_name = st.text_input("이름 (Name)", placeholder="예: 금희")
            u_age = st.slider("나이 (Age)", 5, 100, 25)
            u_nat = st.selectbox("국적 (Nationality)", ["대한민국", "USA", "China", "Japan", "Other"])
            # [유지] 다국어 언어 선택 박스
            u_lang = st.selectbox("대화 언어 (Language)", ["한국어", "English", "日本語", "中文"])
            
            if st.form_submit_button("해치 만나러 가기 (Start)", type="primary", use_container_width=True):
                if u_name:
                    st.session_state.user_profile = {"name": u_name, "age": u_age, "nationality": u_nat, "language": u_lang}
                    st.rerun()

# -------------------------------------------------------------------------
# [화면 2] 메인 탐험 (환영인사 수정 및 스피커 추가)
# -------------------------------------------------------------------------
else:
    user = st.session_state.user_profile
    if not seoul_db:
        st.error("🚨 CSV 데이터를 불러올 수 없습니다. 파일 위치와 인코딩을 확인해주세요.")
        st.stop()

    with st.sidebar:
        st.title(f"🦁 {user['name']} 대원")
        st.write(f"({user['language']} 탐험 중)")
        api_key = st.text_input("🔑 OpenAI API Key", type="password")
        client = OpenAI(api_key=api_key) if api_key else None
        st.markdown("---")
        region = st.selectbox("📍 탐험 지역 선택", list(seoul_db.keys()))
        char = seoul_db[region]
        if st.button("🔄 처음으로 돌아가기"):
            st.session_state.user_profile = None
            st.session_state.messages = []
            st.rerun()

    # 제목 통일
    st.markdown(f'<p class="sub-title">🗺️ {region} - {char["name"]}</p>', unsafe_allow_html=True)
    
    col_img, col_txt = st.columns([1, 1.3], gap="large")
    
    with col_img:
        img_f = find_image_file(region, char['name'])
        if img_f: st.image(img_f, use_container_width=True)
        else: st.info(f"📸 {char['name']} 이미지 준비중 ({region}_{char['name']}.png)")

    with col_txt:
        # 선택한 언어로 UI 정보 번역 표시
        display_role = translate_info(client, char['role'], user['language'])
        display_pers = translate_info(client, char['personality'], user['language'])
        display_tone = translate_info(client, char['tone'], user['language'])
        # [핵심 수정] CSV의 풍성한 환영인사 가져오기
        welcome_msg_full = char['welcome'] 
        display_welcome = translate_info(client, welcome_msg_full, user['language'])

        st.markdown(f"### ✨ {char['name']} 상세 정보")
        st.markdown(f"""
        <div class="info-card">
            <b>🛡️ 역할:</b> {display_role}<br>
            <b>🧬 성격:</b> {display_pers}<br>
            <b>💬 말투:</b> {display_tone}
        </div>
        """, unsafe_allow_html=True)
        
        # [핵심 수정] 풍성한 환영인사 말풍선 표시
        st.markdown(f"<div class='speech-bubble'><b>{char['name']}</b>: \"{display_welcome}\"</div>", unsafe_allow_html=True)
        
        # [핵심 추가] 환영인사 스피커 버튼 (선택 언어로 읽기)
        if st.button(f"🔊 {user['language']}로 인사 듣기"):
            if client: speak(client, display_welcome, user['language'])
            else: st.warning("API Key를 입력해주세요.")

    st.markdown("---")
    # 기존 탭 기능 유지
    t1, t2, t3, t4 = st.tabs(["📜 전설 듣기", "🗣️ 대화하기", "🎨 그림 그리기", "👑 작가 되기"])

    with t1:
        st.subheader(f"📜 {char['name']}가 들려주는 {region} 이야기")
        if st.button("이야기 시작! (Story Start)"):
            if not client: st.error("API Key가 필요합니다.")
            else:
                with st.spinner("해치가 기억을 떠올리고 있습니다..."):
                    # 다국어/연령/페르소나 맞춤 프롬프트
                    prompt = f"""
                    You are {char['name']} from {region}. 
                    Persona: {char['personality']}. Tone of voice: {char['tone']}.
                    Listener: {user['name']} ({user['age']} years old, {user['nationality']}).
                    Language: {user['language']}.
                    [Instruction] Tell the story: {char['story']}. 
                    Strictly maintain the character's unique tone ({char['tone']}) throughout the story.
                    Adjust vocabulary suitable for a {user['age']} year old.
                    """
                    res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"system", "content":prompt}])
                    story_res = res.choices[0].message.content
                    st.write(story_res)
                    if st.button("🔊 이야기 전체 듣기"):
                        speak(client, story_res, user['language'])

    with t2:
        st.subheader(f"🗣️ {char['name']}와 {user['language']}로 대화")
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.write(m["content"])
        
        if chat_input := st.chat_input("궁금한 것을 물어보세요!"):
            if not client: st.error("API Key 필요")
            else:
                st.session_state.messages.append({"role":"user", "content":chat_input})
                with st.chat_message("user"): st.write(chat_input)
                
                with st.chat_message("assistant"):
                    # 실시간 대화용 페르소나 시스템 프롬프트
                    sys_p = f"You are {char['name']}. Persona: {char['personality']}. Tone: {char['tone']}. Language: {user['language']}."
                    res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"system","content":sys_p}]+st.session_state.messages)
                    reply = res.choices[0].message.content
                    st.write(reply)
                    st.session_state.messages.append({"role":"assistant", "content":reply})
                    speak(client, reply, user['language'])

    with t3:
        st.subheader("🎨 해치와 함께 그림 그리기")
        draw_q = st.text_input("어떤 장면을 그릴까요?", value=f"{char['name']} in {region}")
        if st.button("그림 생성"):
            if client:
                with st.spinner("그림을 그리는 중..."):
                    res = client.images.generate(model="dall-e-3", prompt=f"Cute 3D character, Pixar style, {char['visual']}, {draw_q}")
                    st.image(res.data[0].url)

    with t4:
        st.subheader("👑 나만의 해치 동화 만들기")
        user_text = st.text_area("이야기를 적어주세요.")
        if st.button("해치의 피드백"):
            if client:
                feedback_p = f"You are {char['name']}. Tone: {char['tone']}. Give warm feedback in {user['language']} for this story: {user_text}"
                res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"user", "content":feedback_p}])
                st.success(res.choices[0].message.content)
                speak(client, res.choices[0].message.content, user['language'])
