# loctust-autotest-grpc-socket

## Cách chạy:

Chạy ./load_test/app.py với python.exe

## Cấu hình các biến môi trường:

File env: ./load_test/.env

Trong file env có thể thay đổi các link API và link Database

## Cấu trúc file:

Project sẽ được chia ra làm 2 folder chính có code và một folder chứa cấu hình các table cần thiết

1. DB folder

- Chứa DB.sql. File có các câu lệnh SQL để lâp các table cần thiết

2. venv folder

- Chứa venv và các package cần thiết

3. load_test folder: Folder chứa code cho flask

Trong này có các folder sau:

- db_init:

+ db_init.py: Chứa config của SQLAlchemy ORM. Table User_Info không cần thiết, nhưng có thể bỏ comment phần này để chứa dữ liệu người dùng và phân quyền. 
Note: Bỏ comment phần "# Base.metadata.create_all(engine)" để tạo table mới khi chạy

+ insert_data.py: Có thể dùng để tạo các row mới trong test table. Việc tạo các row này trong app.py có thể dẫn đến duplicates

- migrations:

Folder này không dùng đến

- static:

+ CSS:
Chứa các file CSS. Những file: calendarStyle, coreMain, dayGridmain, icomoonStyle, selection.json đều được download và dùng theo cái calendar. 

services.css là file css được dùng riêng cho trang services.

style.css dùng chung cho trang autotest và services.

style.scss.css là file được generate ra từ file style.css để dùng cho một vài nút bấm trong services

+ images:

Folder riêng để chứa các image. Hiện tại không dùng đến nhưng sau này có thể dùng đến

+ JS:

Chứa các file Javascript. coreMain, daygridMain, interactionMain được dùng bởi cái calendar. 

script.js chứa javascript cho datetimepicker

services_script.js chứa các function hỗ trợ cho trang services. 

+ sass:

Dùng để chứa các file scss có thể dùng đến sau này. Trong flask sẽ có một module đọc file này và generate ra những file css mới tương ứng 

- templates:

+ Load test system.html: dùng cho form locust. 

+ login.html: dùng cho trang login

+ services.html: dùng cho services

+ test_registration.html: dùng cho trang có calendar

- .env: 

Chứa các biến môi trường

- app.py:

Chứa code Flask

- config.py:

config cho Flask. 

Được dùng đến ở dòng 23 trong app.py. Có thể thay đổi chế độ development/ production hay thay các config khác.







