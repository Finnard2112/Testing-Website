import functools
import psycopg2
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

def get_db_connection():
    conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])
    return conn

bp = Blueprint('auth', __name__)

@bp.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            age = request.form['age']

            error = None
            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif not email:
                error = 'Email is required'

            if error is None:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute('INSERT INTO userinfo (username, password, age, email)'
                            'VALUES (%s, %s, %s, %s)',
                            (username, password, age, email))
                conn.commit()
                return redirect(url_for('welcome'))

            flash(error)
        except (Exception, psycopg2.Error) as error:
            print("Error fetching data from PostgreSQL table", error)
        finally:
            cur.close()
            conn.close()

    return render_template('register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT * FROM userinfo WHERE email=%s',
            (email))

            userinfo = cur.fetchall()
            error = None

            if userinfo is None:
                error = 'Incorrect username.'
            elif not userinfo[0][2] == password:
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = userinfo['id']
                return redirect(url_for('welcome'))

            flash(error)
        except (Exception, psycopg2.Error) as error:
            print("Error fetching data from PostgreSQL table", error)
        finally:
            cur.close()
            conn.close()

    return render_template('login.html')
