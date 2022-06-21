import os
import psycopg2
import functools
from tkinter.filedialog import test
from flask import Flask, jsonify, render_template, request, url_for, redirect, session, flash, g, Blueprint
import flask
from datetime import datetime
import json


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CAT_FOLDER = os.path.join('static', 'cat_photo')

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'blog.postgre'),
        UPLOAD_FOLDER=CAT_FOLDER
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def get_db_connection():
        conn = psycopg2.connect(host='localhost',
                                database='postgres',
                                user=os.environ['DB_USERNAME'],
                                password=os.environ['DB_PASSWORD'])
        return conn

    @app.route('/')
    def welcome():
        email = session.get('email')
        return render_template('welcome.html', email=email)

    @app.route('/register/', methods=('GET', 'POST'))
    def register():
        if request.method == 'POST':
            try:
                email = request.form['email']
                password = request.form['password']

                error = None
                if not email:
                    error = 'Email is required.'
                elif not password:
                    error = 'Password is required.'

                if error is None:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute('INSERT INTO userinfo (email, password)'
                                'VALUES (%s, %s, %s)',
                                (email, password, 'user'))
                    conn.commit()
                    return redirect(url_for('welcome'))

                flash(error)
            except (Exception, psycopg2.Error) as error:
                return "<h1>" + str(error) + "</h1>"
            finally:
                cur.close()
                conn.close()

        return render_template('register.html')

    @app.route('/login', methods=('GET', 'POST'))
    def login():
        if request.method == 'POST':
            try:
                email = request.form['email']
                password = request.form['password']
                conn = get_db_connection()
                cur = conn.cursor()
                postgreSQL_select_Query = "select * from userinfo where email = %s"
                cur.execute(postgreSQL_select_Query, (email,))
                userinfo = cur.fetchall()
                error = None

                if userinfo is None:
                    error = 'Incorrect email.'
                elif userinfo[0][2] != password:
                    error = 'Incorrect password.'

                if error is None:
                    session.clear()
                    session['email'] = userinfo[0][1]
                    return redirect(url_for('welcome'))

                flash(error)
            except (Exception, psycopg2.Error) as error:
                print(error)
            finally:
                cur.close()
                conn.close()

        return render_template('login.html')

    @app.before_request
    def load_logged_in_user():
        email = session.get('email')
        if email is None:
            g.user = None
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            postgreSQL_select_Query = "select * from userinfo where email = %s"
            cur.execute(postgreSQL_select_Query, (email,))
            g.user = cur.fetchone

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('welcome'))

    def login_required(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                flash("Login needed")
                return redirect(url_for('login'))
            return view(**kwargs)
        return wrapped_view

    @app.route('/autotest_registration', methods=('GET', 'POST', 'DELETE'))
    @login_required
    def autotest():
        conn = get_db_connection()
        cur = conn.cursor()
        if request.method == 'POST':
            try:
                if (request.content_type != 'application/json'):
                    email = session.get('email')
                    startdate = request.form['start_date']
                    startdate += " " + request.form['start_time']
                    enddate = request.form['end_date']
                    enddate += " " + request.form['end_time']
                    cur.execute('select * from tests_registration '
                                'where (startdate, enddate) '
                                'overlaps (%s, %s) and status = %s',
                                (startdate, enddate, 1))
                    overlaps = cur.fetchone()
                    if (overlaps is None):
                        cur.execute('INSERT INTO tests_registration (email, startdate, enddate, status)'
                                    'VALUES (%s, %s, %s, %s)',
                                    (email, startdate, enddate, 1))
                    else:
                        flash("Tests cannot overlap")
                    conn.commit()
                    return jsonify({"status":2})
                else:
                    json_data = flask.request.json
                    cur.execute('UPDATE tests_registration '
                                'SET startdate = %s, '
                                'enddate = %s '
                                'WHERE email = %s AND startdate = %s',
                                (json_data["start"][4:25], json_data["end"][4:25], json_data["title"], json_data["oldstart"][4:25]))
                    conn.commit()
                    return jsonify({"status": 3})
            except (Exception, psycopg2.Error) as error:
                print(error)
            finally:
                cur.close()
                conn.close()
            return redirect(url_for('autotest'))
        elif (request.method == 'DELETE'):
            json_data = flask.request.json
            cur.execute('select * from userinfo where email = \'{}\''.format(session["email"]))
            user = cur.fetchone()
            if (session["email"] == json_data["email"] or user[3] == "admin"):
                cur.execute('UPDATE tests_registration '
                        'SET status = %s WHERE id = %s',
                        (0, json_data["id"]))
                conn.commit()
                return jsonify({"delete":1})
            else:
                return jsonify({"delete":0})
        else:
            events = list()
            cur.execute('SELECT * FROM tests_registration where status = 1;')
            tests = cur.fetchall()
            cur.execute('SELECT * From userinfo where email = \'{}\''.format(session.get("email")))
            user = cur.fetchone()
            admin = False
            if (user[3] == "admin"):
                admin = True
            for entry in tests:
                editable = False
                if(session.get("email") == entry[1] or admin):
                    editable = True
                events.append({
                    "id": entry[0],
                    "title": entry[1],
                    "start": entry[2].strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": entry[3].strftime("%Y-%m-%dT%H:%M:%S"),
                    "editable": editable
                })
            events = str(json.dumps(events)).replace("&#34:", "'")
            cur.close()
            conn.close()
            return render_template('test_registration.html', events=events, email=session["email"], admin=admin)

    return app
