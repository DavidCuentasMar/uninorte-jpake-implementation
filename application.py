from flask import Flask
from flask import request
import json
app = Flask(__name__)
from jpake import JPAKE
import hmac 
from Crypto.Hash import SHA256
from Crypto.Cipher import AES

bobId = b'un-valor-incorrecto-dl-id'
key = b'la-llave-para-introducir-en-sha'
iv = 'This is an IV456'

secret = "secretWithLessEntropy"
alice = JPAKE(secret=secret, signer_id=b"alice")

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

@app.route('/')
def hello_world():
    return 'soy Alice'

@app.route('/firstmessage', methods = ['POST'])
def firstMessage():

    data = request.get_json()
    data['zkp_x1']['id'] = data['zkp_x1']['id'].encode('utf-8')
    data['zkp_x2']['id'] = data['zkp_x2']['id'].encode('utf-8')

    global bobId
    bobId = data['zkp_x2']['id']

    alice.process_one(data)
    return {
        "zkp_x1":{"gr": alice.zkp_x1['gr'], "b":alice.zkp_x1['b'],"id":alice.zkp_x1['id'].decode('utf-8')},
        "zkp_x2":{"gr": alice.zkp_x2['gr'], "b":alice.zkp_x2['b'],"id":alice.zkp_x2['id'].decode('utf-8')},
        "gx1": alice.gx1,
        "gx2": alice.gx2
    }

@app.route('/secondmessage', methods = ['POST'])
def secondMessage():
    data = request.get_json()
    
    data['zkp_A']['id'] = data['zkp_A']['id'].encode('utf-8')
    
    #alice second process
    alice.process_two(data)

    return {
        "A":alice.A, 
        "zkp_A":{"gr": alice.zkp_A['gr'], "b":alice.zkp_A['b'],"id":alice.zkp_A['id'].decode('utf-8')}
    }

# @app.route('/funny', methods = ['POST'])
# def funny():

#     return {"msg":"tenemos el mismo secreto pero no te lo puedo decir jeje"}

@app.route('/securechannel', methods = ['POST'])
def secureChannel():
    
    data = request.get_json()
    
    ciphertext = stringToBytes(data['msg'])
    tBob = stringToBytes(data['t'])

    key = bytes(str(alice.K), 'utf-8') + bobId + alice.signer_id
    hash = SHA256.new()
    hash.update(key)
    shaResult = hash.hexdigest()
    sha_e = shaResult[0:32]
    sha_m = shaResult[32:64]

    bSha_m = bytes(sha_m, 'utf-8')
    objHmac = hmac.new(bSha_m, ciphertext)
    t = objHmac.digest()

    try:
        if hmac.compare_digest(t, tBob):
            objAES = AES.new(sha_e, AES.MODE_CBC, iv)
            mensaje = objAES.decrypt(ciphertext)
            print(mensaje)
    except:
        print('ocurrió un error con la verificación de t')
        return {"msg":"alguien está en el canal o simplemente ocurrió un erro"}

    return {"msg":"mensaje recibido gracias"}

if __name__ == '__main__':
    app.run(port=3000,debug=True) 