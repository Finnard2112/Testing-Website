import os
import psycopg2
import functools
from tkinter.filedialog import test
from flask import Flask, render_template, request, url_for, redirect, session, flash, g, Blueprint

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config= True)
    CAT_FOLDER = os.path.join('static', 'cat_photo')

    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE=os.path.join(app.instance_path, 'blog.postgre'),
        UPLOAD_FOLDER = CAT_FOLDER
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
                                'VALUES (%s, %s)',
                                (email, password))
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
                print( error)
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

    @app.route('/autotest_registration')
    @login_required
    def secret():
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'maine-coon-scaled.jpg')
        return render_template('secret.html', user_image = full_filename)

    
    return app