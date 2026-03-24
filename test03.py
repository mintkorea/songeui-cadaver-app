import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
import os

# -----------------------------
# AI 설정 (안전)
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
st.title("🚨 시신기증 접수 대응 시스템")
st.caption(f"현재시간: {now.strftime('%Y-%m-%d %H:%M')}")

# -----------------------------
# 기본 정보
# -----------------------------
st.subheader("📌 기본 정보")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("고인 성함")
    relation = st.text_input("관계")

with col2:
    death = st.text_input("사망일시")
    phone = st.text_input("연락처")

rrn = st.text_input("주민번호")

# -----------------------------
# 등록 상태
# -----------------------------
st.subheader("📋 등록 상태")

registered = st.radio(
    "사전등록 여부",
    ["확인됨", "등록했다고 함", "미등록"],
    horizontal=True
)

if registered == "미등록":
    st.error("❌ 시신기증 불가")
    st.stop()

# -----------------------------
# 상황 선택
# -----------------------------
st.subheader("🚦 진행 상황")

case = st.radio(
    "현재 상황",
    ["즉시모심", "장례 진행", "장례 미정"],
    horizontal=True
)

# -----------------------------
# 긴급 표시
# -----------------------------
if case == "즉시모심" and is_night:
    st.error("🚨 긴급: 야간 즉시모심 → 즉시 전달 필요")

# -----------------------------
# 대응 결과
# -----------------------------
st.subheader("🧠 대응")

if case == "즉시모심":
    st.success("즉시 접수 진행")
    st.info("위치 / 검안서 / 연락처 확인 후 즉시 전달")

elif case == "장례 진행":
    st.success("장례 후 인계 진행")
    st.info("장례식장 및 발인 시간 확인")

elif case == "장례 미정":
    st.warning("접수 유보")
    st.info("장례 확정 후 재연락 필요")

    # -----------------------------
    # 빠른 대응 버튼
    # -----------------------------
    st.subheader("❓ 빠른 대응")

    if st.button("비용"):
        st.code("장례 비용은 유가족 부담입니다.\n→ 확정 후 다시 연락 부탁드립니다.")

    if st.button("절차"):
        st.code("장례 후 발인 시 인계됩니다.\n→ 일정 확정 후 다시 연락 부탁드립니다.")

    if st.button("종료 멘트"):
        st.code("장례 절차 확정 후 다시 연락 부탁드립니다.")

    # -----------------------------
    # AI 자동 응답
    # -----------------------------
    st.subheader("🤖 AI 자동 응답")

    if not AI_AVAILABLE:
        st.warning("AI 기능 비활성화 상태")
    else:
        question = st.text_input("질문 입력")

        if st.button("AI 답변 생성"):
            if question:
                try:
                    res = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "짧고 명확하게 답변하고 마지막에 반드시 '다시 연락 부탁드립니다.' 포함"},
                            {"role": "user", "content": question}
                        ],
                        temperature=0.2
                    )
                    answer = res.choices[0].message.content
                    st.success(answer)
                except Exception as e:
                    st.error(e)

# -----------------------------
# 카톡 메시지
# -----------------------------
st.subheader("📲 카톡 전달")

kakao_msg = f"""
[시신기증 접수]

성함: {name}
관계: {relation}
사망일시: {death}
연락처: {phone}
상황: {case}
시간: {now.strftime('%Y-%m-%d %H:%M')}
"""

st.text_area("복사", kakao_msg, height=200)

# -----------------------------
# 접수 저장
# -----------------------------
st.subheader("📊 접수 저장")

if st.button("💾 접수 저장"):
    if not name or not phone:
        st.warning("필수 정보 부족")
    else:
        data = {
            "시간": now.strftime('%Y-%m-%d %H:%M'),
            "성함": name,
            "관계": relation,
            "사망일시": death,
            "연락처": phone,
            "주민번호": rrn,
            "등록상태": registered,
            "상황": case
        }

        df = pd.DataFrame([data])

        file = "접수로그.xlsx"

        if os.path.exists(file):
            old = pd.read_excel(file)
            new_df = pd.concat([old, df], ignore_index=True)
        else:
            new_df = df

        new_df.to_excel(file, index=False)

        st.success("저장 완료")

# -----------------------------
# 디버그
# -----------------------------
st.divider()
st.write({
    "case": case,
    "is_night": is_night,
    "ai": AI_AVAILABLE
})