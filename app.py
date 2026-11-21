import streamlit as st
import pandas as pd

st.set_page_config(page_title="섭생노트: 8체질 진단", page_icon="🌿", layout="wide")

# 1. 8체질 핵심 데이터베이스
CONSTITUTION_DB = {
    "수음체질": {
        "en": "Vesicotonia · 위성체질", "group": "금수체질군 (교감신경 항진)",
        "organs": "방광 > 담 > 소장 > 대장 > 위장", "celebs": "박보영",
        "celeb_note": "가냘픈 상체 체형에 섬세한 성향을 지닌 대표 사례로, 소식과 따뜻한 식단이 핵심입니다.",
        "summary": "상체는 가늘고 하체로 부종이 몰리기 쉬우며(상소하대), 위장이 가장 약해 과식·찬 음식에 쉽게 체합니다. 상열하한(얼굴·눈 열감, 아랫배 냉증)이 잘 나타납니다.",
        "good": "찹쌀, 감자, 마, 옥수수, 양배추, 부추, 생강, 마늘, 대추, 계피, 닭고기, 오리고기, 양고기, 흰살생선, 사과, 귤, 토마토, 생강차, 눌은밥",
        "bad": "밀가루, 돼지고기, 보리, 팥, 녹두, 메밀, 오이, 참외, 수박, 배, 멜론, 키위, 맥주, 차가운 물·음료, 날생선(회), 초콜릿",
        "care": "격한 유산소·고중량 운동은 진액을 빼므로 피하고, 기구 필라테스·코어 강화·저녁 족욕·L자 다리 스트레칭으로 하초를 데우세요."
    },
    "수양체질": {
        "en": "Renotonia · 신실체질", "group": "금수체질군 (교감신경 항진)",
        "organs": "신장 > 폐 > 간 > 심장 > 췌장·위장", "celebs": "주현영",
        "celeb_note": "한의원 검사에서 수양체질로 진단받아 찬 음료를 줄이고 따뜻한 식단으로 관리하는 사례입니다.",
        "summary": "어깨가 단정하고 균형 잡힌 체형에 침착·신중한 성격입니다. 땀이 적고 여름 더위·일광욕에 약하며, 변비 경향이 있어도 크게 불편해하지 않습니다.",
        "good": "현미, 찹쌀, 감자, 닭고기, 염소고기, 쇠고기, 미역·다시마, 계피, 생강, 파, 마늘, 사과, 망고, 귤, 오렌지, 토마토, 인삼, 벌꿀, 대추",
        "bad": "보리, 팥, 오이, 돼지고기, 생굴·어패류, 복요리, 감, 참외, 딸기, 바나나, 파인애플, 맥주, 얼음, 찬 음식, 커피, 밀가루, 수박, 사우나",
        "care": "땀을 많이 내는 사우나·일광욕을 피하고 냉수마찰이나 실내 코어 운동·수영으로 체력을 보존하세요."
    },
    "목양체질": {
        "en": "Hepatonia · 간실체질", "group": "목토체질군 (부교감신경 항진)",
        "organs": "간장 > 신장 > 심장 > 췌장 > 폐장", "celebs": "이문세, 마동석",
        "celeb_note": "굵은 골격과 건장한 체격을 지니며 육식과 땀을 내는 활동이 잘 맞는 대표 사례입니다.",
        "summary": "체구가 크고 허리가 굵은 편이며 과묵하고 현실적입니다. 땀을 흠뻑 흘려야 몸이 가뿐해지고 혈압이 평균보다 약간 높을 때 의욕이 왕성합니다.",
        "good": "모든 육식(소고기 등), 쌀, 메주콩, 밀가루, 수수, 뿌리채소(무·당근·도라지·연근), 커피, 우유, 마늘, 호박, 버섯, 견과류, 민물장어, 인삼·녹용",
        "bad": "모든 바다생선 및 조개·게(해산물), 날배추, 포도당 주사, 코코아·초콜릿, 메밀, 고사리, 감, 모과, 체리, 청포도, 수영, 비타민 E",
        "care": "등산·조깅과 온수욕·사우나로 땀을 충분히 배출해 속열을 풀어주는 것이 가장 좋습니다."
    },
    "목음체질": {
        "en": "Cholecystonia · 장성체질", "group": "목토체질군 (부교감신경 항진)",
        "organs": "담낭 > 소장 > 위장 > 방광 > 대장", "celebs": "이동욱, 이광수, 박찬호",
        "celeb_note": "큰 키와 긴 팔다리, 사교적이면서도 감수성이 섬세한 성향을 지닌 대표 유형입니다.",
        "summary": "팔다리가 길고 사교적이나 감정이 섬세해 비판에 예민하며 불면증이 오기 쉽습니다. 대장이 짧아 하루 2~3회 변을 보고 아랫배가 차기 쉽습니다.",
        "good": "쇠고기·돼지고기 등 육식, 쌀, 대두콩, 밀가루, 뿌리채소, 커피, 우유, 율무, 마늘, 호박, 버섯, 견과류, 민물장어, 따뜻한 물 샤워",
        "bad": "모든 바다생선 및 어패류, 술(알코올), 날배추, 메밀, 고사리, 코코아·초콜릿, 청포도, 감, 포도당, 인삼, 오가피, 냉수욕",
        "care": "아랫배를 항상 따뜻하게 보온하고 알코올을 절제하며, 가벼운 유산소 후 온수 샤워를 하세요."
    },
    "토양체질": {
        "en": "Pancreotonia · 신성체질", "group": "목토체질군 (부교감신경 항진)",
        "organs": "췌장 > 심장 > 간장 > 폐장 > 신장", "celebs": "송혜교, 이승기",
        "celeb_note": "활발하고 추진력 있는 에너지와 세련된 인상을 지니며 서늘한 채소·해산물 식단이 이롭습니다.",
        "summary": "엉덩이가 작고 걸음이 빠르며 마음이 항상 바쁘고 솔직합니다. 소화력이 매우 강하나 위열이 많아 매운 음식·닭고기를 먹으면 트러블이 생깁니다.",
        "good": "보리, 쌀, 계란, 밀가루, 콩, 팥, 돼지고기, 쇠고기, 모든 채소, 대부분의 바다생선, 복요리, 수박, 참외, 멜론, 딸기, 바나나, 얼음",
        "bad": "닭고기, 개고기, 염소고기, 현미, 미역·다시마, 사과, 귤, 오렌지, 망고, 토마토, 인삼, 감자, 벌꿀, 매운 음식(고추·생강·파), 술, 냉수욕",
        "care": "조급함을 낮추는 요가·하체 근력 운동과 반신욕으로 상부의 열을 내리는 것이 좋습니다."
    },
    "토음체질": {
        "en": "Gastrotonia · 위실체질", "group": "목토체질군 (부교감신경 항진)",
        "organs": "위장 > 대장 > 소장 > 담낭 > 방광", "celebs": "비(정지훈), 김범수, 지코",
        "celeb_note": "전체 인구 1% 미만의 희귀 체질로 철저한 자기관리와 독특한 감각을 지닌 유형으로 꼽힙니다.",
        "summary": "손등이 통통하고 곱슬머리가 많으며 식사 속도가 느립니다. 위장이 지나치게 예민해 소화불량이 잦고 양약(항생제·진통제) 부작용이 가장 심합니다.",
        "good": "보리, 쌀, 팥, 녹두, 오이 및 푸른 채소, 모든 바다생선 및 패류, 돼지고기, 수박, 참외, 파인애플, 포도, 딸기, 바나나, 시원한 음식",
        "bad": "현미, 찹쌀, 닭고기, 쇠고기, 게, 매운 향신료(겨자·후추·고추·카레·생강), 사과, 귤, 오렌지, 토마토, 미역·다시마, 인삼, 양약",
        "care": "약물 복용을 최소화하고 신선하고 서늘한 음식으로 위장의 과도한 열을 진정시키세요."
    },
    "금양체질": {
        "en": "Pulmotonia · 간성체질", "group": "금수체질군 (교감신경 항진)",
        "organs": "폐장 > 췌장 > 심장 > 신장 > 간장", "celebs": "나얼, 박효신, 하현우",
        "celeb_note": "폐 기능이 강해 뛰어난 발성을 지녔으며 내향적·완벽주의적 성향과 마른 체형이 특징입니다.",
        "summary": "마른 체형에 뒷머리 아랫부분이 나와 있으며 창의적이고 완벽주의적입니다. 간 기능이 약해 육식·약물 섭취 시 아토피나 알레르기가 잘 생깁니다.",
        "good": "모든 바다생선, 게, 조개류, 쌀, 보리, 메밀, 팥, 녹두, 오이·배추·양배추·상추 등 푸른 채소, 바나나, 딸기, 복숭아, 포도당, 냉수욕",
        "bad": "모든 육식(소·돼지·닭), 민물고기, 커피·차류, 인공조미료, 밀가루, 호박, 고추, 마늘, 뿌리채소, 버섯, 설탕, 사과, 배, 인삼, 양약, 사우나",
        "care": "사우나·등산처럼 땀을 빼는 활동을 피하고 평지 산책과 냉수욕, 길게 내뱉는 호흡을 실천하세요."
    },
    "금음체질": {
        "en": "Colonotonia · 장실체질", "group": "금수체질군 (교감신경 항진)",
        "organs": "대장 > 방광 > 위장 > 소장 > 담낭", "celebs": "류준열, 한예슬, 백지영",
        "celeb_note": "아침 찬물 샤워와 채식·해산물 위주 식단으로 건강을 관리한다고 직접 공개한 대표 사례입니다.",
        "summary": "광대뼈가 나와 있고 진취적이며 자존심이 강해 화를 내기 쉽습니다. 심폐력이 좋으나 대변이 가늘고, 육식·분노가 근육 피로를 유발합니다.",
        "good": "메밀, 쌀, 포도당, 모든 바다생선과 게·조개류, 모든 푸른 채소, 오이, 김, 젓갈, 포도, 복숭아, 파인애플, 딸기, 수영, 냉수욕",
        "bad": "모든 육식, 마늘, 인삼·녹용, 민물고기, 커피, 인공조미료, 밀가루, 호박, 메주콩, 우유, 설탕, 배, 사과, 뿌리채소, 버섯, 온수욕·반신욕",
        "care": "화내지 않는 감정 조절과 수영·냉수욕, 어패류·푸른 채소 위주의 식단이 건강의 핵심입니다."
    }
}

# 2. 5단계 25문항 핵심 설문 (단계 이동 시에도 응답 유지)
STEPS = ["1. 체형·외모", "2. 성격·기질", "3. 발한·운동", "4. 순환·소화", "5. 식이 궁합"]

QUESTIONS = [
    ("Q01", 0, "풍채가 좋고 전체적으로 체구와 골격이 크며 허리가 굵은 편이다.", {"목양체질": 2.5, "목음체질": 1.0}),
    ("Q02", 0, "키가 크고 팔다리가 길게 뻗어 있는 편이다.", {"목음체질": 2.5}),
    ("Q03", 0, "엉덩이가 체형에 비해 작은 편이고 걸음걸이가 빠르다.", {"토양체질": 2.5}),
    ("Q04", 0, "곱슬머리이거나 손등에 살집이 있어 통통한 편이다.", {"토음체질": 2.5}),
    ("Q05", 0, "얼굴이 작고 상체 뼈대는 가냘픈데 하체로 부종이 쉽게 쏠린다.", {"수음체질": 2.5, "수양체질": 1.5}),

    ("Q06", 1, "평소 말이 없고 과묵하며, 말을 많이 하면 기운이 빠진다.", {"목양체질": 2.5}),
    ("Q07", 1, "감정이 섬세해 남의 비판이나 섭섭한 소리에 자극을 받으면 잠을 못 잔다.", {"목음체질": 2.5}),
    ("Q08", 1, "마음이 항상 바쁘고 성격이 급하며, 솔직하게 바로 말하는 편이다.", {"토양체질": 2.5}),
    ("Q09", 1, "완벽주의적이고 꼼꼼하며, 자존심이 강해 뜻대로 안 되면 화가 난다.", {"금양체질": 2.0, "금음체질": 2.5}),
    ("Q10", 1, "침착하고 신중하며, 운동보다 지적·창의적 몰입력이 뛰어나다.", {"수음체질": 2.0, "수양체질": 2.5}),

    ("Q11", 2, "운동이나 사우나로 땀을 흠뻑 흘리고 나면 몸이 가볍고 피로가 풀린다.", {"목양체질": 2.5, "목음체질": 2.0}),
    ("Q12", 2, "더운 목욕이나 사우나를 하면 어지럽고 지치며, 냉수욕이 상쾌하다.", {"금양체질": 2.0, "금음체질": 2.0, "수양체질": 1.5}),
    ("Q13", 2, "심폐 지구력이 좋아 오래 달리거나 수영할 때 호흡이 잘 버틴다.", {"금음체질": 2.5, "금양체질": 1.5}),
    ("Q14", 2, "평소 땀이 거의 없고, 격렬한 운동이나 땀을 흘리면 기운이 쭉 빠진다.", {"수음체질": 2.5, "수양체질": 2.0}),
    ("Q15", 2, "식사할 때 땀이 잘 나며, 식사 속도가 남들보다 느린 편이다.", {"토음체질": 2.5, "수음체질": 1.0}),

    ("Q16", 3, "혈압이 평균보다 약간 높아야 몸이 가볍고 의욕이 왕성하다.", {"목양체질": 2.5}),
    ("Q17", 3, "대변을 하루 2~3번 자주 보며, 아랫배가 차가워지면 다리·허리가 무겁다.", {"목음체질": 2.5}),
    ("Q18", 3, "소화력이 아주 좋고 찬 음식이나 얼음물을 마셔도 속이 시원하다.", {"토양체질": 2.5}),
    ("Q19", 3, "양약(항생제·진통제) 부작용이나 아토피·피부 알레르기가 잘 생긴다.", {"토음체질": 2.0, "금양체질": 2.5, "금음체질": 1.5}),
    ("Q20", 3, "위장이 약해 소식해야 편하며, 스트레스 시 얼굴·눈에 열이 오르고 아랫배는 차다.", {"수음체질": 2.5, "수양체질": 1.5}),

    ("Q21", 4, "소고기 등 육식을 먹으면 힘이 나고, 바다생선·해산물은 불편하다.", {"목양체질": 2.5, "목음체질": 2.5}),
    ("Q22", 4, "고추·생강 등 매운 음식이나 닭고기를 먹으면 속이 쓰리고 열이 오른다.", {"토양체질": 2.5, "토음체질": 2.5}),
    ("Q23", 4, "모든 육식·밀가루·커피는 불편하고, 바다생선과 푸른 채소가 잘 맞는다.", {"금양체질": 2.5, "금음체질": 2.5}),
    ("Q24", 4, "찬물·아이스 음료·돼지고기·밀가루를 먹으면 속이 더부룩하고 몸이 붓는다.", {"수음체질": 2.5, "수양체질": 2.0}),
    ("Q25", 4, "닭고기, 찹쌀, 생강·계피차, 인삼 등 따뜻한 음식을 먹으면 속이 편하다.", {"수음체질": 2.0, "수양체질": 2.5, "목양체질": 1.0}),
]

# 3. 세션 상태 초기화
defaults = {
    "step": 0,
    "done": False,
    "const": "수음체질",
    "answers": {},
    "chat": [{"role": "assistant", "content": "안녕하세요! 🌿 체질을 선택하신 뒤 **음식, 운동, 증상, 셀럽**에 대해 무엇이든 질문해 주세요."}],
    "records": [
        {"이름": "샘플_01", "성별": "여성", "연령대": "20대", "1순위": "수음체질", "2순위": "수양체질", "체질군": "금수체질군", "일치율(%)": 86.0},
        {"이름": "샘플_02", "성별": "남성", "연령대": "30대", "1순위": "목양체질", "2순위": "목음체질", "체질군": "목토체질군", "일치율(%)": 82.5},
        {"이름": "샘플_03", "성별": "여성", "연령대": "30대", "1순위": "토양체질", "2순위": "토음체질", "체질군": "목토체질군", "일치율(%)": 79.0},
    ]
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# 4. 사이드바 (프로필 & 프리셋)
st.sidebar.header("👤 참여자 정보")
user_name = st.sidebar.text_input("이름/닉네임", value="게스트_01")
user_gender = st.sidebar.radio("성별", ["여성", "남성"], horizontal=True)
user_age = st.sidebar.selectbox("연령대", ["20대", "30대", "40대", "50대 이상"])

st.sidebar.divider()
st.sidebar.subheader("⚡ 빠른 시연 프리셋")
preset = st.sidebar.selectbox("체험 유형 선택", ["직접 입력", "수음·수양형", "목양·목음형", "토양·토음형", "금양·금음형"])

if st.sidebar.button("프리셋 자동 채우기", use_container_width=True):
    preset_map = {
        "수음·수양형": ["Q05", "Q10", "Q14", "Q20", "Q24", "Q25"],
        "목양·목음형": ["Q01", "Q06", "Q11", "Q16", "Q21", "Q25"],
        "토양·토음형": ["Q03", "Q08", "Q18", "Q22"],
        "금양·금음형": ["Q09", "Q12", "Q13", "Q19", "Q23"]
    }
    target_qs = preset_map.get(preset, [])
    st.session_state["answers"] = {q[0]: ("예 (Y)" if q[0] in target_qs else "아니오 (N)") for q in QUESTIONS}
    for k in [key for key in st.session_state if key.startswith("radio_")]:
        del st.session_state[k]
    st.session_state["step"] = len(STEPS) - 1
    st.session_state["done"] = True
    st.rerun()

if st.sidebar.button("응답 전체 초기화", use_container_width=True):
    st.session_state["answers"] = {}
    for k in [key for key in st.session_state if key.startswith("radio_")]:
        del st.session_state[k]
    st.session_state["step"] = 0
    st.session_state["done"] = False
    st.rerun()

# 5. 메인 화면 및 4개 탭
st.title("🌿 섭생노트: 8체질 진단 & 맞춤 관리 프로그램")
tab1, tab2, tab3, tab4 = st.tabs(["📋 1. 체질 진단", "💬 2. 1:1 상담실", "🌟 3. 셀럽·식재료 검색", "📊 4. 누적 통계"])

# [TAB 1] 체질 진단 설문 & 리포트
with tab1:
    cols = st.columns(5)
    for i, s_name in enumerate(STEPS):
        if cols[i].button(s_name, key=f"sbtn_{i}", type="primary" if st.session_state["step"] == i else "secondary", use_container_width=True):
            st.session_state["step"] = i
            st.rerun()

    curr = st.session_state["step"]
    st.progress((curr + 1) / len(STEPS), text=f"{STEPS[curr]} ({curr + 1}/{len(STEPS)}단계)")

    for code, step_idx, text, _ in QUESTIONS:
        if step_idx == curr:
            saved = st.session_state["answers"].get(code, "아니오 (N)")
            ans = st.radio(f"**{text}**", ["아니오 (N)", "예 (Y)"], index=1 if saved == "예 (Y)" else 0, horizontal=True, key=f"radio_{code}")
            st.session_state["answers"][code] = ans

    c1, c2, c3 = st.columns([1, 2, 1])
    if curr > 0 and c1.button("← 이전", use_container_width=True):
        st.session_state["step"] -= 1
        st.rerun()
    if curr < len(STEPS) - 1 and c3.button("다음 →", use_container_width=True):
        st.session_state["step"] += 1
        st.rerun()
    if curr == len(STEPS) - 1 and c2.button("✨ 진단 결과 확인하기", type="primary", use_container_width=True):
        st.session_state["done"] = True
        yes_cnt = sum(1 for v in st.session_state["answers"].values() if v == "예 (Y)")
        if yes_cnt > 0:
            raw = {c: 0.0 for c in CONSTITUTION_DB}
            mx = {c: 0.0 for c in CONSTITUTION_DB}
            for code, _, _, weights in QUESTIONS:
                is_y = 1.0 if st.session_state["answers"].get(code) == "예 (Y)" else 0.0
                for cname, w in weights.items():
                    raw[cname] += is_y * w
                    mx[cname] += w
            ranked = sorted({c: round((raw[c] / mx[c]) * 100, 1) for c in CONSTITUTION_DB}.items(), key=lambda x: x[1], reverse=True)
            st.session_state["const"] = ranked[0][0]
            st.session_state["records"].append({
                "이름": user_name, "성별": user_gender, "연령대": user_age,
                "1순위": ranked[0][0], "2순위": ranked[1][0],
                "체질군": CONSTITUTION_DB[ranked[0][0]]["group"].split()[0], "일치율(%)": ranked[0][1]
            })

    if st.session_state["done"]:
        yes_cnt = sum(1 for v in st.session_state["answers"].values() if v == "예 (Y)")
        if yes_cnt == 0:
            st.warning("최소 1개 이상의 문항에 '예 (Y)'를 선택해 주세요.")
        else:
            raw = {c: 0.0 for c in CONSTITUTION_DB}
            mx = {c: 0.0 for c in CONSTITUTION_DB}
            for code, _, _, weights in QUESTIONS:
                is_y = 1.0 if st.session_state["answers"].get(code) == "예 (Y)" else 0.0
                for cname, w in weights.items():
                    raw[cname] += is_y * w
                    mx[cname] += w
            scores = {c: round((raw[c] / mx[c]) * 100, 1) for c in CONSTITUTION_DB}
            ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            top1, top2, top3 = ranked[0], ranked[1], ranked[2]
            info = CONSTITUTION_DB[top1[0]]

            st.divider()
            st.success(f"### 🎯 {user_name}님의 1순위 체질: **{top1[0]}** ({info['en']})")
            st.caption(f"분류: {info['group']} | 장부 강약: {info['organs']}")

            m1, m2, m3 = st.columns(3)
            m1.metric("1순위 체질", top1[0], f"일치율 {top1[1]}%")
            m2.metric("2순위 체질", top2[0], f"일치율 {top2[1]}%")
            m3.metric("3순위 체질", top3[0], f"일치율 {top3[1]}%")

            st.bar_chart(pd.DataFrame({"일치율(%)": scores.values()}, index=scores.keys()))
            st.info(f"**🌟 대표 셀럽 ({info['celebs']}):** {info['celeb_note']}")
            st.write(f"**🩺 체질 특징:** {info['summary']}")

            d1, d2 = st.columns(2)
            d1.success(f"**🥗 유익한 음식**\n\n{info['good']}")
            d2.error(f"**🚫 피해야 할 음식**\n\n{info['bad']}")
            st.warning(f"**🧘 운동 및 순환 관리:** {info['care']}")

# [TAB 2] 1:1 체질 상담실 (탭 내부 오류 없는 Form 방식)
with tab2:
    st.subheader("💬 1:1 체질 맞춤 상담실")
    sel_const = st.selectbox("상담 기준 체질 선택", list(CONSTITUTION_DB.keys()), index=list(CONSTITUTION_DB.keys()).index(st.session_state["const"]))
    st.session_state["const"] = sel_const
    cdata = CONSTITUTION_DB[sel_const]

    for msg in st.session_state["chat"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    with st.form("chat_form", clear_on_submit=True):
        q_input = st.text_input(f"[{sel_const}] 궁금한 음식, 운동, 사우나, 연예인 등을 입력하세요")
        if st.form_submit_button("질문하기", type="primary") and q_input.strip():
            st.session_state["chat"].append({"role": "user", "content": q_input})
            if any(k in q_input for k in ["연예인", "셀럽", "누구"]):
                ans = f"**[{sel_const}]** 대표 셀럽은 **{cdata['celebs']}** 입니다. {cdata['celeb_note']}"
            elif any(k in q_input for k in ["운동", "사우나", "목욕", "관리", "땀"]):
                ans = f"**[{sel_const} 생활·운동 관리]** {cdata['care']}"
            elif any(k in q_input for k in ["음식", "식단", "먹"]):
                ans = f"✅ **유익함:** {cdata['good']}\n\n❌ **해로움:** {cdata['bad']}"
            else:
                good_hit = [x.strip() for x in cdata["good"].split(",") if x.strip() and x.strip() in q_input]
                bad_hit = [x.strip() for x in cdata["bad"].split(",") if x.strip() and x.strip() in q_input]
                if good_hit:
                    ans = f"✅ **{', '.join(good_hit)}**은(는) **{sel_const}**에게 **유익한 음식**입니다."
                elif bad_hit:
                    ans = f"❌ **{', '.join(bad_hit)}**은(는) **{sel_const}**에게 **해로운 음식**입니다."
                else:
                    ans = f"**[{sel_const}]**는 {cdata['group']}입니다.\n- **권장:** {cdata['good']}\n- **주의:** {cdata['bad']}"
            st.session_state["chat"].append({"role": "assistant", "content": ans})
            st.rerun()

# [TAB 3] 셀럽 및 식재료 검색
with tab3:
    st.subheader("🌟 8체질별 대표 셀럽 요약")
    celeb_df = pd.DataFrame([{"체질": k, "분류": v["group"].split()[0], "대표 셀럽": v["celebs"], "특징": v["celeb_note"]} for k, v in CONSTITUTION_DB.items()])
    st.dataframe(celeb_df, use_container_width=True, hide_index=True)

    st.subheader("🔎 식재료·습관 궁합 검색")
    kw = st.text_input("검색어 입력 (예: 돼지고기, 밀가루, 닭고기, 바다생선, 사우나, 냉수욕)", value="돼지고기")
    if kw:
        res = []
        for k, v in CONSTITUTION_DB.items():
            status = "✅ 유익함" if kw in (v["good"] + v["care"]) else ("❌ 해로움" if kw in v["bad"] else "➖ 중립")
            res.append({"체질": k, "대분류": v["group"].split()[0], f"'{kw}' 궁합": status, "대표 셀럽": v["celebs"]})
        st.dataframe(pd.DataFrame(res), use_container_width=True, hide_index=True)

# [TAB 4] 누적 데이터 통계 & CSV 다운로드
with tab4:
    st.subheader("📊 참여자 체질 분포 & 데이터 추출")
    df_rec = pd.DataFrame(st.session_state["records"])
    k1, k2, k3 = st.columns(3)
    k1.metric("누적 인원", f"{len(df_rec)}명")
    k2.metric("최다 체질", df_rec["1순위"].mode()[0])
    k3.metric("평균 일치율", f"{df_rec['일치율(%)'].mean():.1f}%")

    c1, c2 = st.columns(2)
    c1.bar_chart(df_rec["1순위"].value_counts())
    c2.bar_chart(df_rec["체질군"].value_counts())
    st.dataframe(df_rec, use_container_width=True, hide_index=True)

    st.download_button("📥 CSV 다운로드", df_rec.to_csv(index=False).encode("utf-8-sig"), "8constitution_data.csv", "text/csv")
