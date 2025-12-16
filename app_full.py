import streamlit as st
import os
from openai import OpenAI

# -------------------------------------------------------------------------
# [설정] V13: 글로벌 토킹 에디션 (다국어 + 장난꾸러기 목소리)
# -------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="Seoul Haechis V13")

# -------------------------------------------------------------------------
# [데이터] 25개 자치구
# -------------------------------------------------------------------------
seoul_db = {
    "종로구": {"name": "초롱해치", "trait": "지혜로움", "desc": "종로의 등불을 밝히는 역사 수호자"},
    "중구": {"name": "쇼퍼해치", "trait": "트렌디함", "desc": "명동과 남대문의 패션 리더"},
    "용산구": {"name": "어텐션해치", "trait": "개방적", "desc": "글로벌 문화를 잇는 통신사"},
    "성동구": {"name": "뚝해치", "trait": "활기참", "desc": "서울숲과 뚝섬의 자연 지킴이"},
    "광진구": {"name": "광나루해치", "trait": "용맹함", "desc": "아차산의 기상을 받은 고구려 전사"},
    "동대문구": {"name": "한약해치", "trait": "치유", "desc": "약령시의 기운으로 사람을 고치는 요정"},
    "중랑구": {"name": "장미해치", "trait": "로맨틱", "desc": "장미축제의 아름다움을 전하는 요정"},
    "성북구": {"name": "선잠해치", "trait": "섬세함", "desc": "비단처럼 고운 마음씨의 수호자"},
    "강북구": {"name": "북수해치", "trait": "자유로움", "desc": "북한산 맑은 바람을 타고 노는 친구"},
    "도봉구": {"name": "호랭해치", "trait": "강인함", "desc": "도봉산 호랑이 기운을 타고난 평화지킴이"},
    "노원구": {"name": "태해치", "trait": "충직함", "desc": "태릉의 역사를 지키는 듬직한 무사"},
    "은평구": {"name": "진관해치", "trait": "차분함", "desc": "천년 고찰의 차 향기를 머금은 선비"},
    "서대문구": {"name": "홍지해치", "trait": "희망찬", "desc": "독립문 앞에서 희망을 노래하는 새"},
    "마포구": {"name": "가수해치", "trait": "열정적", "desc": "홍대의 젊음과 음악을 사랑하는 락스타"},
    "양천구": {"name": "배움해치", "trait": "똑똑함", "desc": "미래를 꿈꾸며 책을 읽는 학구파"},
    "강서구": {"name": "강초해치", "trait": "순수함", "desc": "식물원의 푸르름을 간직한 새싹"},
    "구로구": {"name": "디지털해치", "trait": "혁신적", "desc": "첨단 기술로 미래를 여는 엔지니어"},
    "금천구": {"name": "봉제해치", "trait": "성실함", "desc": "한 땀 한 땀 정성으로 옷을 짓는 장인"},
    "영등포구": {"name": "등포해치", "trait": "유연함", "desc": "금융과 정치의 중심을 흐르는 물결"},
    "동작구": {"name": "현충해치", "trait": "헌신적", "desc": "호국영령의 뜻을 기리는 숭고한 천사"},
    "관악구": {"name": "낙성해치", "trait": "용감함", "desc": "하늘에서 떨어진 별, 강감찬 장군의 후예"},
    "서초구": {"name": "법조해치", "trait": "공정함", "desc": "법과 정의를 수호하는 판관"},
    "강남구": {"name": "패션해치", "trait": "화려함", "desc": "트렌드를 이끄는 스타일 아이콘"},
    "송파구": {"name": "몽촌해치", "trait": "전통적", "desc": "백제의 숨결이 깃든 위례성의 주인"},
    "강동구": {"name": "암사해치", "trait": "순수함", "desc": "선사시대부터 이어온 불꽃의 관리자"}
}

# -------------------------------------------------------------------------
# [UI] 사이드바
# -------------------------------------------------------------------------
with st.sidebar:
    st.title("🎛️ Control Center")
    
    # Secrets 자동 로드
    if "OPENAI_API_KEY" in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
        st.success("🔐 VIP 모드: 다국어 음성 지원")
    else:
        api_key = st.text_input("OpenAI API Key", type="password")
        
    client = None
    if api_key:
        try:
            client = OpenAI(api_key=api_key)
        except:
            st.error("❌ 키 오류")
    
    st.markdown("---")
    
    # 25개 리스트
    region = st.selectbox("자치구 선택", list(seoul_db.keys()))
    char = seoul_db[region]
    
    # 이미지 로딩
    img_path = os.path.join("images", f"{region}_{char['name']}.png")
    if os.path.exists(img_path): st.image(img_path, caption=char['name'])
    else: st.info("📸 이미지 없음")
    
    st.success(f"**성격:** {char['trait']}")
    st.write(char['desc'])

# -------------------------------------------------------------------------
# [메인] 화면 구성
# -------------------------------------------------------------------------

# 1. 메인 배너 (유튜브 무한반복)
youtube_url = "https://youtu.be/YIpxEgUCpmA" 
try:
    st.video(youtube_url, autoplay=True, muted=True, loop=True)
except:
    pass

# 2. 제목
st.markdown("<h3 style='text-align: center; color: gray;'>Talk with Seoul Haechis</h3>", unsafe_allow_html=True)
st.markdown("---")
st.title(f"🦁 {char['name']} AI Creator")

# 기능 탭
tab1, tab2, tab3 = st.tabs(["📝 스토리 창작", "💬 캐릭터 음성 대화", "🎨 캐릭터 변형"])

# --- [Tab 1] 스토리 ---
with tab1:
    st.subheader(f"{region}의 맞춤형 스토리")
    col1, col2 = st.columns(2)
    with col1:
        target = st.selectbox("🎯 독자 연령대", ["어린이 (동화풍)", "MZ세대 (트렌디)", "외국인 (영어 포함)", "부모님 (감성)"])
    with col2:
        genre = st.selectbox("🎭 장르", ["현대 판타지", "전래 동화", "로맨틱 코미디", "미스터리"])

    keywords = st.text_input("소재 입력", key="story_input")
    
    if st.button("✨ 스토리 생성"):
        if not client: st.warning("API Key가 필요합니다.")
        else:
            with st.spinner("작성 중..."):
                prompt = f"주인공: {char['name']}({char['trait']}), 배경: {region}, 타겟: {target}, 장르: {genre}, 소재: {keywords}. 짧은 이야기 써줘."
                resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role":"user", "content":prompt}])
                st.markdown(resp.choices[0].message.content)

# --- [Tab 2] 대화 (글로벌 음성 기능) ---
with tab2:
    st.subheader(f"🎤 {char['name']}와 대화하기")
    
    # [NEW] 언어 선택 기능
    lang_col, _ = st.columns([1, 2])
    with lang_col:
        language = st.radio("언어 선택 (Language)", ["한국어", "English", "日本語", "中文"], horizontal=True)

    st.info(f"💡 {language}로 말을 걸어보세요! 해치가 목소리로 대답합니다.")
    
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    if chat_in := st.chat_input("메시지 입력..."):
        st.session_state.messages.append({"role":"user", "content":chat_in})
        with st.chat_message("user"): st.write(chat_in)
        
        if client:
            with st.spinner(f"{char['name']}가 생각 중..."):
                # 다국어 프롬프트 적용
                sys = f"너는 {region}의 {char['name']}야. 성격: {char['trait']}. 사용자가 선택한 언어인 '{language}'로 대답해. 말투는 친근하고 활기차게(장난꾸러기처럼). 답변은 2~3문장으로 짧게."
                
                resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role":"system", "content":sys}] + st.session_state.messages)
                ai_text = resp.choices[0].message.content
            
            st.session_state.messages.append({"role":"assistant", "content":ai_text})
            with st.chat_message("assistant"):
                st.write(ai_text)
                
                # 음성 생성 (장난꾸러기 톤: nova)
                try:
                    speech_file_path = "speech_output.mp3"
                    response = client.audio.speech.create(
                        model="tts-1",
                        voice="nova",  # [변경] 장난꾸러기 톤
                        input=ai_text
                    )
                    response.stream_to_file(speech_file_path)
                    st.audio(speech_file_path)
                except Exception as e:
                    st.error(f"음성 오류: {e}")

# --- [Tab 3] 이미지 ---
with tab3:
    st.subheader(f"🎨 {char['name']} 이미지 생성")
    style = st.selectbox("스타일", ["3D 애니메이션", "수채화", "웹툰", "실사"])
    desc_input = st.text_input("상황 설명", key="img_input")
    
    if st.button("🖌️ 이미지 만들기"):
        if not client: st.error("API Key가 필요합니다.")
        else:
            with st.spinner("그리는 중..."):
                try:
                    p = f"Cute character '{char['name']}' representing Seoul {region}. Style: {style}. {desc_input}. High quality."
                    res = client.images.generate(model="dall-e-3", prompt=p, size="1024x1024", quality="standard", n=1)
                    st.image(res.data[0].url)
                    st.code(f"저장 파일명: {region}_{char['name']}.png")
                except Exception as e: st.error(f"실패: {e}")
