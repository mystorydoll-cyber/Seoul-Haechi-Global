import streamlit as st
import os
from openai import OpenAI

# -------------------------------------------------------------------------
# [설정] V15: 인포그래픽 & 상세 가이드 에디션 (정보량 증대 및 지도 시각화)
# -------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="Seoul Haechis V15")

# -------------------------------------------------------------------------
# [데이터] 25개 자치구
# -------------------------------------------------------------------------
# (이전 데이터와 동일하여 생략합니다. 기존 코드를 유지하거나 V14의 seoul_db를 그대로 사용하세요.)
# ... (V14와 동일한 seoul_db 코드가 여기에 들어갑니다) ...
seoul_db = {
    "종로구": {"name": "초롱해치", "trait": "박학다식", "desc": "경복궁과 서촌의 구석구석을 아는 가이드"},
    "중구": {"name": "쇼퍼해치", "trait": "힙스터", "desc": "을지로(힙지로)와 명동의 맛집 네비게이션"},
    # ... (나머지 구 데이터는 V14 코드에서 그대로 복사해서 사용해주세요) ...
}
# (※ 편의상 전체 데이터를 생략했습니다. 실제 적용 시에는 V14의 seoul_db 전체를 꼭 넣어야 합니다!)


# -------------------------------------------------------------------------
# [UI] 사이드바 & Secrets 연동
# -------------------------------------------------------------------------
with st.sidebar:
    st.title("🎛️ Control Center")
    if "OPENAI_API_KEY" in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
        st.success("🔐 VIP 모드: 가이드 활성화")
    else:
        api_key = st.text_input("OpenAI API Key", type="password")
    client = OpenAI(api_key=api_key) if api_key else None
    st.markdown("---")
    # 안전한 키 참조를 위해 get 사용
    region = st.selectbox("어디로 떠나볼까요?", list(seoul_db.keys()) if seoul_db else ["데이터 없음"])
    
    if seoul_db and region in seoul_db:
        char = seoul_db[region]
        img_path = os.path.join("images", f"{region}_{char['name']}.png")
        if os.path.exists(img_path): st.image(img_path, caption=char['name'])
        st.info(f"**저는 {char['desc']}입니다!**")
    else:
        char = {"name": "오류 해치", "trait": "없음"} # 임시 처리

# -------------------------------------------------------------------------
# [메인] 화면 구성
# -------------------------------------------------------------------------
youtube_url = "https://youtu.be/YIpxEgUCpmA" 
try: st.video(youtube_url, autoplay=True, muted=True, loop=True)
except: pass

st.markdown(f"<h2 style='text-align: center;'>🦁 {region} AI 로컬 가이드 : {char['name']}</h2>", unsafe_allow_html=True)
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🗺️ 여행 코스 짜기 (상세ver)", "ℹ️ 실시간 안내소 (음성)", "📸 인증샷 만들기"])

# --- [Tab 1] 여행 코스 (정보량 강화 + 지도 이미지) ---
with tab1:
    st.subheader(f"🗺️ {char['name']}의 상세 코스 & 인포그래픽 지도")
    
    col1, col2 = st.columns(2)
    with col1: who = st.selectbox("누구와 함께?", ["혼자", "연인과", "친구들과", "아이와 함께", "부모님 모시고"])
    with col2: theme = st.selectbox("여행 테마", ["맛집 탐방", "인생샷/카페", "역사/문화", "힐링 산책", "쇼핑/마켓"])
    detail = st.text_input("추가 요청 (예: 3시간 코스, 주차 필수, 매운 거 못 먹음)")
    
    # 결과 저장을 위한 세션 상태 초기화
    if "course_result" not in st.session_state: st.session_state.course_result = ""
    if "map_image_url" not in st.session_state: st.session_state.map_image_url = ""

    # 1. 텍스트 코스 생성 버튼
    if st.button("🚀 상세 코스 브리핑 받기"):
        if not client: st.warning("API Key 확인 필요")
        else:
            with st.spinner(f"{region}의 데이터를 샅샅이 뒤지는 중... (시간이 좀 걸립니다)"):
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
                        st.error(f
