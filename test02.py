import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="시신기증 대응 도구", layout="wide")

KST = ZoneInfo("Asia/Seoul")
now = datetime.now(KST)

# -----------------------------
# 판단 로직
# -----------------------------
def generate_response(registered, accident, infection, family_refuse):
    if registered == "아니오":
        return "❌ 사전 등록 없음 → 기증 불가"

    if accident:
        return "❌ 사고사 → 기증 불가"

    if infection:
        return "❌ 전염성 질환 → 기증 불가"

    if family_refuse:
        return "❌ 유가족 반대 → 기증 불가"

    if now.hour < 9 or now.hour >= 18:
        return "⚠ 야간 → 간단 접수 후 주간 상담 유도"

    return "✅ 정상 접수 가능"

# -----------------------------
# UI 시작
# -----------------------------
st.title("🚨 시신기증 접수 대응 도구")

st.caption(f"현재시간: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# -----------------------------
# 상태 입력
# -----------------------------
st.subheader("📌 상황 체크")

col1, col2, col3 = st.columns(3)

accident = col1.checkbox("사고사")
infection = col2.checkbox("전염성 질환")
family_refuse = col3.checkbox("유가족 반대")

registered = st.radio("사전 등록 여부", ["예", "아니오"], horizontal=True)

# -----------------------------
# 결과 (최상단 핵심)
# -----------------------------
result_status = generate_response(registered, accident, infection, family_refuse)

st.subheader("🧠 자동 판단 결과")

if "❌" in result_status:
    st.error(result_status)
    st.info("👉 '해당 경우는 시신기증이 어렵습니다.'")
elif "⚠" in result_status:
    st.warning(result_status)
    st.info("👉 '현재는 간단 접수 후 평일에 다시 안내드립니다.'")
else:
    st.success(result_status)
    st.info("👉 '접수 진행 도와드리겠습니다.'")

# -----------------------------
# 접수 정보 입력
# -----------------------------
st.subheader("📝 접수 정보 입력")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("성함")
    death = st.text_input("사망일시")

with col2:
    location = st.text_input("장소")
    phone = st.text_input("연락처")

# -----------------------------
# 멘트 버튼 (실전 핵심)
# -----------------------------
st.subheader("📞 상황별 멘트")

col1, col2, col3, col4 = st.columns(4)

if col1.button("관계 확인"):
    st.code("고인과 어떤 관계이신가요?")

if col2.button("야간 안내"):
    st.code("현재 담당자가 퇴근하여 자세한 상담은 어렵습니다. 평일 09:30 이후 연락 부탁드립니다.")

if col3.button("검안서 안내"):
    st.code("자택 사망의 경우 사체검안서가 필요합니다.")

if col4.button("장례 안내"):
    st.code("장례 후 발인 시점에 시신 인계가 진행됩니다.")

# -----------------------------
# 접수 결과 생성
# -----------------------------
st.subheader("📤 접수 내용 (복사용)")

result_text = f"""
[시신기증 접수]

상태: {result_status}
성함: {name}
사망일시: {death}
장소: {location}
연락처: {phone}
"""

st.text_area("복사해서 전달하세요", result_text, height=200)

# -----------------------------
# 디버그 (항상 하단 표시)
# -----------------------------
st.divider()
st.caption("🔧 시스템 상태")

st.write({
    "registered": registered,
    "accident": accident,
    "infection": infection,
    "family_refuse": family_refuse,
    "time": now.strftime("%H:%M")
})