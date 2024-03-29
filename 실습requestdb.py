import requests

r = requests.get('http://127.0.0.1:5000/store/1')
print(r.json(),'\n')

r = requests.get('http://127.0.0.1:5000/medicine/EURE')
print(r.json(),'\n')

r = requests.post('http://127.0.0.1:5000/inventory',
                  json={'s_id': 1,
                        'm_id':'EURE',
                        'price': 40000,
                        'count': 500
                        })
print(r.json(),'\n')



r = requests.get('http://127.0.0.1:5000/inventory_store',
                 json={'m_id':'EURE',
                       'city':'수정구'
                 })
print(r.json(),'\n')
