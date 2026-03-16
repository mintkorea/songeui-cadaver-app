import streamlit as st
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# 1. 스타일 설정 (모바일 가독성 중심)
st.set_page_config(page_title="시신기증 야간접수", layout="centered")
st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 1.1rem; }
    .stButton>button { width: 100%; height: 3.8rem; border-radius: 12px; font-weight: bold; font-size: 1.1rem; }
    .status-box { 
        background-color: #262730; padding: 18px; border-radius: 12px; 
        border: 1px solid #464b5d; margin-bottom: 20px; color: #ffffff;
    }
    /* 입력창 간격 확대 */
    .stTextInput input { height: 3.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

# 주소 검색 팝업 (가장 안정적인 방식)
def addr_search_js():
    return """
    <script src="//t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js"></script>
    <script>
        function openAddrSearch() {
            new daum.Postcode({
                oncomplete: function(data) {
                    const addr = data.roadAddress || data.address;
                    window.parent.postMessage({ type: 'address_selected', address: addr }, '*');
                }
            }).open();
        }
    </script>
    <button onclick="openAddrSearch()" style="width:100%; height:3.8rem; background-color:#4CAF50; color:white; border:none; border-radius:12px; font-weight:bold; cursor:pointer; font-size:1.1rem;">
        📍 주소 검색 (터치)
    </button>
    """

st.title("🚨 시신기증 야간 접수")

# --- 세션 상태 관리 ---
today = datetime.now().date()
if 'd_date' not in st.session_state: st.session_state.d_date = today
if 'b_date' not in st.session_state: st.session_state.b_date = today + timedelta(days=2)
if 'relation' not in st.session_state: st.session_state.relation = "미선택"

# 1. 고인 정보
with st.expander("👤 1. 고인 정보 (접수증 상단)", expanded=True):
    name = st.text_input("고인 성함", placeholder="터치 후 키보드 마이크 사용 🎙️")
    jumin = st.text_input("주민등록번호", placeholder="000000-0000000")
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    reg_num = st.text_input("기증 등록번호 (선택)", placeholder="확인 가능한 경우만 입력")
    
    st.write("사망일자")
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        if st.button("어제 (" + (today - timedelta(days=1)).strftime('%m/%d') + ")"): 
            st.session_state.d_date = today - timedelta(days=1); st.rerun()
    with d_col2:
        if st.button("오늘 (" + today.strftime('%m/%d') + ")"): 
            st.session_state.d_date = today; st.rerun()
    
    death_date = st.date_input("날짜 확인", value=st.session_state.d_date)
    st.session_state.d_date = death_date

    t_col1, t_col2 = st.columns([1, 2])
    with t_col1: ampm = st.radio("구분", ["오전", "오후"], horizontal=True)
    with t_col2: death_time = st.time_input("시간", label_visibility="collapsed")
    
    death_place = st.text_input("사망 장소 (기록용)", placeholder="병원명/장례식장 호실")

# 2. 장례 일정 및 운구
with st.expander("📅 2. 장례 일정 및 발인 (접수증 중단)", expanded=True):
    is_immediate = st.toggle("즉시 모심 (장례 없음)")
    
    if not is_immediate:
        cur_d = st.session_state.d_date
        cur_b = st.session_state.b_date
        calc_days = (cur_b - cur_d).days + 1
        st.markdown(f"""
        <div class="status-box">
            <b>[일정 확인]</b><br>
            사망: {cur_d.strftime('%m/%d')} → 발인: {cur_b.strftime('%m/%d')}<br>
            <b>현재 {calc_days}일장 설정됨</b>
        </div>
        """, unsafe_allow_html=True)

        st.write("장례 기간 선택")
        d_opts = st.columns(3)
        with d_opts[0]:
            if st.button("2일장"): st.session_state.b_date = cur_d + timedelta(days=1); st.rerun()
        with d_opts[1]:
            if st.button("3일장"): st.session_state.b_date = cur_d + timedelta(days=2); st.rerun()
        with d_opts[2]:
            if st.button("4일장"): st.session_state.b_date = cur_d + timedelta(days=3); st.rerun()
        
        burn_date = st.date_input("발인일 직접지정", value=st.session_state.b_date)
        st.session_state.b_date = burn_date

        bt_col1, bt_col2 = st.columns([1, 2])
        with bt_col1: burn_ampm = st.radio("발인 구분", ["오전", "오후"], horizontal=True)
        with bt_col2: burn_time = st.time_input("발인 시각", label_visibility="collapsed")

    st.write("🚚 모시러 갈 장소 (운구 주소)")
    components.html(addr_search_js(), height=70)
    pickup_place = st.text_input("상세 주소 입력", placeholder="건물명이나 상세 호실")

# 3. 유가족 정보
with st.expander("📞 3. 유가족 정보 (접수증 하단)", expanded=True):
    u_name = st.text_input("유가족 성함")
    st.write(f"고인과의 관계: **{st.session_state.relation}**")
    rel_cols = st.columns(3)
    relations = ["자(아들)", "녀(딸)", "배우자", "부모", "형(오빠)", "제(남동생)", "기타"]
    for i, rel in enumerate(relations):
        with rel_cols[i % 3]:
            if st.button(rel, key=f"rel_{rel}"):
                st.session_state.relation = rel; st.rerun()
    u_phone = st.text_input("유가족 연락처", placeholder="010-0000-0000")

# 4. 최종 보고
st.divider()
captured_img = st.camera_input("📸 접수증 촬영 (필수)")

jangrae_text = "즉시모심" if is_immediate else f"{calc_days}일장(발인: {st.session_state.b_date.strftime('%m/%d')} {burn_ampm} {burn_time.strftime('%H:%M')})"
summary = f"""[야간접수 보고]
고인: {name}({gender}) / {jumin}
등록: {reg_num if reg_num else '미확인'}
사망: {st.session_state.d_date.strftime('%m/%d')} {ampm} {death_time.strftime('%H:%M')}
장례: {jangrae_text}
모시러 갈 곳: {pickup_place}
보호자: {u_name}({st.session_state.relation}) / {u_phone}
사망장소: {death_place}"""

if st.button("🚀 최종 보고 데이터 생성"):
    if not name or not u_phone or st.session_state.relation == "미선택" or captured_img is None:
        st.error("필수 항목(성함, 관계, 연락처, 사진)이 누락되었습니다.")
    else:
        st.success("데이터 확정! 아래 내용을 복사하여 김보라 선임께 전송하세요.")
        st.code(summary)
