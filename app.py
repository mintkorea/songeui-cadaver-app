import streamlit as st
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# 1. 모바일 맞춤형 스타일 설정
st.set_page_config(page_title="시신기증 접수", layout="centered")
st.markdown("""
    <style>
    /* 전체 폰트 크기 조절 */
    html, body, [class*="st-"] { font-size: 1.05rem; }
    /* 버튼 크기 및 가독성 강화 */
    .stButton>button { 
        width: 100%; 
        height: 3.5rem; 
        border-radius: 10px; 
        font-weight: bold; 
        margin-bottom: 5px;
    }
    /* 라디오 버튼 간격 */
    div[data-testid="stMarkdownContainer"] > p { font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 다음 주소 검색 팝업 스크립트
def addr_search_js():
    return """
    <script src="//t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js"></script>
    <script>
        function openAddrSearch() {
            new daum.Postcode({
                oncomplete: function(data) {
                    const addr = data.roadAddress || data.address;
                    window.parent.postMessage({
                        type: 'address_selected',
                        address: addr,
                        building: data.buildingName
                    }, '*');
                }
            }).open();
        }
    </script>
    <button onclick="openAddrSearch()" style="width:100%; height:3.5rem; background-color:#4CAF50; color:white; border:none; border-radius:10px; font-weight:bold; cursor:pointer;">
        📍 건물명 / 주소 찾기
    </button>
    """

st.title("🚨 시신기증 야간 접수")
st.info("보고처: 김보라 선임 (010-8073-0527)")

# 2. 고인 정보 섹션
with st.expander("👤 1. 고인 정보", expanded=True):
    name = st.text_input("고인 성함")
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    reg_num = st.text_input("등록번호", placeholder="모를 경우 공란")

    today = datetime.now()
    yesterday = today - timedelta(days=1)

    st.write("사망일자")
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        if st.button(f"어제 ({yesterday.strftime('%m/%d')})"):
            st.session_state['death_date'] = yesterday
    with d_col2:
        if st.button(f"오늘 ({today.strftime('%m/%d')})"):
            st.session_state['death_date'] = today
    
    death_date = st.date_input("날짜 확인", value=st.session_state.get('death_date', today))
    
    t_col1, t_col2 = st.columns([1, 2])
    with t_col1:
        ampm = st.radio("구분", ["오전", "오후"], horizontal=True)
    with t_col2:
        death_time = st.time_input("시간", label_visibility="collapsed")
    
    death_place = st.text_input("사망 장소 (기록용)", placeholder="병원명/장례식장 호실")

# 3. 장례 일정 및 장소
with st.expander("🚚 2. 장례 일정 및 운구 장소", expanded=True):
    is_immediate = st.toggle("즉시 모심 (장례 없음)")
    
    if not is_immediate:
        days = st.radio("장례 기간", ["2일장", "3일장", "4일장", "기타"], index=1, horizontal=True)
        
        st.write("발인 예정일")
        b_col1, b_col2, b_col3 = st.columns(3)
        tomorrow = today + timedelta(days=1)
        day_after = today + timedelta(days=2)
        with b_col1:
            if st.button(f"내일"): st.session_state['burn_date'] = tomorrow
        with b_col2:
            if st.button(f"모레"): st.session_state['burn_date'] = day_after
        with b_col3:
            burn_date = st.date_input("직접", value=st.session_state.get('burn_date', day_after), label_visibility="collapsed")
        
        bt_col1, bt_col2 = st.columns([1, 2])
        with bt_col1:
            burn_ampm = st.radio("발인 구분", ["오전", "오후"], horizontal=True)
        with bt_col2:
            burn_time = st.time_input("발인 시간", label_visibility="collapsed")

    st.write("모시러 갈 장소")
    components.html(addr_search_js(), height=65)
    pickup_place = st.text_input("검색된 주소 / 상세 주소", placeholder="건물명이나 상세 호수 입력")

# 4. 유가족 정보
with st.expander("📞 3. 유가족 정보", expanded=True):
    u_name = st.text_input("유가족 성함")
    u_relation = st.selectbox("고인과의 관계", ["자(아들)", "녀(딸)", "배우자", "부모", "형(오빠)", "제(남동생)", "누나(언니)", "매(여동생)", "기타"])
    u_phone = st.text_input("유가족 연락처", placeholder="010-0000-0000")

# 5. 사진 촬영 및 보고
st.divider()
st.subheader("📸 4. 접수증 촬영 및 보고")
captured_img = st.camera_input("접수증 촬영")

summary = f"""[야간접수 보고]
고인: {name}({gender}) / 등록: {reg_num if reg_num else '확인불가'}
사망: {death_date.strftime('%m/%d')} {ampm} {death_time.strftime('%H:%M')}
장례: {"즉시모심" if is_immediate else f"{days}(발인: {burn_date.strftime('%m/%d') if 'burn_date' in locals() else ''} {burn_ampm if 'burn_ampm' in locals() else ''} {burn_time.strftime('%H:%M') if 'burn_time' in locals() else ''})"}
모시러 갈 곳: {pickup_place}
보호자: {u_name}({u_relation}) / {u_phone}
사망장소: {death_place}"""

if st.button("🚀 김보라 선임에게 보낼 데이터 생성"):
    if not name or not u_phone or not pickup_place:
        st.error("고인 성함, 모시러 갈 장소, 보호자 연락처를 입력하세요.")
    else:
        st.success("데이터 구성 완료! 아래 내용을 복사하세요.")
        st.code(summary)
