import random
from fractions import Fraction
from utils import fmt_textbook, fmt_with_paren, fmt_frac_tex

def generate_stage2(level_name):
    q_text = ""
    ans = 0
    comment = "" 
    q_type = "numeric" 
    latex_part = "" 
    options = [] 
    denom_info = 1 

    # -----------------------------------------------------------
    # 2-1. 부호가 같은 덧셈
    # -----------------------------------------------------------
    if "2-1" in level_name: 
        sign = random.choice([1, -1])
        n1 = sign * random.randint(1, 10)
        n2 = sign * random.randint(1, 10)
        q_text = f"{fmt_with_paren(n1)} + {fmt_with_paren(n2)}"
        ans = n1 + n2
        comment = "같은 팀(부호)끼리 만났네요! 부호는 그대로 두고, 숫자(절댓값)끼리 더해서 힘을 합쳐주세요."

    # -----------------------------------------------------------
    # 2-2. 부호가 다른 덧셈
    # -----------------------------------------------------------
    elif "2-2" in level_name: 
        n1 = random.choice([i for i in range(-15, 16) if i != 0])
        n2 = -1 * n1 + random.choice([-5, -4, -3, 3, 4, 5])
        q_text = f"{fmt_with_paren(n1)} + {fmt_with_paren(n2)}"
        ans = n1 + n2
        comment = "다른 팀(부호)끼리 만났네요! 힘(절댓값)이 더 센 쪽의 부호를 따르고, 숫자는 큰 수에서 작은 수를 빼야 합니다."

    # -----------------------------------------------------------
    # 2-3. 덧셈의 연산법칙
    # -----------------------------------------------------------
    elif "2-3" in level_name: 
        q_type = "law_choice" 
        law = random.choice(['comm', 'assoc'])
        if law == 'comm':
            a = random.randint(-10, 10)
            b = random.randint(-10, 10)
            latex_part = f"{fmt_with_paren(a)} + {fmt_with_paren(b)} = {fmt_with_paren(b)} + {fmt_with_paren(a)}"
            ans = "교환법칙"
            comment = "덧셈에서는 두 수의 자리를 서로 '교환'해도 결과가 같습니다."
        else:
            a = random.randint(-5, 5)
            b = random.randint(-5, 5)
            c = random.randint(-5, 5)
            latex_part = f"\\{{ {fmt_with_paren(a)} + {fmt_with_paren(b)} \\}} + {fmt_with_paren(c)} = {fmt_with_paren(a)} + \\{{ {fmt_with_paren(b)} + {fmt_with_paren(c)} \\}}"
            ans = "결합법칙"
            comment = "덧셈에서는 어느 것을 먼저 묶어서(결합해서) 계산해도 결과가 같습니다. 괄호의 위치를 잘 보세요."
        q_text = "위 등식에 사용된 **덧셈의 연산 법칙**은 무엇입니까?"

    # -----------------------------------------------------------
    # 2-4. 정수의 뺄셈
    # -----------------------------------------------------------
    elif "2-4" in level_name: 
        n1 = random.randint(-10, 10)
        n2 = random.randint(-10, 10)
        q_text = f"{fmt_with_paren(n1)} - {fmt_with_paren(n2)}"
        ans = n1 - n2
        comment = "뺄셈은 덧셈으로 바꾸어 계산하세요. (빼기 + 빼기)는 (더하기 + 더하기)로, (빼기 + 더하기)는 (더하기 + 빼기)로 바뀝니다."

    # -----------------------------------------------------------
    # 2-5, 2-6. 유리수의 덧셈과 뺄셈
    # -----------------------------------------------------------
    elif "2-5" in level_name or "2-6" in level_name:
        q_subtype = random.choices(['frac', 'dec'], weights=[15, 1])[0]
        op = random.choice(['+', '-'])
        if q_subtype == 'frac':
            while True:
                denom1 = random.choice([2, 3, 4, 5, 10])
                denom2 = random.choice([2, 3, 4, 5, 10]) if "2-6" in level_name else denom1
                num1 = random.choice([i for i in range(-9, 10) if i!=0])
                num2 = random.choice([i for i in range(-9, 10) if i!=0])
                val1 = Fraction(num1, denom1)
                val2 = Fraction(num2, denom2)
                if val1.denominator != 1 and val2.denominator != 1:
                    break
            q_text = f"({fmt_frac_tex(num1, denom1)}) {op} ({fmt_frac_tex(num2, denom2)})"
            ans = float(val1 + val2) if op == '+' else float(val1 - val2)
            comment = "분모가 다르면 '통분'이 먼저입니다. 뺄셈은 덧셈으로 고치고, 부호 실수에 주의하세요!"
        else:
            while True:
                n1 = round(random.uniform(-5, 5), 1)
                n2 = round(random.uniform(-5, 5), 1)
                if n1 != 0 and n2 != 0 and not n1.is_integer() and not n2.is_integer():
                    break
            q_text = f"({fmt_textbook(n1)}) {op} ({fmt_textbook(n2)})"
            ans = round(n1 + n2, 1) if op == '+' else round(n1 - n2, 1)
            comment = "소수점을 세로로 나란히 맞추어 계산하세요. 뺄셈은 덧셈으로 바꾸는 것이 안전합니다."

    # -----------------------------------------------------------
    # 2-7. 덧셈과 뺄셈의 혼합
    # -----------------------------------------------------------
    elif "2-7" in level_name:
        q_type = random.choices(['int', 'frac', 'float'], weights=[10, 10, 1])[0]
        nums = []
        count = random.randint(2, 4) 
        if q_type == 'int':
            for _ in range(count): nums.append(random.randint(-10, 10))
            ans = sum(nums)
            parts = []
            for i, n in enumerate(nums):
                if n == 0: continue
                if i == 0: parts.append(str(n))
                else: parts.append(f"+ {n}" if n > 0 else f"- {abs(n)}")
            q_text = " ".join(parts)
        elif q_type == 'float':
            for _ in range(count): nums.append(round(random.uniform(-5, 5), 1))
            ans = sum(nums)
            parts = []
            for i, n in enumerate(nums):
                if n == 0: continue
                if i == 0: parts.append(str(n))
                else: parts.append(f"+ {n}" if n > 0 else f"- {abs(n)}")
            q_text = " ".join(parts)
        else: 
            denom = random.choice([2, 4, 5])
            frac_nums = []
            parts = []
            for _ in range(count):
                numer = random.randint(-9, 9)
                if numer == 0: numer = 1
                val = Fraction(numer, denom)
                frac_nums.append(val)
                f_num = val.numerator
                f_den = val.denominator
                if f_den == 1:
                    if _ == 0: parts.append(str(f_num))
                    else:
                        if f_num > 0: parts.append(f"+ {f_num}")
                        else: parts.append(f"- {abs(f_num)}")
                else:
                    if _ == 0: parts.append(f"{'-' if f_num < 0 else ''}\\frac{{{abs(f_num)}}}{{{f_den}}}")
                    else: parts.append(f"{'+' if f_num > 0 else '-'} \\frac{{{abs(f_num)}}}{{{f_den}}}")
            q_text = " ".join(parts)
            ans = float(sum(frac_nums))
            
        comment = "모든 뺄셈을 덧셈으로 바꾸세요. 그 다음 양수는 양수끼리(+), 음수는 음수끼리(-) 모아서 계산하면 훨씬 빠르고 정확합니다."

    return {'q_text': q_text, 'answer': ans, 'comment': comment, 'type': q_type, 'options': options, 'latex_part': latex_part, 'denom_info': denom_info}