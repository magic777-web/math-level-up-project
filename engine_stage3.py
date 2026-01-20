import random
from fractions import Fraction
from utils import fmt_textbook, fmt_with_paren, fmt_frac_tex

def generate_stage3(level_name):
    q_text = ""
    ans = 0
    comment = "" 
    q_type = "numeric" 
    latex_part = "" 
    options = [] 
    denom_info = 1 

    # -----------------------------------------------------------
    # 3-1, 3-2. 곱셈
    # -----------------------------------------------------------
    if "3-1" in level_name or "3-2" in level_name:
        if "3-1" in level_name:
            sign = random.choice([1, -1])
            n1 = sign * random.randint(1, 10)
            n2 = sign * random.randint(1, 10)
        else: # 3-2
            n1 = random.choice([i for i in range(-10, 11) if i != 0])
            if n1 > 0: n2 = random.randint(-10, -1)
            else: n2 = random.randint(1, 10)
            
        q_text = f"{fmt_with_paren(n1)} \\times {fmt_with_paren(n2)}"
        ans = n1 * n2
        comment = "먼저 전체 '부호'를 결정하세요. (같은 부호끼리는 +, 다른 부호끼리는 -). 그 다음 숫자끼리 곱하면 됩니다."

    # -----------------------------------------------------------
    # 3-3. 거듭제곱의 계산
    # -----------------------------------------------------------
    elif "3-3" in level_name: 
        base = random.randint(2, 6)
        exp = random.randint(2, 3)
        case = random.choice(['paren', 'no_paren'])
        if case == 'paren':
            base = -base
            q_text = f"({fmt_textbook(base)})^{exp}" 
            ans = base ** exp
            comment = f"괄호가 있는 ({base})^{exp}은 음수까지 포함해서 {exp}번 곱하는 것입니다. 지수가 짝수면 결과는 양수(+), 홀수면 음수(-)가 됩니다."
        else:
            q_text = f"-{base}^{exp}"
            ans = -1 * (base ** exp)
            comment = f"괄호가 없는 -{base}^{exp}은 {base}를 먼저 거듭제곱한 뒤에 마이너스(-)를 붙이는 것입니다. 괄호가 있을 때와 헷갈리지 마세요!"

    # -----------------------------------------------------------
    # 3-4. 곱셈의 연산법칙
    # -----------------------------------------------------------
    elif "3-4" in level_name: 
        q_type = "law_choice"
        law = random.choice(['comm', 'assoc', 'dist'])
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        c = random.randint(-5, 5)
        if law == 'comm':
            latex_part = f"{fmt_with_paren(a)} \\times {fmt_with_paren(b)} = {fmt_with_paren(b)} \\times {fmt_with_paren(a)}"
            ans = "교환법칙"
            comment = "곱하는 두 수의 앞뒤 '순서'를 바꾸어도 결과가 같다는 성질입니다."
        elif law == 'assoc':
            latex_part = f"\\{{ {fmt_with_paren(a)} \\times {fmt_with_paren(b)} \\}} \\times {fmt_with_paren(c)} = {fmt_with_paren(a)} \\times \\{{ {fmt_with_paren(b)} \\times {fmt_with_paren(c)} \\}}"
            ans = "결합법칙"
            comment = "세 수를 곱할 때, 앞쪽을 먼저 곱하나 뒤쪽을 먼저 곱하나 결과가 같다는 성질입니다."
        else: 
            latex_part = f"{fmt_with_paren(a)} \\times ( {fmt_with_paren(b)} + {fmt_with_paren(c)} ) = {fmt_with_paren(a)} \\times {fmt_with_paren(b)} + {fmt_with_paren(a)} \\times {fmt_with_paren(c)}"
            ans = "분배법칙"
            comment = "괄호 밖의 수를 괄호 안의 숫자들에게 골고루 '분배(나누어)'하여 곱해주는 법칙입니다."
        q_text = "위 등식에 사용된 **연산 법칙**은 무엇입니까?"

    # -----------------------------------------------------------
    # 3-5. 분배법칙의 활용
    # -----------------------------------------------------------
    elif "3-5" in level_name: 
        a = random.choice([-2, 2, -3, 3, -4, 4, -5, 5])
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
        q_text = f"{fmt_with_paren(a)} \\times ( {fmt_with_paren(b)} + {fmt_with_paren(c)} )"
        ans = a * (b + c)
        comment = "괄호 안을 먼저 더해도 되지만, 숫자가 복잡할 땐 분배법칙을 이용해 하나씩 곱해서 꺼내는 것이 더 빠를 수 있습니다."

    # -----------------------------------------------------------
    # 3-6. 역수 구하기
    # -----------------------------------------------------------
    elif "3-6" in level_name: 
        subtype = random.choice(['int', 'frac'])
        if subtype == 'int':
            target = random.choice([-2, -4, -5, -8, -10, 2, 4, 5, 8, 10])
            q_text = f"\\text{{{fmt_with_paren(target)} 의 역수}}"
            ans = 1 / target
        else:
            while True:
                denom = random.choice([2, 3, 4, 5, 7])
                numer = random.choice([i for i in range(-9, 10) if i!=0])
                val = Fraction(numer, denom)
                if val.denominator != 1: 
                    break
            q_text = f"\\text{{{fmt_frac_tex(val.numerator, val.denominator)} 의 역수}}"
            ans = 1 / float(val) 
        comment = "역수는 분모와 분자를 뒤집은 수입니다. 제일 중요한 점: ★부호는 절대 바뀌지 않습니다!★"

    # -----------------------------------------------------------
    # 3-7. 나눗셈의 계산
    # -----------------------------------------------------------
    elif "3-7" in level_name: 
        subtype = random.choice(['int', 'frac'])
        if subtype == 'int':
            n1 = random.choice([i for i in range(-20, 21) if i!=0])
            n2 = random.choice([-5, -4, -2, -1, 1, 2, 4, 5]) 
            n1 = n2 * random.randint(-5, 5) 
            q_text = f"{fmt_with_paren(n1)} \\div {fmt_with_paren(n2)}"
            ans = n1 / n2
        else:
            while True:
                d1 = random.choice([2, 3, 4, 5])
                n1 = random.choice([i for i in range(-9, 10) if i!=0])
                val1 = Fraction(n1, d1)
                d2 = random.choice([2, 3, 4, 5])
                n2 = random.choice([i for i in range(-9, 10) if i!=0])
                val2 = Fraction(n2, d2)
                if val1.denominator != 1 and val2.denominator != 1:
                    break
            q_text = f"({fmt_frac_tex(val1.numerator, val1.denominator)}) \\div ({fmt_frac_tex(val2.numerator, val2.denominator)})"
            ans = float(val1 / val2)
        comment = "나눗셈은 '곱하기 역수'로 바꾸어 계산합니다. 뒤에 있는 수를 뒤집는 것 잊지 마세요!"

    return {'q_text': q_text, 'answer': ans, 'comment': comment, 'type': q_type, 'options': options, 'latex_part': latex_part, 'denom_info': denom_info}