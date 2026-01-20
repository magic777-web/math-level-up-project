import streamlit as st
import random
import time
import matplotlib.pyplot as plt
from fractions import Fraction
from streamlit_drawable_canvas import st_canvas

# ------------------------------------------------------------------
# [유틸리티] 포맷팅 & 시각화 함수
# ------------------------------------------------------------------
def fmt_textbook(num):
    if num == 0: return "0"
    elif num > 0: return f"+{num}"
    else: return f"{num}"

def fmt_with_paren(num):
    if num == 0: return "0"
    return f"({fmt_textbook(num)})"

def fmt_frac_tex(numerator, denominator):
    val = Fraction(numerator, denominator)
    if val.denominator == 1:
        return fmt_textbook(val.numerator)
    sign_str = "+" if val > 0 else "-"
    return f"{sign_str}\\frac{{{abs(val.numerator)}}}{{{abs(val.denominator)}}}"

def draw_textbook_number_line(target_num, denominator=1):
    fig, ax = plt.subplots(figsize=(10, 2))
    # 정수 범위 설정 (최소 -5~5 유지)
    range_val = max(abs(target_num) + 2, 5) 
    ax.set_xlim(-range_val - 0.5, range_val + 0.5)
    ax.set_ylim(-0.6, 0.6)
    ax.axis('off') 
    
    # 메인 수직선
    ax.plot([-range_val - 0.2, range_val + 0.2], [0, 0], color='black', linewidth=1.5, zorder=1)
    ax.plot(range_val + 0.2, 0, marker='>', color='black', markersize=8, clip_on=False)
    ax.plot(-range_val - 0.2, 0, marker='<', color='black', markersize=8, clip_on=False)
    
    # 1. 정수 눈금 및 숫자 표시
    for i in range(-int(range_val), int(range_val) + 1):
        ax.plot([i, i], [-0.1, 0.1], color='black', linewidth=1.5)
        if i == 0: label = "0"
        elif i > 0: label = f"+{i}"
        else: label = f"{i}"
        ax.text(i, -0.25, label, ha='center', va='top', fontsize=12, fontfamily='serif', fontweight='bold')

    # 2. [추가] 소분할 눈금 (분모에 따라 칸 나누기)
    if denominator > 1:
        for i in range(-int(range_val), int(range_val)):
            for j in range(1, denominator):
                sub_tick = i + (j / denominator)
                ax.plot([sub_tick, sub_tick], [-0.05, 0.05], color='gray', linewidth=0.8)

    # 3. 빨간 점 및 물음표 표시
    ax.plot(target_num, 0, 'o', color='#FF0055', markersize=10, zorder=5, markeredgecolor='black') 
    ax.text(target_num, 0.25, '?', fontsize=18, color='#FF0055', ha='center', fontweight='bold')
    return fig