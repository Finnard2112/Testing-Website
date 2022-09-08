# Website testing

## How to run:

Run ./load_test/app.py with python.exe

## Env config:

File env: ./load_test/.env

You can change API links and DB link in the .env file

## Folder Structure:

The project has two main folders that have written code and a folder with necessary table configs

1. DB folder

- Has DB.sql. This file has necessary SQL code to setup needed tables

2. venv folder

- Has venv and necessary packages

3. load_test folder: Folder that has flask code

Child folders:

- db_init:

+ db_init.py: has SQLAlchemy ORM config. Table User_Info isn't necessary, but you can uncomment it to hold User Info or access priveleges. 
Note: Bỏ comment phần "# Base.metadata.create_all(engine)" để tạo table mới khi chạy

+ insert_data.py: Used to manually add rows to tables. Adding rows in app.py could lead to duplicates

- migrations:

I don't write code in here

- static:

+ CSS:
Has CSS files: calendarStyle, coreMain, dayGridmain, icomoonStyle, selection.json are all downloaded to use with calendar 

services.css is a css file that's used for the services page

style.css is used for autotest and services.

style.scss.css là file that was generated from style.scss to style some buttons in services

+ images:

Folder that holds images. No images are in use currently

+ JS:

Holds javascript files. coreMain, daygridMain, interactionMain are all used by the calendar. 

script.js has javascript for datetimepicker

services_script.js has function to support services webpage. 

+ sass:

Holds scss files. There's a module in Flask that reads these files and generate corresponding css files.

- templates:

+ Load test system.html: Used for Locust form. 

+ login.html: used for login

+ services.html: used for services

+ test_registration.html:used for calendar page

- .env: 

Holds environment variables

- app.py:

Holds Python Flask code

- config.py:

Holds Flask configs and is used on line 23 of app.py. You could change development/ production mode or any other config here.







