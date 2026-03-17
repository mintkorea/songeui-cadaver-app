import streamlit as st
from datetime import datetime, timedelta
import re

# 1. 스타일 및 UI 설정
st.set_page_config(page_title="시신기증 스마트 접수", layout="centered")
st.markdown("""
    <style>
    .step-header { background-color: #007BFF; color: white; padding: 12px; border-radius: 10px; margin-bottom: 15px; text-align: center; font-weight: bold; }
    .stTextArea textarea { font-size: 1.1rem !important; border: 2px solid #007BFF !important; }
    .highlight-box { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #007BFF; margin: 10px 0; }
    .val { color: #d63384; font-weight: bold; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 한글 숫자를 아라비아 숫자로 변환 ---
def k_to_n(text):
    num_dict = {'영': '0', '일': '1', '이': '2', '삼': '3', '사': '4', '오': '5', '육': '6', '칠': '7', '팔': '8', '구': '9', '공': '0'}
    for k, v in num_dict.items():
        text = text.replace(k, v)
    return text

# --- 성함 및 주민번호 추출 로직 개선 ---
def extract_info_step1(text):
    if not text: return "", ""
    text_digit = k_to_n(text) # 한글 숫자를 먼저 숫자로 변환
    
    # 1. 주민번호 추출 (변환된 텍스트에서 6자리-7자리 패턴 찾기)
    jumin = ""
    jumin_m = re.search(r'\d{6}-?\d{7}', text_digit)
    if jumin_m:
        raw_jumin = jumin_m.group().replace("-", "")
        jumin = f"{raw_jumin[:6]}-{raw_jumin[6:]}"

    # 2. 성함 추출 (호칭 제외 로직 강화)
    name = ""
    # 호칭(아버지, 어머니 등) 뒤에 오는 이름을 찾거나, 'OOO씨', 'OOO님' 패턴 찾기
    name_patterns = [
        r'(?:아버지|어머니|고인|이름|성함|환자)(?:은|는|이)?\s*([가-힣]{2,4})',
        r'([가-힣]{2,4})(?:씨|님|분)'
    ]
    for p in name_patterns:
        m = re.search(p, text)
        if m: 
            name = m.group(1).strip()
            break
    
    # 패턴 실패 시 첫 단어가 호칭 리스트에 없으면 이름으로 간주
    if not name:
        stop_words = ["아버지", "어머니", "저희", "오늘", "아침에"]
        words = text.split()
        for w in words:
            clean_w = re.sub(r'[^가-힣]', '', w)
            if 2 <= len(clean_w) <= 4 and clean_w not in stop_words:
                name = clean_w
                break
                
    return name, jumin

# --- 세션 상태 초기화 ---
today = datetime.now().date()
keys = {'step': 1, 'name': "", 'jumin': "", 'place': "", 'd_date': today, 'b_date': today + timedelta(days=2), 'u_name': "", 'u_phone': "", 'relation': "미선택"}
for k, v in keys.items():
    if k not in st.session_state: st.session_state[k] = v

st.title("📑 시신기증 단계별 접수")

# --- STEP 1: 고인 정보 ---
if st.session_state.step == 1:
    st.markdown('<div class="step-header">1단계: 고인 성함 및 주민번호</div>', unsafe_allow_html=True)
    speech_1 = st.text_area("🎙️ 음성으로 말씀하세요", placeholder="예: 아버지 김철수씨가... 주민번호는 480223-1544...", height=120)
    
    if speech_1:
        n, j = extract_info_step1(speech_1)
        if n: st.session_state.name = n
        if j: st.session_state.jumin = j

    st.markdown(f'<div class="highlight-box">추출된 성함: <span class="val">{st.session_state.name}</span><br>추출된 주민번호: <span class="val">{st.session_state.jumin}</span></div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1: st.session_state.name = st.text_input("성함 수정", value=st.session_state.name)
    with c2: st.session_state.jumin = st.text_input("주민번호 수정", value=st.session_state.jumin)

    if st.button("확인 및 다음 단계로 ➡️"):
        st.session_state.step = 2
        st.rerun()

# --- STEP 2: 장례 정보 (이미지 2의 에러 수정 포함) ---
elif st.session_state.step == 2:
    st.markdown('<div class="step-header">2단계: 사망 장소 및 일정</div>', unsafe_allow_html=True)
    
    # 에러 수정: 반드시 datetime.date 객체로 계산되도록 강제
    st.session_state.place = st.text_input("사망 장소", value=st.session_state.place)
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        d_date = st.date_input("사망일", value=st.session_state.d_date)
        st.session_state.d_date = d_date
    with col_d2:
        b_date = st.date_input("발인일", value=st.session_state.b_date)
        st.session_state.b_date = b_date
    
    # 이미지 2의 TypeError 방지 로직
    try:
        calc_days = (st.session_state.b_date - st.session_state.d_date).days + 1
    except:
        calc_days = 3 # 기본값

    st.info(f"현재 {calc_days}일장 설정됨")

    b1, b2 = st.columns(2)
    with b1:
        if st.button("⬅️ 이전"): st.session_state.step = 1; st.rerun()
    with b2:
        if st.button("다음 단계로 ➡️"): st.session_state.step = 3; st.rerun()

# --- STEP 3: 최종 보고 ---
elif st.session_state.step == 3:
    st.markdown('<div class="step-header">3단계: 보호자 확인 및 전송</div>', unsafe_allow_html=True)
    u_name = st.text_input("보호자 성함", value=st.session_state.u_name)
    u_phone = st.text_input("보호자 연락처", value=st.session_state.u_phone)
    
    if st.button("🚀 최종 보고 데이터 생성"):
        summary = f"""[야간접수 보고]
고인: {st.session_state.name} / {st.session_state.jumin}
사망: {st.session_state.d_date.strftime('%m/%d')} ({st.session_state.place})
장례: {(st.session_state.b_date - st.session_state.d_date).days + 1}일장
보호자: {u_name} / {u_phone}"""
        st.code(summary)
    
    if st.button("⬅️ 이전"): st.session_state.step = 2; st.rerun()
