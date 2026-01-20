import streamlit as st
import time
from fractions import Fraction
# logic.py에서는 이제 새 문제를 만들지 않으므로 generate_new_problem 호출을 제거합니다.

def check_numeric_answer(answer, level):
    user_input = st.session_state['keypad_input']
    
    if not user_input:
        st.session_state['feedback_msg'] = ('warning', "⚠️ 숫자를 입력해주세요.")
        return

    try:
        if "/" in user_input:
            val = float(Fraction(user_input))
        else:
            val = float(user_input)
            
        if abs(val - answer) < 0.01:
            # (4) 정답인 경우: 데이터 유지, 문제 생성 안 함
            st.session_state['score'] += 10
            st.session_state['session_stats']['correct'] += 1
            st.session_state['session_stats']['total'] += 1
            st.session_state['feedback_msg'] = ('success', f"✅ 정답입니다! ({answer})")
            st.session_state['attempts'] = 0
            # 여기서 바로 리런하여 화면에 정답 메시지와 입력값을 그대로 보여줌
            st.rerun()
        else:
            # 오답 처리
            st.session_state['attempts'] += 1
            count = st.session_state['attempts']
            
            if count >= 3:
                # (3) 3번째 틀린 경우: 데이터 유지, 정답 공개
                st.session_state['feedback_msg'] = ('error', f"❌ 틀렸습니다! 정답은 {answer}입니다.")
                st.session_state['session_stats']['total'] += 1
                st.session_state['attempts'] = 0
                st.rerun()
            else:
                # (1), (2) 1~2번째 틀린 경우: 다시 풀기 위해 입력값 지움
                st.session_state['keypad_input'] = ""
                st.session_state['feedback_msg'] = ('error', f"❌ 틀렸습니다! 다시 풀어보세요.({count}/3)")
                st.rerun()
                
    except (ValueError, ZeroDivisionError):
        st.session_state['feedback_msg'] = ('warning', "⚠️ 올바른 형식이 아닙니다.")
        st.rerun()

def check_ox_button(user, answer, comment, level):
    if user == answer:
        st.session_state['session_stats']['total'] += 1
        st.session_state['score'] += 10
        st.session_state['session_stats']['correct'] += 1
        st.session_state['feedback_msg'] = ('success', "✅ 정답입니다! 참 잘했어요.")
        st.session_state['attempts'] = 0
        st.rerun()
    else:
        st.session_state['attempts'] += 1
        count = st.session_state['attempts']
        
        if count >= 3:
            explanation = f" (해설: {comment})" if comment else ""
            st.session_state['feedback_msg'] = ('error', f"❌ 틀렸습니다! 정답은 {answer}입니다.{explanation}")
            st.session_state['session_stats']['total'] += 1
            st.session_state['attempts'] = 0
            st.rerun()
        else:
            st.session_state['feedback_msg'] = ('error', f"❌ 틀렸습니다! 다시 풀어보세요.({count}/3)")
            st.rerun()

def check_choice_button(user_idx, answer_idx, level):
    if user_idx == answer_idx:
        st.session_state['session_stats']['total'] += 1
        st.session_state['score'] += 10
        st.session_state['session_stats']['correct'] += 1
        st.session_state['feedback_msg'] = ('success', "✅ 정답입니다! (+10%)")
        st.session_state['attempts'] = 0
        st.rerun()
    else:
        st.session_state['attempts'] += 1
        count = st.session_state['attempts']
        
        if count >= 3:
            st.session_state['feedback_msg'] = ('error', "❌ 틀렸습니다! 정답을 확인하세요.")
            st.session_state['session_stats']['total'] += 1
            st.session_state['attempts'] = 0
            st.rerun()
        else:
            st.session_state['feedback_msg'] = ('error', f"❌ 틀렸습니다! 다시 풀어보세요.({count}/3)")
            st.rerun()

def check_law_button(user, answer, level):
    if user == answer:
        st.session_state['session_stats']['total'] += 1
        st.session_state['score'] += 10
        st.session_state['session_stats']['correct'] += 1
        st.session_state['feedback_msg'] = ('success', "✅ 정답입니다!")
        st.session_state['attempts'] = 0
        st.rerun()
    else:
        st.session_state['attempts'] += 1
        count = st.session_state['attempts']
        
        if count >= 3:
            st.session_state['feedback_msg'] = ('error', f"❌ 틀렸습니다! 정답은 {answer}입니다.")
            st.session_state['session_stats']['total'] += 1
            st.session_state['attempts'] = 0
            st.rerun()
        else:
            st.session_state['feedback_msg'] = ('error', f"❌ 틀렸습니다! 다시 풀어보세요.({count}/3)")
            st.rerun()