import streamlit as st
import pandas as pd
import os
from openai import OpenAI
import unicodedata

# 1. [설정] M-CTO: UI & 데이터 엔진 강화 버전
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

# 2. [기능] 이미지 검색 엔진 (Unicode 정규화 포함)
def find_image_file(region, char_name):
    try:
        current_files = os.listdir(".")
        target = f"{region}_{char_name}.png"
        for file in current_files:
            if unicodedata.normalize('NFC', file) == unicodedata.normalize('NFC', target):
                return file
        for file in current_files:
            if file.startswith(region) and file.endswith(".png"):
                return file
    except: pass
    return None

# 3. [데이터 엔진] CSV 로드 (강력한 에러 방지 로직)
@st.cache_data
def load_full_database():
    csv_file = "seoul_data.csv"
    if not os.path.exists(csv_file):
        st.error(f"🚨 '{csv_file}' 파일이 존재하지 않습니다. 파일명을 확인해주세요.")
        return None
    
    # 다양한 인코딩 시도
    df = None
    for enc in ['utf-8-sig', 'cp949', 'utf-8', 'euc-kr']:
        try:
            df = pd.read_csv(csv_file, encoding=enc)
            break
        except: continue

    if df is None:
        st.error("🚨 CSV 파일을 읽을 수 없습니다. 인코딩 형식을 확인해주세요.")
        return None

    try:
        df.columns = df.columns.str.strip()
        df = df.fillna("")
        db = {}
        for _, row in df.iterrows():
            # 컬럼명 유연성 확보 (영어/한글 혼용 대응)
            reg = str(row.get('region', row.get('지역', ''))).strip()
            if reg:
                c_name = name_map.get(reg, "서울해치")
                db[reg] = {
                    "name": c_name,
                    "role": str(row.get('role', row.get('역할', '서울의 수호신'))).strip(),
                    "personality": str(row.get('tone', row.get('말투', '친절함'))).strip(),
                    "story": str(row.get('story', row.get('전설', ''))).strip(),
                    "welcome": str(row.get('welcome-msg', row.get('환영인사', '반갑소!'))).strip(),
                    "visual": str(row.get('visual_desc', row.get('외형', ''))).strip(),
                    "keyword": str(row.get('툭징2', row.get('특징2', reg))).strip()
                }
        return db
    except Exception as e:
        st.error(f"🚨 데이터 처리 중 오류 발생: {e}")
        return None

seoul_db = load_full_database()

# 4. [UI 스타일]
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    * { font-family: 'Jua', sans-serif !important; }
    .main-title { text-align: center; font-size: 3.5rem !important; color: #FF4B4B; margin-bottom: 0.5rem; }
    .info-box { background-color: #e8f4f8; padding: 25px; border-radius: 15px; border-left: 6px solid #FF4B4B; margin-bottom: 20px;}
    .char-title { font-size: 3.2rem !important; color: #FF4B4B; margin-bottom: 5px; line-height: 1.2;}
    .char-role { font-size: 1.6rem !important; color: #555; border-bottom: 3px solid #FFD700; display: inline-block; margin-bottom: 15px; }
    .speech-bubble { background-color: #FFF3CD; border: 2px solid #FFEeba; border-radius: 20px; padding: 20px; font-size: 1.4rem; color: #856404; position: relative; }
    .credit-text { font-size: 0.8rem; color: gray; margin-top: 30px; text-align: right; border-top: 1px dashed #ccc; padding-top: 10px; }
</style>
""", unsafe_allow_html=True)

# 5. [세션 관리]
if "user_profile" not in st.session_state: st.session_state.user_profile = None
if "messages" not in st.session_state: st.session_state.messages = []

# -------------------------------------------------------------------------
# [화면 1] 인트로 : 입단 신청서
# -------------------------------------------------------------------------
if st.session_state.user_profile is None:
    st.markdown('<p class="main-title">🦁 서울 해치 탐험 : 입단 신청서</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.8rem; color: #555;">"안녕? 우리는 서울을 지키는 해치 군단이야!"</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    col_v, col_f = st.columns([1.5, 1], gap="large")
    
    with col_v:
        if os.path.exists("intro/main.mp4"): st.video("intro/main.mp4", autoplay=True, loop=True)
        else: st.info("🦁 서울의 25개 구 수호신들을 만나보세요!")
        
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
        with st.form("join"):
            u_name = st.text_input("이름 (Name)", placeholder="예: 금희")
            u_age = st.slider("나이 (Age)", 5, 100, 25)
            u_nat = st.selectbox("국적 (Nationality)", ["대한민국", "USA", "China", "Japan", "Other"])
            if st.form_submit_button("해치 만나러 가기", type="primary", use_container_width=True):
                if u_name:
                    st.session_state.user_profile = {"name": u_name, "age": u_age, "nationality": u_nat}
                    st.rerun()

# -------------------------------------------------------------------------
# [화면 2] 메인 탐험
# -------------------------------------------------------------------------
else:
    user = st.session_state.user_profile
    if not seoul_db:
        st.error("🚨 데이터를 불러올 수 없습니다. CSV 파일 상태를 점검해주세요.")
        st.stop()
        
    with st.sidebar:
        st.title(f"🦁 {user['name']} 대원님")
        st.write(f"({user['age']}세 / {user['nationality']})")
        st.markdown("---")
        api_key = st.text_input("🔑 OpenAI API Key", type="password")
        client = OpenAI(api_key=api_key) if api_key else None
        st.markdown("---")
        
        # 데이터 로드 확인 후 셀렉트박스 표시
        region_list = list(seoul_db.keys())
        region = st.selectbox("📍 탐험 지역 선택", region_list)
        char = seoul_db[region]
        
        if st.button("🔄 처음으로 돌아가기"):
            st.session_state.user_profile = None
            st.session_state.messages = []
            st.rerun()

    st.markdown(f"<h1 style='color:#FF4B4B;'>🗺️ {region} 탐험</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 1.2])
    with c1:
        img_f = find_image_file(region, char['name'])
        if img_f: st.image(img_f, width=450)
        else: st.info(f"📸 {char['name']} 이미지 준비중")
        
    with c2:
        st.markdown(f"<p class='char-title'>{region} - {char['name']}</p>", unsafe_allow_html=True)
        st.markdown(f"<span class='char-role'>{char['role']}</span>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background-color:#f9f9f9; border:2px solid #eee; border-radius:15px; padding:20px; margin:15px 0;'>
            <b>💡 성격/말투:</b> {char['personality']}<br><br>
            <b>🔑 키워드:</b> {char['keyword']}
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<div class='speech-bubble'><b>{char['name']}</b>: \"{char['welcome']}\"</div>", unsafe_allow_html=True)

    st.markdown("---")
    t1, t2, t3, t4 = st.tabs(["📜 전설 듣기", "🗣️ 대화하기", "🎨 그림 그리기", "👑 작가 되기"])

    with t1:
        st.subheader(f"📜 {char['name']}의 전설")
        if st.button("이야기 들려줘!"):
            if not client: st.error("사이드바에 API Key를 입력해주세요!")
            else:
                with st.spinner("해치가 옛날 이야기를 기억해내고 있습니다..."):
                    prompt = f"""
                    당신은 {region}의 {char['name']}입니다.
                    듣는 사람: {user['name']} ({user['age']}세, {user['nationality']} 국적)
                    말투: {char['personality']}를 완벽히 연기하십시오.
                    [지시]
                    1. 아래 [원본스토리]를 바탕으로 생생하게 들려주세요.
                    2. {user['age']}세 수준에 맞춰 단어 선택을 조절하세요.
                    3. 외국인 대원에게는 한국 고유의 정서를 친절히 설명해주세요.
                    [원본스토리]: {char['story']}
                    """
                    res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"system", "content":prompt}])
                    st.info(res.choices[0].message.content)

    with t2:
        st.subheader(f"🗣️ {char['name']}와 실시간 대화")
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.write(m["content"])
        if chat_p := st.chat_input("해치에게 궁금한 걸 물어보세요!"):
            if not client: st.error("API Key 필요")
            else:
                st.session_state.messages.append({"role":"user", "content":chat_p})
                with st.chat_message("user"): st.write(chat_p)
                with st.chat_message("assistant"):
                    sys_p = f"너는 {char['name']}야. 말투: {char['personality']}. {user['age']}세 {user['nationality']} 대원과 대화 중. 배경: {char['story']}"
                    res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"system","content":sys_p}]+st.session_state.messages)
                    reply = res.choices[0].message.content
                    st.write(reply)
                    st.session_state.messages.append({"role":"assistant", "content":reply})

    with t3:
        st.subheader("🎨 나만의 해치 그리기")
        draw_q = st.text_input("어떤 해치를 그릴까요?", value=f"{region}을 지키는 {char['name']}")
        if st.button("그림 생성"):
            if not client: st.error("API Key 필요")
            else:
                with st.spinner("AI가 그림을 그리는 중..."):
                    res = client.images.generate(model="dall-e-3", prompt=f"Cute 3D character, {char['visual']}, {draw_q}, Pixar style")
                    st.image(res.data[0].url)

    with t4:
        st.subheader("👑 나도 동화 작가")
        u_story = st.text_area("해치와 함께할 새로운 에피소드를 써보세요.")
        if st.button("해치의 평가 받기"):
            if not client: st.error("API Key 필요")
            else:
                eval_p = f"너는 {char['name']}야. {user['age']}세 대원이 쓴 이야기를 읽고 너의 말투로 따뜻한 조언과 감상평을 해줘: {u_story}"
                res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"user", "content":eval_p}])
                st.success(res.choices[0].message.content)
