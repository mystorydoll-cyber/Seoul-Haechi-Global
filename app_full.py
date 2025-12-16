import streamlit as st
import os
from openai import OpenAI

# -------------------------------------------------------------------------
# [설정] V18: 프리미엄 UI 에디션 (디자인 및 레이아웃 강화)
# -------------------------------------------------------------------------
# [디자인 개선 1] 브라우저 탭 아이콘과 제목을 그럴싸하게 변경
st.set_page_config(
    layout="wide",
    page_title="서울 해치: AI 로컬 도슨트 플랫폼",
    page_icon="🏛️",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------
# [데이터] 25개 자치구 (V16/V17과 동일)
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
# [UI] 사이드바 (디자인 개선)
# -------------------------------------------------------------------------
with st.sidebar:
    # [디자인 개선 2] 사이드바 헤더를 좀 더 있어 보이게
    st.markdown("## 🏛️ AI 로컬 도슨트 관제센터")
    st.caption("Seoul AI Local Docent Platform")
    st.markdown("---")
    
    if "OPENAI_API_KEY" in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
        st.success("🔐 VIP 모드: 가이드 활성화됨")
    else:
        api_key = st.text_input("OpenAI API Key", type="password")
        st.warning("🔑 키를 입력해주세요.")
        
    client = OpenAI(api_key=api_key) if api_key else None
    st.markdown("---")
    
    # 지역 선택 강조
    st.markdown("### 📍 지역 선택")
    region = st.selectbox("어디로 떠나볼까요?", list(seoul_db.keys()), label_visibility="collapsed")
    char = seoul_db[region]
    
    st.markdown("---")
    
    # [디자인 개선 3] 캐릭터 프로필 카드화
    with st.container(border=True):
        st.markdown(f"### 🦁 {char['name']}")
        st.caption(f"성격: {char['trait']} | 상태: 🟢 실시간 활동 중")
        
        # [이미지/GIF 로딩 로직 - V16 유지]
        gif_path = os.path.join("images", f"{region}_{char['name']}.gif")
        png_path = os.path.join("images", f"{region}_{char['name']}.png")
        
        if os.path.exists(gif_path):
            st.image(gif_path
