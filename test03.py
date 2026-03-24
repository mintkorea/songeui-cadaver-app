import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="시신기증 접수 도구", layout="wide")

KST = ZoneInfo("Asia/Seoul")
now = datetime.now(KST)

# -----------------------------
# 타이틀
# -----------------------------
st.title("🚨 시신기증 접수 대응 도구")

# -----------------------------
# 기본 정보
# -----------------------------
st.subheader("📌 기본 정보")

name = st.text_input("고인 성함")
relation = st.text_input("관계")
death = st.text_input("사망일시")
phone = st.text_input("연락처")
rrn = st.text_input("주민번호")

# -----------------------------
# 등록 상태
# -----------------------------
st.subheader("📋 등록 상태")

registered = st.radio(
    "사전등록 여부",
    ["확인됨", "등록했다고 함 (증빙 없음)", "미등록"]
)

if registered == "미등록":
    st.error("❌ 사전 등록이 없어 기증 불가")
    st.stop()

# -----------------------------
# 상황 선택
# -----------------------------
st.subheader("🚦 진행 상황")

case = st.radio(
    "현재 상황",
    ["즉시모심", "장례 진행", "장례 미정"]
)

# -----------------------------
# 상황별 처리
# -----------------------------
st.subheader("🧠 대응 결과")

if case == "즉시모심":
    st.success("✅ 즉시 접수 진행")

elif case == "장례 진행":
    st.success("✅ 장례 후 인계 진행")

elif case == "장례 미정":

    # 🔴 여기부터 장례 미정 UI
    st.error("⚠ 장례 절차 미정 → 접수 유보")

    st.info("""
장례 절차 확정 후 접수 진행이 가능합니다.
사체검안서 및 장례식장 결정이 필요합니다.
""")

    st.subheader("❓ 질문 대응")

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
# 결과 출력
# -----------------------------
st.subheader("📤 접수 내용")

summary = f"""
성함: {name}
관계: {relation}
사망일시: {death}
연락처: {phone}
주민번호: {rrn}
상황: {case}
"""

st.text_area("복사용", summary, height=200)

# -----------------------------
# 장례 미정 대응 모드
# -----------------------------
st.subheader("🚫 장례 미정 대응 모드")

st.error("⚠ 장례 절차 미정 → 접수 유보 상태")

st.info("""
✔ 핵심 안내
"장례 절차 확정 후 접수 진행이 가능합니다."

✔ 반드시 필요한 것
- 사체검안서
- 장례식장 결정
""")

# -----------------------------
# 질문 폭주 대응 버튼
# -----------------------------
st.subheader("❓ 자주 묻는 질문 대응")

col1, col2, col3 = st.columns(3)

# 비용 문의
if col1.button("💰 비용 문의"):
    st.code("""
장례 비용은 유가족 부담입니다.
장례식장에서 안내받으시면 됩니다.

→ 장례 확정 후 다시 연락 부탁드립니다.
""")

# 장례 절차
if col2.button("⚱ 장례 절차"):
    st.code("""
장례 절차 진행 후 발인 시 시신 인계가 이루어집니다.

→ 장례 일정 확정 후 다시 연락 부탁드립니다.
""")

# 종교
if col3.button("✝ 종교 관련"):
    st.code("""
종교와 관계없이 기증 가능합니다.

→ 절차 확정 후 다시 안내드리겠습니다.
""")

# -----------------------------
# 추가 질문 대응
# -----------------------------
col4, col5, col6 = st.columns(3)

# 관/수의
if col4.button("🪦 관/수의 필요 여부"):
    st.code("""
관과 수의는 필수 사항이 아닙니다.

→ 장례 방식 확정 후 다시 안내드립니다.
""")

# 가능 여부
if col5.button("❓ 기증 가능 여부"):
    st.code("""
사전 등록 여부 및 조건 확인이 필요합니다.

→ 장례 절차 확정 후 접수 가능합니다.
""")

# 가족 관련
if col6.button("👨‍👩‍👧 가족 동의"):
    st.code("""
유가족 동의가 반드시 필요합니다.

→ 가족 협의 후 다시 연락 부탁드립니다.
""")

# -----------------------------
# 강제 종료 멘트 (핵심)
# -----------------------------
st.subheader("📢 통화 종료 멘트")

if st.button("🚨 종료 멘트 출력"):
    st.code("""
현재 장례 절차가 확정되지 않아 접수 진행이 어렵습니다.
장례 일정과 장소 확정 후 다시 연락 부탁드립니다.
""")

import openai

# API 키 (Streamlit secrets 사용 권장)
openai.api_key = st.secrets.get("OPENAI_API_KEY")

st.subheader("🤖 AI 자동 응답 (질문 대응)")

user_question = st.text_input("질문 입력")

def generate_ai_response(question):
    prompt = f"""
당신은 시신기증 접수 상담 보조 시스템입니다.

규칙:
- 답변은 짧게 (3~4줄)
- 확정되지 않은 내용은 안내하지 말 것
- 반드시 마지막 줄에 종료 유도 문장 포함
- 감정 표현 없이 안내 중심

질문:
{question}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content

if st.button("답변 생성"):
    if user_question:
        try:
            answer = generate_ai_response(user_question)
            st.success(answer)
        except Exception as e:
            st.error(f"에러 발생: {e}")