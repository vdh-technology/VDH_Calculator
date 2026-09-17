# Hướng Dẫn Sử Dụng VDH Calculator

**Giới thiệu chung**
VDH Calculator là phần mềm hỗ trợ tính toán thông minh, giải toán đại số nâng cao, giải tích, lượng giác, chuyển đổi hệ cơ số và quy đổi đơn vị trực tiếp trên dòng lệnh.

## 1. Tính Toán Số Học và Đại Số Cơ Bản
* **Phép tính thông thường:** Nhập trực tiếp biểu thức số học như `15+25`, `12*8`, `(10+5)*2` và nhấn Enter.
* **Phân số:** Nhập với từ khóa `phanso`, ví dụ: `phanso 1phan2+2phan3`.
* **Trị tuyệt đối:** Nhập theo cú pháp `trituyetdoi(-12)` hoặc kèm biểu thức.
* **Lũy thừa, khai căn và Logarit:** 
  + Lũy thừa: Dùng dấu `^` (ví dụ `2^3`).
  + Khai căn: `can(n)số` (ví dụ `can(2)16`).
  + Logarit cơ số: `log[cơ_số]([giá_trị])` (ví dụ `log12(120)`).

## 2. Tổ Hợp, Chỉnh Hợp và Hoán Vị
* **Tổ hợp chập k của n:** Nhập `tohopchap[k]([n])` (ví dụ: `tohopchap3(12)`).
* **Chỉnh hợp chập k của n:** Nhập `chinhhopchap[k]([n])` (ví dụ: `chinhhopchap3(12)`).
* **Hoán vị của n:** Nhập `hoanvi[n]` (ví dụ: `hoanvi5`).

## 3. Giải Tích (Đạo Hàm và Nguyên Hàm)
* **Đạo hàm:** Nhập `daoham` kèm biểu thức theo biến x, ví dụ: `daohamx^2` hoặc `daoham(x^3 + 2*x)`.
* **Nguyên hàm:** Nhập `nguyenham` kèm biểu thức, ví dụ: `nguyenham(x^4)`. (Chương trình sẽ tự động hiển thị song song cả dạng phân số và dạng thập phân với dấu phẩy chuẩn, ví dụ: `0,2*x^5 + C`).
* **Tích phân xác định:** `tíchphan[a:b](biểu_thức)` (ví dụ: `tichphan0:2(x^2)`).

## 4. Giải Phương Trình và Hệ Phương Trình
* **Phương trình bậc 2 ($ax^2 + bx + c = 0$):** `ptb2 a b c` (ví dụ: `ptb2 1 -3 2`).
* **Phương trình bậc 3 và bậc 4:** Nhập `ptb3 a b c d` hoặc `ptb4 a b c d e`.
* **Phương trình bậc n:** Nhập `ptbn a_n a_{n-1} ... a_0`.
* **Hệ phương trình tuyến tính:** 
  * Hệ 2 ẩn: `he2 a1 b1 c1 a2 b2 c2`
  * Hệ 3 ẩn: `he3 a1 b1 c1 d1 a2 b2 c2 d2 a3 b3 c3 d3`
  * Hệ n ẩn tổng quát: `hen [số_ẩn] [danh_sách_hệ_số]`

## 5. Chuyển Đổi Hệ Cơ Số
* **Thập phân sang nhị phân:** `dectobin120`
* **Thập phân sang bát phân:** `dectooct64`
* **Thập phân sang thập lục phân:** `dectohex255`
* **Nhị phân sang thập phân:** `bintodec1010`
* **Bát phân sang thập phân:** `octtodec100`
* **Thập lục phân sang thập phân:** `hextodecff` (hoặc `hextodec FF`)

## 6. Lượng Giác và Quy Đổi Đơn Vị
* **Lượng giác:** Nhập trực tiếp hàm và góc (tính theo độ), ví dụ: `sin30`, `cos60`, `tan45`, `cot45`.
* **Quy đổi đơn vị:** Nhập theo cú pháp `[Số][Đơn vị nguồn]to[Đơn vị đích]`, ví dụ: `5mtofoot`, `100usdtovnd`.

## 7. Thao Tác và Phím Tắt Hỗ Trợ
* **Mở tài liệu:** Gõ `hd`, `0` hoặc `help` để mở file hướng dẫn dạng văn bản.
* **Nghe lại / Đọc lại kết quả:** Nhấn phím `Enter` khi dòng trống hoặc tổ hợp `Ctrl + Enter`.
* **Dán nội dung:** Nhấn `Ctrl + V` để dán dữ liệu từ bộ nhớ tạm vào dòng lệnh.
* **Thoát chương trình:** Nhấn phím `Esc` hoặc gõ `thoat`.