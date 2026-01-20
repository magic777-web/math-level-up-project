import streamlit as st
import random
import time
import matplotlib.pyplot as plt
from fractions import Fraction
from streamlit_drawable_canvas import st_canvas
from data import STAGE4_DB
from utils import fmt_textbook, fmt_with_paren, fmt_frac_tex, draw_textbook_number_line
from engine import generate_new_problem
from styles import apply_custom_css
from logic import check_numeric_answer, check_ox_button, check_choice_button, check_law_button

# ------------------------------------------------------------------
# [기본 설정]
# ------------------------------------------------------------------
st.set_page_config(
    page_title="정.유.소 - 수학 충전소",
    page_icon="⛽",
    layout="wide"
)

apply_custom_css()

TEACHER_PASSWORD = "1234"

# ------------------------------------------------------------------
# [상태 관리]
# ------------------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'score' not in st.session_state:
    st.session_state['score'] = 0 
if 'current_problem' not in st.session_state:
    st.session_state['current_problem'] = None 
if 'current_level' not in st.session_state:
    st.session_state['current_level'] = "1-1. 정수와 유리수의 분류"
if 'attempts' not in st.session_state:
    st.session_state['attempts'] = 0
if 'session_stats' not in st.session_state:
    st.session_state['session_stats'] = {'correct': 0, 'total': 0}
if 'feedback_msg' not in st.session_state:
    st.session_state['feedback_msg'] = None

if 'keypad_input' not in st.session_state:
    st.session_state['keypad_input'] = ""

if 'stage4_history' not in st.session_state:
    st.session_state['stage4_history'] = {'4-1': [], '4-2': [], '4-3': []}

if 'show_memo' not in st.session_state:
    st.session_state['show_memo'] = True 

# ------------------------------------------------------------------
# [로그인 화면]
# ------------------------------------------------------------------
def login_page():
    _, col_main, _ = st.columns([1, 2, 1])
    with col_main:
        left_img = "https://cdn-icons-png.flaticon.com/512/3771/3771278.png"
        right_img = "https://cdn-icons-png.flaticon.com/512/1584/1584808.png"
        st.markdown(f"""
            <h1 style='text-align: center;'>
                <img src='{left_img}' style='width:50px; vertical-align:middle; margin-right:10px;'>
                정.유.소
                <img src='{right_img}' style='width:50px; vertical-align:middle; margin-left:10px;'>
            </h1>
            <h3 style='text-align: center; color: gray;'>정수와 유리수 배터리 충전소</h3>
            <hr>
        """, unsafe_allow_html=True)
        st.info("👋 어서오세요! 방전된 수학 배터리, 여기서 든든하게 충전하세요! ⚡")
        
        with st.form("login_form"):
            st.markdown("### 📝 학생 정보 입력")
            grade = st.selectbox("학년", ["1학년", "2학년", "3학년"])
            ban = st.selectbox("반 (Class)", [i for i in range(1, 21)])
            number = st.selectbox("번호 (Number)", [i for i in range(1, 41)])
            name = st.text_input("이름 (Name)")
            st.markdown("---")
            st.markdown("🔒 **선생님이 알려준 비밀번호**")
            password = st.text_input("비밀번호", type="password")
            st.markdown("<br>", unsafe_allow_html=True) 
            submit_btn = st.form_submit_button("🚀 충전 시작하기", use_container_width=True)
            
            if submit_btn:
                if not name: st.error("이름을 입력해주세요!")
                elif password != TEACHER_PASSWORD: st.error("❌ 비밀번호 오류!")
                else:
                    st.session_state['logged_in'] = True
                    st.session_state['student_info'] = f"{grade} {ban}반 {number}번 {name}"
                    st.rerun()

# ------------------------------------------------------------------
# [메인 화면]
# ------------------------------------------------------------------
def main_page():
    with st.sidebar:
        st.header(f"👤 {st.session_state['student_info']}")
        st.markdown("---")
        
        def change_level(new_level):
            st.session_state['current_level'] = new_level
            st.session_state['current_problem'] = generate_new_problem(new_level)
            st.session_state['session_stats'] = {'correct': 0, 'total': 0}
            st.session_state['feedback_msg'] = None
            st.session_state['keypad_input'] = ""
            st.rerun()

        with st.expander("🌱 Stage 1. 연료 확인", expanded=True):
            for lv in ["1-1. 정수와 유리수의 분류", "1-2. 수직선 위의 수", "1-3. 절댓값의 이해", "1-4. 수의 대소 관계"]:
                is_active = (st.session_state['current_level'] == lv)
                if st.button(lv, use_container_width=True, type="primary" if is_active else "secondary"): change_level(lv)
        
        with st.expander("🚗 Stage 2. 시동 걸기"):
            for lv in ["2-1. 정수의 덧셈 (같은 부호)", "2-2. 정수의 덧셈 (다른 부호)", "2-3. 덧셈의 연산 법칙", "2-4. 정수의 뺄셈", "2-5. 유리수의 덧/뺄셈 (기초)", "2-6. 유리수의 덧/뺄셈 (심화)", "2-7. 괄호를 생략한 덧셈과 뺄셈"]:
                is_active = (st.session_state['current_level'] == lv)
                if st.button(lv, use_container_width=True, type="primary" if is_active else "secondary"): change_level(lv)

        with st.expander("🏎️ Stage 3. 가속 주행"):
            for lv in ["3-1. 정수의 곱셈 (같은 부호)", "3-2. 정수의 곱셈 (다른 부호)", "3-3. 거듭제곱의 계산", "3-4. 곱셈의 연산 법칙", "3-5. 분배법칙", "3-6. 역수 구하기", "3-7. 나눗셈의 계산"]:
                is_active = (st.session_state['current_level'] == lv)
                if st.button(lv, use_container_width=True, type="primary" if is_active else "secondary"): change_level(lv)

        with st.expander("🚀 Stage 4. 터보 부스트"):
            for lv in ["4-1. 곱셈과 나눗셈의 혼합계산", "4-2. 사칙연산의 혼합계산1", "4-3. 사칙연산의 혼합계산2"]:
                is_active = (st.session_state['current_level'] == lv)
                if st.button(lv, use_container_width=True, type="primary" if is_active else "secondary"): change_level(lv)
            
        st.markdown("---")
        if st.button("로그아웃", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    current_level = st.session_state['current_level']
    if st.session_state['current_problem'] is None:
        st.session_state['current_problem'] = generate_new_problem(current_level)

    st.title(f"⛽ {current_level}")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1: st.progress(min(st.session_state['score'] / 100, 1.0))
    with col2: st.metric("배터리", f"{st.session_state['score']}%")
    with col3: 
        s = st.session_state['session_stats']
        st.metric("오늘의 성취", f"⭕ {s['correct']} / {s['total']}")
    
    prob = st.session_state['current_problem']
    
    c_left, c_right = st.columns([2, 1])
    
    with c_left:
        # -------------------------------------------------------
        # [키패드 입력 문제 (주관식)]
        # -------------------------------------------------------
        if prob['type'] not in ['ox', 'choice', 'law_choice']:
            with st.container(border=True): 
                st.markdown("### 📝 문제")
                # 1-2. 수직선: 그래프 출력
                if "1-2" in current_level:
                    st.markdown(prob['q_text'])
                    fig = draw_textbook_number_line(prob['answer'], denominator=prob.get('denom_info', 1))
                    st.pyplot(fig)
                
                # 1-3. 절댓값: 문장형 문제이므로 Markdown으로 출력 (수식 깨짐 방지)
                elif "1-3" in current_level:
                    st.markdown(f"#### {prob['q_text']}")
                
                # 나머지 계산 문제: 수식(LaTeX)으로 출력
                else:
                    st.latex(f"{prob['q_text']} = ?")
                
                # [수정됨] 항상 힌트가 나오던 코드는 삭제했습니다.
                # if prob['comment']: st.caption(...) -> 삭제됨
            
            st.markdown("<br>", unsafe_allow_html=True)
            c_input_area, c_keypad_area = st.columns([1, 1]) 

            def kp_add(v):
                st.session_state['keypad_input'] += str(v)
            def kp_back():
                st.session_state['keypad_input'] = st.session_state['keypad_input'][:-1]
            def kp_clear():
                st.session_state['keypad_input'] = ""

            with c_input_area:
                display_val = st.session_state['keypad_input'] if st.session_state['keypad_input'] else " "
                st.markdown(f'<div class="calc-display">{display_val}</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

                b1, b2 = st.columns(2)
                with b1: 
                    if st.button("정답 확인 🔍", type="primary", use_container_width=True, key="submit_btn", shortcut="Enter"):
                        check_numeric_answer(prob['answer'], current_level)
                with b2: 
                    if st.button("다음 문제로 ⏭️", use_container_width=True, key="next_btn"):
                        st.session_state['current_problem'] = generate_new_problem(current_level)
                        st.session_state['feedback_msg'] = None
                        st.session_state['keypad_input'] = ""
                        st.session_state['attempts'] = 0
                        st.rerun()
                
                # 피드백 및 [수정됨] 힌트 표시 로직
                if st.session_state['feedback_msg']:
                    status, msg = st.session_state['feedback_msg']
                    txt_class = "status-success" if status == 'success' else "status-error"
                    box_content = f"<span class='{txt_class}'>{msg}</span>"
                    
                    # [핵심] 오답(error)일 때만 힌트(comment)를 보여줍니다.
                    if status == 'error' and prob['comment']:
                        st.info(f"💡 **힌트**: {prob['comment']}")
                else:
                    box_content = "<span style='color:#ced4da; font-weight:normal;'>정답 결과가 여기에 표시됩니다.</span>"
                
                st.markdown(f'<div class="feedback-box">{box_content}</div>', unsafe_allow_html=True)

            with c_keypad_area:
                r1c1, r1c2, r1c3, r1c4 = st.columns(4)
                with r1c1: st.button("7", on_click=kp_add, args=("7",), use_container_width=True)
                with r1c2: st.button("8", on_click=kp_add, args=("8",), use_container_width=True)
                with r1c3: st.button("9", on_click=kp_add, args=("9",), use_container_width=True)
                with r1c4: st.button("⌫", on_click=kp_back, use_container_width=True)

                r2c1, r2c2, r2c3, r2c4 = st.columns(4)
                with r2c1: st.button("4", on_click=kp_add, args=("4",), use_container_width=True)
                with r2c2: st.button("5", on_click=kp_add, args=("5",), use_container_width=True)
                with r2c3: st.button("6", on_click=kp_add, args=("6",), use_container_width=True)
                with r2c4: st.button("/", on_click=kp_add, args=("/",), use_container_width=True)

                r3c1, r3c2, r3c3, r3c4 = st.columns(4)
                with r3c1: st.button("1", on_click=kp_add, args=("1",), use_container_width=True)
                with r3c2: st.button("2", on_click=kp_add, args=("2",), use_container_width=True)
                with r3c3: st.button("3", on_click=kp_add, args=("3",), use_container_width=True)
                with r3c4: st.button("＋", on_click=kp_add, args=("+",), use_container_width=True)

                r4c1, r4c2, r4c3, r4c4 = st.columns(4)
                with r4c1: st.button("지우기", on_click=kp_clear, use_container_width=True)
                with r4c2: st.button("0", on_click=kp_add, args=("0",), use_container_width=True)
                with r4c3: st.button(".", on_click=kp_add, args=(".",), use_container_width=True)
                with r4c4: st.button("－", on_click=kp_add, args=("-",), use_container_width=True)

        # -------------------------------------------------------
        # [OX / 객관식 / 법칙 문제]
        # -------------------------------------------------------
        else:
            with st.container(border=True): 
                st.markdown("### 📝 문제")
                if prob['type'] == 'ox':
                    st.markdown(f"#### ${prob['latex_part']}$ {prob['q_text']}")
                elif prob['type'] == 'choice':
                    st.markdown(f"#### {prob['q_text']}")
                    c1, c2 = st.columns(2)
                    with c1: st.latex(prob['options'][0]) 
                    with c2: st.latex(prob['options'][1])
                elif prob['type'] == 'law_choice':
                    st.markdown(f"#### ${prob['latex_part']}$") 
                    st.markdown(f"##### {prob['q_text']}")     
                
                # [수정됨] 여기서도 항상 힌트가 나오던 코드는 삭제했습니다.
            
            st.markdown("<br>", unsafe_allow_html=True)

            if prob['type'] == 'ox':
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("⭕ 맞음", use_container_width=True): check_ox_button("O", prob['answer'], prob['comment'], current_level)
                with c2:
                    if st.button("❌ 틀림", use_container_width=True): check_ox_button("X", prob['answer'], prob['comment'], current_level)
            elif prob['type'] == 'choice':
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("👈 이 수 선택", use_container_width=True, key="btn_left"): check_choice_button(0, prob['answer'], current_level)
                with c2:
                    if st.button("👉 이 수 선택", use_container_width=True, key="btn_right"): check_choice_button(1, prob['answer'], current_level)
            elif prob['type'] == 'law_choice':
                if "3-4" in current_level:
                    c1, c2, c3 = st.columns(3)
                    with c1: 
                        if st.button("곱셈의 교환법칙", use_container_width=True): check_law_button("교환법칙", prob['answer'], current_level)
                    with c2: 
                        if st.button("곱셈의 결합법칙", use_container_width=True): check_law_button("결합법칙", prob['answer'], current_level)
                    with c3: 
                        if st.button("분배법칙", use_container_width=True): check_law_button("분배법칙", prob['answer'], current_level)
                else:
                    c1, c2 = st.columns(2)
                    with c1: 
                        if st.button("덧셈의 교환법칙", use_container_width=True): check_law_button("교환법칙", prob['answer'], current_level)
                    with c2: 
                        if st.button("덧셈의 결합법칙", use_container_width=True): check_law_button("결합법칙", prob['answer'], current_level)
            
            if st.button("다음 문제로 ⏭️", use_container_width=True, key="next_btn_other"):
                st.session_state['current_problem'] = generate_new_problem(current_level)
                st.session_state['feedback_msg'] = None
                st.session_state['attempts'] = 0
                st.rerun()
            
            # 피드백 및 [수정됨] 힌트 표시 로직
            if st.session_state['feedback_msg']:
                st.markdown("<br>", unsafe_allow_html=True)
                status, msg = st.session_state['feedback_msg']
                if status == 'success': 
                    st.success(msg)
                elif status == 'error': 
                    st.error(msg)
                    # [핵심] 오답일 때만 힌트 표시
                    if prob['comment']:
                        st.info(f"💡 **힌트**: {prob['comment']}")
                elif status == 'warning': 
                    st.warning(msg)

    with c_right:
        with st.container(border=True):
            c_title, c_btn = st.columns([2, 1], vertical_alignment="center")
            with c_title: st.markdown("<h4 style='margin: 0;'>📝 연습장</h4>", unsafe_allow_html=True)
            with c_btn:
                if st.button("열기 / 닫기", key="memo_toggle", use_container_width=True):
                    st.session_state['show_memo'] = not st.session_state['show_memo']
            
            if st.session_state['show_memo']:
                st_canvas(
                    fill_color="rgba(255, 165, 0, 0.3)",
                    stroke_width=2,
                    stroke_color="#000000",
                    background_color="#FFFFFF",
                    height=400, 
                    drawing_mode="freedraw",
                    key="canvas_memo",
                )
                st.caption("※ 문제를 풀 때 자유롭게 사용하세요.")

if st.session_state['logged_in']:
    main_page()
else:
    login_page()