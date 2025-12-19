import streamlit as st
import os
import unicodedata
import pandas as pd
from openai import OpenAI

# 1. [설정] V68: CSV 데이터 연동 & 하이브리드 로드
st.set_page_config(
    layout="wide",
    page_title="서울 해치 탐험",
    page_icon="🦁",
    initial_sidebar_state="expanded"
)

# 2. [기능] 스마트 이미지 찾기
def find_image_file(region, char_name):
    # CSV에서 읽어온 이름이 '해치'로만 되어 있을 수 있어, 파일명 매칭을 유연하게 처리
    # 1순위: 지역_이름.png (예: 종로구_초롱해치.png)
    target_name = f"{region}_{char_name}.png"
    if os.path.exists(target_name): return target_name
    
    # 2순위: 한글 자소 분리 문제 해결
    try:
        current_files = os.listdir(".")
        for file in current_files:
            if unicodedata.normalize('NFC', file) == unicodedata.normalize('NFC', target_name):
                return file
    except: pass
    return None

# 3. [데이터] 기본 딕셔너리 (뼈대) + CSV 데이터 주입 (살 붙이기)
# - 기본 데이터: 이름, 비주얼, 말투 (CSV보다 정교한 설정 유지)
seoul_db = {
    "종로구": {"name": "초롱해치", "speech": "점잖은 '사극 톤' (~하오, ~다오)", "visual": "청사초롱을 들고 갓을 쓴 분홍색 해치", "keyword": "경복궁, 광화문, 역사, 전통"},
    "중구": {"name": "쇼퍼해치", "speech": "통통 튀는 '쇼호스트 톤' (~거든요!, ~라구요!)", "visual": "양손에 쇼핑백을 들고 선글라스를 낀 해치", "keyword": "명동, 쇼핑, 패션, 남산타워"},
    "용산구": {"name": "어텐션해치", "speech": "영어를 섞어 쓰는 '교포 힙합 톤' (Yo!)", "visual": "헤드셋을 끼고 힙합 후드티를 입은 해치", "keyword": "이태원, 미군기지, 다양성, 힙합"},
    "성동구": {"name": "뚝해치", "speech": "나긋나긋한 '동화 구연가 톤'", "visual": "빈티지 카메라를 메고 있는 감성적인 해치", "keyword": "성수동, 서울숲, 팝업스토어, 살곶이다리"},
    "광진구": {"name": "광나루해치", "speech": "감탄사가 많은 '먹방 유튜버 톤' (와~!)", "visual": "한 손에 닭다리를 들고 있는 통통한 해치", "keyword": "한강공원, 뚝섬, 건대입구, 맛집"},
    "동대문구": {"name": "한약해치", "speech": "인자하고 따뜻한 '한의사 선생님 톤' (~합니다, ~해보세요)", "visual": "향기 나는 약초가 담긴 작은 주머니를 찬 해치", "keyword": "동대문 약령시, 한방차, 자연 치유"},
    "중랑구": {"name": "장미해치", "speech": "감성적이고 다정한 '로맨티스트 톤'", "visual": "장미 덩굴을 두르고 물뿌리개를 든 아름다운 해치", "keyword": "중랑구, 장미축제, 중랑천"},
    "성북구": {"name": "선잠해치", "speech": "기품 있고 우아한 '왕실 톤'", "visual": "누에가 붙어있는 뽕나무 지팡이를 든 신비로운 해치", "keyword": "선잠단지, 성북동, 전통문화"},
    "강북구": {"name": "북수해치", "speech": "무겁고 중후한 '산신령 톤'", "visual": "돌멩이 목걸이를 하고 바위 위에 앉아있는 강인한 해치", "keyword": "북한산, 우이천, 솔밭공원"},
    "도봉구": {"name": "호랑해치", "speech": "호탕하고 자신감 넘치는 '예술가 대장 톤'", "visual": "붓으로 사용하는 꼬리를 가진 호랑이 무늬 해치", "keyword": "도봉산, 평화문화진지, 예술"},
    "노원구": {"name": "태해치", "speech": "무게감 있고 비장한 '장군 톤'", "visual": "고구려 양식의 검을 들고 늠름하게 서 있는 해치", "keyword": "태릉, 고구려, 역사, 용기"},
    "은평구": {"name": "진관해치", "speech": "여유롭고 차분한 '스님 톤'", "visual": "승복을 연상시키는 옷을 입고 찻잔을 든 해치", "keyword": "진관사, 북한산, 템플스테이"},
    "서대문구": {"name": "홍지해치", "speech": "단호하고 힘찬 '독립투사 톤'", "visual": "한 손에 밝게 빛나는 희망의 등불을 든 해치", "keyword": "서대문형무소, 독립문, 역사"},
    "마포구": {"name": "가수해치", "speech": "감미롭고 리듬감 있는 '싱어송라이터 톤'", "visual": "통기타를 메고 마법 마이크를 든 힙한 해치", "keyword": "홍대, 버스킹, 음악, 젊음"},
    "양천구": {"name": "배움해치", "speech": "친절하고 격려하는 '선생님 톤'", "visual": "학사모를 쓰고 마법의 분필을 든 똑똑한 해치", "keyword": "목동, 교육, 도서관, 배움"},
    "강서구": {"name": "강초해치", "speech": "나긋나긋하고 편안한 '식물원 정원사 톤'", "visual": "꽃으로 장식된 모자를 쓴 초록빛 해치", "keyword": "서울식물원, 허준박물관, 자연"},
    "구로구": {"name": "디지털해치", "speech": "똑부러지고 스마트한 'IT 개발자 톤'", "visual": "반짝이는 스마트폰과 태블릿을 든 스마트한 해치", "keyword": "G밸리, 구로디지털단지, IT"},
    "금천구": {"name": "봉제해치", "speech": "다정하고 챙겨주는 '친절한 언니 톤'", "visual": "실타래와 줄자를 목에 건 따뜻한 인상의 해치", "keyword": "봉제공장, G밸리, 노동의가치"},
    "영등포구": {"name": "등포해치", "speech": "유쾌하고 긍정적인 '예술가 톤'", "visual": "톱니바퀴 장식을 달고 붓을 든 힙한 해치", "keyword": "문래창작촌, 타임스퀘어, 변화"},
    "동작구": {"name": "현충해치", "speech": "예의 바르고 정중한 '감사 톤'", "visual": "하얀 국화 꽃다발을 들고 있는 단정한 해치", "keyword": "국립서울현충원, 호국영령, 감사"},
    "관악구": {"name": "낙성해치", "speech": "지혜롭고 희망찬 '멘토 톤'", "visual": "별을 수집하는 바구니를 든 해치", "keyword": "낙성대, 강강찬, 별빛, 꿈"},
    "서초구": {"name": "법조해치", "speech": "논리적이고 명확한 '판사님 톤'", "visual": "작은 저울(공정함)과 빛나는 법전을 든 해치", "keyword": "예술의전당, 법조타운, 정의"},
    "강남구": {"name": "패션해치", "speech": "시크하고 세련된 '디자이너 톤'", "visual": "마법의 실타래와 줄자를 든 스타일리시한 해치", "keyword": "명품거리, 가로수길, 패션"},
    "송파구": {"name": "몽촌해치", "speech": "활기차고 신나는 '가이드 톤'", "visual": "피크닉을 위한 돗자리를 멘 귀여운 해치", "keyword": "롯데월드타워, 몽촌토성, 올림픽공원"},
    "강동구": {"name": "암사해치", "speech": "신비롭고 고요한 '고대인 톤'", "visual": "작은 빗살무늬 토기 조각을 든 해치", "keyword": "암사동유적, 빗살무늬토기, 역사"}
}

# [핵심 로직] CSV 파일 로드 및 스토리 주입 (Story Injection)
try:
    csv_file = "seoul_data.csv"
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        # 컬럼명 공백 제거 (오류 방지)
        df.columns = df.columns.str.strip()
        
        # CSV 데이터를 순회하며 seoul_db 업데이트
        for index, row in df.iterrows():
            reg = row['region']
            if reg in seoul_db:
                # 1. 풍성한 원본 스토리 덮어쓰기
                if pd.notna(row['story']):
                    seoul_db[reg]['story'] = row['story']
                
                # 2. 역할(Role) 업데이트
                if pd.notna(row['role']):
                    seoul_db[reg]['role'] = row['role']
                
                # 3. 성격(Personality) 업데이트 (CSV의 'tone' 컬럼 활용)
                if pd.notna(row['tone']):
                    seoul_db[reg]['personality'] = row['tone']
                
                # 4. 환영 인사(Welcome) 업데이트
                if pd.notna(row['welcome-msg']):
                    seoul_db[reg]['welcome'] = row['welcome-msg']
    else:
        st.error("🚨 'seoul_data.csv' 파일을 찾을 수 없습니다! 같은 폴더에 넣어주세요.")
except Exception as e:
    st.error(f"CSV 데이터 로드 중 오류 발생: {e}")


# 4. [스타일] CSS
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
    st.markdown("---")
    col1, col2 = st.columns([1.5, 1], gap="large")
    with col1:
        intro_path = "intro/main.mp4"
        if os.path.exists(intro_path):
            st.video(intro_path, autoplay=True, loop=True)
        else: st.info("🦁 인트로 영상을 준비 중입니다.")
        
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
        new_nationality = st.selectbox("🌍 국적 / 언어", ["대한민국", "USA", "China", "Japan", "Other"], index=["대한민국", "USA", "China", "Japan", "Other"].index(user.get("nationality", "대한민국")))
        if new_nationality != user['nationality']:
            user['nationality'] = new_nationality
            st.success("국적 설정이 변경되었습니다.")

        region = st.selectbox("📍 지역 선택", list(seoul_db.keys()))
        char = seoul_db[region]
        
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
        st.markdown(f"<span class='char-role'>{char.get('role', '서울의 수호신')}</span>", unsafe_allow_html=True)
        
        # CSV에서 읽어온 데이터가 없을 경우를 대비해 .get() 사용
        personality = char.get('personality', '알 수 없음')
        speech = char.get('speech', '친절한 말투')
        keyword = char.get('keyword', region)
        welcome = char.get('welcome', '반갑소!')
        
        st.markdown(f"<div style='background-color:#fff; border:2px solid #eee; border-radius:15px; padding:20px; margin:20px 0;'><b>💡 성격:</b> {personality}<br><br><b>🗣️ 말투:</b> {speech}<br><br><b>🔑 키워드:</b> {keyword}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='speech-bubble'><b>{char['name']}</b>: \"{welcome}\"</div>", unsafe_allow_html=True)

    st.markdown("---")
    
    # --------------------------------------------------------------------------------
    # [수정] 4대 기능 탭: CSV 원본 스토리 엄격 준수 (Strict Mode)
    # --------------------------------------------------------------------------------
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
                        story_content = char.get('story', '스토리 데이터가 없습니다.')
                        
                        prompt = f"""
                        당신은 서울 {region}의 {char['name']}입니다.
                        사용자({user['name']})에게 당신의 전설을 들려주세요.

                        [지시사항]
                        1. 아래 [원본 스토리] 내용을 '그대로' 구연동화처럼 생생하게 읽어주세요.
                        2. 내용을 요약하거나 줄이지 마세요. (Full Text 유지)
                        3. 말투는 반드시 지정된 [말투]를 사용하세요.

                        [말투]: {speech}
                        [원본 스토리]: {story_content}
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
                        story_content = char.get('story', '')
                        sys_prompt = f"""
                        당신은 {region}의 {char['name']}입니다.
                        당신의 배경 설정(Origin Story)은 다음과 같습니다:
                        "{story_content}"
                        
                        위 설정에 없는 내용은 모른다고 답하거나, 당신의 이야기로 화제를 돌리세요.
                        말투: {speech}
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

    # 3. 그림 그리기 (기존 유지)
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

    # 4. 작가 되기 (기존 유지)
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
                    {speech} 말투로 감상평을 남겨주세요.
                    칭찬과 함께 더 재미있는 아이디어를 하나 덧붙여주세요.
                    내용: {user_story}
                    """
                    res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": eval_prompt}]
                    )
                    st.success(res.choices[0].message.content)
