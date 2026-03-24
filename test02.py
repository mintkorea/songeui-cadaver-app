import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")

st.set_page_config(page_title="시신기증 매뉴얼", layout="wide")

# 현재 시간
now = datetime.now(KST)
is_night = now.hour < 9 or now.hour >= 18

# 세션 상태
if "step" not in st.session_state:
    st.session_state.step = 0

# 메인 화면
if st.session_state.step == 0:
    st.title("📘 시신기증 대응 앱")

    if st.button("🚨 긴급 접수 시작"):
        st.session_state.step = 1

    if st.button("📞 상담 매뉴얼"):
        st.session_state.step = 100

# STEP 1
elif st.session_state.step == 1:
    st.header("STEP 1. 등록 여부")

    col1, col2 = st.columns(2)

    if col1.button("예"):
        st.session_state.step = 2
    if col2.button("아니오"):
        st.error("❌ 사전 등록이 없어 진행 불가")
        st.session_state.step = 0

# STEP 2
elif st.session_state.step == 2:
    st.header("STEP 2. 관계 확인")

    col1, col2 = st.columns(2)

    if col1.button("유가족"):
        st.session_state.step = 3
    if col2.button("기타"):
        st.error("❌ 유가족만 진행 가능")
        st.session_state.step = 0

# STEP 3
elif st.session_state.step == 3:
    st.header("STEP 3. 불가 사유 체크")

    accident = st.checkbox("사고사")
    infection = st.checkbox("전염성 질환")
    family_refuse = st.checkbox("유가족 반대")

    if st.button("다음"):
        if accident or infection or family_refuse:
            st.error("❌ 시신기증 불가")
            st.session_state.step = 0
        else:
            st.session_state.step = 4

# STEP 4
elif st.session_state.step == 4:
    st.header("STEP 4. 접수 입력")

    name = st.text_input("성함")
    rrn = st.text_input("주민번호")
    death_time = st.text_input("사망일시")
    cause = st.text_input("사망원인")
    location = st.text_input("장소")
    phone = st.text_input("연락처")

    if st.button("접수 완료"):
        st.session_state.data = {
            "성함": name,
            "주민번호": rrn,
            "사망일시": death_time,
            "사망원인": cause,
            "장소": location,
            "연락처": phone,
        }
        st.session_state.step = 5

# STEP 5
elif st.session_state.step == 5:
    st.header("✅ 접수 완료")

    st.json(st.session_state.data)

    st.success("담당자에게 전달하세요")

    if st.button("처음으로"):
        st.session_state.step = 0

# 상담 매뉴얼
elif st.session_state.step == 100:
    st.header("📞 상담 매뉴얼")

    if is_night:
        st.warning("🌙 야간 모드")

        st.info("""
        "현재 담당자가 퇴근하여
        자세한 상담은 어렵습니다.
        평일 09:30 이후 다시 연락 부탁드립니다."
        """)

    st.subheader("자주 사용하는 멘트")

    if st.button("관계 확인"):
        st.code("고인과 어떤 관계이신가요?")

    if st.button("사체검안서 안내"):
        st.code("사체검안서가 필요합니다.")

    if st.button("장례 안내"):
        st.code("장례 후 발인 시 인계됩니다.")

    if st.button("뒤로"):
        st.session_state.step = 0