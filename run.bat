@echo off
rem Chuyển bảng mã sang UTF-8 để hiển thị tiếng Việt có dấu
chcp 65001 >nul

rem Đặt tên cho cửa sổ để trình đọc màn hình đọc tên này thay vì đọc đường dẫn ổ C
title VDH_Calculator

rem Xóa sạch màn hình trước khi chạy để tránh trình đọc màn hình đọc các dòng lệnh thừa
cls

rem Gọi file Python
python "%~dp0vdh_calculator.py" %*