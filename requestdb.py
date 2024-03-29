import requests

r = requests.get('http://127.0.0.1:5000/medicine/MZPD12')
print(r.json(),'\n')

r = requests.get('http://127.0.0.1:5000/prescription')
print(r.json(),'\n')

r = requests.post('http://127.0.0.1:5000/prescription',
                  json={'mid':'MZPD10',
                        'uid':1
                        })
print(r.json(),'\n')


r = requests.get('http://127.0.0.1:5000/prescription/1')
print(r.json(),'\n')

r = requests.post('http://127.0.0.1:5000/prescription/3',
                  json={'mid':'EURE',})
print(r.json(),'\n')