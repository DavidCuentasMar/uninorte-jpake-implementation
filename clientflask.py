import requests
import time
from jpake import JPAKE
 

url = 'http://127.0.0.1:3000/test'
url2 = 'http://127.0.0.1:3000/test2'
url3 = 'http://127.0.0.1:3000/test3'
secret = "1235"
bob = JPAKE(secret=secret, signer_id=b"bob")

response = requests.post(url, json={
        "zkp_x1":{"gr": bob.zkp_x1['gr'], "b":bob.zkp_x1['b'],"id":bob.zkp_x1['id'].decode('utf-8')},
        "zkp_x2":{"gr": bob.zkp_x2['gr'], "b":bob.zkp_x2['b'],"id":bob.zkp_x2['id'].decode('utf-8')},
        "gx1": bob.gx1,
        "gx2": bob.gx2
    })
response.status_code

#print(response.json())
data = response.json()
#print(type(data))
data['zkp_x1']['id'] = data['zkp_x1']['id'].encode('utf-8')
data['zkp_x2']['id'] = data['zkp_x2']['id'].encode('utf-8')
#print(response.json)
#loaded_json = json.loads(response.json)
#obj = response.json
#print(loaded_json)
#print(obj.zkp_x1)
#alice first process
bob.process_one(data)

#print(bob.zkp_A)
response2 = requests.post(url2, json={
    "A":bob.A, 
    "zkp_A":{"gr": bob.zkp_A['gr'], "b":bob.zkp_A['b'],"id":bob.zkp_A['id'].decode('utf-8')}
})

#print(response2.json())
data2 = response2.json()
#print('string data2:')
#print(data2)
data2['zkp_A']['id'] = data2['zkp_A']['id'].encode('utf-8')
#print('---')
#print(data2)
#bob second process
bob.process_two(data2)

print(bob.K)

##response3 = requests.post(url2, json={"msg": "ey alice todo ok"})
##print(response3.json())
