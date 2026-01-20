import random
from fractions import Fraction
from utils import fmt_textbook, fmt_frac_tex

def generate_stage1(level_name):
    q_text = ""
    ans = 0
    comment = "" 
    q_type = "numeric" 
    latex_part = "" 
    options = [] 
    denom_info = 1 

    # -----------------------------------------------------------
    # 1-1. 정수와 유리수의 분류
    # -----------------------------------------------------------
    if "1-1" in level_name:
        q_type = "ox"
        types = ['int_is_rational', 'nat_is_int', 'zero_is_nat', 'neg_is_nat', 'frac_is_int']
        weights = [5, 5, 1, 5, 5] 
        case = random.choices(types, weights=weights, k=1)[0]

        if case == 'int_is_rational':
            n = random.randint(-10, 10)
            latex_part = fmt_textbook(n)
            q_text = "은(는) **유리수**이다."
            ans = "O"
            comment = "정수도 분수(분모가 1인 분수) 꼴로 나타낼 수 있으므로 유리수에 포함됩니다."
        elif case == 'nat_is_int':
            n = random.randint(1, 10)
            latex_part = f"+{n}"
            q_text = "은(는) **자연수**이다."
            ans = "O"
            comment = "양의 정수는 자연수와 같은 말입니다."
        elif case == 'zero_is_nat':
            latex_part = "0"
            q_text = "은(는) **자연수**이다."
            ans = "X"
            comment = "0은 정수이지만, 개수를 셀 때 쓰는 자연수(1, 2, 3...)에는 포함되지 않습니다."
        elif case == 'neg_is_nat':
            n = random.randint(1, 10)
            latex_part = f"-{n}"
            q_text = "은(는) **자연수**이다."
            ans = "X"
            comment = "자연수는 양의 정수만을 의미합니다. 음수는 포함되지 않아요."
        elif case == 'frac_is_int':
            numer = random.choice([1, 2, 4, 5])
            denom = 3
            latex_part = fmt_frac_tex(numer, denom)
            q_text = "은(는) **정수**이다."
            ans = "X"
            comment = "약분했을 때 분모가 1이 되지 않는 분수는 정수가 아닌 유리수입니다."

    # -----------------------------------------------------------
    # 1-2. 수직선 위의 수
    # -----------------------------------------------------------
    elif "1-2" in level_name: 
        case = random.choice(['int', 'dec', 'frac3', 'frac4'])
        if case == 'int':
            ans = random.randint(-4, 4)
            denom_info = 1
            comment = "원점(0)을 기준으로 오른쪽은 양수(+), 왼쪽은 음수(-)입니다."
        elif case == 'dec':
            ans = random.choice([n/2 for n in range(-7, 8) if n % 2 != 0])
            denom_info = 2
            comment = "정수와 정수 사이가 몇 칸으로 나뉘어 있는지 확인해보세요. (2등분)"
        elif case == 'frac3':
            ans = random.choice([n for n in range(-11, 12) if n % 3 != 0]) / 3
            denom_info = 3
            comment = "0에서부터 작은 눈금 몇 칸을 이동했는지 세어보세요. (3등분)"
        else:
            ans = random.choice([n for n in range(-15, 16) if n % 4 != 0]) / 4
            denom_info = 4
            comment = "정수 사이가 4칸으로 나뉘어 있습니다. 한 칸의 크기는 0.25(1/4)입니다."
        
        q_text = "다음 수직선 위에 있는 **빨간 점의 좌표**를 구하세요."
        ans = float(ans)

    # -----------------------------------------------------------
    # 1-3. 절댓값의 이해
    # -----------------------------------------------------------
    elif "1-3" in level_name: 
        prob_type = random.choice(['calc_abs', 'find_num'])

        if prob_type == 'calc_abs':
            target = random.choice([i for i in range(-20, 21) if i !=0])
            q_text = f"$| {fmt_textbook(target)} | = ?$"
            ans = abs(target)
            comment = "절댓값은 수직선 위에서 원점(0)과 그 점 사이의 '거리'를 뜻합니다. 거리는 항상 0보다 크거나 같습니다."
        else:
            is_frac = random.choice([True, False])
            if is_frac:
                denom = random.choice([2, 3, 4, 5])
                numer = random.randint(1, 10)
                abs_val_frac = Fraction(numer, denom)
                
                if abs_val_frac.denominator == 1:
                    abs_val_str = str(abs_val_frac.numerator)
                else:
                    abs_val_str = f"\\frac{{{abs_val_frac.numerator}}}{{{abs_val_frac.denominator}}}"
                
                abs_val_real = float(abs_val_frac)
            else:
                abs_val_real = random.randint(2, 15)
                abs_val_str = str(abs_val_real)

            condition = random.choice(["양수", "음수"])
            
            q_text = f"절댓값이 ${abs_val_str}$인 **{condition}**를 구하세요."
            
            if condition == "양수":
                ans = abs_val_real
                comment = f"절댓값이 {abs_val_str}인 수는 +{abs_val_str}와 -{abs_val_str} 두 개가 있습니다. 그중 0보다 큰 수를 찾아보세요."
            else:
                ans = -abs_val_real
                comment = f"절댓값이 {abs_val_str}인 수는 +{abs_val_str}와 -{abs_val_str} 두 개가 있습니다. 그중 0보다 작은 수를 찾아보세요."

    # -----------------------------------------------------------
    # 1-4. 수의 대소 관계
    # -----------------------------------------------------------
    elif "1-4" in level_name: 
        q_type = "choice" 
        sub_type = random.choice(['int', 'float', 'frac'])
        val_a, val_b = 0, 0
        str_a, str_b = "", ""

        # 힌트 기본값 설정
        base_comment = "수직선에서 더 오른쪽에 있는 수가 큰 수입니다."

        if sub_type == 'int':
            a = random.randint(-10, 10)
            b = random.randint(-10, 10)
            while a == b: b = random.randint(-10, 10)
            val_a, val_b = a, b
            str_a, str_b = fmt_textbook(a), fmt_textbook(b)
            if a < 0 and b < 0:
                base_comment = "둘 다 음수일 때는 절댓값이 작은 수(0에 더 가까운 수)가 더 큽니다."
            elif (a < 0 < b) or (b < 0 < a):
                base_comment = "양수는 항상 음수보다 큽니다."

        elif sub_type == 'float':
            a = round(random.uniform(-5, 5), 1)
            b = round(random.uniform(-5, 5), 1)
            while a == b: b = round(random.uniform(-5, 5), 1)
            val_a, val_b = a, b
            str_a, str_b = fmt_textbook(a), fmt_textbook(b)
            
        else: 
            denom = random.choice([2, 5, 10])
            a_num = random.randint(-10, 10)
            b_num = random.randint(-10, 10)
            while a_num == b_num: b_num = random.randint(-10, 10)
            val_a = Fraction(a_num, denom)
            val_b = Fraction(b_num, denom)
            str_a = fmt_frac_tex(a_num, denom)
            str_b = fmt_frac_tex(b_num, denom)
            base_comment = "분수의 크기 비교가 어렵다면 통분하거나 소수로 바꾸어 생각해보세요."

        # 절댓값 적용 확률 (25%)
        abs_case = random.choices([0, 1, 2, 3], weights=[9, 1, 1, 1], k=1)[0]
        
        real_val_a = val_a
        real_val_b = val_b

        if abs_case == 1 or abs_case == 3: # A에 절댓값
            str_a = f"| {str_a} |"
            real_val_a = abs(val_a)
            base_comment = "절댓값 기호(| |)가 있는 수는 부호를 뗀 양수 값으로 생각해야 합니다."
        
        if abs_case == 2 or abs_case == 3: # B에 절댓값
            str_b = f"| {str_b} |"
            real_val_b = abs(val_b)
            base_comment = "절댓값 기호(| |)가 있는 수는 부호를 뗀 양수 값으로 생각해야 합니다."

        options = [str_a, str_b]
        ans = 0 if real_val_a > real_val_b else 1
        q_text = "다음 두 수 중 **더 큰 수**를 고르세요."
        comment = base_comment

    return {'q_text': q_text, 'answer': ans, 'comment': comment, 'type': q_type, 'options': options, 'latex_part': latex_part, 'denom_info': denom_info}