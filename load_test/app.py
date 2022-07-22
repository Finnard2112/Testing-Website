from dotenv import load_dotenv
load_dotenv()
import os
import functools
from flask import Flask, jsonify, render_template, request, url_for, redirect, session, flash
from sassutils.wsgi import SassMiddleware
import flask
import json
import config
import pytz
import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, and_
import requests
from werkzeug.utils import secure_filename
from db_init.db_init import Tests_Registration, User_Info, Group, Test
import webbrowser



app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config.DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'C:\Temporary Files'
engine = create_engine(os.getenv("DATABASE_URL"), echo = False, echo_pool=False, future=True)
app.secret_key = "pcvMGNKRxmXWYVIGjlYo"
sql_session = Session(engine)
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'app': ('static/sass', 'static/css', '/static/css')
})

def tz_localize(timestamp):
    loc_tz = pytz.timezone(session["user_timezone"])
    loc_dt = loc_tz.localize(timestamp)
    return loc_dt

def is_in_registered_time(username=None):
    if(username is None):
        username = session.get("username")
    user_tests = sql_session.query(Tests_Registration).filter(Tests_Registration.status == 1, Tests_Registration.author == username)
    for entry in user_tests:
        now = pytz.utc.localize(datetime.utcnow())
        if (now >= entry.start_timestamp and now <= entry.end_timestamp):
           return True
    return False

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if (len(session) == 0 or None in session.values()):
            flash("Bạn chưa đăng nhập")
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.before_request
def before_request_callback(): 
    request = flask.request
    endpoint = request.endpoint 
    method = request.method 
    services = ["loadtest_form"]
    if endpoint in services: 
        if (not is_in_registered_time()):
            flash("Chưa tới giờ đăng ký của bạn")
            return redirect(url_for("services"))

@app.route('/tz', methods=['POST'])
def timezone():
    try:
        json_data = flask.request.json
        session["user_timezone"] = json_data.get("Timezone")
        return jsonify({"message" : "success", "status" : "0"})
    except Exception as e:
        return jsonify(message="Cannot understand request")

@app.route('/validate', methods=('POST',))
def validate():
    if (request.content_type == 'application/json'):
        try:
            json_data = flask.request.json
            token = json_data.get("jwt")
            authorization = requests.post(os.getenv("VALIDATE_API_URL"), json={"token" : token})
            if (authorization.ok):
                payload = jwt.decode(token, algorithms=["HS256"], options={"verify_signature": False})
                if (is_in_registered_time(payload.get("name"))):
                    return jsonify(message = "OK", status = 0), 200
                else:
                    return jsonify(message = "User is not in registered time", status = 1), 401
            else:
                return jsonify(message = "Token invalid", status = 1), 401
        except Exception as e:
            return jsonify(message = str(e)), 400
    else:
        return jsonify(message = "Bad Request", status = 1), 400


@app.route('/',  methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        try:
            login_url = os.getenv("LOGIN_URL")
            login_data = {'username': request.form['username'],
                        'password' : request.form['password']}
            authorization = requests.post(login_url, json=login_data)
            if (authorization.headers.get('content-type') == 'application/json'):
                json_response = authorization.json()
                if (authorization.status_code == 200 and json_response["message"] == "OK"):
                    token = json_response["token"]
                    refresh_token = json_response["refresh_token"]
                    session["username"] = request.form['username']
                    session["password"] = request.form['password']
                    session["refresh_token"] = refresh_token
                    session["token"] = token
                    session["first_login"] = True
                    user = sql_session.query(User_Info).filter(User_Info.username == session["username"])
                    for row in user:
                        session["role"] = row.role
                    return redirect(url_for("autotest"))
                else:
                    flash(json_response["message"])
            else:
                flash("Something went wrong")
        except (Exception) as error:
            print(error)
    elif (session.get("username") is not None):
        return redirect(url_for("autotest"))
    return render_template('login.html')

# Clears section and logout

@app.route('/logout')
def logout():
    session["username"] = None
    session["password"] = None
    session["refresh_token"] = None
    session["token"] = None
    return redirect(url_for('login'))

@app.route('/experiment', methods = ["GET"])
@login_required
def experiment():
    service_structure ={}
    groups = sql_session.query(Group).all()
    for group in groups:
        service_structure[group.name] = [x for x in group.tests]
    return render_template("experiment.html", username=session["username"], service_structure = service_structure, is_in_registered_time=is_in_registered_time(), experiment = True)
    

@app.route('/services', methods=['GET', 'POST'])
@login_required
def services():
    if (request.method == 'POST'):
        form_data = request.form.to_dict()
        print(form_data)
        if (form_data["form_name"] == "group"):
            duplicates = sql_session.query(Group).filter(Group.name == form_data["group_name"]).first()
            print(duplicates)
            if (duplicates is not None):
                flash("Không thể đặt tên nhóm trùng với một nhóm khác")
                print("HERE")
            else:
                group = Group(name=form_data["group_name"], type=form_data["group_type"])
                sql_session.add(group)
                sql_session.commit()
        elif (form_data["form_name"] == "test"):
            files = request.files.getlist('file')
            myfiles = None
            for file in files:
                if file.filename !='':
                    file = request.files['file']
                    filename = secure_filename(file.filename)
                    file_directory = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_directory)
                    myfiles = {'file': open(file_directory,'rb')}
            url = form_data["test_url"]
            data_send = requests.request("POST", url, files=myfiles, verify= False)
            if (not data_send.ok):
                flash("Error: " + data_send.text)
            else:
                current_group = sql_session.query(Group).filter(Group.name == form_data["parent_group_type"]).first()
                tc = Test(test_name = form_data["test_name"], groups = current_group, link_test_api = data_send.json()["link_test_api"], username = session["username"], description = form_data["description"], status = data_send.json()["status"], message = data_send.json()["message"], sessionid = data_send.json()["sessionid"])  
                sql_session.add(tc)
                sql_session.commit()
            if (myfiles):
                myfiles["file"].close()
                os.remove(file_directory)
        return redirect(url_for('services'))
    service_structure = {}
    sessions = {}
    types = sql_session.query(Group).filter_by(type=Group.type).distinct()
    for type in types:
        service_structure[type.type] = {}
    groups = sql_session.query(Group).all()
    for group in groups:
        service_structure[group.type][group.name] =  [x.__dict__ for x in group.tests]
        for x in service_structure[group.type][group.name]:
            if (x["sessionid"] is not None):
                sessions[x["test_name"]] = x["sessionid"]
    return render_template("services.html", username=session["username"], service_structure = service_structure, is_in_registered_time=is_in_registered_time(), sessions=sessions)

# Receive loadtest_form data and sends it to API. 

@app.route('/loadtest_form', methods=('GET', 'POST'))
@login_required
def loadtest_form():
    if (request.method == 'POST'):
        form_data = request.form.to_dict()
        form_data = dict((k.rstrip(), v.rstrip()) for k, v in form_data.items() if k != "Authorization")
        form_data["jwt"] = session.get("token")
        try:
            form_data["type_request"] = int(form_data["type_request"])
            form_data["ccu"] = int(form_data["ccu"])
            form_data["stop_timeout"] = int(form_data["stop_timeout"])
        except ValueError as verr:
            flash("Data không hợp lệ hoặc không đầy đủ")
            return redirect(url_for('loadtest_form'))
        files = request.files.getlist('file')
        myfiles = None
        for file in files:
            if file.filename !='':
                file = request.files['file']
                filename = secure_filename(file.filename)
                file_directory = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_directory)
                myfiles = {'file': open(file_directory,'rb')}
        
        url = os.getenv("LOCUST_API_URL")
        payload={'data': json.dumps(form_data)}
        data_send = requests.request("POST", url,data=payload, headers = {"Authorization": "Bearer " + session["token"]}, files=myfiles, verify= False)
        
        if (data_send.status_code == 401):
            response_dict = data_send.json()
            if (response_dict.get("exp") == "token expired"):
                renew = requests.post(os.getenv("TOKEN_REFRESH_URL"), json={"refresh_token":session["refresh_token"]})
                if(renew.status_code == 401):
                    flash("Không thể xác nhận token, hãy đăng nhập lại")
                    return(redirect(url_for("logout")))
                session["refresh_token"] = renew.json().get("refresh_token")
                session["token"] = renew.json().get("token")
                data_send = requests.request("POST", url, headers={"Authorization": session["token"]}, data=payload, files=myfiles, verify= False)
            elif (data_send.json().get("message") == "Unauthorized"):
                flash("Không thể xác nhận token, hãy đăng nhập lại")
                redirect(url_for('login'))
        if (data_send.status_code == 200):
            if (data_send.json()["status"] == 0):
                webbrowser.open(data_send.json()["address"])
                return redirect(url_for("autotest"))
            else:
                flash("Something went wrong: " + data_send.json()["message"])
        else:
            flash("Error: " + data_send.text)
        if (myfiles):
            myfiles["file"].close()
            os.remove(file_directory)
    return render_template('Load test system.html')



@app.route('/autotest_registration', methods=('GET', 'POST', 'DELETE'))
@login_required
def autotest():
    if request.method == 'POST':
        try:    
            if (request.content_type != 'application/json'):
                start = request.form['start_date']
                start += " " + request.form['start_time']
                end = request.form['end_date']
                end += " " + request.form['end_time']
                start = tz_localize(datetime.strptime(start, '%d-%m-%Y %I:%M %p'))
                end = tz_localize(datetime.strptime(end, '%d-%m-%Y %I:%M %p'))
                overlaps = sql_session.query(Tests_Registration).filter(start <= Tests_Registration.end_timestamp, end >= Tests_Registration.start_timestamp, Tests_Registration.status != 0).first()
                if (overlaps):
                    flash("Không thể trùng với thời gian đã được đăng ký")
                elif (start < pytz.utc.localize(datetime.utcnow()) - timedelta(minutes=5)):
                    flash("Không thể test tải trong quá khứ")
                else:
                    new_test = Tests_Registration(start_timestamp = start, end_timestamp = end, status = 1, author = session["username"])
                    sql_session.add(new_test)
                    sql_session.commit()
                return redirect(url_for('autotest'))
            else:
                json_data = flask.request.json
                oldstart = tz_localize(datetime.strptime(json_data["oldstart"][4:25], "%b %d %Y %H:%M:%S "))
                selected_test = sql_session.query(Tests_Registration).filter(and_(Tests_Registration.author == json_data["title"], Tests_Registration.start_timestamp == oldstart))
                for entry in selected_test:
                    entry.start_timestamp = tz_localize(datetime.strptime(json_data["start"][4:25], "%b %d %Y %H:%M:%S "))
                    entry.end_timestamp = tz_localize(datetime.strptime(json_data["end"][4:25], '%b %d %Y %H:%M:%S '))
                sql_session.commit()
                return redirect(url_for('autotest'))
        except (Exception) as error:
            print(error)
    elif (request.method == 'DELETE'):
        json_data = flask.request.json
        if (session["username"] == json_data["username"] or session.get("role") == "admin"):
            delete_test = sql_session.query(Tests_Registration).get(json_data["id"])
            delete_test.status = 0
            sql_session.commit()
            return jsonify({"delete":1})
        else:
            return jsonify({"delete":0})
    else:
        events = list()
        valid_tests = sql_session.query(Tests_Registration).filter(Tests_Registration.status == 1, Tests_Registration.end_timestamp > pytz.utc.localize(datetime.utcnow())) 
        for entry in valid_tests:
            editable = False
            if(session["username"] == entry.author or session.get("role") == "admin"):
                editable = True
            events.append({
                "id": entry.id,
                "title": entry.author,
                "start": str(entry.start_timestamp),
                "end": str(entry.end_timestamp),
                "editable": editable
            })
        events = str(json.dumps(events)).replace("&#34:", "'")
        first_login = False
        if (session.get("first_login") == True):
            first_login = True
            session["first_login"] = False
        return render_template('test_registration.html', events=events, username=session["username"], is_in_registered_time=is_in_registered_time(), role=session.get("role"), first_login = first_login)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
