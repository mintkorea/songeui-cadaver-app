import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

# 기본 설정
st.set_page_config(page_title="시신기증 대응", layout="wide")

KST = ZoneInfo("Asia/Seoul")
now = datetime.now(KST)

# -------------------------------
# 강제 화면 표시 (디버그)
# -------------------------------
st.title("🚨 시신기증 대응 도구")

st.write("현재시간:", now.strftime("%Y-%m-%d %H:%M:%S"))

# -------------------------------
# 상태 체크
# -------------------------------
st.subheader("📌 상태 판단")

col1, col2, col3 = st.columns(3)

accident = col1.checkbox("사고사")
infection = col2.checkbox("전염성 질환")
family_refuse = col3.checkbox("유가족 반대")

# 등록 여부
registered = st.radio("사전 등록 여부", ["예", "아니오"])

# -------------------------------
# 판단 로직
# -------------------------------
def generate_response():
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

result_status = generate_response()

# -------------------------------
# 결과 표시
# -------------------------------
st.subheader("🧠 자동 판단 결과")

if "❌" in result_status:
    st.error(result_status)
elif "⚠" in result_status:
    st.warning(result_status)
else:
    st.success(result_status)

# -------------------------------
# 입력 영역
# -------------------------------
st.subheader("📝 접수 정보")

name = st.text_input("성함")
death = st.text_input("사망일시")
location = st.text_input("장소")
phone = st.text_input("연락처")

# -------------------------------
# 멘트 버튼
# -------------------------------
st.subheader("📞 상황별 멘트")

col1, col2, col3 = st.columns(3)

if col1.button("관계 확인"):
    st.code("고인과 어떤 관계이신가요?")

if col2.button("야간 안내"):
    st.code("현재 담당자가 퇴근하여 평일 09:30 이후 연락 부탁드립니다.")

if col3.button("검안서 안내"):
    st.code("사체검안서가 필요합니다.")

# -------------------------------
# 접수 결과 생성
# -------------------------------
st.subheader("📤 접수 내용")

result_text = f"""
[시신기증 접수]

상태: {result_status}
성함: {name}
사망일시: {death}
장소: {location}
연락처: {phone}
"""

st.text_area("복사용", result_text, height=200)

# -------------------------------
# 디버그용 출력
# -------------------------------
st.divider()
st.caption("🔧 디버그 정보")

st.write({
    "registered": registered,
    "accident": accident,
    "infection": infection,
    "family_refuse": family_refuse,
})