import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="현장 통역 순발력 챌린지", page_icon="🎤", layout="centered")

# ---------------------------------------------------------
# 1. 데이터 구조 (리스트 list & 딕셔너리 활용 - 총 21문항)
# ---------------------------------------------------------
live_phrases = [
    # [팬미팅 MC - 7문항]
    {
        "scene": "팬미팅 MC",
        "jp": "マジで？嘘でしょ！",
        "literal": "정말입니까? 거짓말이겠죠!",
        "pro": "진짜요?! 거짓말! / 헐 대박!",
        "keywords": ["진짜", "거짓말", "대박", "헐", "실화"]
    },
    {
        "scene": "팬미팅 MC",
        "jp": "最高かよ！みんな愛してるぞ！",
        "literal": "최고입니까! 모두 사랑한다!",
        "pro": "완전 최고잖아! 다들 진짜 사랑해!",
        "keywords": ["최고", "사랑해", "미쳤다", "짱"]
    },
    {
        "scene": "팬미팅 MC",
        "jp": "後ろの席までちゃんと見えてるからね〜！",
        "literal": "뒤의 자리까지 제대로 보이고 있으니까요~!",
        "pro": "2층, 3층 맨 뒷자리까지 다 잘 보이고 있어요~!",
        "keywords": ["뒷자리", "뒤", "보이", "끝까지", "다"]
    },
    {
        "scene": "팬미팅 MC",
        "jp": "今日のために日本語めっちゃ勉強してきました！",
        "literal": "오늘을 위해 일본어를 몹시 공부해 왔습니다!",
        "pro": "오늘 여러분 만나려고 일본어 진짜 열심히 공부해 왔어요!",
        "keywords": ["공부", "열심히", "준비", "오늘", "일본어"]
    },
    {
        "scene": "팬미팅 MC",
        "jp": "えっ、もう最後の曲？時間経つの早すぎない？",
        "literal": "엣, 벌써 마지막 곡? 시간 지나는 것 너무 빠르지 않나요?",
        "pro": "헐, 벌써 마지막 곡이라고요? 시간 진짜 순삭이네요!",
        "keywords": ["벌써", "마지막", "시간", "순삭", "빠르", "빨리"]
    },
    {
        "scene": "팬미팅 MC",
        "jp": "みんなの歓声がすごすぎて鳥肌立った！",
        "literal": "모두의 환성이 너무 대단해서 닭살이 돋았다!",
        "pro": "여러분 함성 소리가 너무 커서 소름 돋았어요!",
        "keywords": ["함성", "환호", "소름", "대단", "소리", "응원"]
    },
    {
        "scene": "팬미팅 MC",
        "jp": "今日帰ったら絶対夢に出てくると思う！",
        "literal": "오늘 돌아가면 절대 꿈에 나온다고 생각합니다!",
        "pro": "오늘 집에 가면 무조건 꿈에 나올 것 같아요!",
        "keywords": ["꿈", "집", "무조건", "오늘", "꼭"]
    },

    # [예능 토크 - 7문항]
    {
        "scene": "예능 토크",
        "jp": "いや、それヤバいって！草生えるわ。",
        "literal": "아니, 그것은 위험하다고! 풀이 자라네요.",
        "pro": "아니 그건 좀 선 넘었지! 개웃기네 진짜ㅋㅋ",
        "keywords": ["웃기", "미쳤", "선 넘", "대박", "ㅋㅋ", "장난"]
    },
    {
        "scene": "예능 토크",
        "jp": "ちょっと待って、話盛ってない？",
        "literal": "잠깐 기다려, 이야기를 쌓고 있지 않나요?",
        "pro": "잠깐만요, 지금 MSG 좀 치신 거 아니에요?",
        "keywords": ["잠깐", "과장", "뻥", "거짓말", "msg", "지어", "부풀"]
    },
    {
        "scene": "예능 토크",
        "jp": "いやいや、今の絶対カットしてください！",
        "literal": "아니아니, 지금의 것 절대 컷 해주세요!",
        "pro": "아니 잠깐만요, 방금 건 무조건 편집해 주세요!",
        "keywords": ["편집", "컷", "잘라", "방금", "지금", "무조건"]
    },
    {
        "scene": "예능 토크",
        "jp": "ちょっと！今の完全に黒歴史確定じゃん！",
        "literal": "잠깐! 지금의 것 완전히 흑역사 확정이잖아!",
        "pro": "잠깐만요! 방금 건 완전 흑역사 박제잖아요!",
        "keywords": ["흑역사", "박제", "확정", "방금", "망했"]
    },
    {
        "scene": "예능 토크",
        "jp": "空気読めよ！今そういう流れじゃないでしょ！",
        "literal": "공기를 읽어라! 지금 그런 흐름이 아니잖아요!",
        "pro": "눈치 좀 챙겨! 지금 그런 분위기 아니잖아요!",
        "keywords": ["눈치", "분위기", "흐름", "지금", "파악"]
    },
    {
        "scene": "예능 토크",
        "jp": "ハードル上げすぎだって！プレッシャー半端ないわ！",
        "literal": "허들을 너무 올렸다고! 프레셔가 어중간하지 않네요!",
        "pro": "기대치를 너무 높여놨잖아요! 부담감 장난 아니네!",
        "keywords": ["기대", "부담", "장난", "허들", "압박", "높"]
    },
    {
        "scene": "예능 토크",
        "jp": "奇跡起きた！これ神回決定でしょ！",
        "literal": "기적이 일어났다! 이것 신회 결정이겠죠!",
        "pro": "미쳤다 기적 일어났어! 오늘 완전 레전드 편 확정이죠!",
        "keywords": ["기적", "레전드", "대박", "확정", "최고", "역대급"]
    },

    # [인터뷰 - 7문항]
    {
        "scene": "인터뷰",
        "jp": "言葉にできないくらい胸がいっぱいです。",
        "literal": "말로 할 수 없을 정도로 가슴이 가득 찼습니다.",
        "pro": "말로 다 표현 못 할 만큼 벅차오릅니다.",
        "keywords": ["말로", "표현", "벅차", "가슴", "감동"]
    },
    {
        "scene": "인터뷰",
        "jp": "初心を忘れずに、これからも突き進みます！",
        "literal": "초심을 잊지 않고, 앞으로도 돌진합니다!",
        "pro": "초심 잃지 않고, 앞으로도 거침없이 달려나가겠습니다!",
        "keywords": ["초심", "앞으로", "달려", "나아가", "열심히", "돌진"]
    },
    {
        "scene": "인터뷰",
        "jp": "壁にぶつかることもありましたが、メンバーが支えてくれました。",
        "literal": "벽에 부딪히는 일도 있었습니다만, 멤버가 지탱해 주었습니다.",
        "pro": "힘든 고비도 있었지만, 멤버들이 든든하게 버팀목이 되어 주었습니다.",
        "keywords": ["힘든", "고비", "벽", "멤버", "버팀목", "지탱", "덕분", "의지"]
    },
    {
        "scene": "인터뷰",
        "jp": "今回のアルバムは僕たちの新しい挑戦が詰まっています。",
        "literal": "이번 앨범은 우리들의 새로운 도전이 차 있습니다.",
        "pro": "이번 앨범에는 저희만의 새로운 도전이 꽉꽉 담겨 있습니다.",
        "keywords": ["앨범", "새로운", "도전", "담겨", "가득", "이번"]
    },
    {
        "scene": "인터뷰",
        "jp": "期待に応えられるよう、さらに進化した姿をお見せします。",
        "literal": "기대에 부응할 수 있도록, 더욱 진화한 모습을 보여드리겠습니다.",
        "pro": "기대에 보답할 수 있도록 한층 더 성장한 모습 보여드리겠습니다.",
        "keywords": ["기대", "보답", "부응", "성장", "진화", "모습", "발전"]
    },
    {
        "scene": "인터뷰",
        "jp": "何気ない日常の風景から曲のインスピレーションを受けました。",
        "literal": "아무렇지 않은 일상의 풍경으로부터 곡의 인스피레이션을 받았습니다.",
        "pro": "평범한 일상의 풍경 속에서 곡의 영감을 얻었습니다.",
        "keywords": ["일상", "풍경", "영감", "평범", "곡", "음악"]
    },
    {
        "scene": "인터뷰",
        "jp": "ファンの皆さんの笑顔が、僕たちがステージに立つ理由です。",
        "literal": "팬 여러분의 웃는 얼굴이, 우리들이 스테이지에 서는 이유입니다.",
        "pro": "팬분들의 미소가 바로 저희가 무대에 서는 이유입니다.",
        "keywords": ["팬", "미소", "웃음", "무대", "이유", "스테이지"]
    }
]

# ---------------------------------------------------------
# 2. 함수 (def) 및 3. 조건문 (if-elif-else)
# ---------------------------------------------------------
def evaluate_interpretation(scene_type, difficulty_level, user_answer, target_data):
    base_score = 50
    bonus_msg = ""

    # 키워드 매칭 기본 점수 계산
    matched = False
    for kw in target_data["keywords"]:
        if kw in user_answer:
            matched = True
            break

    if matched:
        base_score += 20
    elif len(user_answer.strip()) > 3:
        base_score += 10
    else:
        return 30, "앗, 멘트가 너무 짧아요! 현장의 텐션을 살려 다시 통역해 볼까요? 😅"

    # 기획서 조건문(if-elif-else) 반영
    if difficulty_level >= 4:
        base_score += 25
        bonus_msg = "⚡ [속사포 현장 경고 돌파!] 고난도 텐션까지 완벽하게 캐치했습니다!"
    elif scene_type == "팬미팅 MC":
        base_score += 15
        bonus_msg = "💖 [팬 소통 뉘앙스 보너스!] 팬들의 심장을 저격하는 찰떡 통역이에요!"
    else:
        base_score += 10
        bonus_msg = "🎙️ [안정적인 현장 톤앤매너] 방송/인터뷰 분위기에 딱 맞는 자연스러운 전달입니다!"

    # 최종 점수 상한선 처리 (최대 100점)
    final_score = min(base_score, 100)

    if final_score >= 90:
        feedback = f"🔥 현장 분위기 살리기 성공! 찰떡 통역! ({bonus_msg})"
    elif final_score >= 70:
        feedback = f"👍 매끄러운 통역이에요! 조금만 더 말맛을 살려볼까요? ({bonus_msg})"
    else:
        feedback = f"💦 아쉽다! 교과서 직역 느낌이에요. 현장의 텐션을 더 올려보세요!"

    return final_score, feedback


# ---------------------------------------------------------
# UI 레이아웃 구성
# ---------------------------------------------------------
st.title("🎤⚡ 현장 통역 순발력 챌린지 (JP ↔ KR)")
st.caption("교과서 일본어는 그만! 최애의 텐션과 현장 말맛을 살리는 실시간 통역 트레이너")
st.divider()

# (1) 현장 상황 선택 & (2) 난이도 선택
col1, col2 = st.columns(2)
with col1:
    scene_type = st.selectbox(
        "(1) 현장 상황 선택",
        ["팬미팅 MC", "예능 토크", "인터뷰"]
    )
with col2:
    difficulty_level = st.slider(
        "(2) 난이도 선택 (속도 & 텐션)",
        min_value=1, max_value=5, value=3,
        format="Lv.%d"
    )

# 선택한 상황에 맞는 문제 필터링
filtered_phrases = [p for p in live_phrases if p["scene"] == scene_type]

# 세션 상태를 이용해 현재 문제 유지 및 변경
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0

# 상황이 바뀌면 인덱스 초기화
if st.session_state.get("last_scene") != scene_type:
    st.session_state.current_idx = 0
    st.session_state.last_scene = scene_type

q_num = (st.session_state.current_idx % len(filtered_phrases)) + 1
current_phrase = filtered_phrases[st.session_state.current_idx % len(filtered_phrases)]

# 제시어 박스 출력
st.info(f"🎧 **[현장 음성 수신 #{q_num}/{len(filtered_phrases)} - Lv.{difficulty_level}]**\n\n### 「 {current_phrase['jp']} 」")

if st.button("🔄 다른 멘트 듣기"):
    st.session_state.current_idx += 1
    st.rerun()

# (3) 내 순발력 답변 입력
user_answer = st.text_input(
    "(3) 내 순발력 답변 입력",
    placeholder="현장의 텐션과 말맛을 살려 통역해 보세요!"
)

# 판정 버튼 및 결과 출력 화면
if st.button("🚀 통역 판정하기!", type="primary", use_container_width=True):
    if not user_answer.strip():
        st.warning("통역할 한국어 멘트를 먼저 입력해 주세요!")
    else:
        st.divider()
        st.subheader("📋 통역 판정 결과")

        # 함수 호출
        score, message = evaluate_interpretation(
            scene_type, difficulty_level, user_answer, current_phrase
        )

        # 랭크 산정
        if score >= 90:
            rank = "S랭크 (프로 통역사급)"
        elif score >= 75:
            rank = "A랭크 (현장 에이스)"
        elif score >= 60:
            rank = "B랭크 (통역 유망주)"
        else:
            rank = "C랭크 (직역 탈출 필요)"

        # 결과 1: 텍스트 메시지
        st.success(message)

        # 결과 2: 강조 수치 (Metric)
        st.metric(
            label="순발력 랭크 점수",
            value=f"{score}점 / {rank}",
            delta=f"난이도 Lv.{difficulty_level} 반영"
        )

        # 결과 3: 4. 반복문 (for)을 활용한 실전 뉘앙스 비교표 (DataFrame)
        st.markdown("#### 📊 상황별 실전 뉘앙스 비교표")
        table_rows = []
        for item in live_phrases:
            table_rows.append({
                "상황": item["scene"],
                "현장 일본어": item["jp"],
                "직역 (딱딱함)": item["literal"],
                "통역사 추천 (살아있는 표현)": item["pro"]
            })

        df = pd.DataFrame(table_rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
