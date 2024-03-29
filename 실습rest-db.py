from flask import Flask, request, jsonify
import pandas as pd
from 실습database import * #다른 py파일에 있는 * 모든 요소를 import시킴
from sqlalchemy.orm import Session
from sqlalchemy import select

app = Flask(__name__) #인스턴스화
app.config['JSON_AS_ASCII'] = False
db = get_engine() #database에 있는 함수 가져오기

@app.route('/store/<s_id>', methods=['GET'])
def store(s_id):
    if request.method == 'GET':
        sess = Session(db) #alchemy의 세션에 engine넣음
        md = sess.get(Store, s_id)
        return jsonify(md.to_dict()) #필드를 dictionary화

@app.route('/medicine/<m_id>', methods=['GET'])
def medicine(m_id):
    if request.method == 'GET':
        sess = Session(db) #alchemy의 세션에 engine넣음
        md = sess.get(Medicine, m_id)
        return jsonify(md.to_dict()) #필드를 dictionary화

@app.route('/inventory', methods=['POST'])
def inventory():
    if request.method == 'POST':
        # jnt) #orm형성son 인자를 활용하여 json 형태로 데이터를 전달받음
        m_id = request.json['m_id'] #요청 변수 받아옴
        s_id = request.json['s_id']
        price = request.json['price']
        count = request.json['count']
        iv = Inventory(manage_date = datetime.now(),
                          m_id = m_id,
                          s_id = s_id,
                        price = price,
                       count = count)
        sess = Session(db)
        sess.add(iv)
        sess.commit()
        return jsonify(iv.to_dict())

@app.route('/inventory_store', methods=['GET'])
def inventory_store():
    if request.method == 'GET':
        # json 인자를 활용하여 json 형태로 데이터를 전달받음
        m_id = request.json['m_id']
        city = request.json['city']
        sess = Session(db)

        stmt = (select(Inventory)\
            .join(Inventory.store) \
            .where(Store.city == city)
            .where(Inventory.m_id == m_id)
            )

        q = sess.scalars(stmt).all()

        qs = [qq.store.name for qq in q]
        return jsonify(qs)


if __name__ == "__main__":
    app.run(debug=True) #서버실행