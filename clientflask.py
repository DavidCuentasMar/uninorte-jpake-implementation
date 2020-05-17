import requests
import time
from jpake import JPAKE
import hmac 
from Crypto.Hash import SHA256
from Crypto.Cipher import AES

aliceId = b'el-id-de-alice'
key=b'la-llave-para-introducir-en-sha'
iv = 'This is an IV456'

firstUrl = 'http://127.0.0.1:3000/firstmessage'
secondUrl = 'http://127.0.0.1:3000/secondmessage'
thirdUrl = 'http://127.0.0.1:3000/funny'
secureUrl = 'http://127.0.0.1:3000/secureChannel'

secret = "secretWithLessEntropy"

bob = JPAKE(secret=secret, signer_id=b"bob")

try:
    firstResponse = requests.post(firstUrl, json={
        "zkp_x1":{"gr": bob.zkp_x1['gr'], "b":bob.zkp_x1['b'], "id":bob.zkp_x1['id'].decode('utf-8')},
        "zkp_x2":{"gr": bob.zkp_x2['gr'], "b":bob.zkp_x2['b'], "id":bob.zkp_x2['id'].decode('utf-8')},
        "gx1": bob.gx1,
        "gx2": bob.gx2
    })

    data = firstResponse.json()
    #print(data)
    
    aliceId =bytes(data['zkp_x2']['id'], 'utf-8') 

    data['zkp_x1']['id'] = data['zkp_x1']['id'].encode('utf-8')
    data['zkp_x2']['id'] = data['zkp_x2']['id'].encode('utf-8')

    #bob first process
    bob.process_one(data)
except:
    print('error en el primer mensaje')

try:
    secondResponse = requests.post(secondUrl, json={
        "A":bob.A, 
        "zkp_A":{"gr": bob.zkp_A['gr'], "b":bob.zkp_A['b'],"id":bob.zkp_A['id'].decode('utf-8')}
    })

    data2 = secondResponse.json()
    
    data2['zkp_A']['id'] = data2['zkp_A']['id'].encode('utf-8')
    #print(data2)

    #bob second process
    bob.process_two(data2)
    time.sleep(1)
    print(bob.k)
    #key = bob.k+bob.signer_id+data['zkp_x2']['id']
except ValueError:
    print('error:'+ValueError)
except:
    print('error en el segundo mensaje')

# try:
#     thirdResponse = requests.post(thirdUrl, json={"msg": "ey alice todo ok"})
#     print(thirdResponse.json())
# except:
#     print('error en el tercer mensaje')

key = bytes(str(bob.K), 'utf-8') + bob.signer_id + aliceId
hash = SHA256.new()
hash.update(key)
shaResult = hash.hexdigest()
print(shaResult)
sha_e = shaResult[0:32]
sha_m = shaResult[32:64]
print(sha_e)
print(sha_m)

obj = AES.new(sha_e, AES.MODE_CBC, iv)
message = "The answer is no"
ciphertext = obj.encrypt(message)
print(ciphertext)

bSha_m = bytes(sha_e, 'utf-8')
objT = hmac.new(bSha_m,ciphertext)

t = objT.digest()
# print(t) send t to Alice

try:
    secureChannelResponse = requests.post(secureUrl, json={"t":t, "msg": ciphertext})
    print(secureChannelResponse.json())
except:
    print('error en el canal seguro')  