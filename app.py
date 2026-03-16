import streamlit as st
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# 1. 스타일 및 UI 설정
st.set_page_config(page_title="시신기증 야간접수", layout="centered")
st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 1.05rem; }
    .stButton>button { width: 100%; height: 3.5rem; border-radius: 10px; font-weight: bold; }
    .status-box { 
        background-color: #262730; padding: 15px; border-radius: 10px; 
        border: 1px solid #464b5d; margin-bottom: 20px; color: #ffffff;
    }
    .rel-btn>div>button { height: 3rem !important; font-size: 0.9rem !important; margin-bottom: 5px; }
    /* 음성 입력 버튼 강조 스타일 */
    .st-emotion-cache-1kyx7g3 { flex-direction: row-reverse; } 
    </style>
    """, unsafe_allow_html=True)

# 브라우저 음성 인식 컴포넌트 (음성 결과를 텍스트 박스로 직접 보냄)
def voice_input_js(label):
    return f"""
    <script>
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'ko-KR';
    recognition.onresult = (event) => {{
        const text = event.results[0][0].transcript;
        const inputs = window.parent.document.querySelectorAll('input');
        for (let input of inputs) {{
            if (input.ariaLabel && input.ariaLabel.includes('{label}')) {{
                input.value = text;
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
        }}
    }};
    </script>
    <button onclick="recognition.start()" style="border-radius:50%; width:40px; height:40px; border:none; background-color:#FF4B4B; color:white; cursor:pointer;">🎙️</button>
    """

def addr_search_js():
    return """
    <script src="//t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js"></script>
    <script>
        function openAddrSearch() {{
            new daum.Postcode({{
                oncomplete: function(data) {{
                    const addr = data.roadAddress || data.address;
                    window.parent.postMessage({{ type: 'address_selected', address: addr }}, '*');
                }}
            }}).open();
        }}
    </script>
    <button onclick="openAddrSearch()" style="width:100%; height:3.5rem; background-color:#4CAF50; color:white; border:none; border-radius:10px; font-weight:bold;">📍 주소 검색</button>
    """

st.title("🚨 시신기증 야간 접수")

# 세션 관리
today = datetime.now().date()
if 'd_date' not in st.session_state: st.session_state.d_date = today
if 'b_date' not in st.session_state: st.session_state.b_date = today + timedelta(days=2)
if 'relation' not in st.session_state: st.session_state.relation = "미선택"

# 1. 고인 정보
with st.expander("👤 1. 고인 정보", expanded=True):
    # 성함 + 음성버튼
    c1, c2 = st.columns([5, 1])
    with c1: name = st.text_input("고인 성함", key="name")
    with c2: st.write(""); components.html(voice_input_js("고인 성함"), height=45)

    # 주민등록번호 추가
    c3, c4 = st.columns([5, 1])
    with c3: jumin = st.text_input("고인 주민번호", placeholder="000000-0000000")
    with c4: st.write(""); components.html(voice_input_js("고인 주민번호"), height=45)
    
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    reg_num = st.text_input("기증 등록번호 (선택)")
    
    st.write("사망일자")
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        if st.button("어제"): st.session_state.d_date = today - timedelta(days=1); st.rerun()
    with d_col2:
        if st.button("오늘"): st.session_state.d_date = today; st.rerun()
    
    death_date = st.date_input("사망일 확인", value=st.session_state.d_date)
    st.session_state.d_date = death_date

    t_col1, t_col2 = st.columns([1, 2])
    with t_col1: ampm = st.radio("구분", ["오전", "오후"], horizontal=True)
    with t_col2: death_time = st.time_input("사망시간", label_visibility="collapsed")

    c5, c6 = st.columns([5, 1])
    with c5: death_place = st.text_input("사망 장소", key="place")
    with c6: st.write(""); components.html(voice_input_js("사망 장소"), height=45)

# 2. 장례 일정 및 운구
with st.expander("📅 2. 장례 일정 및 발인", expanded=True):
    is_immediate = st.toggle("즉시 모심 (장례 없음)")
    
    if not is_immediate:
        cur_d = st.session_state.d_date
        cur_b = st.session_state.b_date
        calc_days = (cur_b - cur_d).days + 1
        st.markdown(f"""<div class="status-box"><b>[일정]</b> {cur_d.strftime('%m/%d')} ~ {cur_b.strftime('%m/%d')} ({calc_days}일장)</div>""", unsafe_allow_html=True)

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
        with bt_col1: burn_ampm = st.radio("발인구분", ["오전", "오후"], horizontal=True)
        with bt_col2: burn_time = st.time_input("발인시각", label_visibility="collapsed")

    st.write("🚚 모시러 갈 장소")
    components.html(addr_search_js(), height=65)
    pickup_place = st.text_input("상세 주소 입력", key="pickup")

# 3. 유가족 정보
with st.expander("📞 3. 유가족 정보", expanded=True):
    u_name = st.text_input("유가족 성함")
    st.write(f"관계: **{st.session_state.relation}**")
    rel_cols = st.columns(3)
    relations = ["자(아들)", "녀(딸)", "배우자", "부모", "형(오빠)", "제(남동생)", "기타"]
    for i, rel in enumerate(relations):
        with rel_cols[i % 3]:
            if st.button(rel, key=f"rel_{rel}"): st.session_state.relation = rel; st.rerun()
    u_phone = st.text_input("유가족 연락처")

# 4. 최종 보고
st.divider()
captured_img = st.camera_input("📸 접수증 촬영")

jangrae_text = "즉시모심" if is_immediate else f"{calc_days}일장(발인: {st.session_state.b_date.strftime('%m/%d')} {burn_ampm} {burn_time.strftime('%H:%M')})"
summary = f"""[야간접수 보고]
고인: {name}({gender}) / {jumin}
등록: {reg_num if reg_num else '미확인'}
사망: {st.session_state.d_date.strftime('%m/%d')} {ampm} {death_time.strftime('%H:%M')}
장례: {jangrae_text}
모시러 갈 곳: {pickup_place}
보호자: {u_name}({st.session_state.relation}) / {u_phone}
사망장소: {death_place}"""

if st.button("🚀 최종 데이터 확정 및 문자 생성"):
    if not name or not u_phone or st.session_state.relation == "미선택" or captured_img is None:
        st.error("필수 항목(성함, 관계, 연락처, 사진)을 확인하세요.")
    else:
        st.success("데이터 확정! 아래 내용을 복사하세요.")
        st.code(summary)
