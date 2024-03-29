import requests #사용자가 flask서버에 요청

#
# # # medicine 정보 요청
# r = requests.get('http://127.0.0.1:5000/medicine/MZPD12')  #함수 실행 결과가 r, 즉 응답의 결과값
# print(r.json()) #딕셔너리화하여 출력
# # #{'ing_code': '250504ATR', 'ing_name': '졸피뎀타르타르산염 12.5mg', 'name_en': 'Stilnox CR Tab. 12.5mg', 'name_ko': '스틸녹스CR정12.5mg', 'size': '1'}

# prescriptions 정보 요청
r = requests.get('http://127.0.0.1:5000/prescription')
print(r.json())
#[{'email': 'trave1@aiot.com', 'mid': 'MZPD10'}]

# # prescriptions 생성 요청
# # json 인자를 활용하여 요청 #데이터 쓰기/추가
r = requests.post('http://127.0.0.1:5000/prescription',
                  json={'mid':'EURE',
                        'email':'trave2@aiot.com'
                        })
print(r.json())
# #{'email': 'trave2@aiot.com', 'mid': 'EURE'}
#
#
# # 이미지 업로드 요청
# f = {'image': open('img.jpg', 'rb')} #파일을 데이터화, 직렬화시켜 보냄
# r = requests.post('http://127.0.0.1:5000/file',files=f)
# print(r.json())