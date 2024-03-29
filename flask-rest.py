from flask import Flask, request, jsonify #flask는 요청을 받아서 사용자에게 응답을 보내줌 #요청에 따른 라우터 구성
#Flask: 서버 엔진, #request: request 받아내기위한 모듈

import pandas as pd
app = Flask(__name__) #사용되는 기능 정해져 있음 #모듈에 대한 이름이 들어가야함
app.config['JSON_AS_ASCII'] = False #딕셔너리 구조 #ASCII코드가 아니라 utf 그대로 이용

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
]  #prescriptions 매개변수에 저장

"""
app 모듈의 route 데코레이터를 활용하여 url 경로 구성
methods 인자에는 http 메소드를 입력
    # GET, POST, PUT, DELETE
유저가 url를 통해 요청시 데코레이트된 정의 함수가 실행
정의 함수의 인자에는 < >안에 들어간 요청 인자를 입력
"""
# 도메인(IP) /medicine/<mid>   #http://127.0.0.1:5000/medicine/MZPD12
@app.route('/medicine/<mid>', methods=['GET']) #데코레이터: 클래스에서 상속 받듯이, 함수의 상속을 받는 개념 #url경로,method:http 통신방식(get-데이터 가져와 읽기, post-데이터 수정, put, delete) #<mid>는 경로인자
def medicine(mid): #경로인자를 통해 데이터 받아서 함수 안에 넣어줌
    if request.method == 'GET': #request는 route를 통해서 넘어온 요청(보통 json형태): url주소, 매개변수
        md = MEDICINES.loc[mid].to_dict() #Medicine의 id 한개를 딕셔너리 형태로 받아옴

        return jsonify(md)  # jsonify() 통해 딕셔너리를 json으로 바꿔서 전달 #사용자에게 응답으로 돌려줌

"""
GET 과 POST 둘다 가능한 url 라우트
POST는 주로 데이터를 등록할 때 사용
request에 요청 인자 값들이 변수로 할당됨
"""
@app.route('/prescription', methods=['GET','POST'])
def prescription():
    # if 문을 활용해 GET과 POST 메소드를 구분
    if request.method == 'GET':
        return jsonify(prescriptions) #위에서 딕셔너리로 구성
    elif request.method == 'POST':
        # json 인자를 활용하여 json 형태로 데이터를 전달받음
        mid = request.json['mid'] #json으로 요청을 보내면 해당 키값을 가져옴
        email = request.json['email']
        prescriptions.append({'email': email,
                             'mid':mid}) #딕셔너리 구성된 것 저장
        return jsonify(prescriptions[-1])

# 이미지 파일등은 files 인자에 입력
import cv2
import numpy as np
@app.route('/file', methods=["POST"]) #이미지 전송 받아서
def process_image():
    file = request.files['image']
    img = file.stream.read() #byte단위로 쭈욱 들어간 형태 -> 타입 바꿔주고 opencv로 다시 이미지화
    img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_UNCHANGED)
    return jsonify({'img_shape': img.shape})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0') #서버가 실행 #host= #port= 쓰고 있지 않는 포트 넣어야함
    #IP가 고정되어 있지 않는 상황에는 넣어주지 않으면 됨 #port는 5000이 디폴트