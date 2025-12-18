import streamlit as st
import os
from openai import OpenAI

# -------------------------------------------------------------------------
# [설정] V47: 서울 해치 탐험 (Content Expanded - 10 Districts)
# -------------------------------------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="서울 해치 탐험",
    page_icon="🦁",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------
# [스타일] CSS (디자인 고도화)
# -------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

    /* [공통] 폰트 적용 */
    h1, h2, h3, h4, .stMarkdown, p, div {
        font-family: 'Jua', sans-serif !important;
    }

    /* 인트로 메인 타이틀 */
    .main-title {
        text-align: center;
        font-size: 3.5rem !important;
        color: #FF4B4B; 
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-title {
        text-align: center;
        font-size: 1.8rem !important;
        color: #555;
        margin-bottom: 2rem;
    }
    
    /* 메인 페이지 타이틀 */
    .app-header {
        font-size: 2.8rem !important;
        color: #333;
        text-shadow: 2px 2px 0px #eee;
        margin-bottom: 20px;
    }
    .app-header .highlight {
        color: #FF4B4B;
        font-size: 1.2em;
        text-decoration: underline;
        text-decoration-style: wavy;
        text-decoration-color: #FFD700;
        margin: 0 5px;
    }

    /* 입력 폼 및 박스 스타일 */
    div[data-testid="stForm"] {
        background-color: #f9f9f9;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 2px solid #eee;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 25px;
        border-radius: 15px;
        margin-top: 20px;
        border-left: 6px solid #FF4B4B;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        color: #333;
    }
    .info-box h4 {
         font-size: 1.5rem !important;
         margin-bottom: 15px;
         border-bottom: 2px dashed #b3d7ff;
         padding-bottom: 10px;
    }
    .info-item {
        margin-bottom: 12px;
        font-size: 1rem;
        line-height: 1.6;
        color: #444;
    }
    .info-item strong {
        color: #007bff;
        font-weight: 700;
        font-size: 1.1rem;
    }
    .copyright {
        font-size: 0.8em; 
        color: gray; 
        margin-top: 20px;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# [데이터] CEO 원천 소스 (총 10개 구 확장)
# -------------------------------------------------------------------------
seoul_db = {
    "종로구": {
        "name": "초롱해치",
        "role": "전통과 역사를 지키는 선비 해치",
        "personality": "진지하고 사려 깊은 성격",
        "speech": "점잖은 '사극 톤' (~하오, ~다오)",
        "story": "조선시대 궁궐의 밤을 밝히던 초롱불이 해치가 되었어요. 경복궁과 광화문을 지키며 역사를 잊은 사람들에게 옛 이야기를 들려줍니다.",
        "welcome": "내 초롱은 언제나 빛나고 있어.",
        "visual": "청사초롱을 들고 갓을 쓴 분홍색 해치",
        "keyword": "경복궁, 광화문, 역사, 전통"
    },
    "중구": {
        "name": "쇼퍼해치",
        "role": "쇼핑과 패션을 사랑하는 힙한 해치",
        "personality": "활기차고 유행에 민감함",
        "speech": "통통 튀는 '쇼호스트 톤' (~거든요!, ~라구요!)",
        "story": "명동과 동대문의 쇼핑 열기 속에서 태어났어요. 마법의 쇼핑백으로 사람들에게 딱 맞는 패션 아이템을 찾아준답니다.",
        "welcome": "어머! 이 옷은 꼭 사야 해!",
        "visual": "양손에 쇼핑백을 들고 선글라스를 낀 해치",
        "keyword": "명동, 쇼핑, 패션, 남산타워"
    },
    "용산구": {
        "name": "어텐션해치",
        "role": "세계 문화를 잇는 글로벌 해치",
        "personality": "개방적이고 쿨함",
        "speech": "영어를 섞어 쓰는 '교포 힙합 톤' (Yo!)",
        "story": "이태원의 다양성 속에서 태어난 해치. 서로 다른 언어와 문화를 가진 사람들을 연결해주며 평화를 노래해요.",
        "welcome": "Yo! We are the world!",
        "visual": "헤드셋을 끼고 힙합 후드티를 입은 해치",
        "keyword": "이태원, 미군기지, 다양성, 힙합"
    },
    "성동구": {
        "name": "뚝해치",
        "role": "과거와 현재를 잇는 감성 해치",
        "personality": "신중하고 감성적임",
        "speech": "나긋나긋한 '동화 구연가 톤'",
        "story": "성수동 카페거리와 살곶이 다리에 살아요. 오래된 공장이 힙한 카페로 변하는 모습을 보며 시간의 마법을 부린답니다.",
        "welcome": "낡은 것에는 아름다운 이야기가 숨어있단다.",
        "visual": "빈티지 카메라를 메고 있는 감성적인 해치",
        "keyword": "성수동, 서울숲, 팝업스토어, 살곶이다리"
    },
    "광진구": {
        "name": "광나루해치",
        "role": "한강의 맛을 즐기는 미식가 해치",
        "personality": "먹는 것을 가장 좋아함",
        "speech": "감탄사가 많은 '먹방 유튜버 톤' (와~!)",
        "story": "한강 뚝섬유원지에서 배달음식 냄새를 맡고 깨어났어요. 맛있는 음식을 먹을 때 가장 행복한 마법이 나온답니다.",
        "welcome": "음~! 치킨 냄새가 나를 부르는군!",
        "visual": "한 손에 닭다리를 들고 있는 통통한 해치",
        "keyword": "한강공원, 뚝섬, 건대입구, 맛집"
    },
    # [신규 확장 지역]
    "강남구": {
        "name": "스타일해치",
        "role": "K-Culture를 이끄는 슈퍼스타 해치",
        "personality": "자신감 넘치고 화려함",
        "speech": "자신감 넘치는 '아이돌 센터 톤'",
        "story": "강남의 화려한 조명 아래서 태어난 슈퍼스타! K-POP 댄스로 사람들에게 에너지를 주고, 최신 유행을 창조해요.",
        "welcome": "Are you ready? 강남 스타일로 놀아볼까?",
        "visual": "화려한 무대 의상을 입고 마이크를 든 해치",
        "keyword": "강남스타일, 코엑스, K-POP, 가로수길"
    },
    "마포구": {
        "name": "힙스터해치",
        "role": "거리의 낭만을 노래하는 버스킹 해치",
        "personality": "자유분방하고 예술적임",
        "speech": "툭툭 던지는 '인디 밴드 보컬 톤'",
        "story": "홍대 거리의 버스킹 음악 소리를 듣고 자랐어요. 누구나 자신의 꿈을 노래할 수 있도록 용기를 북돋아 준답니다.",
        "welcome": "길거리가 곧 나의 무대야.",
        "visual": "통기타를 메고 베레모를 쓴 예술가 해치",
        "keyword": "홍대, 버스킹, 연남동, 젊음"
    },
    "송파구": {
        "name": "로맨틱해치",
        "role": "사랑과 환상을 지키는 큐피트 해치",
        "personality": "사랑스럽고 꿈이 많음",
        "speech": "달콤하고 상냥한 '놀이공원 캐스트 톤'",
        "story": "석촌호수의 벚꽃과 롯데월드의 환상 속에서 태어났어요. 연인들의 사랑을 이루어주고, 아이들의 동심을 지켜줘요.",
        "welcome": "환상의 나라로 온 걸 환영해!",
        "visual": "풍선을 들고 머리띠를 한 귀여운 해치",
        "keyword": "롯데월드, 석촌호수, 벚꽃, 잠실종합운동장"
    },
    "영등포구": {
        "name": "골드해치",
        "role": "성공과 부를 가져다주는 금융 해치",
        "personality": "스마트하고 계산이 빠름",
        "speech": "논리 정연한 '펀드매니저 톤'",
        "story": "여의도의 높은 빌딩 숲과 한강의 불꽃축제를 보며 태어났어요. 열심히 일하는 사람들에게 성공의 기운을 불어넣어 준답니다.",
        "welcome": "시간은 금이라고! 성공하고 싶나?",
        "visual": "금테 안경을 쓰고 정장을 입은 똑똑한 해치",
        "keyword": "여의도, 더현대서울, 한강불꽃축제, 금융"
    },
    "서초구": {
        "name": "마에스트로해치",
        "role": "예술과 빛을 지휘하는 지휘자 해치",
        "personality": "우아하고 기품 있음",
        "speech": "중후하고 멋진 '지휘자 톤'",
        "story": "예술의 전당의 클래식 선율과 세빛섬의 야경이 어우러져 태어났어요. 서울의 밤을 아름다운 빛과 음악으로 지휘한답니다.",
        "welcome": "자, 서울이라는 오케스트라를 시작해볼까?",
        "visual": "지휘봉을 들고 턱시도를 입은 클래식한 해치",
        "keyword": "예술의전당, 세빛섬, 반포대교, 고속터미널"
    }
}

# -------------------------------------------------------------------------
# [로직] 사용자 프로필 관리
# -------------------------------------------------------------------------
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None

# -------------------------------------------------------------------------
# [화면 1] 인트로: 입단 신청서
# -------------------------------------------------------------------------
if st.session_state.user_profile is None:
    st.markdown('<p class="main-title">🦁 서울 해치 탐험 : 입단 신청서</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">"안녕? 우리는 서울을 지키는 해치 군단이야!"</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns([1.5, 1], gap="large")
    
    with col1:
        intro_dir = "intro"
        video_name = "main.mp4" 
        image_name = "main.png" 

        try:
            if os.path.exists(intro_dir):
                all_files = os.listdir(intro_dir)
                if video_name in all_files:
                    st.video(os.path.join(intro_dir, video_name), autoplay=True, loop=True, muted=True)
                elif image_name in all_files:
                    st.image(os.path.join(intro_dir, image_name), use_column_width=True)
                else:
                     st.info("🦁 인트로 미디어를 준비 중입니다.")
            else:
                 st.warning("⚠️ 'intro' 폴더가 없습니다.")
        except Exception as e:
             st.error(f"Error: {e}")
             
        # 정보 박스 (HTML)
        st.markdown("""
<div class="info-box">
<h4>💡 해치(Haechi)는 어떤 친구인가요?</h4>
<div class="info-item">
<strong>🐣 탄생의 비밀</strong><br>
해치는 선과 악을 구별하고, 화재나 재앙을 막아주는 전설 속 신비한 동물이에요.
정의로운 마음을 가지고 서울에서 태어났답니다!
</div>
<div class="info-item">
<strong>🦁 매력 포인트</strong><br>
방울을 달고 서울 25개 구 곳곳에 숨어 살아요.<br>
동네마다 모습과 성격이 달라서 찾아보는 재미가 쏠쏠하답니다.
</div>
<div class="info-item">
<strong>🍀 함께하면 좋은 점</strong><br>
해치와 함께라면 서울 여행이 더 안전하고 행운이 가득해져요.<br>
진짜 서울 사람들만 아는 숨은 핫플레이스도 알려줄 거예요!
</div>
<div class="copyright">
© 2025 My Story Doll & Seoul Haechi. All rights reserved.<br>
Powered by M-Unit AI Technology.
</div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🎫 탐험대원 등록 카드")
        st.caption("너에 대해 알려주면 딱 맞는 해치를 소개해줄게!")
        
        with st.form("intro_form"):
            name = st.text_input("이름 (Name)", placeholder="예: 길동이")
            age = st.slider("나이 (Age)", 5, 100, 25)
            gender = st.radio("성별 (Gender)", ["남성", "여성", "기타"], horizontal=True)
            nationality = st.selectbox("국적 (Nationality)", ["대한민국", "USA", "China", "Japan", "France", "Germany", "Other"])
            
            st.markdown("---")
            submitted = st.form_submit_button("해치 만나러 가기 (Start Adventure)", type="primary", use_container_width=True)
            
            if submitted and name:
                st.session_state.user_profile = {
                    "name": name,
                    "age": age,
                    "gender": gender,
                    "nationality": nationality
                }
                st.rerun()
            elif submitted and not name:
                st.error("이름을 알려줘야 시작할 수 있어!")

# -------------------------------------------------------------------------
# [화면 2] 메인 앱 (Main Application)
# -------------------------------------------------------------------------
else:
    user = st.session_state.user_profile
    
    with st.sidebar:
        st.title(f"반갑소, {user['name']}!")
        st.caption(f"{user['age']}세 / {user['nationality']}")
        
        if st.button("🔄 내 정보 다시 입력하기"):
            st.session_state.user_profile = None
            st.rerun()
        st.markdown("---")
        
        st.markdown("### 🌐 언어 모드 (Language)")
        lang_options = ["한국어", "English", "中文 (Chinese)", "日本語 (Japanese)", "Français (French)", "Deutsch (German)"]
        
        default_idx = 0
        if user['nationality'] == "USA": default_idx = 1
        elif user['nationality'] == "China": default_idx = 2
        elif user['nationality'] == "Japan": default_idx = 3
        
        selected_lang = st.selectbox("대화 언어 선택", lang_options, index=default_idx)
        st.markdown("---")
        
        if "OPENAI_API_KEY" in st.secrets:
            api_key = st.secrets["OPENAI_API_KEY"]
        else:
            api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
        
        client = None
        if api_key:
            try:
                client = OpenAI(api_key=api_key)
            except: pass
        
        if not client:
            st.error("🚨 왼쪽 칸에 API Key를 넣고 [ENTER]를 쳐주세요!")
        
        st.markdown("### 📍 탐험할 지역 선택")
        region = st.selectbox("어느 구의 해치를 만날까?", list(seoul_db.keys()))
        char = seoul_db[region]
        
        with st.container(border=True):
            st.subheader(f"✨ {char['name']}")
            st.caption(f"{char['role']}")
            
            # [이미지 체크] 새로운 지역 이미지가 없으면 기본값으로 표시됨
            img_name = f"{region}_{char['name']}.png"
            if os.path.exists(img_name):
                st.image(img_name)
            else:
                st.info(f"📸 {char['visual']} (이미지 준비중)")
            st.markdown(f"**🔑 키워드:** {char['keyword']}")

    # 메인 페이지 타이틀
    st.markdown(f"""
    <div class='app-header'>
        🗺️ {region} 해치 탐험 : <span class='highlight'>{char['name']}</span>와의 만남
    </div>
    """, unsafe_allow_html=True)
    
    if client and "welcome_msg" not in st.session_state:
        pass 
    st.info(f"👋 **{char['name']}**: \"어서 와, {user['name']}! ({selected_lang} 모드 작동 중)\"")
    st.markdown("---")

    # 탭 메뉴
    tab1, tab2, tab3, tab4 = st.tabs(["🦁📜 전설 듣기", "🦁🗣️ 수다 떨기", "🦁🎨 삽화 그리기", "🦁✍️ 나도 전설 작가"])

    # [Tab 1] 전설 듣기
    with tab1:
        st.subheader(f"📖 {char['name']}의 이야기 보따리")
        
        if st.button(f"▶️ 이야기 들려주세요 ({selected_lang})", type="primary"):
            if not client: st.error("🚨 API Key가 필요합니다!")
            else:
                with st.spinner(f"{user['name']}님을 위해 이야기를 각색하는 중..."):
                    try:
                        prompt = f"""
                        당신은 '{char['name']}'입니다.
                        [원래 이야기]: {char['story']}
                        [말투]: {char['speech']}
                        [사용자 정보]: {user['age']}세, {user['nationality']}, {user['name']}
                        [필수 언어]: **{selected_lang}**로 답변하세요.
                        [미션]: 위 사용자가 가장 흥미로워하고 이해하기 쉽게 이야기를 '각색'해서 들려주세요.
                        """
                        resp = client.chat.completions.create(model="gpt-4", messages=[{"role":"user", "content":prompt}])
                        full_story = resp.choices[0].message.content
                        st.write(full_story)

                        with st.spinner("목소리 가다듬는 중..."):
                            tts_res = client.audio.speech.create(model="tts-1", voice="onyx", input=full_story[:4096])
                            tts_res.stream_to_file("story_audio.mp3")
                            st.audio("story_audio.mp3", format="audio/mp3")
                    except Exception as e: st.error(f"오류: {e}")

    # [Tab 2] 수다 떨기
    with tab2:
        st.subheader(f"🗣️ {char['name']}와 {selected_lang}로 대화하기")
        if "rp_messages" not in st.session_state: st.session_state.rp_messages = []
        
        for m in st.session_state.rp_messages:
            with st.chat_message(m["role"]): st.write(m["content"])
            
        if user_input := st.chat_input(f"{selected_lang}로 말을 걸어보세요..."):
            st.session_state.rp_messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"): st.write(user_input)
            
            if client:
                try:
                    sys_prompt = f"""
                    당신은 '{char['name']}'입니다. ({char['personality']}, {char['speech']})
                    상대방: {user['age']}세 {user['nationality']} {user['name']}
                    **중요: 반드시 {selected_lang}로 대화하세요.**
                    """
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "system", "content": sys_prompt}] + st.session_state.rp_messages
                    )
                    ai_reply = response.choices[0].message.content
                    st.session_state.rp_messages.append({"role": "assistant", "content": ai_reply})
                    with st.chat_message("assistant"): st.write(ai_reply)
                except Exception as e: st.error(f"오류: {e}")
            else: st.error("🚨 API Key가 필요합니다!")

    # [Tab 3] 이미지
    with tab3:
        st.subheader("🎨 상상화 그리기")
        scene = st.text_input("어떤 장면을 그릴까요?", placeholder="예: 떡볶이 먹는 해치")
        if st.button("그림 생성"):
            if client:
                with st.spinner("그리는 중..."):
                    try:
                        p = f"Illustration of {char['name']} ({char['visual']}). Scene: {scene}. Target Audience Age: {user['age']}"
                        res = client.images.generate(model="dall-e-3", prompt=p, size="1024x1024")
                        st.image(res.data[0].url)
                    except Exception as e: st.error(f"오류: {e}")
            else: st.error("🚨 API Key가 필요합니다!")

    # [Tab 4] 작가 모드
    with tab4:
        st.subheader("👑 내가 만드는 새로운 전설")
        col1, col2 = st.columns(2)
        with col1: user_name = st.text_input("작가님 이름", value=user['name'])
        with col2: keywords = st.text_input("소재 (예: AI, 우주선)")
        
        if st.button("✨ 새 전설 창작하기"):
            if not client: st.error("🚨 API Key가 필요합니다!")
            elif not keywords: st.warning("소재를 입력해주세요!")
            else:
                with st.spinner("창작 중..."):
                    try:
                        prompt = f"""
                        작가: {user_name} ({user['age']}세)
                        주인공: {char['name']}
                        소재: {keywords}
                        {user['age']}세 작가의 눈높이에 맞는 재미있는 동화를 써주세요.
                        """
                        resp = client.chat.completions.create(model="gpt-4", messages=[{"role":"user", "content":prompt}])
                        st.write(resp.choices[0].message.content)
                    except Exception as e: st.error(f"오류: {e}")
