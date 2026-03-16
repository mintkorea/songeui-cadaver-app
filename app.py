import streamlit as st
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import re

# 1. 스타일 및 UI 설정
st.set_page_config(page_title="시신기증 실시간 접수", layout="centered")
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 1.1rem !important; border: 2px solid #FF4B4B !important; }
    .live-status { color: #FF4B4B; font-weight: bold; font-size: 0.9rem; margin-bottom: 5px; }
    .stButton>button { height: 3.5rem; border-radius: 12px; }
    .field-label { font-weight: bold; color: #4CAF50; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ 실시간 음성-데이터 매칭 접수")

# --- 데이터 파싱 및 세션 동기화 로직 ---
def sync_data(text):
    # 1. 주민번호 (가장 명확한 패턴)
    jumin = re.search(r'\d{6}-\d{7}', text)
    if jumin: st.session_state.jumin = jumin.group()
    
    # 2. 성함 (패턴: "이름은 OO", "고인 OO", "성함 OO")
    name = re.search(r'(?:성함|이름|고인)\s*([가-힣]{2,4})', text)
    if name: st.session_state.name = name.group(1)
    
    # 3. 사망 장소 (패턴: "OO병원", "OO장례식장", "자택")
    place = re.search(r'([가-힣]+(?:병원|장례식장|자택|요양원))', text)
    if place: st.session_state.place = place.group(1)

    # 4. 장례 기간 (패턴: "O일장")
    days = re.search(r'([2-4])일장', text)
    if days: 
        st.session_state.b_date = st.session_state.d_date + timedelta(days=int(days.group(1))-1)

# --- 세션 초기화 ---
today = datetime.now().date()
fields = ['name', 'jumin', 'place', 'u_name', 'u_phone']
for f in fields:
    if f not in st.session_state: st.session_state[f] = ""
if 'd_date' not in st.session_state: st.session_state.d_date = today
if 'b_date' not in st.session_state: st.session_state.b_date = today + timedelta(days=2)
if 'relation' not in st.session_state: st.session_state.relation = "미선택"

# --- [핵심] 실시간 음성 입력창 ---
st.markdown('<p class="live-status">● 실시간 음성 인식 중 (키보드 마이크 권장)</p>', unsafe_allow_html=True)
# 실시간으로 받아적는 영역
input_text = st.text_area("유가족과의 대화나 접수증 내용을 읽어주세요.", 
                         placeholder="예: 고인 김철수, 주민번호 500101-1111111, 서울성모병원에서 오늘 사망, 3일장입니다.",
                         height=100)

# 입력값이 변할 때마다 하단 데이터 즉시 갱신
if input_text:
    sync_data(input_text)

st.divider()

# --- 2. 자동 채워진 결과 확인 및 수정 ---
st.subheader("📝 자동 분류 결과 (오류 시 직접 수정)")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.name = st.text_input("고인 성함", value=st.session_state.name)
        st.session_state.jumin = st.text_input("주민등록번호", value=st.session_state.jumin)
    with col2:
        st.session_state.place = st.text_input("사망 장소", value=st.session_state.place)
        st.session_state.relation = st.selectbox("관계", ["미선택", "자(아들)", "녀(딸)", "배우자", "부모", "기타"], 
                                               index=["미선택", "자(아들)", "녀(딸)", "배우자", "부모", "기타"].index(st.session_state.relation))

    c1, c2 = st.columns(2)
    with c1:
        st.session_state.d_date = st.date_input("사망일", value=st.session_state.d_date)
    with c2:
        st.session_state.b_date = st.date_input("발인일", value=st.session_state.b_date)

st.divider()

# --- 3. 유가족 및 사진 ---
u_col1, u_col2 = st.columns(2)
with u_col1:
    u_name = st.text_input("유가족 성함", placeholder="보호자 성함")
with u_col2:
    u_phone = st.text_input("유가족 연락처", placeholder="010-0000-0000")

captured_img = st.camera_input("📸 최종 접수증 촬영")

# --- 4. 최종 결과 출력 ---
if st.button("🚀 김보라 선임 보고용 텍스트 생성"):
    calc_days = (st.session_state.b_date - st.session_state.d_date).days + 1
    summary = f"""[야간접수 보고]
고인: {st.session_state.name} / {st.session_state.jumin}
사망: {st.session_state.d_date.strftime('%m/%d')} ({st.session_state.place})
장례: {calc_days}일장 (발인: {st.session_state.b_date.strftime('%m/%d')})
보호자: {u_name}({st.session_state.relation}) / {u_phone}"""
    
    st.success("데이터가 생성되었습니다.")
    st.code(summary)
