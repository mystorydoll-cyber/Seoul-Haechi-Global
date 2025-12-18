import streamlit as st
import os
from openai import OpenAI

# -------------------------------------------------------------------------
# [설정] V43: 서울 해치 탐험 (HTML Rendering Fix)
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

    .main-title {
        font-family: 'Jua', sans-serif;
        text-align: center;
        font-size: 3.5rem !important;
        color: #FF4B4B; 
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-title {
        font-family: 'Jua', sans-serif;
        text-align: center;
        font-size: 1.8rem !important;
        color: #555;
        margin-bottom: 2rem;
    }
    div[data-testid="stForm"] {
        background-color: #f9f9f9;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 2px solid #eee;
    }
    /* 정보 박스 디자인 */
    .info-box {
        background-color: #e8f4f8;
        padding: 25px;
        border-radius: 15px;
        margin-top: 20px;
        border-left: 6px solid #FF4B4B;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        color: #333; /* 글자색 강제 지정 */
    }
    .info-box h4 {
         font-family: 'Jua', sans-serif !important;
         color: #333 !important;
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
# [데이터] CEO 원천 소스
# -------------------------------------------------------------------------
seoul_db = {
    "종로구": {
        "name": "초롱해치",
        "role": "전통과 역사를 소중히 여기며 지키려는 마음을 가진 해치",
        "personality": "진지하고 사려 깊은 성격",
        "speech": "옛스런 어휘를 쓰며 점잖게 타이르는 '사극 톤' (~하오, ~다오)",
        "story": "옛날 조선시대, 궁궐에서 밤길을 밝히던 초롱이 오랜 세월 빚어지면서 해치가 되었어요. 그는 궁궐의 균형을 지키며 밤을 밝히는 역할을 했어요. 그런데 어느 날, 경복궁과 창덕궁, 종묘의 도깨비들이 봉인을 깨고 탈출했어요! 초롱해치는 탈출한 도깨비들을 잡기 위해 종로로 나섰어요. 삼청동 붓가게에서 낙서를 하던 도깨비와 글씨 대결을, 인사동 찻집에선 차 시음 대결을 펼쳐 승리했죠. 마지막으로 광화문 네온사인에 홀린 도깨비에게 '네온사인은 변하지만 궁궐의 빛은 변하지 않아'라고 설득해 다시 돌려보냈답니다. 지금도 종로의 밤거리엔 내 눈빛이 서려 있다오.",
        "welcome": "내 초롱은 언제나 빛나고 있어.",
        "visual": "청사초롱을 들고 갓을 쓴 점잖은 모습의 분홍색 해치",
        "item": "전통차 한 잔",
        "keyword": "경복궁, 창덕궁, 종묘, 광화문, 전통차"
    },
    "중구": {
        "name": "쇼퍼해치",
        "role": "마법의 쇼핑백을 들고 사람들에게 필요한 물건을 찾아주는 도우미 도깨비",
        "personality": "항상 새로운 물건을 찾는 데 열정적인 도깨비",
        "speech": "활기차고 느낌표가 많은 '쇼호스트 톤' (~거든요!, ~라구요!)",
        "story": "서울 중구의 번화한 거리에서 쇼핑을 사랑하는 도깨비, 쇼퍼해치가 살고 있었어요. 하루는 명동 거리에서 비싼 가격 때문에 치마를 못 사고 슬퍼하는 소녀를 봤어요. '걱정하지 마! 내가 너에게 딱 맞는 치마를 찾아줄게!' 쇼퍼해치는 마법의 쇼핑백을 꺼내 소녀에게 딱 맞는 예쁜 치마를 찾아주었죠. 남대문에서는 지갑 잃어버린 아저씨를 도와주고, 동대문에선 예쁜 신발을 찾아주었답니다. 쇼핑을 통해 사람들에게 행복을 주는 것이 나의 가장 큰 기쁨이야!",
        "welcome": "이건 꼭 필요해! 나도 이거 사야지!",
        "visual": "양손에 화려한 쇼핑백을 들고 선글라스를 낀 힙한 해치",
        "item": "마법의 쇼핑백",
        "keyword": "쇼핑, 예쁜 쇼핑백, 패션 아이템, 명동, 동대문"
    },
    "용산구": {
        "name": "어텐션해치",
        "role": "다양한 문화를 이어주며 이해와 평화를 이끄는 신비로운 도깨비",
        "personality": "사려 깊고 경청하며, 항상 긍정적인 해결책을 찾는 성격",
        "speech": "영어(Yo, Respect)를 섞어 쓰는 쿨한 '교포 힙합 톤'",
        "story": "Hey! I'm Attention Haechi! 이태원과 용산 미군 기지 근처에는 세계 여러 나라 사람들의 이야기를 마법처럼 들을 수 있는 내가 살고 있지. 어느 날, 이태원에서 서로 다른 문화 때문에 갈등하는 외국인들을 만났어. 나는 그들의 고향 이야기를 들어주며 서로를 연결해 주었지. '다르다는 건 틀린 게 아니야.' 내 이야기는 이태원을 더욱 다채롭고 포용적인 곳으로 만들었단다. Peace!",
        "welcome": "다른 사람의 이야기를 듣는 것이 세상을 이해하는 첫걸음이야.",
        "visual": "헤드셋을 끼고 힙합 스타일 후드티를 입은 자유로운 영혼",
        "item": "세계 지도 손수건",
        "keyword": "이태원, 세계 음식, 다양성, 화합"
    },
    "성동구": {
        "name": "뚝해치",
        "role": "살곶이다리에 마법을 걸어 과거와 현재를 잇는 도깨비",
        "personality": "신중하고 지혜로우며, 오래된 것을 소중히 여기는 성격",
        "speech": "나긋나긋하고 감성적인 '동화 구연가 톤' (~했답니다, ~군요)",
        "story": "옛날 성동구 살곶이다리에는 사람들의 발걸음을 지켜보는 뚝해치가 살았어요. 요즘 사람들이 스마트폰만 보며 다리의 이야기를 잊어가자, 나는 작은 마법을 걸었답니다. 다리를 지날 때 소원을 빌면 과거가 보이도록요! 한 꼬마가 소원을 빌자, 조선시대 말을 탄 장수와 선비의 모습이 눈앞에 펼쳐졌어요. '와! 이 다리는 이야기가 흐르는 곳이네요!' 그날 이후 살곶이다리는 다시 시간을 잇는 다리가 되었답니다.",
        "welcome": "다리는 단순한 돌덩이가 아니라, 이야기가 흐르는 길이지!",
        "visual": "오래된 돌망태를 메고 성수동 카페거리에 앉아있는 감성적인 해치",
        "item": "작은 돌멩이",
        "keyword": "살곶이다리, 성동구의 옛날 이야기, 성수동, 시간여행"
    },
    "광진구": {
        "name": "광나루해치",
        "role": "음식을 음미하는 기쁨을 나눠주는 미식 도깨비",
        "personality": "미식가이며 장난기 많지만 진심으로 음식을 사랑함",
        "speech": "맛을 음미하며 감탄사를 연발하는 '미식가 톤' (음~!, 캬~!)",
        "story": "옛날 한강 나루터에는 미각이 뛰어난 광나루해치가 살았어요. '음, 서쪽 행신로 냄새! 오늘은 양꼬치군!' 그런데 사람들이 바쁘게 먹기만 하고 맛을 느끼지 못하자, 나는 장난을 쳤어요. 음식 냄새를 싹 없애버린 거죠! '어? 왜 곱창 냄새가 안 나지?' 사람들은 당황했고, 그제야 천천히 씹으며 맛을 음미하기 시작했어요. '아, 음식은 즐기는 거였지!' 나는 흐뭇하게 웃으며 냄새를 돌려주었답니다. 음~! 이게 한강의 맛이지!",
        "welcome": "음~! 이건 그냥 맛있는 게 아니라, '진짜' 맛있는 거야!",
        "visual": "한 손에 은색 숟가락을 들고 입맛을 다시는 통통한 해치",
        "item": "작은 은색 숟가락",
        "keyword": "한강, 양꼬치, 곱창, 미식, 맛있는 냄새"
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
    # 1. 헤더 (타이틀)
    st.markdown('<p class="main-title">🦁 서울 해치 탐험 : 입단 신청서</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">"안녕? 우리는 서울을 지키는 해치 군단이야!"</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns([1.5, 1], gap="large")
    
    with col1:
        # 1-1. 미디어 플레이어
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
             
        # 1-2. [수정됨] 정보 박스 (변수로 분리하여 안전하게 렌더링)
        info_html = """
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
        """
        # ★ 여기가 중요! unsafe_allow_html=True를 꼭 넣어서 HTML로 해석하게 함
        st.markdown(info_html, unsafe_allow_html=True)

    with col2:
        # 2. 입력 카드
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
# [화면 2] 메인 앱
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
            
            img_name = f"{region}_{char['name']}.png"
            if os.path.exists(img_name):
                st.image(img_name)
            else:
                st.info(f"📸 {char['visual']}")
            st.markdown(f"**🔑 키워드:** {char['keyword']}")

    st.markdown(f"# 🗺️ {region} 해치 탐험 : {char['name']}와의 만남")
    
    if client and "welcome_msg" not in st.session_state:
        pass 
    st.info(f"👋 **{char['name']}**: \"어서 와, {user['name']}! ({selected_lang} 모드 작동 중)\"")
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["📜 전설 듣기", "🗣️ 수다 떨기", "🎨 삽화 그리기", "✍️ 나도 전설 작가"])

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
