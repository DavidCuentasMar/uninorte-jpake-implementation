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
    print(type(data))
    data['zkp_x1']['id'] = data['zkp_x1']['id'].encode('utf-8')
    data['zkp_x2']['id'] = data['zkp_x2']['id'].encode('utf-8')
    #print(request.json)
    #loaded_json = json.loads(request.json)
    #obj = request.json
    #print(loaded_json)
    #print(obj.zkp_x1)
    
    #alice first process
    alice.process_one(data)
    return {"mensaje":"ok"}

if __name__ == '__main__':
    app.run(port=3000,debug=True)