import streamlit as st
import os
from openai import OpenAI

# -------------------------------------------------------------------------
# [설정] V33: 서울 해치 탐험 (Cinematic Video Intro)
# -------------------------------------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="서울 해치 탐험",
    page_icon="🦁",
    initial_sidebar_state="expanded"
)

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
# [화면 1] 인트로: 사용자 정보 입력 (Video Hero + Gallery)
# -------------------------------------------------------------------------
if st.session_state.user_profile is None:
    st.title("🦁 서울 해치 탐험 : 입단 신청서")
    
    col1, col2 = st.columns([1.6, 1]) 
    with col1:
        st.markdown("### \"안녕? 우리는 서울을 지키는 해치 군단이야!\"")
        
        # [핵심 로직] 동영상(mp4) > 이미지(main.png) > 나머지
        intro_dir = "intro"
        video_name = "main.mp4" # 1순위: 동영상
        image_name = "main.png" # 2순위: 이미지

        try:
            if os.path.exists(intro_dir):
                all_files = os.listdir(intro_dir)
                
                # 1. 동영상이 있으면 플레이어 작동 (자동재생, 반복)
                if video_name in all_files:
                    video_path = os.path.join(intro_dir, video_name)
                    st.video(video_path, autoplay=True, loop=True, muted=True)
                    st.markdown("---")
                
                # 2. 동영상이 없고 메인 이미지가 있으면 표시
                elif image_name in all_files:
                    st.image(os.path.join(intro_dir, image_name), use_column_width=True)
                    st.markdown("---")
                
                # 3. 나머지 이미지들 갤러리 (main.mp4, main.png 제외)
                # 이미지 파일만 골라내기
                gallery_images = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                # 메인 이미지는 갤러리에서 빼기 (중복 방지)
                gallery_images = [img for img in gallery_images if img != image_name]
                
                if gallery_images:
                    st.caption("👇 더 많은 친구들을 소개할게!")
                    cols = st.columns(3)
                    for i, img_file in enumerate(gallery_images):
                        with cols[i % 3]:
                            st.image(os.path.join(intro_dir, img_file), use_column_width=True)
                elif not (video_name in all_files or image_name in all_files):
                     st.warning("해치들이 아직 도착하지 않았소.")

            else:
                 st.warning("아직 'intro' 폴더가 없군요.")
                 
        except Exception as e:
             st.error(f"미디어 로딩 오류: {e}")

    with col2:
        with st.container(border=True):
            st.markdown("#### 📝 탐험대원 등록")
            st.caption("너에 대해 알려주면 딱 맞는 해치를 소개해줄게!")
            with st.form("intro_form"):
                name = st.text_input("이름 (Name)", placeholder="길동이")
                age = st.slider("나이 (Age)", 5, 100, 25)
                gender = st.radio("성별 (Gender)", ["남성", "여성", "기타"])
                nationality = st.selectbox("국적 (Nationality)", ["대한민국", "USA", "China", "Japan", "France", "Germany", "Other"])
                
                st.markdown("") 
                submitted = st.form_submit_button("🚀 해치 만나러 가기 (Start)", type="primary", use_container_width=True)
                
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
# [화면 2] 메인 앱 (변동 없음)
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
            api_key = st.text_input("OpenAI API Key", type="password")
        
        client = OpenAI(api_key=api_key) if api_key else None
        
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
            if not client: st.warning("API Key 필요")
            else:
                with st.spinner(f"{user['name']}님을 위해 이야기를 각색하는 중..."):
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
                    try:
                        tts_res = client.audio.speech.create(
                            model="tts-1",
                            voice="onyx",
                            input=full_story[:4096]
                        )
                        tts_res.stream_to_file("story_audio.mp3")
                        st.audio("story_audio.mp3", format="audio/mp3")
                    except Exception as e:
                        st.error(f"오디오 오류: {e}")

    # [Tab 2] 수다 떨기
    with tab2:
        st.subheader(f"🗣️ {char['name']}와 {selected_lang}로 대화하기")
        
        if "rp_messages" not in st.session_state:
            st.session_state.rp_messages = []
            
        for m in st.session_state.rp_messages:
            with st.chat_message(m["role"]): st.write(m["content"])
                
        if user_input := st.chat_input(f"{selected_lang}로 말을 걸어보세요..."):
            st.session_state.rp_messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"): st.write(user_input)
            
            if client:
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

    # [Tab 3] 이미지
    with tab3:
        st.subheader("🎨 상상화 그리기")
        scene = st.text_input("어떤 장면을 그릴까요?")
        if st.button("그림 생성"):
            if client:
                with st.spinner("그리는 중..."):
                    p = f"Illustration of {char['name']} ({char['visual']}). Scene: {scene}. Target Audience Age: {user['age']}"
                    try:
                        res = client.images.generate(model="dall-e-3", prompt=p, size="1024x1024")
                        st.image(res.data[0].url)
                    except: st.error("오류 발생")

    # [Tab 4] 작가 모드
    with tab4:
        st.subheader("👑 내가 만드는 새로운 전설")
        col1, col2 = st.columns(2)
        with col1: user_name = st.text_input("작가님 이름", value=user['name'])
        with col2: keywords = st.text_input("소재 (예: AI, 우주선)")
            
        if st.button("✨ 새 전설 창작하기"):
            if client and keywords:
                with st.spinner("창작 중..."):
                    prompt = f"""
                    작가: {user_name} ({user['age']}세)
                    주인공: {char['name']}
                    소재: {keywords}
                    {user['age']}세 작가의 눈높이에 맞는 재미있는 동화를 써주세요.
                    """
                    resp = client.chat.completions.create(model="gpt-4", messages=[{"role":"user", "content":prompt}])
                    st.write(resp.choices[0].message.content)
