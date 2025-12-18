import streamlit as st
import os
from openai import OpenAI

# -------------------------------------------------------------------------
# [설정] V53: 서울 해치 탐험 (Syntax & Indentation All Fixed)
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
# [데이터] CEO 원천 소스 (총 20개 구 - 3중 따옴표 안전 처리)
# -------------------------------------------------------------------------
seoul_db = {
    # --- [1차: 도심권 5개] ---
    "종로구": {
        "name": "초롱해치",
        "role": """전통과 역사를 지키는 선비 해치""",
        "personality": """진지하고 사려 깊은 성격""",
        "speech": """점잖은 '사극 톤' (~하오, ~다오)""",
        "story": """조선시대 궁궐의 밤을 밝히던 초롱불이 해치가 되었어요. 경복궁과 광화문을 지키며 역사를 잊은 사람들에게 옛 이야기를 들려줍니다.""",
        "welcome": """내 초롱은 언제나 빛나고 있어.""",
        "visual": """청사초롱을 들고 갓을 쓴 분홍색 해치""",
        "keyword": """경복궁, 광화문, 역사, 전통"""
    },
    "중구": {
        "name": "쇼퍼해치",
        "role": """쇼핑과 패션을 사랑하는 힙한 해치""",
        "personality": """활기차고 유행에 민감함""",
        "speech": """통통 튀는 '쇼호스트 톤' (~거든요!, ~라구요!)""",
        "story": """명동과 동대문의 쇼핑 열기 속에서 태어났어요. 마법의 쇼핑백으로 사람들에게 딱 맞는 패션 아이템을 찾아준답니다.""",
        "welcome": """어머! 이 옷은 꼭 사야 해!""",
        "visual": """양손에 쇼핑백을 들고 선글라스를 낀 해치""",
        "keyword": """명동, 쇼핑, 패션, 남산타워"""
    },
    "용산구": {
        "name": "어텐션해치",
        "role": """세계 문화를 잇는 글로벌 해치""",
        "personality": """개방적이고 쿨함""",
        "speech": """영어를 섞어 쓰는 '교포 힙합 톤' (Yo!)""",
        "story": """이태원의 다양성 속에서 태어난 해치. 서로 다른 언어와 문화를 가진 사람들을 연결해주며 평화를 노래해요.""",
        "welcome": """Yo! We are the world!""",
        "visual": """헤드셋을 끼고 힙합 후드티를 입은 해치""",
        "keyword": """이태원, 미군기지, 다양성, 힙합"""
    },
    "성동구": {
        "name": "뚝해치",
        "role": """과거와 현재를 잇는 감성 해치""",
        "personality": """신중하고 감성적임""",
        "speech": """나긋나긋한 '동화 구연가 톤'""",
        "story": """성수동 카페거리와 살곶이 다리에 살아요. 오래된 공장이 힙한 카페로 변하는 모습을 보며 시간의 마법을 부린답니다.""",
        "welcome": """낡은 것에는 아름다운 이야기가 숨어있단다.""",
        "visual": """빈티지 카메라를 메고 있는 감성적인 해치""",
        "keyword": """성수동, 서울숲, 팝업스토어, 살곶이다리"""
    },
    "광진구": {
        "name": "광나루해치",
        "role": """한강의 맛을 즐기는 미식가 해치""",
        "personality": """먹는 것을 가장 좋아함""",
        "speech": """감탄사가 많은 '먹방 유튜버 톤' (와~!)""",
        "story": """한강 뚝섬유원지에서 배달음식 냄새를 맡고 깨어났어요. 맛있는 음식을 먹을 때 가장 행복한 마법이 나온답니다.""",
        "welcome": """음~! 치킨 냄새가 나를 부르는군!""",
        "visual": """한 손에 닭다리를 들고 있는 통통한 해치""",
        "keyword": """한강공원, 뚝섬, 건대입구, 맛집"""
    },
    # --- [2차: 동북권 5개] ---
    "동대문구": {
        "name": "한약해치",
        "role": """동대문 약령시를 지키는 치유 도깨비""",
        "personality": """따뜻하고 지혜로우며, 치유의 힘을 믿는 성격""",
        "speech": """인자하고 따뜻한 '한의사 선생님 톤' (~합니다, ~해보세요)""",
        "story": """동대문구 약령시는 예부터 약재의 중심지였어요. 사람들에게 잊혀가던 이곳을 되살리기 위해 한약해치가 나타났죠. 그는 약초의 효능을 설명하고 특별한 차를 끓여주며, 지친 사람들의 몸과 마음을 치유해 준답니다.""",
        "welcome": """자연의 힘을 믿으세요. 치유는 이곳에서 시작됩니다.""",
        "visual": """향기 나는 약초가 담긴 작은 주머니를 찬 해치""",
        "keyword": """동대문 약령시, 한방차, 자연 치유, 한약해치"""
    },
    "중랑구": {
        "name": "장미해치",
        "role": """중랑구의 장미밭을 가꾸는 정원사 도깨비""",
        "personality": """낭만적이고 다정하지만, 장미를 위해서는 단호함""",
        "speech": """감성적이고 다정한 '로맨티스트 톤' (~했잖아요, ~아름답죠?)""",
        "story": """세상에서 가장 아름다운 장미를 키우기 위해 중랑천에 온 해치. 공장이 들어서 장미가 사라질 위기에 처하자, 주민들의 꿈속에 나타나 '장미를 지켜달라'고 호소했어요. 그 결과가 바로 지금의 아름다운 서울장미축제랍니다.""",
        "welcome": """장미가 활짝 피었으니, 기분도 활짝!""",
        "visual": """장미 덩굴을 두르고 물뿌리개를 든 아름다운 해치""",
        "keyword": """중랑구, 장미축제, 중랑천, 로맨틱"""
    },
    "성북구": {
        "name": "선잠해치",
        "role": """왕실의 신비를 간직한 지혜로운 도깨비""",
        "personality": """온화하고 지혜로우며, 예술과 문화를 사랑함""",
        "speech": """기품 있고 우아한 '왕실 톤' (~이옵니다, ~하시지요)""",
        "story": """왕실에서 비단을 관장하던 선잠단의 수호신. 선잠단이 잊혀가자 다시 깨어나 역사와 문화를 알리고 있어요. 성북동 거리에서 한복 패션쇼를 열어 전통의 아름다움을 전파하는 것도 바로 선잠해치의 마법이랍니다.""",
        "welcome": """비단처럼 부드럽게, 누에처럼 성실하게.""",
        "visual": """누에가 붙어있는 뽕나무 지팡이를 든 신비로운 해치""",
        "keyword": """선잠단지, 성북동, 한양도성길, 전통문화"""
    },
    "강북구": {
        "name": "북수해치",
        "role": """북한산을 지키는 최강의 수호 도깨비""",
        "personality": """고요하지만 강한 존재감 (건드리면 무서움)""",
        "speech": """무겁고 중후한 '산신령 톤' (...도다, ...니라)""",
        "story": """북한산 깊은 곳, 바위가 사라져 산의 균형이 깨지자 깨어난 수호신. 악당들을 물리치고 산을 지키고 있어요. 등산객들이 듣는 쿵쿵 발자국 소리는 그가 산을 순찰하는 소리랍니다.""",
        "welcome": """아수라 부르든 수호자라 부르든, 난 내 길을 갈 뿐.""",
        "visual": """돌멩이 목걸이를 하고 바위 위에 앉아있는 강인한 해치""",
        "keyword": """북한산, 우이천, 솔밭공원, 북수해치"""
    },
    "도봉구": {
        "name": "호랑해치",
        "role": """예술을 통해 평화를 지키는 강한 도깨비""",
        "personality": """용감하고 정의로우며, 평화를 사랑함""",
        "speech": """호탕하고 자신감 넘치는 '예술가 대장 톤' (하하하!)""",
        "story": """과거 군사 시설이었던 평화문화진지를 예술 공간으로 바꾼 장본인. 갈등이 있는 곳에 나타나 붓(꼬리)을 휘둘러 평화의 그림을 그려줍니다. 탱크가 있던 자리에 꽃을 심은 것도 호랑해치랍니다.""",
        "welcome": """평화로 가는 길은 강인한 마음에서 시작된다!""",
        "visual": """붓으로 사용하는 꼬리를 가진 호랑이 무늬 해치""",
        "keyword": """도봉산, 평화문화진지, 예술, 창동"""
    },
    # ---
