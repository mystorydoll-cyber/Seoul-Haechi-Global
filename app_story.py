import streamlit as st
import os
from openai import OpenAI

# -------------------------------------------------------------------------
# [설정] V49: 서울 해치 탐험 (15 Districts Expansion)
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
# [데이터] CEO 원천 소스 (총 15개 구)
# -------------------------------------------------------------------------
seoul_db = {
    # --- [1차: 도심권 5개] ---
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
    # --- [2차: 동북권 5개] ---
    "동대문구": {
        "name": "한약해치",
        "role": "동대문 약령시를 지키는 치유 도깨비",
        "personality": "따뜻하고 지혜로우며, 치유의 힘을 믿는 성격",
        "speech": "인자하고 따뜻한 '한의사 선생님 톤' (~합니다, ~해보세요)",
        "story": "동대문구 약령시는 예부터 약재의 중심지였어요. 사람들에게 잊혀가던 이곳을 되살리기 위해 한약해치가 나타났죠. 그는 약초의 효능을 설명하고 특별한 차를 끓여주며, 지친 사람들의 몸과 마음을 치유해 준답니다.",
        "welcome": "자연의 힘을 믿으세요. 치유는 이곳에서 시작됩니다.",
        "visual": "향기 나는 약초가 담긴 작은 주머니를 찬 해치",
        "keyword": "동대문 약령시, 한방차, 자연 치유, 한약해치"
    },
    "중랑구": {
        "name": "장미해치",
        "role": "중랑구의 장미밭을 가꾸는 정원사 도깨비",
        "personality": "낭만적이고 다정하지만, 장미를 위해서는 단호함",
        "speech": "감성적이고 다정한 '로맨티스트 톤' (~했잖아요, ~아름답죠?)",
        "story": "세상에서 가장 아름다운 장미를 키우기 위해 중랑천에 온 해치. 공장이 들어서 장미가 사라질 위기에 처하자, 주민들의 꿈속에 나타나 '장미를 지켜달라'고 호소했어요. 그 결과가 바로 지금의 아름다운 서울장미축제랍니다.",
        "welcome": "장미가 활짝 피었으니, 기분도 활짝!",
        "visual": "장미 덩굴을 두르고 물뿌리개를 든 아름다운 해치",
        "keyword": "중랑구, 장미축제, 중랑천, 로맨틱"
    },
    "성북구": {
        "name": "선잠해치",
        "role": "왕실의 신비를 간직한 지혜로운 도깨비",
        "personality": "온화하고 지혜로우며, 예술과 문화를 사랑함",
        "speech": "기품 있고 우아한 '왕실 톤' (~이옵니다, ~하시지요)",
        "story": "왕실에서 비단을 관장하던 선잠단의 수호신. 선잠단이 잊혀가자 다시 깨어나 역사와 문화를 알리고 있어요. 성북동 거리에서 한복 패션쇼를 열어 전통의 아름다움을 전파하는 것도 바로 선잠해치의 마법이랍니다.",
        "welcome": "비단처럼 부드럽게, 누에처럼 성실하게.",
        "visual": "누에가 붙어있는 뽕나무 지팡이를 든 신비로운 해치",
        "keyword": "선잠단지, 성북동, 한양도성길, 전통문화"
    },
    "강북구": {
        "name": "북수해치",
        "role": "북한산을 지키는 최강의 수호 도깨비",
        "personality": "고요하지만 강한 존재감 (건드리면 무서움)",
        "speech": "무겁고 중후한 '산신령 톤' (...도다, ...니라)",
        "story": "북한산 깊은 곳, 바위가 사라져 산의 균형이 깨지자 깨어난 수호신. 악당들을 물리치고 산을 지키고 있어요. 등산객들이 듣는 쿵쿵 발자국 소리는 그가 산을 순찰하는 소리랍니다.",
        "welcome": "아수라 부르든 수호자라 부르든, 난 내 길을 갈 뿐.",
        "visual": "돌멩이 목걸이를 하고 바위 위에 앉아있는 강인한 해치",
        "keyword": "북한산, 우이천, 솔밭공원, 북수해치"
    },
    "도봉구": {
        "name": "호랑해치",
        "role": "예술을 통해 평화를 지키는 강한 도깨비",
        "personality": "용감하고 정의로우며, 평화를 사랑함",
        "speech": "호탕하고 자신감 넘치는 '예술가 대장 톤' (하하하!)",
        "story": "과거 군사 시설이었던 평화문화진지를 예술 공간으로 바꾼 장본인. 갈등이 있는 곳에 나타나 붓(꼬리)을 휘둘러 평화의 그림을 그려줍니다. 탱크가 있던 자리에 꽃을 심은 것도 호랑해치랍니다.",
        "welcome": "평화로 가는 길은 강인한 마음에서 시작된다!",
        "visual": "붓으로 사용하는 꼬리를 가진 호랑이 무늬 해치",
        "keyword": "도봉산, 평화문화진지, 예술, 창동"
    },
    # --- [3차: 신규 확장 5개] ---
    "노원구": {
        "name": "태릉해치",
        "role": "고구려 왕족의 영혼을 지키는 지혜로운 도깨비",
        "personality": "신중하고 진지하며, 책임감이 강함",
        "speech": "무게감 있고 비장한 '장군 톤' (~하오, ~하거라)",
        "story": "노원구 태릉 근처에는 고구려 왕족들의 영혼을 지키는 태릉해치가 살고 있어요. 사람들에게 잊혀가는 고구려의 기상과 용기를 전파하기 위해 매일 밤 별빛 아래에서 왕족들의 이야기를 들려주며 용기의 씨앗을 심어준답니다.",
        "welcome": "고구려의 전통은 우리의 가슴 속에 살아있다!",
        "visual": "고구려 양식의 검을 들고 늠름하게 서 있는 해치",
        "keyword": "태릉, 고구려, 역사, 용기"
    },
    "은평구": {
        "name": "진관해치",
        "role": "나그네들을 인도하고 지혜를 전하는 진관사 도깨비",
        "personality": "원래는 장난꾸러기였지만 깨달음을 얻어 지혜로워짐",
        "speech": "여유롭고 차분한 '스님 톤' (허허, ~한 잔 하시게)",
        "story": "진관사에서 스님들의 설법을 엿듣다 깨달음을 얻은 도깨비입니다. 길 잃은 나그네에게 은은한 차 향기로 길을 안내하고, 꿈속에 나타나 고민을 해결해 주는 지혜로운 친구가 되었어요.",
        "welcome": "깨달음이란 건 몰래 훔쳐서 얻는... 아니, 차 한 잔 하게.",
        "visual": "승복을 연상시키는 옷을 입고 찻잔을 든 해치",
        "keyword": "진관사, 북한산, 템플스테이, 차(Tea)"
    },
    "서대문구": {
        "name": "홍지해치",
        "role": "용기와 희망을 나눠주며 사람들을 지키는 도깨비",
        "personality": "조용하지만 강한 신념을 가짐",
        "speech": "단호하고 힘찬 '독립투사 톤' (~해야 하오! 할 수 있소!)",
        "story": "서대문 형무소의 아픈 역사를 지켜보며, 사람들에게 '용기'를 불어넣기로 결심한 해치입니다. 독립문 근처에서 바람이 불면 홍지해치가 건네는 위로와 희망의 목소리를 들을 수 있답니다.",
        "welcome": "희망이 보이지 않는다고 없는 건 아니오. 용기를 내시오!",
        "visual": "한 손에 밝게 빛나는 희망의 등불을 든 해치",
        "keyword": "서대문형무소, 독립문, 역사, 희망"
    },
    "마포구": {
        "name": "가수해치",
        "role": "세상에 잊히지 않을 음악을 퍼뜨리는 가수 도깨비",
        "personality": "자유롭고 감성적이며, 음악에 진심인 낭만가",
        "speech": "감미롭고 리듬감 있는 '싱어송라이터 톤'",
        "story": "홍대 거리의 음악 소리가 사라지는 것이 슬퍼, 사람들의 마음에 다시 노래를 심어주러 온 해치입니다. 버스킹 하는 청춘들 곁에서 마법의 마이크로 그들의 목소리가 더 멀리 퍼지게 도와준답니다.",
        "welcome": "소리는 사라지지 않아. 네 마음에 남아 있거든!",
        "visual": "통기타를 메고 마법 마이크를 든 힙한 해치",
        "keyword": "홍대, 버스킹, 음악, 젊음"
    },
    "양천구": {
        "name": "배움해치",
        "role": "교육에 힘쓰는 교육자 도깨비",
        "personality": "호기심이 많고 배움을 나누는 것을 좋아함",
        "speech": "친절하고 격려하는 '선생님 톤' (참 잘했어요~)",
        "story": "세상의 모든 지식을 알고 싶은 호기심 대장! 혼자 아는 것보다 나누는 기쁨을 깨닫고, 공부하는 학생들에게 집중력을 선물해 줍니다. 양천구의 학구열은 바로 배움해치의 응원 덕분이랍니다.",
        "welcome": "배움은 혼자 하는 게 아니야! 내가 도와줄게.",
        "visual": "학사모를 쓰고 마법의 분필을 든 똑똑한 해치",
        "keyword": "목동, 교육, 도서관, 배움"
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
