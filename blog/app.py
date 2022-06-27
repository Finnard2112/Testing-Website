import os
import functools
from flask import Flask, jsonify, render_template, request, url_for, redirect, session, flash, g
import flask
import json
import config
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, and_
import requests
from werkzeug.utils import secure_filename
from db_init.db_init import Tests_Registration

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config.DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'C:\Temporary Files'
engine = create_engine("postgresql://postgres:Abcde1234@localhost:5432/Autotest_Registration", echo = False, echo_pool=False, future=True)
app.secret_key = "pcvMGNKRxmXWYVIGjlYo"
app.permanent_session_lifetime = timedelta(minutes=30)
sql_session = Session(engine)

@app.route('/',  methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        try:
            login_url = "http://192.168.41.243:8000/auth/login"
            login_data = {'username': request.form['username'],
                        'password' : request.form['password']}
            authorization = requests.post(login_url, json=login_data)
            if (authorization.headers.get('content-type') == 'application/json'):
                if (authorization.status_code == 201):
                    token = authorization.json()["token"]
                    refresh_token = authorization.json()["refresh_token"]
                    session["username"] = request.form['username']
                    session["password"] = request.form['password']
                    session["refresh_token"] = refresh_token
                    session["token"] = token
                    return redirect(url_for("autotest"))
                else:
                    flash(authorization.json()["message"])
            else:
                flash("Incorrect Password or Username")
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


def is_in_registered_time():
    user_tests = sql_session.query(Tests_Registration).filter(Tests_Registration.status == 1, Tests_Registration.author == session["username"])
    for entry in user_tests:
        if (datetime.now() >= entry.start_timestamp and datetime.now() <= entry.end_timestamp):
           return True
    return False


# Checks for token when requesting autotest_registration or loadtest_form. If invalid or expired token, use refresh token

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if (len(session) == 0 or None in session.values()):
            flash("Login needed")
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

# Receive loadtest_form data and sends it to API. 

@app.route('/loadtest_form', methods=('GET', 'POST'))
@login_required
def loadtest_form():
    if (request.method == 'POST'):
        if (not is_in_registered_time()):
            flash("Cannot loadtest at this time")
            return redirect('autotest_registration') 
        form_data = request.form.to_dict()
        form_data = dict((k.rstrip(), v.rstrip()) for k, v in form_data.items() if k != "Authorization")
        try:
            form_data["type_request"] = int(form_data["type_request"])
            form_data["ccu"] = int(form_data["ccu"])
            form_data["stop_timeout"] = int(form_data["stop_timeout"])
        except ValueError as verr:
            flash("Incorrect data types")
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
        url = "http://192.168.41.243:8000/loctust/api/create"
        payload={'data': json.dumps(form_data)}
        data_send = requests.request("POST", url,data=payload, headers = {"Authorization": "Bearer " + session["token"]}, files=myfiles, verify= False)
        if (data_send.status_code == 401):
            response_dict = data_send.json()
            if (response_dict.get("exp") == "token expired"):
                renew = requests.post("http://192.168.41.243:8000/auth/refresh", json={"refresh_token":session["refresh_token"]})
                if(renew.status_code == 401):
                    flash("Token Invalid, please log in again")
                    return(redirect(url_for("logout")))
                session["refresh_token"] = renew.json().get("refresh_token")
                session["token"] = renew.json().get("token")
                data_send = requests.request("POST", url, headers={"Authorization": "Bearer " + str(session["token"])}, data=payload, files=myfiles, verify= False)
            elif (data_send.json().get("message") == "Unauthorized"):
                flash("Invalid Token, please login again")
                redirect(url_for('login'))
        if (data_send.status_code == 200):
            if (data_send.json()["status"] == 0):
                flash("Success")
                print(data_send.text)
                return redirect(data_send.json()["address"])
            else:
                flash("Something went wrong: " + data_send.json()["message"])
        else:
            print("Error: " + data_send.text)
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
                start = datetime.strptime(start, '%d-%b-%Y %I:%M %p')
                end = datetime.strptime(end, '%d-%b-%Y %I:%M %p')
                overlaps = sql_session.query(Tests_Registration).filter(start <= Tests_Registration.end_timestamp, end >= Tests_Registration.start_timestamp, Tests_Registration.status != 0).first()
                if (overlaps):
                    flash("Tests cannot overlap")
                elif (start <= datetime.now()):
                    flash("Tests cannot be in the past")
                else:
                    new_test = Tests_Registration(start_timestamp = start, end_timestamp = end, status = 1, author = session["username"])
                    sql_session.add(new_test)
                    sql_session.commit()
                return redirect(url_for('autotest'))
            else:
                json_data = flask.request.json
                selected_test = sql_session.query(Tests_Registration).filter(and_(Tests_Registration.author == json_data["title"], Tests_Registration.start_timestamp == json_data["oldstart"][4:25]))
                for entry in selected_test:
                    entry.start_timestamp = datetime.strptime(json_data["start"][4:25], "%b %d %Y %H:%M:%S ")
                    entry.end_timestamp = datetime.strptime(json_data["end"][4:25], '%b %d %Y %H:%M:%S ')
                sql_session.commit()
                return redirect(url_for('autotest'))
        except (Exception) as error:
            print(error)
    elif (request.method == 'DELETE'):
        json_data = flask.request.json
        if (session["username"] == json_data["username"]):
            delete_test = sql_session.query(Tests_Registration).get(json_data["id"])
            delete_test.status = 0
            sql_session.commit()
            return jsonify({"delete":1})
        else:
            return jsonify({"delete":0})
    else:
        events = list()
        valid_tests = sql_session.query(Tests_Registration).filter(Tests_Registration.status == 1, Tests_Registration.end_timestamp > datetime.now()) 
        print("START PRINTING")
        print(valid_tests)
        for entry in valid_tests:
            print("entry")
            editable = False
            if(session["username"] == entry.author):
                editable = True
            events.append({
                "id": entry.id,
                "title": entry.author,
                "start": entry.start_timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": entry.end_timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
                "editable": editable
            })
        events = str(json.dumps(events)).replace("&#34:", "'")
        print(events)
        return render_template('test_registration.html', events=events, username=session["username"], is_in_registered_time=is_in_registered_time())

if __name__ == '__main__':
    app.run()
