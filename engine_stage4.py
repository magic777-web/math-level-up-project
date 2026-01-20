import random
import streamlit as st
from data import STAGE4_DB

def generate_stage4(level_name):
    q_text = ""
    ans = 0
    comment = "" 
    q_type = "numeric" 
    latex_part = "" 
    options = [] 
    denom_info = 1 

    if "4-1" in level_name:
        range_key = '4-1'
        all_ids = list(range(41, 71)) 
        comment = "나눗셈은 모두 곱셈(역수)으로 바꾸세요. 그 다음 전체 식에 있는 음수(-)의 개수를 세어 부호를 먼저 확정 지으면 실수를 줄일 수 있습니다."
    elif "4-2" in level_name:
        range_key = '4-2'
        all_ids = list(range(71, 91)) 
        comment = "덧셈/뺄셈보다 '곱셈/나눗셈'이 먼저입니다! 계산 순서를 번호로 매기고 차근차근 풀어보세요. 눈으로만 풀면 틀리기 쉬워요."
    else: # 4-3
        range_key = '4-3'
        all_ids = list(range(91, 101)) 
        comment = "끝판왕 문제입니다! ① 거듭제곱 ② 괄호(소->중->대) ③ 곱셈/나눗셈 ④ 덧셈/뺄셈. 연습장에 풀이 과정을 꼭 적으면서 푸세요."
        
    used_ids = st.session_state['stage4_history'][range_key]
    available_ids = [i for i in all_ids if i not in used_ids]
    
    if not available_ids:
        used_ids = []
        st.session_state['stage4_history'][range_key] = []
        available_ids = all_ids
        
    pick_id = random.choice(available_ids)
    st.session_state['stage4_history'][range_key].append(pick_id)
    
    prob_data = STAGE4_DB[pick_id]
    q_text = prob_data["q"]
    ans = prob_data["a"]
    
    return {'q_text': q_text, 'answer': ans, 'comment': comment, 'type': q_type, 'options': options, 'latex_part': latex_part, 'denom_info': denom_info}