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

# Nội dung tài liệu hướng dẫn được nhúng sẵn vào mã nguồn
HD_CONTENT = """TÀI LIỆU HƯỚNG DẪN SỬ DỤNG CHƯƠNG TRÌNH VDH CALCULATOR
Chương trình hỗ trợ tính toán số học, phân số, trị tuyệt đối, tổ hợp, chỉnh hợp, hoán vị, căn bậc n, lượng giác và quy đổi đơn vị.

1. TÍNH TOÁN SỐ HỌC, PHÂN SỐ, TRỊ TUYỆT ĐỐI VÀ TỔ HỢP - CHỈNH HỢP - HOÁN VỊ
- Phép tính cơ bản: Nhập trực tiếp biểu thức cộng, trừ, nhân, chia như 15+25, 100-35, 12*8, 144/12 hoặc kết hợp dấu ngoặc (10+5)*2 rồi nhấn Enter.
- Phép tính phân số: Nhập theo cú pháp phan so, ví dụ phan so 1phan2+2phan3 rồi nhấn Enter.
- Trị tuyệt đối: Nhập trituyetdoi kèm theo số, ví dụ trituyetdoi(-12).
- Tổ hợp: Nhập theo cú pháp tohopchap[k]cua[n], ví dụ tohopchap3cua12.
- Chỉnh hợp: Nhập theo cú pháp chinhhopchap[k]cua[n], ví dụ chinhhopchap3cua12.
- Hoán vị: Nhập theo cú pháp hoanvi[n], ví dụ hoanvi5.
- Phép tính lũy thừa (mũ): Dùng dấu ^, ví dụ 2^3.
- Căn bậc n: Nhập can(n)số, ví dụ can(2)16.

2. TÍNH TOÁN LƯỢNG GIÁC
- Nhập sin30, cos60, tan45, cot45...

3. QUY ĐỔI ĐƠN VỊ ĐO LƯỜNG
- Cú pháp chuẩn: [Số lượng][Đơn vị nguồn]to[Đơn vị đích] (ví dụ: 5mtofoot, 100usdtovnd).

4. CÁC PHÍM TẮT VÀ THAO TÁC HỖ TRỢ
- Mở tài liệu hướng dẫn: Gõ hd hoặc 0 hoặc help.
- Nghe lại kết quả: Nhấn phím Enter khi dòng trống hoặc Ctrl + Enter.
- Thoát chương trình: Nhấn Escape (Esc) hoặc Alt + F4."""

# ==========================================
# CÁC HÀM TIỆN ÍCH LÕI & XỬ LÝ TOÁN HỌC
# ==========================================
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

    # Xử lý tổ hợp: tohopchap3cua12 -> math.comb(12, 3)
    match_tohop = re.match(r"^tohopchap(\d+)cua(\d+)$", query)
    if match_tohop:
        k_str, n_str = match_tohop.groups()
        k, n = int(k_str), int(n_str)
        if k > n:
            return "Lỗi: k không được lớn hơn n trong tổ hợp.", ""
        res = math.comb(n, k)
        num_format = format_number(res)
        text_format = read_vn_number(res)
        return f"Kết quả tổ hợp chập {k} của {n}: {num_format}\nĐọc là: {text_format}", num_format

    # Xử lý chỉnh hợp: chinhhopchap3cua12 -> math.perm(12, 3)
    match_chinhhop = re.match(r"^chinhhopchap(\d+)cua(\d+)$", query)
    if match_chinhhop:
        k_str, n_str = match_chinhhop.groups()
        k, n = int(k_str), int(n_str)
        if k > n:
            return "Lỗi: k không được lớn hơn n trong chỉnh hợp.", ""
        res = math.perm(n, k)
        num_format = format_number(res)
        text_format = read_vn_number(res)
        return f"Kết quả chỉnh hợp chập {k} của {n}: {num_format}\nĐọc là: {text_format}", num_format

    # Xử lý hoán vị: hoanvi5 -> math.factorial(5)
    match_hoanvi = re.match(r"^hoanvi(\d+)$", query)
    if match_hoanvi:
        n_str = match_hoanvi.groups()[0]
        n = int(n_str)
        res = math.factorial(n)
        num_format = format_number(res)
        text_format = read_vn_number(res)
        return f"Kết quả hoán vị của {n}: {num_format}\nĐọc là: {text_format}", num_format

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