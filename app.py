import streamlit as st
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import re

# 1. 스타일 설정
st.set_page_config(page_title="시신기증 야간접수", layout="centered")
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 1.2rem !important; background-color: #1e1e26 !important; border: 2px solid #4CAF50 !important; }
    .status-box { background-color: #262730; padding: 15px; border-radius: 10px; border: 1px solid #464b5d; margin-bottom: 20px; }
    .stButton>button { height: 3.5rem; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚨 시신기증 스마트 접수")

# --- 데이터 파싱 로직 ---
def parse_free_text(text):
    data = {}
    # 1. 성함 추출 (보통 첫 단어 혹은 '이름은 OO')
    name_match = re.search(r'(?:이름은|고인)\s*([가-힣]{2,4})', text)
    if name_match: data['name'] = name_match.group(1)
    
    # 2. 주민번호 추출 (000000-0000000 형태)
    jumin_match = re.search(r'\d{6}-\d{7}', text)
    if jumin_match: data['jumin'] = jumin_match.group()
    
    # 3. 장례 기간 추출 (2일장, 3일장, 4일장)
    day_match = re.search(r'([2-4])일장', text)
    if day_match: data['days'] = int(day_match.group(1))
    
    # 4. 사망 장소 추출 (병원, 자택 등)
    place_match = re.search(r'([가-힣]+(?:병원|장례식장|자택|요양원))', text)
    if place_match: data['place'] = place_match.group(1)
    
    return data

# --- 세션 상태 초기화 ---
today = datetime.now().date()
if 'd_date' not in st.session_state: st.session_state.d_date = today
if 'b_date' not in st.session_state: st.session_state.b_date = today + timedelta(days=2)
if 'relation' not in st.session_state: st.session_state.relation = "미선택"

# --- 상단 자유 입력창 ---
st.subheader("🎙️ 한꺼번에 말씀하세요")
free_text = st.text_area("예: 고인 홍길동, 주민번호 500101-1234567, 서울성모병원에서 오늘 사망, 3일장입니다.", height=120)

if st.button("✨ 데이터 자동 분류하기"):
    parsed = parse_free_text(free_text)
    if parsed:
        if 'name' in parsed: st.session_state['name_input'] = parsed['name']
        if 'jumin' in parsed: st.session_state['jumin_input'] = parsed['jumin']
        if 'place' in parsed: st.session_state['place_input'] = parsed['place']
        if 'days' in parsed: st.session_state.b_date = st.session_state.d_date + timedelta(days=parsed['days']-1)
        st.success("데이터가 분류되었습니다. 아래 상세 항목을 확인하세요.")
    else:
        st.warning("분류할 데이터를 찾지 못했습니다. 항목별로 확인해 주세요.")

st.divider()

# 2. 상세 항목 (자동 입력 결과 확인)
with st.expander("👤 1. 고인 및 장례 정보", expanded=True):
    name = st.text_input("고인 성함", key="name_input")
    jumin = st.text_input("주민등록번호", key="jumin_input")
    
    col1, col2 = st.columns(2)
    with col1:
        death_date = st.date_input("사망일", value=st.session_state.d_date)
        st.session_state.d_date = death_date
    with col2:
        burn_date = st.date_input("발인일", value=st.session_state.b_date)
        st.session_state.b_date = burn_date

    death_place = st.text_input("사망 장소", key="place_input")

with st.expander("📞 2. 유가족 정보", expanded=True):
    u_name = st.text_input("유가족 성함")
    st.write(f"관계: **{st.session_state.relation}**")
    rel_cols = st.columns(4)
    relations = ["자(아들)", "녀(딸)", "배우자", "부모"]
    for i, rel in enumerate(relations):
        with rel_cols[i]:
            if st.button(rel): st.session_state.relation = rel; st.rerun()
    u_phone = st.text_input("연락처")

# 3. 최종 보고
st.divider()
captured_img = st.camera_input("📸 접수증 촬영")

calc_days = (st.session_state.b_date - st.session_state.d_date).days + 1
summary = f"""[야간접수 보고]
고인: {st.session_state.get('name_input', '')} / {st.session_state.get('jumin_input', '')}
사망: {st.session_state.d_date.strftime('%m/%d')}
장례: {calc_days}일장(발인: {st.session_state.b_date.strftime('%m/%d')})
장소: {st.session_state.get('place_input', '')}
보호자: {u_name}({st.session_state.relation}) / {u_phone}"""

if st.button("🚀 최종 보고 데이터 생성"):
    st.code(summary)
