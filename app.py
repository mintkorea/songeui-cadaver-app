import streamlit as st
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# 1. 모바일 및 음성인식 최적화 스타일
st.set_page_config(page_title="시신기증 접수", layout="centered")
st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 1.05rem; }
    .stButton>button { width: 100%; height: 3.5rem; border-radius: 10px; font-weight: bold; }
    .status-box { 
        background-color: #262730; padding: 15px; border-radius: 10px; 
        border: 1px solid #464b5d; margin-bottom: 20px; color: #ffffff;
    }
    /* 음성 인식 버튼 스타일 */
    .mic-btn { background-color: #ff4b4b; color: white; border: none; border-radius: 50%; width: 40px; height: 40px; }
    </style>
    """, unsafe_allow_html=True)

# 브라우저 음성 인식 JS (Web Speech API 활용)
def stt_js(target_id):
    return f"""
    <script>
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'ko-KR';
    recognition.onresult = (event) => {{
        const text = event.results[0][0].transcript;
        window.parent.postMessage({{ type: 'stt_result', target: '{target_id}', text: text }}, '*');
    }};
    </script>
    <button onclick="recognition.start()" style="border-radius:50%; width:45px; height:45px; border:none; background-color:#FF4B4B; color:white; cursor:pointer;">🎙️</button>
    """

# 주소 검색 JS
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
    <button onclick="openAddrSearch()" style="width:100%; height:3.5rem; background-color:#4CAF50; color:white; border:none; border-radius:10px; font-weight:bold; cursor:pointer;">
        📍 건물명 / 주소 찾기
    </button>
    """

st.title("🚨 시신기증 야간 접수")

# --- 세션 상태 관리 ---
today = datetime.now().date()
if 'd_date' not in st.session_state: st.session_state.d_date = today
if 'b_date' not in st.session_state: st.session_state.b_date = today + timedelta(days=2)
if 'relation' not in st.session_state: st.session_state.relation = "선택안됨"

# 1. 고인 정보 (접수증 상단 순서)
with st.expander("👤 1. 고인 정보", expanded=True):
    col_n1, col_n2 = st.columns([4, 1])
    with col_n1: name = st.text_input("고인 성함", key="name_input")
    with col_n2: st.write(""); components.html(stt_js("name_input"), height=50) # 성함 음성 입력
    
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    reg_num = st.text_input("등록번호", placeholder="모를 경우 공란")
    
    st.write("사망일자")
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        if st.button("어제"): st.session_state.d_date = today - timedelta(days=1); st.rerun()
    with d_col2:
        if st.button("오늘"): st.session_state.d_date = today; st.rerun()
    
    death_date = st.date_input("날짜 확인", value=st.session_state.d_date)
    st.session_state.d_date = death_date

    t_col1, t_col2 = st.columns([1, 2])
    with t_col1: ampm = st.radio("구분", ["오전", "오후"], horizontal=True)
    with t_col2: death_time = st.time_input("시간", label_visibility="collapsed")

    col_p1, col_p2 = st.columns([4, 1])
    with col_p1: death_place = st.text_input("사망 장소 (기록용)", key="place_input")
    with col_p2: st.write(""); components.html(stt_js("place_input"), height=50)

# 2. 장례 일정 및 운구 (접수증 중단 순서)
with st.expander("📅 2. 장례 일정 및 발인", expanded=True):
    is_immediate = st.toggle("즉시 모심 (장례 없음)")
    
    if not is_immediate:
        cur_d = st.session_state.d_date
        cur_b = st.session_state.b_date
        calc_days = (cur_b - cur_d).days + 1
        
        st.markdown(f"""<div class="status-box"><b>[일정 확인]</b> {cur_d.strftime('%m/%d')} ~ {cur_b.strftime('%m/%d')} ({calc_days}일장)</div>""", unsafe_allow_html=True)

        st.write("장례 기간 선택")
        d_opts = st.columns(3)
        with d_opts[0]:
            if st.button("2일장"): st.session_state.b_date = cur_d + timedelta(days=1); st.rerun()
        with d_opts[1]:
            if st.button("3일장"): st.session_state.b_date = cur_d + timedelta(days=2); st.rerun()
        with d_opts[2]:
            if st.button("4일장"): st.session_state.b_date = cur_d + timedelta(days=3); st.rerun()
        
        burn_date = st.date_input("발인날짜 직접지정", value=st.session_state.b_date)
        st.session_state.b_date = burn_date

        bt_col1, bt_col2 = st.columns([1, 2])
        with bt_col1: burn_ampm = st.radio("발인 구분", ["오전", "오후"], horizontal=True)
        with bt_col2: burn_time = st.time_input("발인 시각", label_visibility="collapsed")

    st.write("🚚 모시러 갈 장소")
    components.html(addr_search_js(), height=65)
    pickup_place = st.text_input("상세 주소 입력", placeholder="운구차가 갈 주소를 입력하세요")

# 3. 유가족 정보 (접수증 하단 순서)
with st.expander("📞 3. 유가족 정보", expanded=True):
    u_name = st.text_input("유가족 성함")
    
    st.write(f"고인과의 관계: **{st.session_state.relation}**")
    rel_cols = st.columns(3)
    relations = ["자(아들)", "녀(딸)", "배우자", "부모", "형(오빠)", "제(남동생)", "누나(언니)", "매(여동생)", "기타"]
    for i, rel in enumerate(relations):
        with rel_cols[i % 3]:
            if st.button(rel, key=f"rel_{rel}"): st.session_state.relation = rel; st.rerun()
                
    u_phone = st.text_input("유가족 연락처")

# 4. 사진 촬영 및 보고
st.divider()
captured_img = st.camera_input("📸 접수증 촬영")

if is_immediate: final_jangrae = "즉시모심"
else: final_jangrae = f"{calc_days}일장(발인: {st.session_state.b_date.strftime('%m/%d')} {burn_ampm} {burn_time.strftime('%H:%M')})"

summary = f"""[야간접수 보고]
고인: {name}({gender})
사망: {st.session_state.d_date.strftime('%m/%d')} {ampm} {death_time.strftime('%H:%M')}
장례: {final_jangrae}
모시러 갈 곳: {pickup_place}
보호자: {u_name}({st.session_state.relation}) / {u_phone}"""

if st.button("🚀 김보라 선임에게 보고 데이터 생성"):
    if not name or not u_phone or captured_img is None:
        st.error("성함, 연락처, 사진은 필수입니다.")
    else:
        st.success("데이터 구성 완료!")
        st.code(summary)
