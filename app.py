import streamlit as st
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# 1. 모바일 스타일 설정
st.set_page_config(page_title="시신기증 접수", layout="centered")
st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 1.05rem; }
    .stButton>button { width: 100%; height: 3.5rem; border-radius: 10px; font-weight: bold; }
    .status-box { 
        background-color: #262730; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #464b5d;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 다음 주소 검색 JS
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
                        address: addr
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

# 세션 상태 초기화
today = datetime.now().date()
if 'death_date' not in st.session_state: st.session_state['death_date'] = today
if 'burn_date' not in st.session_state: st.session_state['burn_date'] = today + timedelta(days=2)
if 'days_val' not in st.session_state: st.session_state['days_val'] = "3일장"

# 2. 고인 정보 섹션
with st.expander("👤 1. 고인 정보", expanded=True):
    name = st.text_input("고인 성함")
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    
    st.write("사망일자")
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        if st.button("어제"): st.session_state['death_date'] = today - timedelta(days=1)
    with d_col2:
        if st.button("오늘"): st.session_state['death_date'] = today
    
    death_date = st.date_input("날짜 확인", value=st.session_state['death_date'])
    st.session_state['death_date'] = death_date # 수동 변경 반영

    t_col1, t_col2 = st.columns([1, 2])
    with t_col1: ampm = st.radio("구분", ["오전", "오후"], horizontal=True)
    with t_col2: death_time = st.time_input("시간", label_visibility="collapsed")

# 3. 장례 일정 섹션 (연동 로직 포함)
with st.expander("📅 2. 장례 일정 및 발인", expanded=True):
    is_immediate = st.toggle("즉시 모심 (장례 없음)")
    
    if not is_immediate:
        # 상단 요약 표시
        burn_date = st.session_state['burn_date']
        calc_days = (burn_date - death_date).days + 1
        
        st.markdown(f"""
        <div class="status-box">
            <b>[일정 확인]</b><br>
            사망일: {death_date.strftime('%m/%d')} ({['월','화','수','목','금','토','일'][death_date.weekday()]})<br>
            발인일: {burn_date.strftime('%m/%d')} ({['월','화','수','목','금','토','일'][burn_date.weekday()]})<br>
            <b>현재 {calc_days}일장 설정됨</b>
        </div>
        """, unsafe_allow_html=True)

        # 장례일자 선택 시 -> 발인일 자동 변경
        st.write("장례 기간 선택")
        day_opts = ["2일장", "3일장", "4일장", "기타"]
        selected_day = st.radio("장례 기간", day_opts, index=day_opts.index(st.session_state['days_val']) if st.session_state['days_val'] in day_opts else 1, horizontal=True)
        
        if selected_day == "2일장": st.session_state['burn_date'] = death_date + timedelta(days=1)
        elif selected_day == "3일장": st.session_state['burn_date'] = death_date + timedelta(days=2)
        elif selected_day == "4일장": st.session_state['burn_date'] = death_date + timedelta(days=3)
        
        # 발인 예정일 선택 시 -> 장례 기간 자동 계산
        st.write("또는 발인일 직접 선택")
        b_col1, b_col2, b_col3 = st.columns(3)
        with b_col1:
            if st.button("내일"): st.session_state['burn_date'] = death_date + timedelta(days=1)
        with b_col2:
            if st.button("모레"): st.session_state['burn_date'] = death_date + timedelta(days=2)
        with b_col3:
            new_burn_date = st.date_input("직접", value=st.session_state['burn_date'], label_visibility="collapsed")
            st.session_state['burn_date'] = new_burn_date

        bt_col1, bt_col2 = st.columns([1, 2])
        with bt_col1: burn_ampm = st.radio("발인 구분", ["오전", "오후"], horizontal=True)
        with bt_col2: burn_time = st.time_input("발인 시각", label_visibility="collapsed")

    st.write("🚚 모시러 갈 장소")
    components.html(addr_search_js(), height=65)
    pickup_place = st.text_input("검색된 주소 / 상세 호수", placeholder="건물명이나 상세 주소 입력")

# 4. 유가족 정보
with st.expander("📞 3. 유가족 정보", expanded=True):
    u_name = st.text_input("유가족 성함")
    u_relation = st.selectbox("고인과의 관계", ["자(아들)", "녀(딸)", "배우자", "부모", "형(오빠)", "제(남동생)", "누나(언니)", "매(여동생)", "기타"])
    u_phone = st.text_input("유가족 연락처", placeholder="010-0000-0000")

# 5. 사진 촬영 및 보고
st.divider()
captured_img = st.camera_input("📸 접수증 촬영 (필수)")

summary = f"""[야간접수 보고]
고인: {name}({gender})
사망: {death_date.strftime('%m/%d')} {ampm} {death_time.strftime('%H:%M')}
장례: {"즉시모심" if is_immediate else f"{calc_days}일장(발인: {st.session_state['burn_date'].strftime('%m/%d')} {burn_ampm} {burn_time.strftime('%H:%M')})"}
모시러 갈 곳: {pickup_place}
보호자: {u_name}({u_relation}) / {u_phone}"""

if st.button("🚀 김보라 선임에게 보고 데이터 생성"):
    if not name or not u_phone or not pickup_place or captured_img is None:
        st.error("성함, 모시러 갈 장소, 연락처, 접수증 사진은 필수입니다.")
    else:
        st.success("데이터 구성 완료!")
        st.code(summary)
