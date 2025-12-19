import streamlit as st
import os
import pandas as pd
from openai import OpenAI
import unicodedata

# 1. [설정] V71: CSV 연동 최종 완성본 (오류 원천 차단)
st.set_page_config(
    layout="wide",
    page_title="서울 해치 탐험",
    page_icon="🦁",
    initial_sidebar_state="expanded"
)

# 2. [기능] 스마트 이미지 찾기
def find_image_file(region, char_name):
    try:
        current_files = os.listdir(".")
        for file in current_files:
            # 1. 지역명으로 시작하는 파일 찾기 (예: 종로구_해치.png)
            if file.startswith(region) and file.endswith(".png"):
                return file
            # 2. 한글 자소 분리 해결
            if unicodedata.normalize('NFC', file) == unicodedata.normalize('NFC', f"{region}_{char_name}.png"):
                return file
    except: pass
    return None

# 3. [데이터] CSV 파일 로드 및 변환 (핵심 엔진)
@st.cache_data
def load_seoul_data():
    csv_file = "seoul_data.csv"
    
    # 파일이 없는 경우를 대비한 깡통 데이터
    default_db = {
        "종로구": {
            "name": "해치", "role": "데이터 없음", "personality": "친절함", "speech": "친절한 해요체",
            "story": "CSV 파일이 없습니다. seoul_data.csv 파일을 업로드해주세요.",
            "welcome": "파일을 찾을 수 없어요!", "visual": "기본 해치", "keyword": "데이터 없음"
        }
    }

    if not os.path.exists(csv_file):
        return None, default_db

    try:
        df = pd.read_csv(csv_file)
        # 컬럼명 공백 제거 (오류 방지)
        df.columns = df.columns.str.strip()
        df = df.fillna("")
        
        db = {}
        for _, row in df.iterrows():
            reg = str(row.get('region', '')).strip()
            if reg:
                db[reg] = {
                    "name": str(row.get('mascot', '해치')).strip(),
                    "role": str(row.get('role', '서울의 수호신')).strip(),
                    # CSV 컬럼명 'tone'을 성격과 말투로 공통 사용
                    "personality": str(row.get('tone', '친절함')).strip(),
                    "speech": str(row.get('tone', '친절한 말투')).strip(),
                    "story": str(row.get('story', '스토리가 없습니다.')).strip(),
                    "welcome": str(row.get('welcome-msg', '반갑소!')).strip(),
                    "visual": str(row.get('visual_desc', '귀여운 해치')).strip(),
                    # 오타가 있던 컬럼명 '툭징2'도 안전하게 처리
                    "keyword": str(row.get('툭징2', reg)).strip()
                }
        return df, db
    except Exception as e:
        st.error(f"CSV 데이터 로드 중 오류: {e}")
        return None, default_db

# 데이터 로드 실행
df_data, seoul_db = load_seoul_data()

# -------------------------------------------------------------------------
# [로직] 인트로 + 메인 앱
# -------------------------------------------------------------------------
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# A. 입단 신청서 (Intro)
if st.session_state.user_profile is None:
    st.markdown('<p class="main-title">🦁 서울 해치 탐험 : 입단 신청서</p>', unsafe_allow_html=True)
    
    # 파일 로드 상태 표시
    if df_data is None:
        st.error("🚨 'seoul_data.csv' 파일을 찾을 수 없습니다. 폴더에 파일을 넣어주세요.")
    else:
        st.success(f"✅ {len(seoul_db)}개 지역 스토리를 성공적으로 불러왔습니다.")

    st.markdown("---")
    col1, col2 = st.columns([1.5, 1], gap="large")
    with col1:
        intro_path = "intro/main.mp4"
        if os.path.exists(intro_path):
            st.video(intro_path, autoplay=True, loop=True)
        else: st.info("🦁 (인트로 영상 준비 중)")
        
        st.markdown("""
        <div class="info-box">
            <h4>💡 해치(Haechi)는 어떤 친구인가요?</h4>
            <div style="margin-top:10px;"><strong>🐣 탄생의 비밀</strong><br>선과 악을 구별하고 재앙을 막는 서울의 수호신이에요.</div>
            <div style="margin-top:10px;"><strong>🦁 매력 포인트</strong><br>25개 구마다 다른 개성을 가진 해치가 살고 있어요.</div>
            <div style="font-size: 0.8rem; color: gray; margin-top: 20px; text-align: right; border-top: 1px dashed #ccc; padding-top: 10px;">
            © 2025 My Story Doll & Seoul Haechi. Powered by M-Unit AI Technology.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🎫 탐험대원 등록 카드")
        with st.form("intro_form"):
            name = st.text_input("이름 (Name)", placeholder="예: 금희")
            age = st.slider("나이 (Age)", 5, 100, 25)
            nationality = st.selectbox("국적", ["대한민국", "USA", "China", "Japan", "Other"])
            if st.form_submit_button("해치 만나러 가기", type="primary", use_container_width=True):
                if name:
                    st.session_state.user_profile = {"name": name, "age": age, "nationality": nationality}
                    st.rerun()

# B. 메인 앱 (Main)
else:
    user = st.session_state.user_profile
    
    with st.sidebar:
        st.title(f"반갑소, {user['name']}!")
        
        if "api_key" not in st.session_state:
            st.session_state.api_key = ""
        
        api_key_input = st.text_input("OpenAI API Key", type="password", value=st.session_state.api_key)
        if api_key_input:
            st.session_state.api_key = api_key_input
        
        client = OpenAI(api_key=st.session_state.api_key) if st.session_state.api_key else None
        
        st.markdown("---")
        # 국적 변경
        new_nationality = st.selectbox("🌍 국적 / 언어", ["대한민국", "USA", "China", "Japan", "Other"], index=["대한민국", "USA", "China", "Japan", "Other"].index(user.get("nationality", "대한민국")))
        if new_nationality != user['nationality']:
            user['nationality'] = new_nationality
            st.success("국적 설정이 변경되었습니다.")

        # 지역 선택 (CSV 데이터 기반)
        if not seoul_db:
            st.warning("데이터가 로드되지 않았습니다.")
            region_list = ["데이터 없음"]
        else:
            region_list = list(seoul_db.keys())

        region = st.selectbox("📍 지역 선택", region_list)
        
        # 선택된 지역 데이터 가져오기 (없으면 기본값)
        char = seoul_db.get(region, {"name": "해치", "role": "", "personality": "", "speech": "", "story": "", "welcome": "", "visual": "", "keyword": ""})
        
        st.markdown("---")
        if st.button("🔄 처음으로 돌아가기"):
            st.session_state.user_profile = None
            st.session_state.messages = []
            st.rerun()

    # [메인 화면 구성]
    st.markdown(f"<div class='app-header'>🗺️ {region} 해치 탐험</div>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1], gap="medium")
    
    with c1:
        img_file = find_image_file(region, char['name'])
        if img_file: st.image(img_file, width=400)
        else: st.info(f"📸 {char['name']} 이미지 준비중")
        
    with c2:
        st.markdown(f"<p class='char-title'>{char['name']}</p>", unsafe_allow_html=True)
        st.markdown(f"<span class='char-role'>{char['role']}</span>", unsafe_allow_html=True)
        st.markdown(f"<div style='background-color:#fff; border:2px solid #eee; border-radius:15px; padding:20px; margin:20px 0;'><b>💡 성격:</b> {char['personality']}<br><br><b>🗣️ 말투:</b> {char['speech']}<br><br><b>🔑 키워드:</b> {char['keyword']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='speech-bubble'><b>{char['name']}</b>: \"{char['welcome']}\"</div>", unsafe_allow_html=True)

    st.markdown("---")
    
    t1, t2, t3, t4 = st.tabs(["📜 전설 듣기", "🗣️ 대화하기", "🎨 그림 그리기", "👑 작가 되기"])

    # 1. 전설 듣기 (CSV 원본 스토리 출력)
    with t1:
        st.subheader(f"📜 {char['name']}의 숨겨진 전설")
        if st.button("전설 이야기 들려줘!", key="btn_legend"):
            if not client:
                st.error("🚨 사이드바에 OpenAI API Key를 입력해주세요!")
            else:
                with st.spinner(f"{char['name']}가 이야기를 시작합니다..."):
                    try:
                        # [핵심] CSV에서 가져온 긴 스토리를 프롬프트에 주입
                        prompt = f"""
                        당신은 서울 {region}의 {char['name']}입니다.
                        사용자({user['name']})에게 당신의 전설을 들려주세요.

                        [지시사항]
                        1. 아래 [원본 스토리] 내용을 '그대로' 구연동화처럼 생생하게 읽어주세요.
                        2. 내용을 요약하거나 줄이지 마세요. (Full Text 유지)
                        3. 말투는 반드시 지정된 [말투]를 사용하세요.

                        [말투]: {char['speech']}
                        [원본 스토리]: {char['story']}
                        """
                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[{"role": "system", "content": prompt}],
                            temperature=0.3
                        )
                        st.info(response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"오류 발생: {e}")

    # 2. 대화하기 (세계관 고정)
    with t2:
        st.subheader(f"🗣️ {char['name']}와 대화하기")
        
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        if prompt := st.chat_input("해치에게 말을 걸어보세요..."):
            if not client:
                st.error("🚨 API Key가 필요합니다!")
            else:
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.write(prompt)
                
                with st.chat_message("assistant"):
                    with st.spinner("생각 중..."):
                        sys_prompt = f"""
                        당신은 {region}의 {char['name']}입니다.
                        당신의 배경 설정(Origin Story)은 다음과 같습니다:
                        "{char['story']}"
                        
                        위 설정에 없는 내용은 모른다고 답하거나, 당신의 이야기로 화제를 돌리세요.
                        말투: {char['speech']}
                        """
                        full_msgs = [{"role": "system", "content": sys_prompt}] + st.session_state.messages
                        
                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=full_msgs,
                            temperature=0.5
                        )
                        bot_reply = response.choices[0].message.content
                        st.write(bot_reply)
                        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # 3. 그림 그리기
    with t3:
        st.subheader("🎨 나만의 해치 그리기")
        draw_prompt = st.text_input("어떤 해치를 그리고 싶나요?", placeholder=f"{region}의 거리를 걷는 {char['name']}")
        if st.button("그림 생성하기", key="btn_draw"):
            if not client:
                st.error("🚨 API Key가 필요합니다!")
            else:
                with st.spinner("붓을 들고 그림을 그리는 중..."):
                    try:
                        visual_info = char.get('visual', '귀여운 해치')
                        final_prompt = f"High quality 3D render style. Cute character. {visual_info}. {draw_prompt}"
                        response = client.images.generate(
                            model="dall-e-3",
                            prompt=final_prompt,
                            size="1024x1024",
                            quality="standard",
                            n=1,
                        )
                        image_url = response.data[0].url
                        st.image(image_url, caption="생성된 해치 그림")
                    except Exception as e:
                        st.error(f"그림 생성 실패: {e}")

    # 4. 작가 되기
    with t4:
        st.subheader("👑 내가 만드는 해치 이야기")
        user_story = st.text_area("당신만의 이야기를 써보세요!", height=150)
        if st.button("해치에게 평가받기", key="btn_writer"):
            if not client:
                st.error("🚨 API Key가 필요합니다!")
            else:
                with st.spinner("읽어보는 중..."):
                    eval_prompt = f"""
                    사용자가 쓴 {region} {char['name']} 이야기를 읽고,
                    {char['speech']} 말투로 감상평을 남겨주세요.
                    칭찬과 함께 더 재미있는 아이디어를 하나 덧붙여주세요.
                    내용: {user_story}
                    """
                    res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": eval_prompt}]
                    )
                    st.success(res.choices[0].message.content)

# [스타일] CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    h1, h2, h3, h4, .stMarkdown, p, div, span, button, input, label, textarea {
        font-family: 'Jua', sans-serif !important;
    }
    .main-title { text-align: center; font-size: 3.5rem !important; color: #FF4B4B; margin-bottom: 0.5rem; }
    .info-box { background-color: #e8f4f8; padding: 25px; border-radius: 15px; border-left: 6px solid #FF4B4B; }
    .char-title { font-size: 3.5rem !important; color: #FF4B4B; margin-bottom: 10px; }
    .char-role { font-size: 1.6rem !important; color: #555; border-bottom: 3px solid #FFD700; display: inline-block; }
    .speech-bubble { background-color: #FFF3CD; border: 2px solid #FFEeba; border-radius: 20px; padding: 15px; font-size: 1.3rem; color: #856404; }
    .stButton>button { width: 100%; border-radius: 10px; font-size: 1.2rem; }
</style>
""", unsafe_allow_html=True)
