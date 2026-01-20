import streamlit as st
from engine_stage1 import generate_stage1
from engine_stage2 import generate_stage2
from engine_stage3 import generate_stage3
from engine_stage4 import generate_stage4

def generate_new_problem(level_name):
    # [공통] 문제 생성 시 시도 횟수 및 입력창 초기화
    st.session_state['attempts'] = 0
    st.session_state['keypad_input'] = ""
    
    # 레벨 이름에 따라 적절한 파일(함수)로 연결
    if level_name.startswith("1-"):
        return generate_stage1(level_name)
    elif level_name.startswith("2-"):
        return generate_stage2(level_name)
    elif level_name.startswith("3-"):
        return generate_stage3(level_name)
    elif level_name.startswith("4-"):
        return generate_stage4(level_name)
    else:
        # 예외 처리: 혹시라도 알 수 없는 레벨이면 1-1로
        return generate_stage1("1-1. 정수와 유리수의 분류")