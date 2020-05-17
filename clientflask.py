import requests
import time
from jpake import JPAKE
import hashlib 
from Crypto.Hash import SHA256

aliceId = b'alice'
jPakeKey = b'mensage'

url = 'http://127.0.0.1:3000/fisrtMessage'
url2 = 'http://127.0.0.1:3000/secondMessage'
url3 = 'http://127.0.0.1:3000/onlyForProveTheKey'
secret = "1235"


bob = JPAKE(secret=secret, signer_id="bob")

try:
    response = requests.post(url, json={
        "zkp_x1":{"gr": bob.zkp_x1['gr'], "b":bob.zkp_x1['b'],"id":bob.zkp_x1['id'].decode('utf-8')},
        "zkp_x2":{"gr": bob.zkp_x2['gr'], "b":bob.zkp_x2['b'],"id":bob.zkp_x2['id'].decode('utf-8')},
        "gx1": bob.gx1,
        "gx2": bob.gx2
    })

    response.status_code

    data = response.json()
    print(data)
    
    aliceId = data['zkp_x2']['id']

    data['zkp_x1']['id'] = data['zkp_x1']['id'].encode('utf-8')
    data['zkp_x2']['id'] = data['zkp_x2']['id'].encode('utf-8')


    #bob first process
    bob.process_one(data)
except:
    print('error en el primer mensaje')

try:
    response2 = requests.post(url2, json={
    "A":bob.A, 
    "zkp_A":{"gr": bob.zkp_A['gr'], "b":bob.zkp_A['b'],"id":bob.zkp_A['id'].decode('utf-8')}
    })

    data2 = response2.json()
    print(data2)
    data2['zkp_A']['id'] = data2['zkp_A']['id'].encode('utf-8')

    #bob second process
    bob.process_two(data2)

    print(bob.K)
    jPakeKey = bob.k
    key = bob.k+bob.signer_id+data['zkp_x2']['id']
except:
    print('error en el segundo mensaje')

try:
    response3 = requests.post(url2, json={"msg": "ey alice todo ok"})
    print(response3.json())
except:
    print('error en el tercer mensaje')

key = jPakeKey+ bob.signer_id + aliceId
hash = SHA256.new()
hash.update(key)
shaResult = hash.hexdigest()
print(shaResult)
sha_e = shaResult[0:32]
sha_m = shaResult[32:64]
print(sha_e)
print(sha_m)