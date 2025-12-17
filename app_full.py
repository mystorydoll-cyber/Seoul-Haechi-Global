import streamlit as st
import os
from openai import OpenAI

# -------------------------------------------------------------------------
# [설정] V21: 미식가 해치 에디션 (맛집 탭 독립)
# -------------------------------------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="해치의 AI 여행 라운지",
    page_icon="🦁",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------
# [데이터] 25개 자치구
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
# [UI] 사이드바
# -------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🦁 해치의 AI 여행 라운지")
    st.caption("Haechi's AI Travel Lounge")
    st.markdown("---")
    
    if "OPENAI_API_KEY" in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
        st.success("🔐 VIP 모드: 가이드 활성화됨")
    else:
        api_key = st.text_input("OpenAI API Key", type="password")
        
    client = OpenAI(api_key=api_key) if api_key else None
    
    st.markdown("---")
    
    st.markdown("### 📍 지역 선택")
    region = st.selectbox("어디로 떠나볼까요?", list(seoul_db.keys()), label_visibility="collapsed")
    char = seoul_db[region]
    
    st.markdown("---")
    
    with st.container(border=True):
        st.markdown(f"### 🦁 {char['name']}")
        st.caption(f"성격: {char['trait']} | 상태: 🟢 실시간 활동 중")
        
        gif_path = os.path.join("images", f"{region}_{char['name']}.gif")
        png_path = os.path.join("images", f"{region}_{char['name']}.png")
        
        if os.path.exists(gif_path):
            st.image(gif_path, use_column_width=True)
        elif os.path.exists(png_path):
            st.image(png_path, use_column_width=True)
        else:
            st.info("📸 이미지 준비 중...")
        
        st.info(f"Bot: \"{char['desc']}\"")


# -------------------------------------------------------------------------
# [메인] 화면 구성
# -------------------------------------------------------------------------
st.markdown("# 🇰🇷 서울 해치: 당신만의 AI 로컬 가이드")
st.markdown("### Seoul Haechi: Your Personal AI Local Guide")
st.markdown("---")

local_video_path = "images/intro_video.mp4" 
youtube_url = "https://youtu.be/YIpxEgUCpmA" 

if os.path.exists(local_video_path):
    st.video(local_video_path, autoplay=True, muted=True, loop=True)
else:
    try:
        st.video(youtube_url, autoplay=True, muted=True, loop=True)
    except:
        pass

st.markdown("---")
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.markdown(f"## 🚩 지금 우리는 : **서울시 {region}**")
    st.write(f"{region}의 숨은 매력을 {char['name']}와 함께 발견해보세요.")
with col_h2:
    with st.container(border=True):
        st.metric(label="현재 라운지 상태", value="OPEN 🟢")

st.markdown("---")

# [V21 핵심] 탭을 4개로 확장 (맛집 탭 독립)
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ 여행 코스", "🍽️ 찐맛집 추천", "🎤 안내소 (음성)", "📸 인증샷"])

# --- [Tab 1] 여행 코스 ---
with tab1:
    st.subheader(f"🗺️ {char['name']}의 상세 코스 & 인포그래픽 지도")
    col1, col2 = st.columns(2)
    with col1: who = st.selectbox("누구와 함께?", ["혼자", "연인과", "친구들과", "아이와 함께", "부모님 모시고"])
    with col2: theme = st.selectbox("여행 테마", ["감성 카페 투어", "역사/문화 탐방", "힐링 산책", "쇼핑/마켓", "야경 투어"]) # 맛집 제거(독립)

    detail = st.text_input("추가 요청 (예: 3시간 코스, 주차 필수)", key="course_in")
    
    if "course_result" not in st.session_state: st.session_state.course_result = ""
    if "map_image_url" not in st.session_state: st.session_state.map_image_url = ""

    if st.button("🚀 상세 코스 브리핑 받기", type="primary"):
        if not client: st.warning("API Key 확인 필요")
        else:
            with st.spinner(f"{region} 데이터를 분석 중입니다..."):
                try:
                    prompt = f"당신은 {region} 가이드 '{char['name']}'. 사용자({who}, 테마:{theme}, 요청:{detail})를 위한 코스 작성. 1.코스요약 2.상세안내 3.마무리멘트. 형식:Markdown."
                    resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role":"user", "content":prompt}])
                    st.session_state.course_result = resp.choices[0].message.content
                    st.session_state.map_image_url = "" 
                except Exception as e: st.error(f"오류: {e}")

    if st.session_state.course_result:
        st.markdown(st.session_state.course_result)
        st.markdown("---")
        st.subheader("🗺️ 이 코스를 지도로 보기")
        if st.button("🎨 AI 인포그래픽 지도 그리기"):
            if not client: st.warning("API Key 필요")
            else:
                with st.spinner("AI 화가가 지도를 그리는 중..."):
                    try:
                        summary_prompt = f"Summarize course in {region}: {st.session_state.course_result[:500]}"
                        summary_resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role":"user", "content":summary_prompt}])
                        locations = summary_resp.choices[0].message.content
                        image_prompt = f"Cute tourist map infographic of Seoul {region}. Locations: {locations}. Character '{char['name']}'. Clear text labels. High quality."
                        res = client.images.generate(model="dall-e-3", prompt=image_prompt, size="1024x1024", quality="standard", n=1)
                        st.session_state.map_image_url = res.data[0].url
                    except: st.error("지도 실패")

    if st.session_state.map_image_url:
        st.image(st.session_state.map_image_url, caption=f"{region} 여행 지도")

# --- [Tab 2] 찐맛집 추천 (신규 독립!) ---
with tab2:
    st.subheader(f"🍽️ {char['name']}가 보증하는 {region} 맛집")
    st.caption("현지인만 아는 숨은 맛집부터 핫플레이스까지!")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1: food_type = st.selectbox("음식 종류", ["한식 (노포/전통)", "양식 (파스타/스테이크)", "일식/아시아", "디저트/카페", "술집/바"])
    with col_f2: vibe = st.selectbox("선호하는 분위기", ["가성비 최고", "분위기 깡패", "조용한/룸", "뷰가 좋은", "회식/모임"])
    
    food_detail = st.text_input("먹고 싶은 메뉴나 상황 (예: 매운 떡볶이, 비오는 날 파전)", key="food_in")
    
    if st.button("🍴 맛집 리스트업", type="primary"):
        if not client: st.warning("API Key 필요")
        else:
            with st.spinner(f"{region} 골목골목 맛집 스캔 중..."):
                try:
                    # 맛집 전용 프롬프트
                    prompt = f"""
                    당신은 {region}의 미식가 '{char['name']}'입니다.
                    사용자({food_type}, {vibe}, {food_detail})에게 딱 맞는 {region}의 **실제 맛집 3곳**을 추천해주세요.
                    
                    [출력 양식]
                    1. **식당 이름 (실제 상호명)**
                       - 🥘 **추천 메뉴:** (가격대 포함)
                       - 💡 **특징:** (왜 추천하는지, 분위기 등)
                       - 📍 **위치 힌트:** (예: OOO역 3번 출구 근처)
                    
                    마지막에는 '{char['trait']}' 말투로 "맛있게 먹어!"라고 인사해줘.
                    """
                    resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role":"user", "content":prompt}])
                    st.markdown(resp.choices[0].message.content)
                except Exception as e: st.error(f"오류: {e}")

# --- [Tab 3] 실시간 안내소 ---
with tab3:
    st.subheader(f"🎤 {char['name']}에게 물어보세요")
    lang_col, _ = st.columns([1, 2])
    with lang_col: language = st.radio("Language", ["한국어", "English", "日本語", "中文"], horizontal=True)
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages: with st.chat_message(m["role"]): st.write(m["content"])
    if chat_in := st.chat_input("질문 입력..."):
        st.session_state.messages.append({"role":"user", "content":chat_in})
        with st.chat_message("user"): st.write(chat_in)
        if client:
            with st.spinner("생각 중..."):
                sys = f"너는 {region} 가이드 '{char['name']}'. 언어:{language}. 톤:{char['trait']}하고 활기참."
                resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role":"system", "content":sys}] + st.session_state.messages)
                ai_text = resp.choices[0].message.content
            st.session_state.messages.append({"role":"assistant", "content":ai_text})
            with st.chat_message("assistant"):
                st.write(ai_text)
                try:
                    response = client.audio.speech.create(model="tts-1", voice="nova", input=ai_text)
                    response.stream_to_file("speech.mp3")
                    st.audio("speech.mp3")
                except: pass

# --- [Tab 4] 인증샷 ---
with tab4:
    st.subheader(f"📸 {char['name']}와 함께 찰칵")
    style = st.selectbox("화풍 선택", ["웹툰 스타일", "수채화", "실사 풍경", "3D 캐릭터"])
    desc_input = st.text_input("상황 설명", key="img_input")
    if st.button("🖌️ 기념사진 생성", type="primary"):
        if not client: st.error("API Key 필요")
        else:
            with st.spinner("사진 인화 중..."):
                try:
                    p = f"Character '{char['name']}' in Seoul {region}, {desc_input}. Style: {style}."
                    res = client.images.generate(model="dall-e-3", prompt=p, size="1024x1024", quality="standard", n=1)
                    st.image(res.data[0].url)
                except Exception as e: st.error(f"실패: {e}")

# 푸터
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>ⓒ 2024 Seoul AI Local Docent Platform. Powered by M-Unit & OpenAI.</div>", unsafe_allow_html=True)
