import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")
now = datetime.now(KST)

st.set_page_config(layout="wide")

st.title("🚨 시신기증 접수 도구")

# --- 상태 판단 ---
st.subheader("📌 상태")

col1, col2, col3 = st.columns(3)
accident = col1.checkbox("사고사")
infection = col2.checkbox("전염병")
family_refuse = col3.checkbox("유가족 반대")

if accident or infection or family_refuse:
    st.error("❌ 기증 불가")
    status = "불가"
else:
    st.success("✅ 진행 가능")
    status = "가능"

# --- 입력 ---
st.subheader("📝 접수 정보")

name = st.text_input("성함")
death = st.text_input("사망일시")
location = st.text_input("장소")
phone = st.text_input("연락처")

# --- 멘트 ---
st.subheader("📞 멘트 버튼")

col1, col2, col3 = st.columns(3)

if col1.button("관계 확인"):
    st.code("고인과 어떤 관계이신가요?")

if col2.button("야간 안내"):
    st.code("현재 담당자가 퇴근하여 평일 09:30 이후 연락 부탁드립니다.")

if col3.button("검안서 안내"):
    st.code("사체검안서가 필요합니다.")

# --- 결과 생성 ---
st.subheader("📤 접수 결과")

result = f"""
[시신기증 접수]

상태: {status}
성함: {name}
사망일시: {death}
장소: {location}
연락처: {phone}
"""

st.text_area("복사용", result, height=200)

if st.button("📋 전체 복사"):
    st.success("복사해서 사용하세요")