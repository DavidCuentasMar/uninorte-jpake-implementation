from flask import Flask
from flask import request
import json
app = Flask(__name__)

from jpake import JPAKE

secret = "1235"
alice = JPAKE(secret=secret, signer_id=b"alice")

@app.route('/')
def hello_world():
    return 'soy Alice'

@app.route('/test', methods = ['POST'])
def update_text():
    data = request.get_json()
    print(data)
    data['zkp_x1']['id'] = data['zkp_x1']['id'].encode('utf-8')
    data['zkp_x2']['id'] = data['zkp_x2']['id'].encode('utf-8')
    #print(request.json)
    #loaded_json = json.loads(request.json)
    #obj = request.json
    #print(loaded_json)
    #print(obj.zkp_x1)
    
    #alice first process
    alice.process_one(data)
    return {
        "zkp_x1":{"gr": alice.zkp_x1['gr'], "b":alice.zkp_x1['b'],"id":alice.zkp_x1['id'].decode('utf-8')},
        "zkp_x2":{"gr": alice.zkp_x2['gr'], "b":alice.zkp_x2['b'],"id":alice.zkp_x2['id'].decode('utf-8')},
        "gx1": alice.gx1,
        "gx2": alice.gx2
    }

@app.route('/test2', methods = ['POST'])
def update_text2():
    #print('TWO')
    data = request.get_json()
    print(data)
    data['zkp_A']['id'] = data['zkp_A']['id'].encode('utf-8')
    #print(request.json)
    #loaded_json = json.loads(request.json)
    #print(loaded_json)
    
    #alice second process
    alice.process_two(data)
    #print(alice.K)
    return {
        "A":alice.A, 
        "zkp_A":{"gr": alice.zkp_A['gr'], "b":alice.zkp_A['b'],"id":alice.zkp_A['id'].decode('utf-8')}
    }
@app.route('/test3', methods = ['POST'])
def update_text3():
    #print(alice.K)
    return {"msg":"tenemos el mismo secreto"}


if __name__ == '__main__':
    app.run(port=3000,debug=True) 