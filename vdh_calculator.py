# -*- coding: utf-8 -*-
import sys
import os
import re
import msvcrt
import math
import urllib.request
import json
import subprocess
from fractions import Fraction
import cmath

HD_CONTENT = """TÀI LIỆU HƯỚNG DẪN SỬ DỤNG CHƯƠNG TRÌNH VDH CALCULATOR
Chương trình hỗ trợ tính toán số học, phân số, trị tuyệt đối, tổ hợp, chỉnh hợp, hoán vị, giải phương trình, hệ phương trình, căn bậc n, lượng giác, quy đổi đơn vị, giải tích và hệ cơ số.

1. TÍNH TOÁN VÀ GIẢI TOÁN ĐẠI SỐ & GIẢI TÍCH
- Phép tính cơ bản: Nhập biểu thức như 15+25, 12*8, (10+5)*2.
- Phân số: Nhập theo cú pháp phan so, ví dụ phan so 1phan2+2phan3.
- Trị tuyệt đối: Nhập trituyetdoi kèm theo số hoặc biểu thức, ví dụ trituyetdoi(-12).
- Tổ hợp - Chỉnh hợp - Hoán vị:
  + Tổ hợp: tohopchap[k]([n]) (ví dụ: tohopchap3(12))
  + Chỉnh hợp: chinhhopchap[k]([n]) (ví dụ: chinhhopchap3(12))
  + Hoán vị: hoanvi[n] (ví dụ: hoanvi5)
- Giải phương trình:
  + Bậc 2 (ax^2 + bx + c = 0): ptb2 a b c (ví dụ: ptb2 1 -3 2)
  + Bậc 3 (ax^3 + bx^2 + cx + d = 0): ptb3 a b c d
  + Bậc 4 (ax^4 + ... + e = 0): ptb4 a b c d e
  + Bậc n: ptbn a_n a_{n-1} ... a_0
- Giải hệ phương trình tuyến tính:
  + Hệ 2 phương trình: he2 a1 b1 c1 a2 b2 c2 (với a1x + b1y = c1)
  + Hệ 3 phương trình: he3 a1 b1 c1 d1 a2 b2 c2 d2 a3 b3 c3 d3
  + Hệ n phương trình: hen [số_ẩn] [danh_sách_hệ_số...]
- Lũy thừa, khai căn và Logarit: 
  + Lũy thừa: 2^3
  + Khai căn: can(n)số (ví dụ can(2)16)
  + Logarit cơ số: log[cơ_số]([giá_trị]) (ví dụ log3(12))
- Giải tích cơ bản theo biến x:
  + Đạo hàm: daohamx^2 hoặc daoham(x^3 + 2*x)
  + Nguyên hàm: nguyenhamx^2 (hoặc nguyenham(x^2))
  + Tích phân xác định từ a đến b: tichphan[a:b](biểu_thức), ví dụ tichphan0:2(x^2)

2. TÍNH TOÁN LƯỢNG GIÁC, QUY ĐỔI ĐƠN VỊ VÀ HỆ CƠ SỐ
- Lượng giác: sin30, cos60, tan45, cot45...
- Quy đổi đơn vị: [Số][Đơn vị nguồn]to[Đơn vị đích] (ví dụ: 5mtofoot, 100usdtovnd).
- Chuyển đổi hệ cơ số:
  + Thập phân sang nhị phân: dectobin120 (hoặc dectobin 120)
  + Thập phân sang bát phân: dectooct64
  + Thập phân sang thập lục phân: dectohex255
  + Nhị phân sang thập phân: bintodec1010
  + Bát phân sang thập phân: octtodec100
  + Thập lục phân sang thập phân: hextodecFF

3. THAO TÁC HỖ TRỢ
- Xem hướng dẫn: gõ hd, 0 hoặc help.
- Nghe lại kết quả: Nhấn Enter khi dòng trống hoặc Ctrl + Enter.
- Thoát: Nhấn Esc."""

def paste_from_clipboard():
    try:
        import ctypes
        ctypes.windll.user32.OpenClipboard(0)
        if ctypes.windll.user32.IsClipboardFormatAvailable(13):
            pcontents = ctypes.windll.user32.GetClipboardData(13)
            data = ctypes.c_wchar_p(pcontents).value
            ctypes.windll.user32.CloseClipboard()
            return data if data else ""
        ctypes.windll.user32.CloseClipboard()
        return ""
    except Exception:
        try: ctypes.windll.user32.CloseClipboard()
        except: pass
        return ""

def copy_to_clipboard(text):
    if not text: return
    try:
        p = subprocess.Popen(['clip'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate(input=str(text).encode('utf-8'))
    except Exception:
        pass

def fetch_live_rates():
    def _fetch():
        global currency_factors
        try:
            url = "https://open.er-api.com/v6/latest/USD"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode('utf-8'))
                if data and 'rates' in data:
                    rates = data['rates']
                    for code in ['VND', 'EUR', 'JPY', 'THB', 'RUB', 'HKD', 'SGD', 'CNY']:
                        if code in rates:
                            currency_factors[code.lower()] = float(rates[code])
        except Exception:
            pass
    import threading
    threading.Thread(target=_fetch, daemon=True).start()

length_factors = {'m': 1.0, 'cm': 100.0, 'mm': 1000.0, 'km': 0.001, 'inch': 39.3701, 'foot': 3.28084}
weight_factors = {'kg': 1.0, 'g': 1000.0, 'mg': 1000000.0, 'lb': 2.20462, 'oz': 35.274, 'tan': 0.001, 'ta': 0.01, 'yen': 0.1, 'tấn': 0.001, 'tạ': 0.01, 'yến': 0.1}
currency_factors = {'usd': 1.0, 'vnd': 25400.0, 'eur': 0.92, 'jpy': 151.0, 'thb': 36.5, 'rub': 93.0, 'hkd': 7.8, 'sgd': 1.35, 'cny': 7.24}
unit_aliases = {'eu': 'eur', 'euro': 'eur', 'vn': 'vnd', 'u': 'usd', 'bat': 'thb', 'rup': 'rub', 'uk': 'hkd', 'up': 'sgd', 'tq': 'cny', 'ndt': 'cny'}

def format_number(num):
    try: num = float(num)
    except ValueError: return str(num)
    num = round(num, 6)
    if num.is_integer(): return str(int(num))
    else: return f"{num:.4f}".rstrip('0').rstrip('.').replace(".", ",")

def format_complex(c):
    if abs(c.imag) < 1e-7:
        return format_number(c.real)
    r = format_number(c.real)
    i = format_number(abs(c.imag))
    sign = " + " if c.imag > 0 else " - "
    return f"{r}{sign}{i}i"

def read_vn_number(n):
    if n == 0: return "không"
    chu_so = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    def doc_3_so(g, doc_tram=False):
        t = g // 100
        c = (g % 100) // 10
        d = g % 10
        res = ""
        if doc_tram or t > 0:
            res += chu_so[t] + " trăm "
            if c == 0 and d > 0: res += "lẻ "
        if c == 1: res += "mười "
        elif c > 1: res += chu_so[c] + " mươi "
        if d == 1 and c > 1: res += "mốt"
        elif d == 4 and c > 1: res += "tư"
        elif d == 5 and c > 0: res += "lăm"
        elif d > 0: res += chu_so[d]
        return res.strip()

    prefix = "âm " if n < 0 else ""
    n = abs(round(n, 6))
    int_part = int(n)
    dec_str = f"{n:.4f}".split('.')[1].rstrip('0') if '.' in f"{n:.4f}" else ""
    
    if int_part == 0: result = "không"
    else:
        chunks = []
        temp = int_part
        while temp > 0:
            chunks.append(temp % 1000)
            temp //= 1000
        units = ["", "ngàn", "triệu", "tỷ", "ngàn tỷ"]
        result_parts = []
        for i in range(len(chunks)-1, -1, -1):
            if chunks[i] == 0 and i > 0: continue
            doc_tram = (i < len(chunks) - 1)
            part = doc_3_so(chunks[i], doc_tram)
            if part: result_parts.append(part + " " + units[i])
        result = " ".join(result_parts).strip()
    
    if dec_str: result += " phẩy " + " ".join([chu_so[int(x)] for x in dec_str])
    return prefix + re.sub(r'\s+', ' ', result).strip()

def evaluate_math(expression):
    try:
        expression = expression.replace("^", "**")
        allowed_chars = "0123456789+-*/.** ()"
        if all(c in allowed_chars for c in expression):
            result = eval(expression)
            num_format = format_number(result)
            text_format = read_vn_number(result)
            return f"Kết quả: {num_format}\nĐọc là: {text_format}", num_format
        else:
            return "Lỗi: Biểu thức toán học chứa ký tự không hợp lệ.", ""
    except Exception as e:
        return f"Lỗi tính toán: {e}", ""

def process_fraction(expression):
    try:
        expr = expression.replace("phanso", "").strip()
        def repl(match):
            num, den = match.groups()
            return f"Fraction({num}, {den})"
        
        expr_parsed = re.sub(r'(\d+)phan(\d+)', repl, expr)
        allowed_chars = "0123456789+-*/().Fraction,"
        if not all(c in allowed_chars or c.isspace() for c in expr_parsed):
            return "Lỗi: Biểu thức phân số chứa ký tự không hợp lệ.", ""
            
        result = eval(expr_parsed, {"Fraction": Fraction})
        
        if isinstance(result, Fraction):
            num = result.numerator
            den = result.denominator
            float_val = float(result)
            res_str = f"{num}" if den == 1 else f"{num}/{den}"
            text_format = read_vn_number(float_val)
            return f"Kết quả phân số: {res_str} (Thập phân: {format_number(float_val)})\nĐọc là: {text_format}", res_str
        else:
            num_format = format_number(result)
            return f"Kết quả: {num_format}", num_format
    except Exception as e:
        return f"Lỗi tính toán phân số: {e}", ""

def solve_quadratic(a, b, c):
    if a == 0:
        if b == 0:
            return "Phương trình vô nghiệm." if c != 0 else "Phương trình vô số nghiệm."
        return f"Phương trình bậc nhất, nghiệm x = {format_number(-c / b)}"
    delta = b**2 - 4*a*c
    if delta > 0:
        x1 = (-b + math.sqrt(delta)) / (2*a)
        x2 = (-b - math.sqrt(delta)) / (2*a)
        return f"Phương trình có 2 nghiệm phân biệt:\nx1 = {format_number(x1)}\nx2 = {format_number(x2)}"
    elif delta == 0:
        x = -b / (2*a)
        return f"Phương trình có nghiệm kép: x = {format_number(x)}"
    else:
        real_part = -b / (2*a)
        imag_part = math.sqrt(-delta) / (2*a)
        c1 = complex(real_part, imag_part)
        c2 = complex(real_part, -imag_part)
        return f"Phương trình có 2 nghiệm phức:\nx1 = {format_complex(c1)}\nx2 = {format_complex(c2)}"

def solve_cubic(a, b, c, d):
    if a == 0:
        return solve_quadratic(b, c, d)
    b /= a
    c /= a
    d /= a
    
    p = c - (b**2)/3.0
    q = (2*(b**3))/27.0 - (b*c)/3.0 + d
    discriminant = (q/2.0)**2 + (p/3.0)**3
    
    roots = []
    def cbrt(val):
        return math.copysign(abs(val)**(1/3.0), val)
    if discriminant > 0:
        sqrt_disc = math.sqrt(discriminant)
        u = cbrt(-q/2.0 + sqrt_disc)
        v = cbrt(-q/2.0 - sqrt_disc)
        roots.append(complex(u + v - b/3.0, 0))
    elif discriminant == 0:
        u_val = cbrt(-q/2.0)
        roots.append(complex(2*u_val - b/3.0, 0))
        roots.append(complex(-u_val - b/3.0, 0))
    else:
        r = math.sqrt(-(p/3.0)**3)
        phi = math.acos(max(-1.0, min(1.0, -q / (2.0 * r))))
        s = 2.0 * math.sqrt(-p/3.0)
        for k in range(3):
            roots.append(complex(s * math.cos((phi + 2*k*math.pi)/3.0) - b/3.0, 0))
            
    res_str = "Các nghiệm của phương trình bậc 3:\n"
    for i, r in enumerate(roots, 1):
        res_str += f"x{i} = {format_complex(r)}\n"
    return res_str.strip()

def solve_polynomial(coeffs):
    n = len(coeffs) - 1
    if n <= 0:
        return "Hệ số không hợp lệ."
    if n == 1:
        a, b = coeffs[0], coeffs[1]
        if a == 0: return "Vô nghiệm hoặc vô số nghiệm."
        return f"Nghiệm x = {format_number(-b/a)}"
    if n == 2:
        return solve_quadratic(coeffs[0], coeffs[1], coeffs[2])
    if n == 3:
        return solve_cubic(coeffs[0], coeffs[1], coeffs[2], coeffs[3])
    
    try:
        import numpy as np
        rts = np.roots(coeffs)
        res = "Các nghiệm phương trình bậc " + str(n) + ":\n"
        for i, r in enumerate(rts, 1):
            res += f"x{i} = {format_complex(complex(r))}\n"
        return res.strip()
    except Exception:
        return "Cần cài đặt thư viện hỗ trợ nâng cao cho phương trình bậc lớn hơn 3."

def solve_linear_system(matrix):
    n = len(matrix)
    for i in range(n):
        max_el = abs(matrix[i][i])
        max_row = i
        for k in range(i + 1, n):
            if abs(matrix[k][i]) > max_el:
                max_el = abs(matrix[k][i])
                max_row = k
                
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        if abs(matrix[i][i]) < 1e-11:
            return "Hệ phương trình vô nghiệm hoặc có vô số nghiệm."
            
        for k in range(i + 1, n):
            c = -matrix[k][i] / matrix[i][i]
            for j in range(i, n + 1):
                if i == j:
                    matrix[k][j] = 0
                else:
                    matrix[k][j] += c * matrix[i][j]
                    
    x = [0.0 for _ in range(n)]
    for i in range(n - 1, -1, -1):
        x[i] = matrix[i][n]
        for j in range(i + 1, n):
            x[i] -= matrix[i][j] * x[j]
        x[i] /= matrix[i][i]
        
    res = "Nghiệm của hệ phương trình:\n"
    for i, val in enumerate(x, 1):
        res += f"x{i} = {format_number(val)}\n"
    return res.strip()

def compute_derivative(expr_str):
    expr = expr_str.replace(" ", "")
    if expr.startswith("(") and expr.endswith(")"):
        expr = expr[1:-1]
    
    terms = re.findall(r'([+\-]?\d*\.?\d*\*?x(?:\^\d+)?)', expr)
    if not terms:
        if not re.search(r'x', expr):
            return "Đạo hàm của hằng số = 0", "0"
        return "Chưa hỗ trợ biểu thức đạo hàm phức tạp này.", ""
    
    deriv_parts = []
    for t in terms:
        t = t.replace("*", "")
        m = re.match(r'([+\-]?\d*\.?\d*)x(?:\^(\d+))?', t)
        if m:
            coef_str, exp_str = m.groups()
            coef = 1.0 if coef_str in ["", "+"] else (-1.0 if coef_str == "-" else float(coef_str))
            exp = int(exp_str) if exp_str else 1
            
            new_coef = coef * exp
            new_exp = exp - 1
            
            if new_exp == 0:
                deriv_parts.append(f"{new_coef:+g}".replace("+", "+ "))
            elif new_exp == 1:
                deriv_parts.append(f"{new_coef:+g}*x".replace("+", "+ "))
            else:
                deriv_parts.append(f"{new_coef:+g}*x^{new_exp}".replace("+", "+ "))
    
    res = " ".join(deriv_parts).strip()
    if res.startswith("+"):
        res = res[1:].strip()
    return f"Đạo hàm: {res if res else '0'}", res

def compute_integral(expr_str):
    expr = expr_str.replace(" ", "")
    if expr.startswith("(") and expr.endswith(")"):
        expr = expr[1:-1]
        
    terms = re.findall(r'([+\-]?\d*\.?\d*\*?x(?:\^\d+)?)', expr)
    if not terms:
        if not re.search(r'x', expr):
            try:
                c = float(expr)
                c_str = format_number(c)
                return f"Nguyên hàm: {c_str}*x + C", f"{c_str}*x"
            except:
                pass
        return "Chưa hỗ trợ biểu thức nguyên hàm phức tạp này.", ""
        
    integ_parts_frac = []
    integ_parts_dec = []
    
    for t in terms:
        t = t.replace("*", "")
        m = re.match(r'([+\-]?\d*\.?\d*)x(?:\^(\d+))?', t)
        if m:
            coef_str, exp_str = m.groups()
            if coef_str in ["", "+"]:
                coef_frac = Fraction(1, 1)
            elif coef_str == "-":
                coef_frac = Fraction(-1, 1)
            else:
                coef_frac = Fraction(coef_str)
                
            exp = int(exp_str) if exp_str else 1
            new_exp = exp + 1
            new_coef_frac = coef_frac / new_exp
            
            num = new_coef_frac.numerator
            den = new_coef_frac.denominator
            
            if den == 1:
                frac_part = str(num)
            else:
                frac_part = f"{num}/{den}"
                
            float_val = float(new_coef_frac)
            dec_part = format_number(float_val)
            
            var_part = f"x^{new_exp}" if new_exp > 1 else "x"
            
            if frac_part == "1": t_frac = var_part
            elif frac_part == "-1": t_frac = f"-{var_part}"
            else: t_frac = f"{frac_part}*{var_part}"
            
            if dec_part == "1": t_dec = var_part
            elif dec_part == "-1": t_dec = f"-{var_part}"
            else: t_dec = f"{dec_part}*{var_part}"
            
            integ_parts_frac.append(t_frac)
            integ_parts_dec.append(t_dec)
            
    res_frac = " + ".join(integ_parts_frac).replace("+ -", "- ")
    res_dec = " + ".join(integ_parts_dec).replace("+ -", "- ")
    
    if res_frac != res_dec:
        return f"Nguyên hàm:\n- Dạng phân số: {res_frac} + C\n- Dạng thập phân: {res_dec} + C", res_dec
    else:
        return f"Nguyên hàm: {res_frac} + C", res_dec

def compute_definite_integral(a, b, expr_str):
    try:
        n = 1000
        h = (b - a) / n
        total = 0.5 * (eval_at_x(expr_str, a) + eval_at_x(expr_str, b))
        for i in range(1, n):
            total += eval_at_x(expr_str, a + i * h)
        total *= h
        return f"Tích phân từ {a} đến {b} = {format_number(total)}", format_number(total)
    except Exception as e:
        return f"Lỗi tính tích phân: {e}", ""

def eval_at_x(expr, x_val):
    clean_expr = expr.replace("^", "**")
    clean_expr = re.sub(r'(\d)x', r'\1*x', clean_expr)
    clean_expr = clean_expr.replace("x", str(x_val))
    return eval(clean_expr)

def process_query(query):
    if query.startswith("phanso"):
        return process_fraction(query)

    if query.startswith("trituyetdoi"):
        val_expr = query.replace("trituyetdoi", "").strip()
        if val_expr.startswith("(") and val_expr.endswith(")"):
            val_expr = val_expr[1:-1]
        try:
            val_expr_eval = val_expr.replace("^", "**")
            allowed_chars = "0123456789+-*/.** ()"
            if all(c in allowed_chars for c in val_expr_eval):
                res = abs(eval(val_expr_eval))
                num_format = format_number(res)
                text_format = read_vn_number(res)
                return f"Kết quả trị tuyệt đối: {num_format}\nĐọc là: {text_format}", num_format
            else:
                return "Lỗi: Biểu thức trị tuyệt đối chứa ký tự không hợp lệ.", ""
        except Exception as e:
            return f"Lỗi tính trị tuyệt đối: {e}", ""

    match_tohop = re.match(r"^tohopchap(\d+)\(([\d\.]+)\)$", query)
    if match_tohop:
        k_str, n_str = match_tohop.groups()
        k, n = int(k_str), int(n_str)
        if k > n: return "Lỗi: k không được lớn hơn n.", ""
        res = math.comb(n, k)
        return f"Kết quả tổ hợp chập {k} của {n}: {format_number(res)}", format_number(res)

    match_chinhhop = re.match(r"^chinhhopchap(\d+)\(([\d\.]+)\)$", query)
    if match_chinhhop:
        k_str, n_str = match_chinhhop.groups()
        k, n = int(k_str), int(n_str)
        if k > n: return "Lỗi: k không được lớn hơn n.", ""
        res = math.perm(n, k)
        return f"Kết quả chỉnh hợp chập {k} của {n}: {format_number(res)}", format_number(res)

    match_hoanvi = re.match(r"^hoanvi(\d+)$", query)
    if match_hoanvi:
        n = int(match_hoanvi.groups()[0])
        res = math.factorial(n)
        return f"Kết quả hoán vị của {n}: {format_number(res)}", format_number(res)

    if query.startswith("daoham"):
        return compute_derivative(query.replace("daoham", "").strip())

    if query.startswith("nguyenham"):
        return compute_integral(query.replace("nguyenham", "").strip())

    match_tp = re.match(r"^tichphan([-\d\.]+):([-\d\.]+)\((.+)\)$", query)
    if match_tp:
        a_str, b_str, expr_part = match_tp.groups()
        return compute_definite_integral(float(a_str), float(b_str), expr_part)

    match_log = re.match(r"^log(\d+)\(([\d\.]+)\)$", query)
    if match_log:
        base_str, val_str = match_log.groups()
        base, val = float(base_str), float(val_str)
        if base <= 0 or base == 1 or val <= 0:
            return "Lỗi: Cơ số logarit phải > 0 và khác 1, giá trị phải > 0.", ""
        res = math.log(val, base)
        base_display = int(base) if base.is_integer() else base
        return f"Kết quả: log{base_display}({format_number(val)}) = {format_number(res)}", format_number(res)

    if query.startswith("dectobin"):
        try: val = int(query.replace("dectobin", "").strip()); return f"Nhị phân: {bin(val)[2:]}", bin(val)[2:]
        except: return "Lỗi cú pháp dectobin[số]", ""
    if query.startswith("dectooct"):
        try: val = int(query.replace("dectooct", "").strip()); return f"Bát phân: {oct(val)[2:]}", oct(val)[2:]
        except: return "Lỗi cú pháp dectooct[số]", ""
    if query.startswith("dectohex"):
        try: val = int(query.replace("dectohex", "").strip()); return f"Thập lục phân: {hex(val)[2:].upper()}", hex(val)[2:].upper()
        except: return "Lỗi cú pháp dectohex[số]", ""
    if query.startswith("bintodec"):
        try: val = query.replace("bintodec", "").strip(); res = int(val, 2); return f"Thập phân: {res}", str(res)
        except: return "Lỗi cú pháp bintodec[chuỗi_nhị_phân]", ""
    if query.startswith("octtodec"):
        try: val = query.replace("octtodec", "").strip(); res = int(val, 8); return f"Thập phân: {res}", str(res)
        except: return "Lỗi cú pháp octtodec[chuỗi_bát_phân]", ""
    if query.startswith("hextodec"):
        try: val = query.replace("hextodec", "").strip(); res = int(val, 16); return f"Thập phân: {res}", str(res)
        except: return "Lỗi cú pháp hextodec[chuỗi_hex]", ""

    match_ptb2 = re.match(r"^ptb2\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)$", query)
    if match_ptb2:
        a, b, c = map(float, match_ptb2.groups())
        res = solve_quadratic(a, b, c)
        return res, ""

    match_ptb3 = re.match(r"^ptb3\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)$", query)
    if match_ptb3:
        a, b, c, d = map(float, match_ptb3.groups())
        res = solve_cubic(a, b, c, d)
        return res, ""

    match_ptb4 = re.match(r"^ptb4\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)$", query)
    if match_ptb4:
        coeffs = list(map(float, match_ptb4.groups()))
        res = solve_polynomial(coeffs)
        return res, ""

    if query.startswith("ptbn"):
        parts = query.replace("ptbn", "").strip().split()
        try:
            coeffs = [float(x) for x in parts]
            res = solve_polynomial(coeffs)
            return res, ""
        except Exception:
            return "Lỗi cú pháp phương trình bậc n. Dùng: ptbn [hệ_số...]", ""

    match_he2 = re.match(r"^he2\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)$", query)
    if match_he2:
        vals = list(map(float, match_he2.groups()))
        matrix = [
            [vals[0], vals[1], vals[2]],
            [vals[3], vals[4], vals[5]]
        ]
        return solve_linear_system(matrix), ""

    match_he3 = re.match(r"^he3\s+" + r"\s+".join([r"([-\d\.]+)" for _ in range(12)]) + r"$", query)
    if match_he3:
        vals = list(map(float, match_he3.groups()))
        matrix = [
            [vals[0], vals[1], vals[2], vals[3]],
            [vals[4], vals[5], vals[6], vals[7]],
            [vals[8], vals[9], vals[10], vals[11]]
        ]
        return solve_linear_system(matrix), ""

    if query.startswith("hen"):
        parts = query.replace("hen", "").strip().split()
        if len(parts) < 1:
            return "Lỗi cú pháp hệ n phương trình.", ""
        try:
            n = int(parts[0])
            vals = [float(x) for x in parts[1:]]
            if len(vals) != n * (n + 1):
                return f"Lỗi: Hệ {n} phương trình cần đúng {n*(n+1)} hệ số.", ""
            matrix = []
            idx = 0
            for i in range(n):
                row = vals[idx:idx+n+1]
                matrix.append(row)
                idx += n + 1
            return solve_linear_system(matrix), ""
        except Exception as e:
            return f"Lỗi xử lý hệ n phương trình: {e}", ""

    query = query.replace(" ", "") 
    query = query.replace("$", "usd")

    if query in ['hd', '0', 'help']:
        dir_path = os.path.dirname(os.path.abspath(__file__))
        doc_file = os.path.join(dir_path, "hd.txt")
        try:
            with open(doc_file, "w", encoding="utf-8") as f:
                f.write(HD_CONTENT)
            subprocess.Popen(["notepad.exe", doc_file])
            return "Đã mở tài liệu hướng dẫn sử dụng.", ""
        except Exception as e:
            return f"Lỗi khi mở tài liệu: {e}", ""
    
    match_trig = re.match(r"^(sin|cos|tan|tag|cot)\(?([-]?[\d\.]+)\)?$", query)
    if match_trig:
        func, val_str = match_trig.groups()
        try: x = float(val_str)
        except ValueError: return "Lỗi: Giá trị góc độ không hợp lệ.", ""
        rad = math.radians(x)
        if func == 'sin': res = math.sin(rad)
        elif func == 'cos': res = math.cos(rad)
        elif func in ['tan', 'tag']: res = math.tan(rad)
        elif func == 'cot': res = 1 / math.tan(rad)
        return f"Kết quả: {func}({format_number(x)}) = {format_number(res)}", format_number(res)

    match_root = re.match(r"^can\((\d+)\)([-]?[\d\.]+)$", query)
    if match_root:
        n_str, x_str = match_root.groups()
        n, x = int(n_str), float(x_str)
        if n == 0: return "Lỗi: Không tồn tại căn bậc không.", ""
        if x < 0 and n % 2 == 0: return "Lỗi: Căn bậc chẵn của số âm.", ""
        res = - (abs(x) ** (1 / n)) if x < 0 else x ** (1 / n)
        return f"Kết quả: căn({n}) của {format_number(x)} = {format_number(res)}", format_number(res)

    match_unit = re.match(r"^([\d\.]+)([a-zà-ỹ0-9]+)to([a-zà-ỹ0-9]+)$", query)
    if match_unit:
        val_str, from_u, to_u = match_unit.groups()
        if from_u in unit_aliases: from_u = unit_aliases[from_u]
        if to_u in unit_aliases: to_u = unit_aliases[to_u]
        try: value = float(val_str)
        except ValueError: return "Lỗi: Giá trị số không hợp lệ.", ""

        res = None
        if from_u in length_factors and to_u in length_factors:
            res = value / length_factors[from_u] * length_factors[to_u]
        elif from_u in weight_factors and to_u in weight_factors:
            res = value / weight_factors[from_u] * weight_factors[to_u]
        elif from_u in currency_factors and to_u in currency_factors:
            res = value / currency_factors[from_u] * currency_factors[to_u]
            
        if res is not None:
            return f"Kết quả: {format_number(value)} {from_u} = {format_number(res)} {to_u}", format_number(res)
        else:
            return f"Lỗi: Không hỗ trợ chuyển đổi đơn vị này.", ""
            
    return evaluate_math(query)

def get_input_with_hotkeys():
    user_input = ""
    while True:
        char = msvcrt.getwch()
        code = ord(char)
        if code == 22:
            pasted_text = paste_from_clipboard()
            if pasted_text:
                pasted_text = pasted_text.replace('\n', '').replace('\r', '').strip()
                user_input += pasted_text
                sys.stdout.write(pasted_text)
                sys.stdout.flush()
        elif code == 27:
            print()
            return "thoat"
        elif code == 10 or code == 13:
            print()
            if user_input.strip() == "": return "nl"
            return user_input
        elif code == 8:
            if len(user_input) > 0:
                user_input = user_input[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        elif code == 0 or code == 224:
            msvcrt.getwch()
        elif code >= 32:
            user_input += char
            sys.stdout.write(char)
            sys.stdout.flush()

def main():
    fetch_live_rates()

    if len(sys.argv) >= 2:
        query = "".join(sys.argv[1:]).lower()
        res_text, copy_text = process_query(query)
        print(res_text)
        copy_to_clipboard(copy_text)
        return
    
    last_result = "Chưa có kết quả nào để nghe lại."
    
    while True:
        try:
            query = get_input_with_hotkeys().strip().lower()
            if query == 'thoat':
                break
            if query == 'nl':
                print(last_result)
                continue
                
            result_text, copy_text = process_query(query)
            print(result_text)
            copy_to_clipboard(copy_text)
            last_result = result_text
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()