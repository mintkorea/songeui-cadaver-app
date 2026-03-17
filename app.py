import streamlit as st
from datetime import datetime, timedelta
import re

# 1. 모바일 UI 최적화
st.set_page_config(page_title="시신기증 스마트 접수", layout="centered")
st.markdown("""
    <style>
    .step-header { background-color: #007BFF; color: white; padding: 12px; border-radius: 10px; margin-bottom: 15px; text-align: center; font-weight: bold; }
    .stTextArea textarea { font-size: 1.1rem !important; border: 2px solid #007BFF !important; border-radius: 10px; }
    .highlight-box { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #007BFF; margin: 10px 0; }
    .val { color: #d63384; font-weight: bold; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 유연한 성함 추출 함수 ---
def extract_name(text):
    if not text: return ""
    # 1. '성함은/이름은/고인/고인은' 뒤의 한글 2~4자 추출
    patterns = [
        r'(?:성함|이름|고인|환자)(?:은|는|이)?\s*([가-힣]{2,4})',
        r'([가-힣]{2,4})(?:님| 분)?'
    ]
    for p in patterns:
        match = re.search(p, text)
        if match: return match.group(1).strip()
    
    # 2. 패턴 실패 시, 문장에서 가장 처음 나오는 2~4자 한글 단어를 이름으로 추정
    words = text.split()
    for word in words:
        clean_word = re.sub(r'[^가-힣]', '', word)
        if 2 <= len(clean_word) <= 4:
            return clean_word
    return ""

# --- 세션 초기화 ---
today = datetime.now().date()
if 'step' not in st.session_state: st.session_state.step = 1
if 'name' not in st.session_state: st.session_state.name = ""
if 'jumin' not in st.session_state: st.session_state.jumin = ""
if 'place' not in st.session_state: st.session_state.place = ""
if 'd_date' not in st.session_state: st.session_state.d_date = today
if 'b_date' not in st.session_state: st.session_state.b_date = today + timedelta(days=2)

st.title("📑 시신기증 단계별 접수")

# --- STEP 1: 고인 인적사항 ---
if st.session_state.step == 1:
    st.markdown('<div class="step-header">1단계: 고인 성함 및 주민번호</div>', unsafe_allow_html=True)
    
    # 실시간 입력 및 추출
    speech_1 = st.text_area("🎙️ 음성으로 말씀하세요", 
                           placeholder="예: '고인 홍길동, 주민번호 500101-1111111'", 
                           height=120)
    
    if speech_1:
        # 성함 추출 (개선된 로직 사용)
        extracted_n = extract_name(speech_1)
        if extracted_n: st.session_state.name = extracted_n
        
        # 주민번호 추출
        jumin_m = re.search(r'\d{6}-\d{7}', speech_1)
        if jumin_m: st.session_state.jumin = jumin_m.group()

    # 추출 결과 가시화 및 수동 수정
    st.markdown(f"""
    <div class="highlight-box">
        추출된 성함: <span class="val">{st.session_state.name if st.session_state.name else '미인식'}</span><br>
        추출된 주민번호: <span class="val">{st.session_state.jumin if st.session_state.jumin else '미인식'}</span>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1: st.session_state.name = st.text_input("성함 수정", value=st.session_state.name)
    with c2: st.session_state.jumin = st.text_input("주민번호 수정", value=st.session_state.jumin)

    if st.button("확인 및 다음 단계로 ➡️"):
        if not st.session_state.name:
            st.warning("고인 성함을 입력해 주세요.")
        else:
            st.session_state.step = 2
            st.rerun()

# --- STEP 2: 일정 및 장소 ---
elif st.session_state.step == 2:
    st.markdown('<div class="step-header">2단계: 사망 장소 및 장례 일정</div>', unsafe_allow_html=True)
    
    speech_2 = st.text_area("🎙️ 음성으로 말씀하세요", 
                           placeholder="예: '오늘 사망, 서울성모병원, 3일장'", 
                           height=120)
    
    if speech_2:
        # 장소 추출
        place_m = re.search(r'([가-힣]+(?:병원|장례식장|자택|요양원))', speech_2)
        if place_m: st.session_state.place = place_m.group(1)
        
        # 장례 일수 추출
        days_m = re.search(r'([2-4])일장', speech_2)
        if days_m:
            st.session_state.b_date = st.session_state.d_date + timedelta(days=int(days_m.group(1))-1)

    st.markdown(f"""
    <div class="highlight-box">
        추출된 장소: <span class="val">{st.session_state.place if st.session_state.place else '미인식'}</span><br>
        설정된 발인일: <span class="val">{st.session_state.b_date.strftime('%m/%d')}</span>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.place = st.text_input("장소 수정", value=st.session_state.place)
    
    col_d1, col_d2 = st.columns(2)
    with col_d1: st.session_state.d_date = st.date_input("사망일", value=st.session_state.d_date)
    with col_d2: st.session_state.b_date = st.date_input("발인일", value=st.session_state.b_date)

    b1, b2 = st.columns(2)
    with b1:
        if st.button("⬅️ 이전"): st.session_state.step = 1; st.rerun()
    with b2:
        if st.button("다음 단계로 ➡️"): st.session_state.step = 3; st.rerun()

# --- STEP 3: 유가족 및 전송 (생략, 기존 로직과 동일) ---
# ... (생략)
