import streamlit as st
import os
from openai import OpenAI

# -------------------------------------------------------------------------
# [설정] V15: 인포그래픽 & 상세 가이드 에디션 (Final Fix)
# -------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="Seoul Haechis V15")

# -------------------------------------------------------------------------
# [데이터] 25개 자치구 (오류 방지를 위해 정렬 완료)
# -------------------------------------------------------------------------
seoul_db = {
    "종로구": {"name": "초롱해치", "trait": "박학다식", "desc": "경복궁과 서촌의 구석구석을 아는 가이드"},
    "중구": {"name": "쇼퍼해치", "trait": "힙스터", "desc": "을지로(힙지로)와 명동의 맛집 네비게이션"},
    "용산구": {"name": "어텐션해치", "trait": "글로벌", "desc": "이태원과 용리단길의 핫플 전문가"},
    "성동구": {"name": "뚝해치", "trait": "감성적", "desc": "성수동 카페거리와 팝업스토어 알리미"},
    "광진구": {"name": "광나루해치", "trait": "활기참", "desc": "건대 맛의 거리와 한강공원 피크닉 담당"},
    "동대문구": {"name": "한약해치", "trait": "전통적", "desc": "경동시장과 청량리의 숨은 노포 맛집 탐험가"},
    "중랑구": {"name": "장미해치", "trait": "로맨틱", "desc": "서울장미축제와 면목동의 힐링 코스 가이드"},
    "성북구": {"name": "선잠해치", "trait": "예술적", "desc": "성북동 갤러리와 한옥 카페 투어 리더"},
    "강북구": {"name": "북수해치", "trait": "자연친화", "desc": "북한산 둘레길과 4.19 카페거리 가이드"},
    "도봉구": {"name": "호랭해치", "trait": "강인함", "desc": "도봉산 등산 코스와 창동 문화거리 안내원"},
    "노원구": {"name": "태해치", "trait": "교육적", "desc": "경춘선 숲길과 불암산 힐링 타운 지킴이"},
    "은평구": {"name": "진관해치", "trait": "여유로움", "desc": "은평한옥마을과 불광천 산책로 가이드"},
    "서대문구": {"name": "홍지해치", "trait": "젊음", "desc": "신촌 이대 거리와 연희동 맛집 투어"},
    "마포구": {"name": "가수해치", "trait": "열정적", "desc": "홍대 버스킹 거리와 망원시장 투어 대장"},
    "양천구": {"name": "배움해치", "trait": "스마트", "desc": "목동의 학구열과 안양천 자전거길 안내"},
    "강서구": {"name": "강초해치", "trait": "웰빙", "desc": "서울식물원과 마곡 카페거리 큐레이터"},
    "구로구": {"name": "디지털해치", "trait": "미래지향", "desc": "G밸리의 IT단지와 깔깔거리 음식점 안내"},
    "금천구": {"name": "봉제해치", "trait": "패션", "desc": "가산 디지털단지 아울렛 쇼핑 가이드"},
    "영등포구": {"name": "등포해치", "trait": "다채로움", "desc": "여의도 더현대와 문래 창작촌 핫플 담당"},
    "동작구": {"name": "현충해치", "trait": "성실함", "desc": "노량진 컵밥거리와 사육신 공원 안내자"},
    "관악구": {"name": "낙성해치", "trait": "청년", "desc": "샤로수길 맛집과 관악산 등산로 가이드"},
    "서초구": {"name": "법조해치", "trait": "클래식", "desc": "예술의 전당과 반포 한강공원 무지개분수 안내"},
    "강남구": {"name": "패션해치", "trait": "럭셔리", "desc": "가로수길과 코엑스 청담동 명품거리 가이드"},
    "송파구": {"name": "몽촌해치", "trait": "액티브", "desc": "롯데타워와 석촌호수 올림픽공원 데이트 코스"},
    "강동구": {"name": "암사해치", "trait": "역사적", "desc": "암사 유적지와 강풀 만화거리 안내원"}
}

# -------------------------------------------------------------------------
# [UI] 사이드바 & Secrets 연동
# -------------------------------------------------------------------------
with st.sidebar:
    st.title("🎛️ Control Center")
    
    # Secrets 자동 로드
    if "OPENAI_API_KEY" in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
        st.success("🔐 VIP 모드: 가이드 활성화")
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
    region = st.selectbox("어디로 떠나볼까요?", list(seoul_db.keys()))
    char = seoul_db[region]
    
    # 이미지 로딩
    img_path = os.path.join("images", f"{region}_{char['name']}.png")
    if os.path.exists(img_path): st.image(img_path, caption=char['name'])
    
    st.info(f"**저는 {char['desc']}입니다!**")


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
st.markdown(f"<h2 style='text-align: center;'>🦁 {region} AI 로컬 가이드 : {char['name']}</h2>", unsafe_allow_html=True)
st.markdown("---")

# 기능 탭 (V15: 상세 코스 & 지도 이미지 추가)
tab1, tab2, tab3 = st.tabs(["🗺️ 여행 코스 짜기 (상세ver)", "ℹ️ 실시간 안내소 (음성)", "📸 인증샷 만들기"])

# --- [Tab 1] 여행 코스 (정보량 강화 + 지도 이미지) ---
with tab1:
    st.subheader(f"🗺️ {char['name']}의 상세 코스 & 인포그래픽 지도")
    
    col1, col2 = st.columns(2)
    with col1:
        who = st.selectbox("누구와 함께?", ["혼자", "연인과", "친구들과", "아이와 함께", "부모님 모시고"])
    with col2:
        theme = st.selectbox("여행 테마", ["맛집 탐방", "인생샷/카페", "역사/문화", "힐링 산책", "쇼핑/마켓"])

    detail = st.text_input("추가 요청 (예: 3시간 코스, 주차 필수, 매운 거 못 먹음)")
    
    # 결과 저장을 위한 세션 상태 초기화
    if "course_result" not in st.session_state: st.session_state.course_result = ""
    if "map_image_url" not in st.session_state: st.session_state.map_image_url = ""

    # 1. 텍스트 코스 생성 버튼
    if st.button("🚀 상세 코스 브리핑 받기"):
        if not client: st.warning("API Key 확인 필요")
        else:
            with st.spinner(f"{region}의 데이터를 샅샅이 뒤지는 중... (시간이 좀 걸립니다)"):
                try:
                    # [강력해진 프롬프트] 정보량을 늘리기 위한 구체적 지시
                    prompt = f"""
                    당신은 {region}의 전문 가이드 '{char['name']}'입니다.
                    사용자({who}, 테마:{theme}, 요청:{detail})를 위한 {region}의 실제 여행 코스를 아주 상세하게 작성하세요.
                    
                    [필수 포함 내용]
                    1. **코스 요약:** 전체 동선 (장소A -> 장소B -> 장소C)
                    2. **상세 안내 (장소별):**
                       - **장소명 (실제 상호/명소):** - **추천 이유 & 특징:** (왜 이곳이 테마에 맞는지 2~3문장)
                       - **운영 정보:** (대략적인 운영 시간, 휴무일)
                       - **꿀팁:** (사진 포인트, 추천 메뉴, 덜 붐비는 시간 등)
                       - **이동 방법:** (다음 장소까지 도보/교통편 및 소요 시간)
                    3. **마무리 멘트:** {char['trait']} 성격을 살린 인사말.
                    
                    출력 형식은 가독성 좋은 마크다운(Markdown)을 사용하고, 적절한 이모지를 많이 넣으세요.
                    """
                    resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role":"user", "content":prompt}])
                    st.session_state.course_result = resp.choices[0].message.content
                    st.session_state.map_image_url = "" # 새 코스 생성 시 기존 지도 초기화
                except Exception as e:
                    st.error(f"오류 발생: {e}")

    # 생성된 텍스트 결과 표시
    if st.session_state.course_result:
        st.markdown(st.session_state.course_result)
        st.markdown("---")
        st.subheader("🗺️ 이 코스를 지도로 보기")

        # 2. 지도 이미지 생성 버튼 (텍스트 결과가 있을 때만 표시)
        if st.button("🎨 AI 인포그래픽 지도 그리기"):
            if not client: st.warning("API Key 필요")
            else:
                with st.spinner("AI 화가가 코스를 지도로 그리는 중..."):
                    try:
                        # 텍스트 코스를 요약해서 그림 프롬프트로 사용
                        summary_prompt = f"Summarize this travel course in Seoul {region} into a list of locations for a map drawing: {st.session_state.course_result[:500]}"
                        summary_resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role":"user", "content":summary_prompt}])
                        locations = summary_resp.choices[0].message.content

                        # 이미지 생성 프롬프트
                        image_prompt = f"A cute, illustrated tourist map infographic of Seoul {region}. It clearly shows a path connecting these locations: {locations}. The style is friendly, colorful, with small icons for each spot and a character '{char['name']}' guiding the way. High quality, poster design."
                        
                        res = client.images.generate(model="dall-e-3", prompt=image_prompt, size="1024x1024", quality="standard", n=1)
                        st.session_state.map_image_url = res.data[0].url
                    except Exception as e:
                        st.error(f"지도 생성 실패: {e}")

    # 생성된 지도 이미지 표시
    if st.session_state.map_image_url:
        st.image(st.session_state.map_image_url, caption=f"{region} 여행 코스 인포그래픽")


# --- [Tab 2] 실시간 안내소 (글로벌 음성) ---
with tab2:
    st.subheader(f"🎤 {char['name']}에게 물어보세요")
    
    # 언어 선택
    lang_col, _ = st.columns([1, 2])
    with lang_col:
        language = st.radio("Language", ["한국어", "English", "日本語", "中文"], horizontal=True)

    st.write(f"💡 예시: '{region}에서 가장 유명한 빵집이 어디야?', '지금 가볼 만한 축제 있어?'")
    
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    if chat_in := st.chat_input("질문 입력..."):
        st.session_state.messages.append({"role":"user", "content":chat_in})
        with st.chat_message("user"): st.write(chat_in)
        
        if client:
            with st.spinner("정보 찾는 중..."):
                sys = f"""
                너는 {region}의 관광 홍보 주무관 '{char['name']}'야. 
                사용자 언어: {language}. 
                목소리 톤: {char['trait']}하고 활기참.
                역할: {region}의 역사, 문화, 관광지 정보를 정확하게 전달하는 것. 
                모르는 내용은 지어내지 말고 솔직하게 안내소에 문의하라고 할 것.
                답변 길이: 3문장 이내.
                """
                resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role":"system", "content":sys}] + st.session_state.messages)
                ai_text = resp.choices[0].message.content
            
            st.session_state.messages.append({"role":"assistant", "content":ai_text})
            with st.chat_message("assistant"):
                st.write(ai_text)
                try:
                    speech_file_path = "speech_output.mp3"
                    response = client.audio.speech.create(
                        model="tts-1",
                        voice="nova", 
                        input=ai_text
                    )
                    response.stream_to_file(speech_file_path)
                    st.audio(speech_file_path)
                except: pass

# --- [Tab 3] 인증샷 (V14 유지) ---
with tab3:
    st.subheader(f"📸 {char['name']}와 함께 찰칵")
    st.write("여행의 추억을 AI 그림으로 남겨보세요.")
    style = st.selectbox("화풍 선택", ["웹툰 스타일", "수채화", "실사 풍경", "3D 캐릭터"])
    desc_input = st.text_input("상황 설명 (예: 경복궁 앞에서 한복 입고 브이 하는 모습)", key="img_input")
    
    if st.button("🖌️ 기념사진 생성"):
        if not client: st.error("API Key 필요")
        else:
            with st.spinner("사진 인화 중..."):
                try:
                    p = f"Character '{char['name']}' in Seoul {region}, {desc_input}. Style: {style}. High quality, tourism poster vibe."
                    res = client.images.generate(model="dall-e-3", prompt=p, size="1024x1024", quality="standard", n=1)
                    st.image(res.data[0].url)
                except Exception as e: st.error(f"실패: {e}")
