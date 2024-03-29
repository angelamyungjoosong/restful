# https://fastapi.tiangolo.com/ko/#api_2
# pip install fastapi # pip install "uvicorn[standard]"
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pandas as pd

app = FastAPI()

MEDICINES = pd.read_csv('2022_국립공주병원_의약품 정보.csv', encoding = 'cp949')\
    .drop(['순번','성분영문명'], axis = 1)\
    .rename({'약품코드' : 'mid',
            '약품영문명': 'name_en',
            '약품한글명': 'name_ko',
            '규격': 'size',
            '성분코드': 'ing_code',
            '성분한글명': 'ing_name'}, axis = 1)\
    .dropna()\
    .drop_duplicates(subset=['mid'])\
    .set_index('mid')

prescriptions = [
    {'email':'trave1@aiot.com', 'mid':'MZPD10'}
]

"""
app 모듈의 get 데코레이터를 활용하여 GET 메소드의 url 경로 구성
{} 를 사용하여 경로에 인자를 전달하고 정의된 함수에서 인자로 사용
딕셔너리를 리턴하면 자동으로 json으로 전달
"""

# 함수 get: 방식, {mid}: 경로매개변수-> 인자로 들어감
@app.get('/medicine/{mid}')
def get_medicine(mid):
    md = MEDICINES.loc[mid].to_dict()
    return md  # fast api에서는 리턴하면 자동으로 json형식으로 응답

# 인자가 많을 경우 필드를 가지는 클래스로 생성
class Prescription(BaseModel): #클래스 안에 필드 만들고 값 할당 없이 타입만 지정해주면 됨 -> 클래스 정의
    mid: str
    email: str


@app.get('/prescription')
def get_prescription():
    return prescriptions

"""
정의 함수 인자를 필드가 정의된 클래스 타입으로 지정
josn 인자로 요청시 해당 클래스의 필드로 자동 할당
"""
@app.post('/prescription')
def add_prescription(prescription: Prescription): #prescription이라는 인자(외부에서 들어오는 매개변수)
    prescriptions.append({'mid': prescription.mid, #내부의 객체 접근
                          'email': prescription.email})
    return prescriptions[-1]

# 파일 전송시에는 UploadFile 클래스를 활용
# pip install python-multipart
from fastapi import UploadFile
import cv2
import numpy as np
@app.post('/file')
def process_image(image:UploadFile): #UploadFile이라는 객체 이용
    img = image.file.read()
    img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_UNCHANGED)
    return {'img_shape': img.shape}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
    #flask에서 app자체적으로 run해준 것과는 달리 fast-api에서는 univorn사용