import streamlit as st
import os
from openai import OpenAI

# -------------------------------------------------------------------------
# [설정] V23: 서울 전설 탐험대 (Global Creator Edition)
# -------------------------------------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="서울 해치 전설 탐험대",
    page_icon="🦁",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------
# [데이터] CEO 원천 소스 반영 (종로, 중구, 용산, 성동, 광진)
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
# [UI] 사이드바 & 다국어 설정
# -------------------------------------------------------------------------
with st.sidebar:
    st.title("🦁 서울 전설 탐험대")
    st.caption("Seoul Legend Expedition V23")
    st.markdown("---")
    
    # API 키 입력
    if "OPENAI_API_KEY" in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
    else:
        api_key = st.text_input("OpenAI API Key", type="password")
    
    client = OpenAI(api_key=api_key) if api_key else None
    
    # [기능 1] 다국어 지원 설정
    st.markdown("### 🌍 언어 선택 (Language)")
    lang_code = st.selectbox(
        "어떤 언어로 대화할까요?",
        ["한국어", "English", "中文 (Chinese)", "日本語 (Japanese)", "Français (French)", "Deutsch (German)"]
    )
    
    st.markdown("### 📍 탐험할 지역 선택")
    region = st.selectbox("어느 구의 전설을 들을까?", list(seoul_db.keys()))
    char = seoul_db[region]
    
    # 캐릭터 카드
    with st.container(border=True):
        st.subheader(f"✨ {char['name']}")
        st.caption(f"{char['role']}")
        
        img_name = f"{region}_{char['name']}.png"
        if os.path.exists(img_name):
            st.image(img_name)
        else:
            st.info(f"📸 {char['visual']}")
            
        st.success(f"💬 \"{char['welcome']}\"")
        st.markdown(f"**🔑 키워드:** {char['keyword']}")

# -------------------------------------------------------------------------
# [메인] 탭 구성 (4개 탭)
# -------------------------------------------------------------------------
st.markdown(f"# 🗺️ {region} 전설 탐험 : {char['name']}와의 만남")
st.markdown(f"### \"{char['welcome']}\"")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📜 전설 듣기", "🗣️ 수다 떨기 (Global Chat)", "🎨 삽화 그리기", "✍️ 나도 전설 작가"])

# [Tab 1] 전설 이야기
with tab1:
    st.subheader(f"📖 {char['name']}의 비하인드 스토리")
    st.write(f"**배경:** {char['story']}")  # 원문 텍스트 표시
    
    if st.button("▶️ AI 성우가 읽어주기 (TTS)", type="primary"):
        if not client: st.warning("API Key 필요")
        else:
            with st.spinner("목소리 가다듬는 중..."):
                try:
                    # 텍스트가 너무 길면 요약해서 읽기
                    response = client.audio.speech.create(
                        model="tts-1",
                        voice="onyx",
                        input=char['story'][:4096]
                    )
                    response.stream_to_file("story_audio.mp3")
                    st.audio("story_audio.mp3")
                except Exception as e:
                    st.error(f"오류: {e}")

# [Tab 2] 다국어 프리토킹 (업그레이드)
with tab2:
    st.subheader(f"🌍 {char['name']}와 {lang_code}로 대화하기")
    st.info(f"지금 {char['name']}는 **{lang_code}**를 완벽하게 구사하며, **{char['speech']}** 말투를 유지합니다!")

    if "rp_messages" not in st.session_state:
        st.session_state.rp_messages = []
        
    for m in st.session_state.rp_messages:
        with st.chat_message(m["role"]): st.write(m["content"])
            
    if user_input := st.chat_input(f"{lang_code}로 말을 걸어보세요..."):
        st.session_state.rp_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"): st.write(user_input)
        
        if client:
            # 다국어 페르소나 프롬프트
            sys_prompt = f"""
            당신은 '{char['name']}'입니다.
            [성격]: {char['personality']}
            [원래 말투]: {char['speech']}
            [설정]: {char['story']}
            
            [미션]: 사용자와 대화하되, 반드시 **{lang_code}**로 답변하세요.
            단, 언어가 바뀌어도 당신 특유의 '말투'나 '성격' 느낌은 살려야 합니다.
            (예: 사극 톤이라면 영어에서도 고어(Thee, Thou)를 쓰거나 점잖게 표현)
            """
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": sys_prompt}] + st.session_state.rp_messages
            )
            ai_reply = response.choices[0].message.content
            st.session_state.rp_messages.append({"role": "assistant", "content": ai_reply})
            with st.chat_message("assistant"): st.write(ai_reply)

# [Tab 3] 이미지 생성
with tab3:
    st.subheader("🎨 상상화 그리기")
    scene = st.text_input("어떤 장면을 그릴까요? (예: 떡볶이 먹는 해치)")
    if st.button("그림 생성"):
        if client:
            with st.spinner("그리는 중..."):
                p = f"Illustration of {char['name']} ({char['visual']}), Style: Children's book art. Scene: {scene}"
                try:
                    res = client.images.generate(model="dall-e-3", prompt=p, size="1024x1024")
                    st.image(res.data[0].url)
                except: st.error("이미지 생성 오류")

# [Tab 4] 나만의 전설 만들기 (신규 기능)
with tab4:
    st.subheader("👑 내가 만드는 새로운 전설")
    st.write(f"**{char['name']}**가 주인공인 새로운 이야기를 만들어보세요!")
    
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("작가님 이름 (Your Name)")
    with col2:
        keywords = st.text_input("이야기 소재 (예: 좀비, 지하철, 아이돌)")
        
    if st.button("✨ 새 전설 창작하기"):
        if not client: st.warning("API Key 필요")
        elif not keywords: st.warning("소재를 입력해주세요!")
        else:
            with st.spinner("해치가 머리를 굴리는 중..."):
                prompt = f"""
                당신은 동화 작가입니다.
                주인공: {char['name']} ({char['role']})
                원래 배경: {char['story']}
                
                [요청]: 위 주인공이 등장하는 새로운 짧은 동화를 지어주세요.
                [필수 소재]: {keywords}
                [작가 이름]: {user_name}
                
                이야기는 아주 흥미진진하고 유머러스하게 써주세요.
                마지막에는 "{user_name} 작가님의 상상력, 대단하오!" 처럼 칭찬 멘트를 덧붙여주세요.
                """
                resp = client.chat.completions.create(model="gpt-4", messages=[{"role":"user", "content":prompt}])
                st.success(f"🎉 {user_name} 작가님의 신작 발표!")
                st.markdown(resp.choices[0].message.content)
