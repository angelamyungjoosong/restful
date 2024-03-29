from flask import Flask, request, jsonify
import pandas as pd
from database import * #다른 py파일에 있는 * 모든 요소를 import시킴
from sqlalchemy.orm import Session
from sqlalchemy import select

app = Flask(__name__) #인스턴스화
app.config['JSON_AS_ASCII'] = False
db = get_engine() #database에 있는 함수 가져오기

@app.route('/medicine/<mid>', methods=['GET'])
def store(mid):
    if request.method == 'GET':
        sess = Session(db) #alchemy의 세션에 engine넣음
        md = sess.get(Medicine, mid)
        return jsonify(md.to_dict()) #필드를 dictionary화

@app.route('/prescription', methods=['GET','POST'])
def prescription():
    # if 문을 활용해 GET과 POST 메소드를 구분
    if request.method == 'GET':
        sess = Session(db)
        ps = sess.scalars(select(Prescription)).all()
        ps_dict = [p.to_dict() for p in ps] #여러개를 리스트안에 넣기. append와 비슷.
        return jsonify(ps_dict)
    elif request.method == 'POST':
        # json 인자를 활용하여 json 형태로 데이터를 전달받음
        mid = request.json['mid']
        uid = request.json['uid']
        ps = Prescription(date = datetime.now(),
                          mid = mid,
                          uid = uid) #orm형성
        sess = Session(db)
        sess.add(ps)
        sess.commit()
        return jsonify(ps.to_dict())

@app.route('/prescription/<uid>', methods=['GET','POST'])
def user_prescrip(uid):
    if request.method == 'GET':
        sess = Session(db)
        user = sess.get(User, uid)
        ps = [p.to_dict() for p in user.prescrip]
        return jsonify(ps)

    elif request.method == 'POST':
        # json 인자를 활용하여 json 형태로 데이터를 전달받음
        mid = request.json['mid']
        sess = Session(db)

        stmt = select(Prescription)\
            .join(Prescription.user)\
            .where(Prescription.mid == mid)\
            .where(User.uid == uid)
        q = sess.scalars(stmt).one()
        return jsonify(q.to_dict())

if __name__ == "__main__":
    app.run(debug=True) #서버실행