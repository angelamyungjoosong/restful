
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from database2 import *
from sqlalchemy.orm import Session
from sqlalchemy import select

app = FastAPI()
db = get_engine()

@app.get('/medicine/{mid}') #flask와는 달리 fast api에서는 중괄호 사용
def get_medicine(mid):
    sess = Session(db)
    md = sess.get(Medicine, mid)
    return md.to_dict()

@app.get('/store/{sid}')
def get_store(sid):
    sess = Session(db)
    st = sess.get(Store, sid)
    return st.to_dict()

@app.get('/inventory/list')
def get_inventory():
    sess = Session(db)
    q = sess.scalars(select(Inventory)).all()
    invs = [inv.to_dict() for inv in q]
    return invs
class CityMidInv(BaseModel): #요청으로 내부로 들어오는 매개변수를 필드에 할당
    mid: str
    city: str
@app.get('/inventory')
def qr_inventory(rq:CityMidInv): #넣어놓은 인자에서 변수구성 #rq라는 변수에 클래스라는 타입을 인스턴스화한 것을 가져옴
    sess = Session(db)
    stmt = select(Inventory) \
        .join(Inventory.store) \
        .where(Inventory.m_id == rq.mid) \
        .where(Store.city == rq.city)
    q = sess.scalars(stmt).all()
    inv_dict = [inv.to_dict() for inv in q]
    return inv_dict

class AddInvReq(BaseModel):
    mid: str
    sid: int
    price: int
    count: int
@app.post('/inventory')
def add_inventory(rq:AddInvReq):

    inv = Inventory(price=rq.price, #필드접근해서 할당
                    count=rq.count,
                    manage_date=datetime.now(),
                    m_id=rq.mid,
                    s_id=rq.sid)
    sess = Session(db)
    sess.add(inv)
    sess.commit()
    return inv.to_dict()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

    #flask와의 차이점:
    #post와 get을 따로
    #객체화 시켜서 간단히 구성
    #자체 서버가 아니고 univorn서버 사용