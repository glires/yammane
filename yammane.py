#!/usr/bin/env python

'''
yammane.py
'''

__doc__  = 'Your advanced manager for merciful animals necessary for experiments'

__author__  = 'Shunpei Okamura and Kohji Okamura'
__date__    = '2023-05-23'
__version__ = 0.1

# The following settings should be provided by a JSON file later.
settings = \
  {
    'institute': 'National Cetner for Child Health and Development',
    'inquiry': 'https://www.ncchd.go.jp/scholar/research/section/animal/',
    'news': '/var/www/opt/yammane/var/notices.tsv',
    'tcp_port': 80,
    'lifetime': 4,
    'db_host': 'localhost',
    'db_port': 3306,
    'db_name': 'mammals',
    'db_user': 'mammal',
    'db_password': 'mmm+1221',
  }

import sys
import string
import random
import hashlib
import datetime
import pymysql.cursors

from flask import Flask, request, session, render_template, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

host = settings['db_host']
user = settings['db_user']
password = settings['db_password']
database = settings['db_name']
port = settings['db_port']
eng = create_engine(f'mariadb+pymysql://{user}:{password}@{host}:{port}/{database}')
base = declarative_base()

class Users(base):
    __tablename__ = "Users"
    __table_args__ = ({"mysql_charset": "utf8mb4"})
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String(40))
    user_password = Column(String(255))
    user_name = Column(String(40))
    pronunciation = Column(String(50))
    mailAdress = Column(String(255))
    belong = Column(String(100))
    admin_user = Column(Boolean)
    chief_user = Column(Boolean)

def connection_sql(sql, mode, db):
    connection = pymysql.connect(
        host = host,
        user = user,
        password = password,
        database = db,
        charset = 'utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    if mode == 'w':
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
            connection.commit()

    elif mode == 'r':
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result

def get_random_str(n):
  char_data = string.digits + string.ascii_lowercase + string.ascii_uppercase
  return ''.join([random.choice(char_data) for i in range(n)])

def check_permission():
  if session.get('user_id') is not None:
    user_id = session.get('user_id')
    sql = f'select admin_user from Users where user_id = {user_id}'
    result = connection_sql(sql, 'r', database)
    admin_user = result[0]['admin_user']
    return admin_user

app = Flask(__name__)
app.secret_key = str(random.random())
app.permanent_session_lifetime = datetime.timedelta(hours = settings['lifetime'])

@app.route('/', methods = ('GET', 'POST'))
def top():
  if request.method == 'GET': return render_template('top.html', inquiry = settings['inquiry'])
  session.permanent = True
  account_id = request.form.get('account')
  password = request.form.get('password')
  hash_pass = hashlib.sha256(password.encode()).hexdigest()
  sql = f'select user_id, user_password from Users where account_id = "{account_id}"'
  result = connection_sql(sql, 'r', database)
  user_id = result[0]['user_id']
  sql_password = result[0]['user_password']

  if hash_pass == sql_password:
    session_key = get_random_str(100)
    hashed_session = hashlib.sha256(session_key.encode()).hexdigest()
    sql = f"insert session(session_id, user_id, session_key) values (null, {user_id}, '{hashed_session}') on duplicate key update session_key = '{hashed_session}'"
    connection_sql(sql, 'w', database)

    session['user_id'] = user_id
    session['session_key'] = session_key
    news = []	# getting latest news each time
    with open(settings['news']) as tsv:
      for line in tsv:
        fields = line[:-1].split('\t')
        n = {}
        n['date'], n['title'], n['text'] = fields
        news.append(n)
    return render_template('loggedin.html', who = account_id, administrator = check_permission(), news = news)
  else:
    return render_template('login.html', error = '認証に失敗しました。')

@app.route('/login')
def loggedin():
  return render_template('login.html')

@app.route('/animals')
def animals():
  return render_template('animals.html', who = 'alice')

@app.route('/passwd', methods = ('GET', 'POST'))
def passwd():
  if request.method == 'GET': return render_template('passwd.html')
  account_id = request.form.get('account_id')
  passwd_cu = request.form.get('password_cu')
  passwd_nw = request.form.get('password_nw')
  passwd_re = request.form.get('password_re')
  sql_Users = f"select * from Users where account_id = '{account_id}'"

  result_Users = connection_sql(sql_Users, 'r', database)
  user_id = result_Users[0]['user_id']
  sql_account_id = result_Users[0]['account_id']
  user_password = result_Users[0]['user_password']
  user_name = result_Users[0]['user_name']
  pronunciation = result_Users[0]['pronunciation']
  mailAdress = result_Users[0]['mailAdress']
  belong = result_Users[0]['belong']
  admin_user = result_Users[0]['admin_user']
  chief_user = result_Users[0]['chief_user']
  hash_now = hashlib.sha256(passwd_cu.encode()).hexdigest()

  if passwd_nw != passwd_re:
    msg = '新しいパスワードが一致しません。'
  elif user_password != hash_now:
    msg = '現在のアカウントまたはパスワードが一致しません。'
  else:
    hash_new_password = hashlib.sha256(passwd_nw.encode()).hexdigest()
    sql_changePassword = f"insert into Users(user_id, account_id, user_password, user_name, pronunciation, mailAdress, belong, admin_user, chief_user) values('{user_id}', '{sql_account_id}', '{hash_new_password}', '{user_name}', '{pronunciation}', '{mailAdress}', '{belong}', '{admin_user}', '{chief_user}') on duplicate key update user_password = '{hash_new_password}'"
    connection_sql(sql_changePassword, 'w', database)
    msg = f'{account_id}のパスワードを変更しました。'
  return render_template("passwd.html", msg = msg)

@app.route("/apply", methods = ('GET', 'POST'))
def apply():
    if request.method == "POST": pass
    else: return render_template("request.html")

@app.route("/out", methods=["POST", "GET"])
def out():
    if request.method == "POST": pass
    else: return redirect(url_for('/'))

@app.route("/adduser", methods=["POST", "GET"])
def adduser():
    if request.method == "POST":
        account_id = request.form.get("account_id")
        user_password = request.form.get("user_password")
        password_comf = request.form.get("password_comf")
        user_name = request.form.get("user_name")
        pronunciation = request.form.get("pronunciation")
        mailAdress = request.form.get("mailAdress")
        belong = request.form.get("belong")
        admin_user = request.form.get("admin_user", type = int)
        chief_user = request.form.get("chief_user", type=int)
        error = ""
        msg = ""

        if user_password == password_comf:
            hash_password = hashlib.sha256(user_password.encode()).hexdigest()
            sql_Users = "insert Users(user_id, account_id, user_password, user_name, pronunciation, mailAdress, belong, admin_user, chief_user)"
            sql_Users += f"values(null, '{account_id}', '{hash_password}', '{user_name}', '{pronunciation}', '{mailAdress}', '{belong}', '{admin_user}', '{chief_user}');"
            connection_sql(sql_Users, 'w', database)

            msg = f'{account_id}を登録しました'
            return render_template("adduser_success.html", msg=msg)

        else:
            error = "パスワードと確認用パスワードが一致しません"
            return render_template("adduser.html", error=error)
    else:
        return render_template("adduser.html")

@app.route("/request_index")
def request_index():
    if check_permission():
        try:
            sql = f"select request_id, user_id, title_name, allow, request_date from request"
            results = connection_sql(sql, 'r', database)

            return render_template("request_index.html", results=results)
        except:
            error = "申請はありません"
            return render_template("request_index.html", error=error)
    else:
        return redirect(url_for('/'))

@app.route('/verify')
def verify():
  user_id = session.get('user_id')
  sql_request = f'select request_id, title_name, start_time, finish_time, allow from request where user_id = {user_id}'
  results = connection_sql(sql_request, 'r', database)
  sql_user_name = f'select user_name from Users where user_id = {user_id}'
  result_user_name = connection_sql(sql_user_name, 'r', database)
  user_name = result_user_name[0]['user_name']
  return render_template('verify.html', result = results, user_name = user_name)

@app.route("/send_mail")
def send_mail():
    mak = sessionmaker(bind=eng)
    ses = mak()
    mailing_list = []

    for u in ses.query(Users).filter(Users.admin_user == True).order_by(Users.mailAdress).all():
        mailing_list.append(u)

    return render_template("send_mail.html", mailing_list=mailing_list)

@app.route('/logout')
def logout():
  session.pop('user_id', None)
  session.clear()
  return redirect('/')

if __name__ == '__main__':
  app.run(host = '0.0.0.0', port = settings['tcp_port'], debug = True)
