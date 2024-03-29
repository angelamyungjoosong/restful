from flask import Flask, request, jsonify
import pandas as pd
from database2 import * # 모든 정의를 그래돌 가져오겠다
from sqlalchemy.orm import Session
from sqlalchemy import select

# database에서 정의한 함수들 사용하는 곳

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
db = get_engine() # database에서 return된 engine을 db로 사용

@app.route('/medicine/<mid>', methods=['GET']) # app 안의 route라는 데코레이터 #method는 통신방식 #<mid>는 url 구성할떄 넣어주는 경로 매개변수
def medicine(mid):
    if request.method == 'GET': # request라는 모듈로 정보를 받음
        sess = Session(db) # 엔진 넣어 세션 열어 #데이터베이스 접근
        md = sess.get(Medicine, mid) # md라는 orm
        return jsonify(md.to_dict()) # json형태로 전달

@app.route('/store/<sid>', methods=['GET'])
def store(sid):
    if request.method == 'GET':
        sess = Session(db)
        st = sess.get(Store, sid)
        return jsonify(st.to_dict())

@app.route('/inventory/list', methods=['GET'])
def inv_all():
    if request.method == 'GET':
        sess = Session(db)
        q = sess.scalars(select(Inventory)).all() #q는 모든 inventory 다 가져온 리스트
        invs = [inv.to_dict() for inv in q]
        return jsonify(invs)

@app.route('/inventory', methods=['GET','POST']) #경로변수가 아니라 파라미터로 직접 넣어보내 요청
def inventory():
    # if 문을 활용해 GET과 POST 메소드를 구분
    if request.method == 'GET':
        mid = request.json['mid'] #사용자에게 json형태로 묶어서 보내달라 #mid키의 값을 가져옴
        city = request.json['city']
        sess = Session(db)
        stmt = select(Inventory)\
            .join(Inventory.store)\
            .where(Inventory.m_id == mid)\
            .where(Store.city == city)
        # .where을 이어서 쓰면 and연산자 where()안에 &,| 연산자 사용 가능
        q = sess.scalars(stmt).all() # 여러개 나올 경우 all(), 한개가 명확하면 one()
        inv_dict = [inv.to_dict() for inv in q]
        return jsonify(inv_dict)

    elif request.method == 'POST':
        # json 인자를 활용하여 json 형태로 데이터를 전달받음
        mid = request.json['mid']
        sid = request.json['sid']
        price = request.json['price']
        count = request.json['count']
        inv = Inventory(price=price, count=count, manage_date=datetime.now(), m_id=mid, s_id=sid)
        sess = Session(db)
        sess.add(inv)
        sess.commit()
        return jsonify(inv.to_dict()) # 데이터 변동된 것 적용

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000) # host는 인터넷 주소, 즉 IP