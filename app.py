import streamlit as st
from datetime import datetime, timedelta

# 1. 초기 설정 및 스타일 (다크모드 및 모바일 최적화)
st.set_page_config(page_title="시신기증 야간접수", layout="centered")
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 3em; font-weight: bold; }
    .main { background-color: #121212; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚨 시신기증 야간 접수")
st.info("보고처: 김보라 선임 (010-8073-0527)")

# 2. 고인 정보 섹션
st.subheader("1. 고인 정보")
name = st.text_input("고인 성함")
gender = st.radio("성별 (필수)", ["남성", "여성"], horizontal=True)
reg_num = st.text_input("등록번호 (선택)", placeholder="모를 경우 공란")

# 날짜 퀵 버튼 로직
today = datetime.now()
yesterday = today - timedelta(days=1)

date_col1, date_col2, date_col3 = st.columns(3)
with date_col1:
    if st.button(f"어제\n({yesterday.strftime('%m/%d')})"):
        st.session_state['death_date'] = yesterday
with date_col2:
    if st.button(f"오늘\n({today.strftime('%m/%d')})"):
        st.session_state['death_date'] = today
with date_col3:
    death_date = st.date_input("날짜 직접선택", value=st.session_state.get('death_date', today))

# 시간 입력
time_col1, time_col2 = st.columns(2)
with time_col1:
    ampm = st.radio("구분", ["오전", "오후"], horizontal=True)
with time_col2:
    death_time = st.time_input("시간 선택")

death_place = st.text_input("사망 장소", placeholder="병원명/장례식장 호실")

---

# 3. 유가족 정보 섹션
st.subheader("2. 유가족(신고자) 정보")
u_name = st.text_input("유가족 성함")
u_relation = st.selectbox("고인과의 관계", 
    ["자(아들)", "녀(딸)", "배우자", "부모", "형(오빠)", "제(남동생)", "누나(언니)", "매(여동생)", "기타"])
u_phone = st.text_input("유가족 연락처", placeholder="010-0000-0000")

---

# 4. 장례 일정 섹션
st.subheader("3. 장례 일정")
is_immediate = st.toggle("즉시 모심 (장례 없음)")

if not is_immediate:
    days = st.radio("장례 일수", ["2일장", "3일장", "4일장", "기타"], index=1, horizontal=True)
    
    # 발인일 퀵 계산 (오늘/내일/모레/글피)
    tomorrow = today + timedelta(days=1)
    day_after = today + timedelta(days=2)
    two_days_after = today + timedelta(days=3)
    
    st.write("발인 예정일 선택")
    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        if st.button(f"내일\n({tomorrow.strftime('%m/%d')})"):
            st.session_state['burn_date'] = tomorrow
    with b_col2:
        if st.button(f"모레\n({day_after.strftime('%m/%d')})"):
            st.session_state['burn_date'] = day_after
    with b_col3:
        if st.button(f"글피\n({two_days_after.strftime('%m/%d')})"):
            st.session_state['burn_date'] = two_days_after
            
    burn_date = st.date_input("발인날짜 확인", value=st.session_state.get('burn_date', day_after))
    burn_time_ampm = st.radio("발인 시간 구분", ["오전", "오후"], horizontal=True, key="bt_ampm")
    burn_time = st.time_input("발인 시각")

---

# 5. 사진 촬영 및 보고
st.subheader("4. 최종 보고")
captured_img = st.camera_input("접수증 사진 촬영 (필수)")

# 보고 내용 요약 생성
summary = f"""[야간접수 보고]
고인: {name}({gender}) / 등록: {reg_num if reg_num else '확인불가'}
사망: {death_date.strftime('%m/%d')} {ampm} {death_time.strftime('%H:%M')}
장례: {"즉시모심" if is_immediate else f"{days}(발인: {burn_date.strftime('%m/%d')} {burn_time_ampm} {burn_time.strftime('%H:%M')})"}
보호자: {u_name}({u_relation}) / {u_phone}
장소: {death_place}"""

st.text_area("보고 내용 요약", summary, height=150)

if st.button("🚀 김보라 선임에게 보고 전송"):
    if not name or not u_phone or captured_img is None:
        st.error("성함, 연락처, 접수증 사진은 필수입니다.")
    else:
        # 실제 환경에서는 SMS API나 카카오톡 API 연동 구간
        st.success("메시지 구성 완료! 김보라 선임님께 전송합니다.")
        st.code(summary) # 복사하기 편하도록 코드블록 제공
