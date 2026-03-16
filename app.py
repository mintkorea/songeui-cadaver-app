import streamlit as st
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import re

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
    </style>
    """, unsafe_allow_html=True)

# 브라우저 음성 인식 컴포넌트 (범용)
def voice_input_js(target_key, label_msg):
    return f"""
    <script>
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'ko-KR';
    recognition.onresult = (event) => {{
        const text = event.results[0][0].transcript;
        window.parent.postMessage({{ 
            type: 'stt_event', 
            target: '{target_key}', 
            text: text 
        }}, '*');
    }};
    </script>
    <button onclick="recognition.start()" style="border-radius:50%; width:40px; height:40px; border:none; background-color:#FF4B4B; color:white; cursor:pointer;" title="{label_msg}">🎙️</button>
    """

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
    <button onclick="openAddrSearch()" style="width:100%; height:3.5rem; background-color:#4CAF50; color:white; border:none; border-radius:10px; font-weight:bold;">📍 주소 검색</button>
    """

st.title("🚨 시신기증 야간 접수")

# --- 세션 관리 및 음성 텍스트 처리 ---
today = datetime.now().date()
if 'd_date' not in st.session_state: st.session_state.d_date = today
if 'b_date' not in st.session_state: st.session_state.b_date = today + timedelta(days=2)
if 'relation' not in st.session_state: st.session_state.relation = "미선택"

# 음성 날짜 해석 함수
def parse_date(text):
    if "오늘" in text: return today
    if "어제" in text: return today - timedelta(days=1)
    if "내일" in text: return today + timedelta(days=1)
    if "모레" in text: return today + timedelta(days=2)
    # "3월 16일" 형태 파싱
    match = re.search(r'(\d+)월\s*(\d+)일', text)
    if match:
        month, day = int(match.group(1)), int(match.group(2))
        return datetime(today.year, month, day).date()
    return None

# 1. 고인 정보
with st.expander("👤 1. 고인 정보", expanded=True):
    c1, c2 = st.columns([5, 1])
    with c1: name = st.text_input("고인 성함")
    with c2: st.write(""); components.html(voice_input_js("name", "성함 입력"), height=45)

    c3, c4 = st.columns([5, 1])
    with c3: jumin = st.text_input("고인 주민번호", placeholder="000000-0000000")
    with c4: st.write(""); components.html(voice_input_js("jumin", "주민번호 입력"), height=45)
    
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    
    # 사망일자 (음성 병행)
    st.write("사망일자")
    sd_col1, sd_col2, sd_col3 = st.columns([2, 3, 1])
    with sd_col1:
        if st.button("어제/오늘"): 
            st.session_state.d_date = today
            st.rerun()
    with sd_col2:
        death_date = st.date_input("날짜 확인", value=st.session_state.d_date, label_visibility="collapsed")
        st.session_state.d_date = death_date
    with sd_col3:
        components.html(voice_input_js("death_date", "날짜 말하기"), height=45)

    t_col1, t_col2 = st.columns([1, 2])
    with t_col1: ampm = st.radio("구분", ["오전", "오후"], horizontal=True)
    with t_col2: death_time = st.time_input("사망시간", label_visibility="collapsed")

    c5, c6 = st.columns([5, 1])
    with c5: death_place = st.text_input("사망 장소")
    with c6: st.write(""); components.html(voice_input_js("place", "장소 입력"), height=45)

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
        
        # 발인일 (음성 병행)
        st.write("발인일 직접 선택 또는 음성 입력")
        bd_col1, bd_col2 = st.columns([5, 1])
        with bd_col1:
            burn_date = st.date_input("발인일 확인", value=st.session_state.b_date, label_visibility="collapsed")
            st.session_state.b_date = burn_date
        with bd_col2:
            components.html(voice_input_js("burn_date", "발인일 말하기"), height=45)

        bt_col1, bt_col2 = st.columns([1, 2])
        with bt_col1: burn_ampm = st.radio("발인구분", ["오전", "오후"], horizontal=True)
        with bt_col2: burn_time = st.time_input("발인시각", label_visibility="collapsed")

    st.write("🚚 모시러 갈 장소")
    components.html(addr_search_js(), height=65)
    pickup_place = st.text_input("상세 주소 입력")

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
사망: {st.session_state.d_date.strftime('%m/%d')} {ampm} {death_time.strftime('%H:%M')}
장례: {jangrae_text}
모시러 갈 곳: {pickup_place}
보호자: {u_name}({st.session_state.relation}) / {u_phone}
사망장소: {death_place}"""

if st.button("🚀 최종 데이터 확정 및 문자 생성"):
    if not name or not u_phone or st.session_state.relation == "미선택" or captured_img is None:
        st.error("성함, 관계, 연락처, 사진은 필수입니다.")
    else:
        st.success("데이터 확정! 아래 내용을 복사하세요.")
        st.code(summary)
