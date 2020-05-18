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
secureUrl = 'http://127.0.0.1:3000/securechannel'

secret = "secretWithLessEntropy"

bob = JPAKE(secret=secret, signer_id=b"bob")

def bytesToString(bytesToFormat):
    string = ''
    for byte in bytesToFormat:
        string = string+'-'+ str(byte)
    return string    

def stringToBytes(stringToFormat):
    stringCut = stringToFormat.split('-')
    bytesCode = b''
    for eachPos in stringCut:
        if eachPos != '':
            bytesCode = bytesCode + bytes([int(eachPos)]) 
    return bytesCode  

try:
    firstResponse = requests.post(firstUrl, json={
        "zkp_x1":{"gr": bob.zkp_x1['gr'], "b":bob.zkp_x1['b'], "id":bob.zkp_x1['id'].decode('utf-8')},
        "zkp_x2":{"gr": bob.zkp_x2['gr'], "b":bob.zkp_x2['b'], "id":bob.zkp_x2['id'].decode('utf-8')},
        "gx1": bob.gx1,
        "gx2": bob.gx2
    })

    data = firstResponse.json()
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

    #bob second process
    bob.process_two(data2)
except:
    print('error en el segundo mensaje')

# creación de la nueva key para trabar con el Sha256 y Hmac
key = bytes(str(bob.K), 'utf-8') + bob.signer_id + aliceId

# Calculo del Sha256
hash = SHA256.new()
hash.update(key)
shaResult = hash.hexdigest()

# particion del Sha para transformarlo en 2 nuevas llaves
sha_e = shaResult[0:32]
sha_m = shaResult[32:64]

# Se configura el cifrador de AES en modo CBC
objAES = AES.new(sha_e, AES.MODE_CBC, iv)

# Input strings must be a multiple of 16 in length
message = "the answer is ye"
ciphertext = objAES.encrypt(message)

# calculamos el t con hmac
bSha_m = bytes(sha_m, 'utf-8')
objHmac = hmac.new(bSha_m, ciphertext)
t = objHmac.digest() 

# transformamos los formatos de bytes en string 
# para poder enviar con nuestra implementación
t_to_send = bytesToString(t)
ciphertext_to_send = bytesToString(ciphertext)

secureChannelResponse = requests.post(secureUrl, json={"t":t_to_send, "msg": ciphertext_to_send})
print('mensaje enviado a Alice')
print('Respuesta de alice:')
print(secureChannelResponse.json())