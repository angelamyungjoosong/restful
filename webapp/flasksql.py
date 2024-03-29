from flask import Flask, url_for, request, redirect, render_template, session
import datetime

import database
from database import *
from sqlalchemy.orm import Session

app = Flask(__name__)
# 플라스크 세션을 사용하기 위한 암호키
app.config['SECRET_KEY'] = 'aiot'
database.init_db()

"""
플라스크로 webapp 구성시 라우트 함수마다 실제적인 공간이 분리되어있음
사용자가 여러 라우터에서 공유해야할 데이터는 플라스크 세션에 저장
플라스크 세션은 특정 시간이 지나면 자동으로 초기화
"""
# 서버 실행시 초기화 작업
# 세션 옵션 초기화
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=5) # 5분이 지나면 세션 초기화
    session.modified = True

@app.route('/')
def index():
    return render_template('/index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'userName' in session:
        return redirect(url_for('profile'))
    else:
        if request.method == 'POST':
            username = request.form['userName']
            password = request.form['uPassword']

            db = Session(engine)
            user = db.get(User, username)
            if user is not None and user.passward == password:
                session['userName'] = username
                return redirect(url_for('profile'))
            else:
                return redirect(url_for('login'))
        else:
            return render_template('login.html') #html파일은 templates밑에 넣어둬야함 #페이지를 rendering해서 보내줌


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['userName']
        password = request.form['uPassword']

        db = Session(engine)
        user = User(username, password)
        db.add(user)
        db.commit()
        return redirect(url_for('login'))
    else:
        return render_template('register.html')



@app.route('/user')
def profile():
    if 'userName' in session:
        return render_template('profile.html', username=session['userName'])
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run('0.0.0.0', 9999, debug=True)
    init_db()