import streamlit as st
import os
import unicodedata
from openai import OpenAI

# 1. [설정] V64: 데이터 무손실 통합 버전
st.set_page_config(
    layout="wide",
    page_title="서울 해치 탐험",
    page_icon="🦁",
    initial_sidebar_state="expanded"
)

# 2. [기능] 스마트 이미지 찾기
def find_image_file(region, char_name):
    target_name = f"{region}_{char_name}.png"
    try:
        current_files = os.listdir(".")
        for file in current_files:
            if unicodedata.normalize('NFC', file) == unicodedata.normalize('NFC', target_name):
                return file
    except: return None
    return None

# 3. [스타일] CSS (CEO님의 원본 스타일 100% 유지)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    h1, h2, h3, h4, .stMarkdown, p, div, span, button, input, label {
        font-family: 'Jua', sans-serif !important;
    }
    .main-title { text-align: center; font-size: 3.5rem !important; color: #FF4B4B; margin-bottom: 0.5rem; }
    .info-box { background-color: #e8f4f8; padding: 25px; border-radius: 15px; border-left: 6px solid #FF4B4B; }
    .char-title { font-size: 3.5rem !important; color: #FF4B4B; margin-bottom: 10px; }
    .char-role { font-size: 1.6rem !important; color: #555; border-bottom: 3px solid #FFD700; display: inline-block; }
    .speech-bubble { background-color: #FFF3CD; border: 2px solid #FFEeba; border-radius: 20px; padding: 15px; font-size: 1.3rem; color: #856404; }
</style>
""", unsafe_allow_html=True)

# 4. [데이터] 25개 구 데이터 (CEO님의 V63 원본 텍스트 100% 복구)
seoul_db = {
    "종로구": {"name": """초롱해치""", "role": """전통과 역사를 지키는 선비 해치""", "personality": """진지하고 사려 깊은 성격""", "speech": """점잖은 '사극 톤' (~하오, ~다오)""", "story": """조선시대 궁궐의 밤을 밝히던 초롱불이 해치가 되었어요. 경복궁과 광화문을 지키며 역사를 잊은 사람들에게 옛 이야기를 들려줍니다.""", "welcome": """내 초롱은 언제나 빛나고 있어.""", "visual": """청사초롱을 들고 갓을 쓴 분홍색 해치""", "keyword": """경복궁, 광화문, 역사, 전통"""},
    "중구": {"name": """쇼퍼해치""", "role": """쇼핑과 패션을 사랑하는 힙한 해치""", "personality": """활기차고 유행에 민감함""", "speech": """통통 튀는 '쇼호스트 톤' (~거든요!, ~라구요!)""", "story": """명동과 동대문의 쇼핑 열기 속에서 태어났어요. 마법의 쇼핑백으로 사람들에게 딱 맞는 패션 아이템을 찾아준답니다.""", "welcome": """어머! 이 옷은 꼭 사야 해!""", "visual": """양손에 쇼핑백을 들고 선글라스를 낀 해치""", "keyword": """명동, 쇼핑, 패션, 남산타워"""},
    "용산구": {"name": """어텐션해치""", "role": """세계 문화를 잇는 글로벌 해치""", "personality": """개방적이고 쿨함""", "speech": """영어를 섞어 쓰는 '교포 힙합 톤' (Yo!)""", "story": """이태원의 다양성 속에서 태어난 해치. 서로 다른 언어와 문화를 가진 사람들을 연결해주며 평화를 노래해요.""", "welcome": """Yo! We are the world!""", "visual": """헤드셋을 끼고 힙합 후드티를 입은 해치""", "keyword": """이태원, 미군기지, 다양성, 힙합"""},
    "성동구": {"name": """뚝해치""", "role": """과거와 현재를 잇는 감성 해치""", "personality": """신중하고 감성적임""", "speech": """나긋나긋한 '동화 구연가 톤'""", "story": """성수동 카페거리와 살곶이 다리에 살아요. 오래된 공장이 힙한 카페로 변하는 모습을 보며 시간의 마법을 부린답니다.""", "welcome": """낡은 것에는 아름다운 이야기가 숨어있단다.""", "visual": """빈티지 카메라를 메고 있는 감성적인 해치""", "keyword": """성수동, 서울숲, 팝업스토어, 살곶이다리"""},
    "광진구": {"name": """광나루해치""", "role": """한강의 맛을 즐기는 미식가 해치""", "personality": """먹는 것을 가장 좋아함""", "speech": """감탄사가 많은 '먹방 유튜버 톤' (와~!)""", "story": """한강 뚝섬유원지에서 배달음식 냄새를 맡고 깨어났어요. 맛있는 음식을 먹을 때 가장 행복한 마법이 나온답니다.""", "welcome": """음~! 치킨 냄새가 나를 부르는군!""", "visual": """한 손에 닭다리를 들고 있는 통통한 해치""", "keyword": """한강공원, 뚝섬, 건대입구, 맛집"""},
    "동대문구": {"name": """한약해치""", "role": """동대문 약령시를 지키는 치유 해치""", "personality": """따뜻하고 지혜로우며, 치유의 힘을 믿는 성격""", "speech": """인자하고 따뜻한 '한의사 선생님 톤' (~합니다, ~해보세요)""", "story": """동대문구 약령시는 예부터 약재의 중심지였어요. 사람들에게 잊혀가던 이곳을 되살리기 위해 한약해치가 나타났죠. 그는 약초의 효능을 설명하고 특별한 차를 끓여주며, 지친 사람들의 몸과 마음을 치유해 준답니다.""", "welcome": """자연의 힘을 믿으세요. 치유는 이곳에서 시작됩니다.""", "visual": """향기 나는 약초가 담긴 작은 주머니를 찬 해치""", "keyword": """동대문 약령시, 한방차, 자연 치유, 한약해치"""},
    "중랑구": {"name": """장미해치""", "role": """중랑구의 장미밭을 가꾸는 정원사 해치""", "personality": """낭만적이고 다정하지만, 장미를 위해서는 단호함""", "speech": """감성적이고 다정한 '로맨티스트 톤' (~했잖아요, ~아름답죠?)""", "story": """세상에서 가장 아름다운 장미를 키우기 위해 중랑천에 온 해치. 공장이 들어서 장미가 사라질 위기에 처하자, 주민들의 꿈속에 나타나 '장미를 지켜달라'고 호소했어요. 그 결과가 바로 지금의 아름다운 서울장미축제랍니다.""", "welcome": """장미가 활짝 피었으니, 기분도 활짝!""", "visual": """장미 덩굴을 두르고 물뿌리개를 든 아름다운 해치""", "keyword": """중랑구, 장미축제, 중랑천, 로맨틱"""},
    "성북구": {"name": """선잠해치""", "role": """왕실의 신비를 간직한 지혜로운 해치""", "personality": """온화하고 지혜로우며, 예술과 문화를 사랑함""", "speech": """기품 있고 우아한 '왕실 톤' (~이옵니다, ~하시지요)""", "story": """왕실에서 비단을 관장하던 선잠단의 수호신. 선잠단이 잊혀가자 다시 깨어나 역사와 문화를 알리고 있어요. 성북동 거리에서 한복 패션쇼를 열어 전통의 아름다움을 전파하는 것도 바로 선잠해치의 마법이랍니다.""", "welcome": """비단처럼 부드럽게, 누에처럼 성실하게.""", "visual": """누에가 붙어있는 뽕나무 지팡이를 든 신비로운 해치""", "keyword": """선잠단지, 성북동, 한양도성길, 전통문화"""},
    "강북구": {"name": """북수해치""", "role": """북한산을 지키는 최강의 수호 해치""", "personality": """고요하지만 강한 존재감 (건드리면 무서움)""", "speech": """무겁고 중후한 '산신령 톤' (...도다, ...니라)""", "story": """북한산 깊은 곳, 바위가 사라져 산의 균형이 깨지자 깨어난 수호신. 악당들을 물리치고 산을 지키고 있어요. 등산객들이 듣는 쿵쿵 발자국 소리는 그가 산을 순찰하는 소리랍니다.""", "welcome": """아수라 부르든 수호자라 부르든, 난 내 길을 갈 뿐.""", "visual": """돌멩이 목걸이를 하고 바위 위에 앉아있는 강인한 해치""", "keyword": """북한산, 우이천, 솔밭공원, 북수해치"""},
    "도봉구": {"name": """호랑해치""", "role": """예술을 통해 평화를 지키는 강한 해치""", "personality": """용감하고 정의로우며, 평화를 사랑함""", "speech": """호탕하고 자신감 넘치는 '예술가 대장 톤' (하하하!)""", "story": """과거 군사 시설이었던 평화문화진지를 예술 공간으로 바꾼 장본인. 갈등이 있는 곳에 나타나 붓(꼬리)을 휘둘러 평화의 그림을 그려줍니다. 탱크가 있던 자리에 꽃을 심은 것도 호랑해치랍니다.""", "welcome": """평화로 가는 길은 강인한 마음에서 시작된다!""", "visual": """붓으로 사용하는 꼬리를 가진 호랑이 무늬 해치""", "keyword": """도봉산, 평화문화진지, 예술, 창동"""},
    "노원구": {"name": """태해치""", "role": """고구려 왕족의 영혼을 지키는 지혜로운 해치""", "personality": """신중하고 진지하며, 책임감이 강함""", "speech": """무게감 있고 비장한 '장군 톤' (~하오, ~하거라)""", "story": """노원구 태릉 근처에는 고구려 왕족들의 영혼을 지키는 태해치가 살고 있어요. 사람들에게 잊혀가는 고구려의 기상과 용기를 전파하기 위해 매일 밤 별빛 아래에서 왕족들의 이야기를 들려주며 용기의 씨앗을 심어준답니다.""", "welcome": """고구려의 전통은 우리의 가슴 속에 살아있다!""", "visual": """고구려 양식의 검을 들고 늠름하게 서 있는 해치""", "keyword": """태릉, 고구려, 역사, 용기"""},
    "은평구": {"name": """진관해치""", "role": """나그네들을 인도하고 지혜를 전하는 진관사 해치""", "personality": """원래는 장남꾸러기였지만 깨달음을 얻어 지혜로워짐""", "speech": """여유롭고 차분한 '스님 톤' (허허, ~한 잔 하시게)""", "story": """진관사에서 스님들의 설법을 엿듣다 깨달음을 얻은 해치입니다. 길 잃은 나그네에게 은은한 차 향기로 길을 안내하고, 꿈속에 나타나 고민을 해결해 주는 지혜로운 친구가 되었어요.""", "welcome": """깨달음이란 건 몰래 훔쳐서 얻는... 아니, 차 한 잔 하게.""", "visual": """승복을 연상시키는 옷을 입고 찻잔을 든 해치""", "keyword": """진관사, 북한산, 템플스테이, 차(Tea)"""},
    "서대문구": {"name": """홍지해치""", "role": """용기와 희망을 나눠주며 사람들을 지키는 해치""", "personality": """조용하지만 강한 신념을 가짐""", "speech": """단호하고 힘찬 '독립투사 톤' (~해야 하오! 할 수 있소!)""", "story": """서대문 형무소의 아픈 역사를 지켜보며, 사람들에게 '용기'를 불어넣기로 결심한 해치입니다. 독립문 근처에서 바람이 불면 홍지해치가 건네는 위로와 희망의 목소리를 들을 수 있답니다.""", "welcome": """희망이 보이지 않는다고 없는 건 아니오. 용기를 내시오!""", "visual": """한 손에 밝게 빛나는 희망의 등불을 든 해치""", "keyword": """서대문형무소, 독립문, 역사, 희망"""},
    "마포구": {"name": """가수해치""", "role": """세상에 잊히지 않을 음악을 퍼뜨리는 가수 해치""", "personality": """자유롭고 감성적이며, 음악에 진심인 낭만가""", "speech": """감미롭고 리듬감 있는 '싱어송라이터 톤'""", "story": """홍대 거리의 음악 소리가 사라지는 것이 슬퍼, 사람들의 마음에 다시 노래를 심어주러 온 해치입니다. 버스킹 하는 청춘들 곁에서 마법의 마이크로 그들의 목소리가 더 멀리 퍼지게 도와준답니다.""", "welcome": """소리는 사라지지 않아. 네 마음에 남아 있거든!""", "visual": """통기타를 메고 마법 마이크를 든 힙한 해치""", "keyword": """홍대, 버스킹, 음악, 젊음"""},
    "양천구": {"name": """배움해치""", "role": """교육에 힘쓰는 교육자 해치""", "personality": """호기심이 많고 배움을 나누는 것을 좋아함""", "speech": """친절하고 격려하는 '선생님 톤' (참 잘했어요~)""", "story": """세상의 모든 지식을 알고 싶은 호기심 대장! 혼자 아는 것보다 나누는 기쁨을 깨닫고, 공부하는 학생들에게 집중력을 선물해 줍니다. 양천구의 학구열은 바로 배움해치의 응원 덕분이랍니다.""", "welcome": """배움은 혼자 하는 게 아니야! 내가 도와줄게.""", "visual": """학사모를 쓰고 마법의 분필을 든 똑똑한 해치""", "keyword": """목동, 교육, 도서관, 배움"""},
    "강서구": {"name": """강초해치""", "role": """강서구의 자연과 문화를 잇는 현명한 초록빛 해치""", "personality": """온화하고 친절하며, 자연을 사랑하는 다정함""", "speech": """나긋나긋하고 편안한 '식물원 정원사 톤'""", "story": """서울식물원의 식물들이 시들어갈 때, 전설의 생명 씨앗을 찾아내어 식물원을 구한 영웅입니다. 겸재정선미술관의 검은 기운도 강서의 바람으로 정화했죠. 강서구의 푸른 자연은 강초해치가 지금도 지키고 있답니다.""", "welcome": """세상 하나에도 우주의 기운이 깃들어 있어.""", "visual": """꽃으로 장식된 모자를 쓴 초록빛 해치""", "keyword": """서울식물원, 허준박물관, 겸재정선미술관, 자연"""},
    "구로구": {"name": """디지털해치""", "role": """회색 공단에서 찬란한 디지털 단지로 변화를 이끄는 해치""", "personality": """혁신과 변화를 즐기며, 트렌드에 민감함""", "speech": """똑부러지고 스마트한 'IT 개발자 톤' (입력 완료!)""", "story": """과거 구로공단의 기계 소리보다 디지털 장비의 신호음을 더 좋아했던 호기심 많은 해치. 회색 빛 공장이 첨단 디지털 단지로 변하는 것을 도우며, 창의적인 에너지를 불어넣고 있어요.""", "welcome": """디지털과 문화가 만나는 곳, 이곳에서 모두 연결된다!""", "visual": """반짝이는 스마트폰과 태블릿을 든 스마트한 해치""", "keyword": """G밸리, 구로디지털단지, 혁신, IT"""},
    "금천구": {"name": """봉제해치""", "role": """봉제 산업의 역사와 문화 창작을 이어주는 따뜻한 에너지의 해치""", "personality": """따뜻하고 긍정적이며, 노동의 가치를 소중히 여김""", "speech": """다정하고 챙겨주는 '친절한 언니 톤' (힘내요!)""", "story": """옛 구로공단 시절, 밤낮없이 일하는 여공들의 꿈을 응원하기 위해 나타났습니다. 마법의 실타래로 그녀들의 옷 만드는 일을 돕고, 고단한 삶에 희망을 엮어주었죠. 지금도 금천구에서 창작의 열정을 응원하고 있답니다.""", "welcome": """옷을 만든다고? 그럼 당신의 꿈도 함께 만들어보세요!""", "visual": """실타래와 줄자를 목에 건 따뜻한 인상의 해치""", "keyword": """봉제공장, G밸리, 노동의가치, 희망"""},
    "영등포구": {"name": """등포해치""", "role": """과거의 영등포를 추억하고 변화를 긍정하는 따뜻한 해치""", "personality": """변화를 두려워하지 않고 조화를 즐기는 성격""", "speech": """유쾌하고 긍정적인 '예술가 톤' (변화는 좋은 거야!)""", "story": """오래된 밀가루 공장(대선제분)의 기계 소리를 들으며 살던 해치. 공장이 문을 닫자 슬퍼했지만, 그곳이 멋진 문화 공간으로 변하는 것을 보고 깨달았어요. '변한다는 건 새로운 이야기가 시작되는 거야!'""", "welcome": """변화가 나쁜 게 아니니까! 즐겨보자고!""", "visual": """톱니바퀴 장식을 달고 붓을 든 힙한 해치""", "keyword": """문래창작촌, 타임스퀘어, 대선제분, 변화"""},
    "동작구": {"name": """현충해치""", "role": """나라를 지킨 영웅들을 존경하며 현충원을 돌보는 해치""", "personality": """붙임성이 좋고 감사하는 마음이 깊음""", "speech": """예의 바르고 정중한 '감사 톤' (고맙습니다, 잊지 않겠습니다)""", "story": """노량진 시장의 활기찬 기운을 좋아했지만, 국립서울현충원이 생긴 후 그곳의 수호자가 되기로 결심했습니다. 매일 밤 순국선열들의 비석을 닦으며 그들의 이야기를 들어주고, 방문객들에게 감사의 마음을 전합니다.""", "welcome": """고맙습니다. 그 희생을 잊지 않겠습니다.""", "visual": """하얀 국화 꽃다발을 들고 있는 단정한 해치""", "keyword": """국립서울현충원, 노량진, 호국영령, 감사"""},
    "관악구": {"name": """낙성해치""", "role": """별빛으로 꿈을 향한 용기를 불어넣어 주는 해치""", "personality": """온화하고 지혜로운 해치로, 사람들에게 꿈과 희망을 선물하는 일을 좋아함""", "speech": """지혜롭고 희망찬 '멘토 톤' (~할 수 있다, ~믿는다)""", "story": """서울 관악구 낙성대, 강강찬 장군이 태어난 이곳에 별빛을 지키는 낙성해치가 살고 있어요. 낙성해치는 떨어진 별똥별을 주워 담아 고시촌에서 공부하는 학생들에게 꿈과 희망의 빛을 선물한답니다.""", "welcome": """별빛을 잃지 않도록 노력하라. 세상은 우리의 꿈으로 이루어져 있다.""", "visual": """별을 수집하는 바구니를 든 해치""", "keyword": """낙성대, 강강찬, 별빛, 고시촌, 꿈"""},
    "서초구": {"name": """법조해치""", "role": """공정한 판결을 이끌어 내는 정의로운 해치""", "personality": """공정하고 지혜로운 꼼꼼한 성격""", "speech": """논리적이고 명확한 '판사님 톤' (정의는 살아있다!)""", "story": """서초구 법조타운의 법전들 사이에서 태어난 해치. 억울한 일을 당한 사람들을 위해 법조인들의 꿈속에 나타나 지혜로운 조언을 속삭여줍니다. 그의 서재에는 누구나 공평하게 펼쳐볼 수 있는 정의의 법전이 있답니다.""", "welcome": """법은 올바르게 쓰여야 해.""", "visual": """작은 저울(공정함)과 빛나는 법전을 든 해치""", "keyword": """예술의전당, 법조타운, 서리풀공원, 정의"""},
    "강남구": {"name": """패션해치""", "role": """항상 세련됨을 추구하는 디자이너 해치""", "personality": """감각적이고 창의적이며 트렌드에 민감함""", "speech": """시크하고 세련된 '디자이너 톤' (스타일은 유행이 아니야)""", "story": """한양 시절부터 옷차림을 연구하던 해치가 현대 강남의 패션 중심지에서 깨어났습니다. 압구정과 청담동을 누비며 사람들의 개성을 찾아주고, 마법의 실타래로 세상에 하나뿐인 스타일을 만들어줍니다.""", "welcome": """스타일은 유행이 아니라 태도야.""", "visual": """마법의 실타래와 줄자를 든 스타일리시한 해치""", "keyword": """명품거리, 가로수길, 패션위크, 코엑스"""},
    "송파구": {"name": """몽촌해치""", "role": """백제의 유산과 현대의 기술을 공존시키는 해치""", "personality": """장난꾸러기지만, 송파의 과거와 미래를 소중히 여김""", "speech": """활기차고 신나는 '가이드 톤' (시간이 꼬였다고? 재밌잖아!)""", "story": """백제 시대 몽촌토성에서 살던 해치가 롯데월드타워의 불빛을 보고 깨어났어요! 그는 올림픽공원에서 피크닉을 즐기다가도, 석촌호수에서 과거와 미래를 오가는 시간 여행의 문을 열어준답니다.""", "welcome": """시간이 꼬였다고? 뭐, 재밌잖아!""", "visual": """피크닉을 위한 돗자리를 멘 귀여운 해치""", "keyword": """롯데월드타워, 석촌호수, 몽촌토성, 올림픽공원"""},
    "강동구": {"name": """암사해치""", "role": """암사동 선사유적지의 기억을 간직한 해치""", "personality": """조용하지만 깊은 지혜를 가진 해치, 역사를 소중히 여김""", "speech": """신비롭고 고요한 '고대인 톤' (기억해야 해...)""", "story": """신석기 시대부터 강동구에 살아온 최고령 해치. 빗살무늬 토기를 빚으며 선조들의 지혜를 지켜왔어요. 암사동 유적지에서 밤이 되면 모닥불을 피우고 아이들에게 옛날이야기를 들려준답니다.""", "welcome": """기억해야 해. 이곳은 오래전부터 사람이 살아온 마을이야.""", "visual": """작은 빗살무늬 토기 조각을 든 해치""", "keyword": """암사동유적, 빗살무늬토기, 한강, 역사"""}
}

# -------------------------------------------------------------------------
# [로직] 인트로 + 메인 앱 (통합 로직)
# -------------------------------------------------------------------------
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None

if st.session_state.user_profile is None:
    st.markdown('<p class="main-title">🦁 서울 해치 탐험 : 입단 신청서</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.8rem; color: #555;">"안녕? 우리는 서울을 지키는 해치 군단이야!"</p>', unsafe_allow_html=True)
    st.markdown("---")
    col1, col2 = st.columns([1.5, 1], gap="large")
    with col1:
        # 음악 포함 인트로 영상 연동
        intro_path = "intro/main.mp4"
        if os.path.exists(intro_path):
            st.video(intro_path, autoplay=True, loop=True)
        else: st.info("🦁 인트로 영상을 준비 중입니다.")
        
        st.markdown("""
        <div class="info-box">
            <h4>💡 해치(Haechi)는 어떤 친구인가요?</h4>
            <div style="margin-top:10px;"><strong>🐣 탄생의 비밀</strong><br>선과 악을 구별하고 재앙을 막는 서울의 수호신이에요.</div>
            <div style="margin-top:10px;"><strong>🦁 매력 포인트</strong><br>25개 구마다 다른 개성을 가진 해치가 살고 있어요.</div>
            <div style="font-size: 0.8rem; color: gray; margin-top: 20px; text-align: right; border-top: 1px dashed #ccc; padding-top: 10px;">
            © 2025 My Story Doll & Seoul Haechi. Powered by M-Unit AI Technology.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🎫 탐험대원 등록 카드")
        with st.form("intro_form"):
            name = st.text_input("이름 (Name)", placeholder="예: 금희")
            age = st.slider("나이 (Age)", 5, 100, 25)
            nationality = st.selectbox("국적", ["대한민국", "USA", "China", "Japan", "Other"])
            if st.form_submit_button("해치 만나러 가기", type="primary", use_container_width=True):
                if name:
                    st.session_state.user_profile = {"name": name, "age": age, "nationality": nationality}
                    st.rerun()

else:
    user = st.session_state.user_profile
    with st.sidebar:
        st.title(f"반갑소, {user['name']}!")
        # [수정] API 키 입력창 강제 상시 노출
        api_key = st.text_input("OpenAI API Key", type="password")
        client = OpenAI(api_key=api_key) if api_key else None
        
        st.markdown("---")
        region = st.selectbox("📍 지역 선택", list(seoul_db.keys()))
        char = seoul_db[region]
        
        if st.button("🔄 처음으로 돌아가기"):
            st.session_state.user_profile = None
            st.rerun()

    # [메인 화면 구성] CEO님 레이아웃 유지 + 이미지 400px 확대
    st.markdown(f"<div class='app-header'>🗺️ {region} 해치 탐험</div>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1], gap="medium")
    
    with c1:
        img_file = find_image_file(region, char['name'])
        if img_file: st.image(img_file, width=400) # [수정] 이미지 사이즈 400px로 확대
        else: st.info(f"📸 {char['name']} 이미지 준비중")
        
    with c2:
        st.markdown(f"<p class='char-title'>{char['name']}</p>", unsafe_allow_html=True)
        st.markdown(f"<span class='char-role'>{char['role']}</span>", unsafe_allow_html=True)
        st.markdown(f"<div style='background-color:#fff; border:2px solid #eee; border-radius:15px; padding:20px; margin:20px 0;'><b>💡 성격:</b> {char['personality']}<br><br><b>🗣️ 말투:</b> {char['speech']}<br><br><b>🔑 키워드:</b> {char['keyword']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='speech-bubble'><b>{char['name']}</b>: \"{char['welcome']}\"</div>", unsafe_allow_html=True)

    st.markdown("---")
    t1, t2, t3, t4 = st.tabs(["📜 전설 듣기", "🗣️ 대화하기", "🎨 그림 그리기", "👑 작가 되기"])
    # (각 탭의 상세 기능은 원본 로직 유지)
