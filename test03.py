import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

# -----------------------------
# AI 설정 (최신 방식)
# -----------------------------
try:
    from openai import OpenAI
    client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="시신기증 접수 도구", layout="wide")

KST = ZoneInfo("Asia/Seoul")
now = datetime.now(KST)
is_night = now.hour < 9 or now.hour >= 18

# -----------------------------
# 타이틀
# -----------------------------
st.title("🚨 시신기증 접수 대응 도구")
st.caption(f"현재시간: {now.strftime('%Y-%m-%d %H:%M')}")

# -----------------------------
# 1. 기본 정보
# -----------------------------
st.subheader("📌 기본 정보")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("고인 성함")
    relation = st.text_input("관계")

with col2:
    death = st.text_input("사망일시")
    phone = st.text_input("연락처")

rrn = st.text_input("주민번호 (없으면 생략 가능)")

# -----------------------------
# 2. 등록 상태
# -----------------------------
st.subheader("📋 등록 상태")

registered = st.radio(
    "사전등록 여부",
    ["확인됨", "등록했다고 함 (증빙 없음)", "미등록"],
    horizontal=True
)

if registered == "등록했다고 함 (증빙 없음)":
    st.info("👉 주민번호로 조회 후 접수 진행 가능")

if registered == "미등록":
    st.error("❌ 사전 등록이 없어 시신기증 불가")
    st.stop()

# -----------------------------
# 3. 상황 선택
# -----------------------------
st.subheader("🚦 진행 상황")

case = st.radio(
    "현재 상황",
    ["즉시모심", "장례 진행", "장례 미정"],
    horizontal=True
)

# -----------------------------
# 4. 대응 결과
# -----------------------------
st.subheader("🧠 자동 대응")

if case == "즉시모심":
    st.success("✅ 즉시 접수 진행")
    st.info(f"""
- 사체검안서 확인
- 위치 확인
- 연락처 확보

"즉시 모실 수 있도록 접수 진행하겠습니다."

{'⚠ 야간: 기본 접수 후 담당자 전달' if is_night else ''}
""")

elif case == "장례 진행":
    st.success("✅ 장례 후 인계 진행")
    st.info(f"""
- 장례식장 확인
- 발인 시간 확인

"발인 시점에 시신 인계가 진행됩니다."

{'⚠ 야간: 일정만 확인 후 주간 안내' if is_night else ''}
""")

elif case == "장례 미정":

    st.error("⚠ 장례 절차 미정 → 접수 유보")

    st.info("""
장례 절차 확정 후 접수 진행이 가능합니다.

필요 사항:
- 사체검안서
- 장례식장 결정
""")

    # -----------------------------
    # 질문 버튼
    # -----------------------------
    st.subheader("❓ 빠른 질문 대응")

    col1, col2, col3 = st.columns(3)

    if col1.button("비용"):
        st.code("장례 비용은 유가족 부담입니다.\n→ 확정 후 다시 연락 부탁드립니다.")

    if col2.button("절차"):
        st.code("장례 후 발인 시 인계됩니다.\n→ 일정 확정 후 다시 연락 부탁드립니다.")

    if col3.button("종교"):
        st.code("종교와 무관합니다.\n→ 절차 확정 후 안내드립니다.")

    col4, col5, col6 = st.columns(3)

    if col4.button("관/수의"):
        st.code("필수 아닙니다.\n→ 장례 방식 확정 후 안내드립니다.")

    if col5.button("가능 여부"):
        st.code("조건 확인 필요합니다.\n→ 확정 후 접수 진행됩니다.")

    if col6.button("가족 동의"):
        st.code("유가족 동의 필요합니다.\n→ 협의 후 연락 부탁드립니다.")

    if st.button("🚨 종료 멘트"):
        st.code("""
현재 장례 절차가 확정되지 않아 접수 진행이 어렵습니다.
확정 후 다시 연락 부탁드립니다.
""")

    # -----------------------------
    # 🤖 AI 자동 응답
    # -----------------------------
    st.subheader("🤖 AI 자동 응답")

    if not AI_AVAILABLE:
        st.warning("⚠ AI 기능 사용 불가 (openai 미설치 또는 API 키 없음)")
    else:
        question = st.text_input("질문 입력")

        def generate_ai(q):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """
시신기증 상담 보조 시스템.
짧고 명확하게 답변.
확정되지 않은 내용은 말하지 말 것.
마지막 문장은 반드시:
'확정 후 다시 연락 부탁드립니다.'
"""
                    },
                    {"role": "user", "content": q}
                ],
                temperature=0.2
            )
            return response.choices[0].message.content

        if st.button("AI 답변 생성"):
            if question:
                try:
                    answer = generate_ai(question)
                    st.success(answer)

                    # 복사용
                    st.text_area("복사용", answer, height=120)

                except Exception as e:
                    st.error(f"AI 오류: {e}")

# -----------------------------
# 5. 접수 요약
# -----------------------------
st.subheader("📤 접수 내용")

summary = f"""
[시신기증 접수]

성함: {name}
관계: {relation}
사망일시: {death}
연락처: {phone}
주민번호: {rrn}
등록상태: {registered}
상황: {case}
접수시간: {now.strftime('%Y-%m-%d %H:%M')}
"""

st.text_area("복사해서 전달하세요", summary, height=220)

# -----------------------------
# 디버그
# -----------------------------
st.divider()
st.caption("🔧 시스템 상태")

st.write({
    "registered": registered,
    "case": case,
    "is_night": is_night,
    "ai_available": AI_AVAILABLE
})