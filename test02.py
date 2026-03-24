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
st.caption(f"현재시간: {now.strftime('%Y-%m-%d %H:%M')}")

# -----------------------------
# 1. 기본 정보 (전화 받자마자)
# -----------------------------
st.subheader("📌 기본 정보")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("고인 성함")
    relation = st.text_input("신고자 관계")

with col2:
    death = st.text_input("사망일시")
    phone = st.text_input("연락처")

rrn = st.text_input("주민번호 (없으면 생략 가능)")

# -----------------------------
# 2. 등록 확인 (현실 반영)
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
    st.info("👉 장기기증 상담 또는 일반 장례 안내")
    st.stop()

# -----------------------------
# 3. 진행 상황 선택 (핵심)
# -----------------------------
st.subheader("🚦 진행 상황 선택")

case = st.radio(
    "현재 상황",
    ["즉시모심", "장례 진행", "장례 미정"],
    horizontal=True
)

# -----------------------------
# 4. 야간 판단
# -----------------------------
is_night = now.hour < 9 or now.hour >= 18

# -----------------------------
# 5. 상황별 대응
# -----------------------------
st.subheader("🧠 자동 대응 결과")

if case == "즉시모심":
    st.success("✅ 즉시 접수 진행")

    st.info(f"""
✔ 확인 사항
- 사체검안서
- 위치 (운구 장소)
- 연락처

✔ 멘트
"즉시 모실 수 있도록 접수 진행하겠습니다."

{'⚠ 야간: 기본 접수 후 담당자 전달 필수' if is_night else ''}
    """)

elif case == "장례 진행":
    st.success("✅ 장례 후 인계 진행")

    st.info(f"""
✔ 확인 사항
- 장례식장
- 발인 시간

✔ 멘트
"발인 시점에 시신 인계가 진행됩니다."

{'⚠ 야간: 일정만 확인 후 주간 재안내' if is_night else ''}
    """)

elif case == "장례 미정":
    st.warning("⚠ 접수 유보")

    st.info("""
✔ 안내 멘트
"장례 절차 확정 후 접수 진행이 가능합니다."

✔ 필요 사항
- 사체검안서
- 장례식장 결정

✔ 마무리 멘트
"확정 후 다시 연락 부탁드립니다."
    """)

# -----------------------------
# 6. 상황별 멘트 버튼
# -----------------------------
st.subheader("📞 빠른 멘트")

col1, col2, col3, col4, col5 = st.columns(5)

if col1.button("관계 확인"):
    st.code("고인과 어떤 관계이신가요?")

if col2.button("검안서 안내"):
    st.code("자택 사망의 경우 사체검안서가 필요합니다.")

if col3.button("장례 안내"):
    st.code("장례 후 발인 시점에 시신 인계가 진행됩니다.")

if col4.button("유보 안내"):
    st.code("장례 절차 확정 후 다시 연락 부탁드립니다.")

if col5.button("🌙 야간 멘트"):
    st.code("""
현재 담당자가 퇴근하여 자세한 상담은 어렵습니다.
기본 접수 후 평일 오전에 다시 안내드리겠습니다.
    """)

# -----------------------------
# 7. 접수 결과 자동 생성
# -----------------------------
st.subheader("📤 접수 내용 (복사용)")

summary = f"""
[시신기증 접수]

성함: {name}
관계: {relation}
사망일시: {death}
연락처: {phone}
주민번호: {rrn}
등록상태: {registered}
진행상황: {case}
접수시간: {now.strftime('%Y-%m-%d %H:%M')}
"""

st.text_area("복사해서 전달하세요", summary, height=220)

# -----------------------------
# 8. 디버그
# -----------------------------
st.divider()
st.caption("🔧 시스템 상태")

st.write({
    "registered": registered,
    "case": case,
    "is_night": is_night,
    "time": now.strftime("%H:%M")
})