import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

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

registered = st.radio("사전등록 여부", ["확인됨", "등록했다고 함", "미등록"])

if registered == "미등록":
    st.error("❌ 시신기증 불가")
    st.stop()

# -----------------------------
# 상황 선택
# -----------------------------
st.subheader("🚦 진행 상황")

case = st.radio("현재 상황", ["즉시모심", "장례 진행", "장례 미정"])

# -----------------------------
# 대응
# -----------------------------
st.subheader("🧠 대응 결과")

if case == "즉시모심":
    if is_night:
        st.error("🚨 야간 즉시모심")
        st.info("위치 확보 후 담당자 전달 필수")
    else:
        st.success("즉시 접수 진행")

elif case == "장례 진행":
    st.success("장례 후 인계")

elif case == "장례 미정":
    st.warning("접수 유보")
    st.info("장례 확정 후 재연락")

# -----------------------------
# 접수 내용
# -----------------------------
st.subheader("📤 접수")

summary = f"""
성함: {name}
관계: {relation}
사망일시: {death}
연락처: {phone}
상황: {case}
"""

st.text_area("복사", summary)