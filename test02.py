import streamlit as st
from datetime import datetime
import json

st.set_page_config(page_title="시신기증 접수 앱", layout="wide")

# 상태 저장
if "step" not in st.session_state:
    st.session_state.step = 0

if "data" not in st.session_state:
    st.session_state.data = {}

# 메인 메뉴
st.title("📱 시신기증 접수 시스템")

menu = st.sidebar.radio("메뉴 선택", [
    "긴급 접수",
    "상담 매뉴얼",
    "절차 안내",
    "FAQ",
    "연락처"
])

# -------------------------
# 1. 긴급 접수
# -------------------------
if menu == "긴급 접수":

    st.header("🔴 긴급 접수")

    # STEP 1
    if st.session_state.step == 0:
        st.subheader("1. 등록 여부")
        if st.button("등록됨"):
            st.session_state.data["등록"] = True
            st.session_state.step = 1
        if st.button("등록 안됨"):
            st.error("❌ 시신기증 불가")
    
    # STEP 2
    elif st.session_state.step == 1:
        st.subheader("2. 유가족 여부")
        if st.button("유가족"):
            st.session_state.step = 2
        if st.button("아님"):
            st.error("❌ 접수 불가 (조장 연락)")
    
    # STEP 3
    elif st.session_state.step == 2:
        st.subheader("3. 사고사 여부")
        if st.button("예"):
            st.error("❌ 시신기증 불가")
        if st.button("아니오"):
            st.session_state.step = 3
    
    # STEP 4
    elif st.session_state.step == 3:
        st.subheader("4. 전염병 여부")
        if st.button("있음"):
            st.error("❌ 시신기증 불가")
        if st.button("없음"):
            st.session_state.step = 4

    # STEP 5 입력
    elif st.session_state.step == 4:
        st.subheader("5. 접수 정보 입력")

        name = st.text_input("고인 성함")
        rrn = st.text_input("주민번호")
        death_time = st.text_input("사망일시")
        cause = st.text_input("사망원인")
        location = st.text_input("위치")
        phone = st.text_input("연락처")

        if st.button("접수 완료"):
            st.session_state.data.update({
                "성함": name,
                "주민번호": rrn,
                "사망일시": death_time,
                "사망원인": cause,
                "위치": location,
                "연락처": phone,
                "시간": str(datetime.now())
            })
            st.session_state.step = 5

    # STEP 6 결과
    elif st.session_state.step == 5:
        st.success("✅ 접수 완료")

        st.json(st.session_state.data)

        st.download_button(
            "📄 접수 데이터 다운로드",
            json.dumps(st.session_state.data, ensure_ascii=False, indent=2),
            file_name="접수.json"
        )

# -------------------------
# 2. 상담 매뉴얼
# -------------------------
elif menu == "상담 매뉴얼":
    st.header("☎️ 상담 멘트")

    if st.button("관계 확인"):
        st.code("지금 전화주시는 분은 고인과 어떤 관계이신가요?")

    if st.button("야간 안내"):
        st.code("현재 담당자가 퇴근하여 평일 09:30 이후 연락 부탁드립니다.")

    if st.button("검안서 안내"):
        st.code("사체검안서를 발급받으셔야 합니다.")

# -------------------------
# 3. 절차 안내
# -------------------------
elif menu == "절차 안내":
    st.header("📋 시신기증 절차")

    st.markdown("""
    1. 등록
    2. 사망
    3. 장례
    4. 시신 인계
    5. 연구
    6. 화장
    """)

# -------------------------
# 4. FAQ
# -------------------------
elif menu == "FAQ":
    st.header("❓ FAQ")

    st.markdown("""
    - 유가족 반대 시 불가
    - 사고사 불가
    - 전염병 불가
    """)

# -------------------------
# 5. 연락처
# -------------------------
elif menu == "연락처":
    st.header("📞 연락처")

    st.write("총무팀: 2258-7135")
    st.write("담당자: 010-8073-0527")