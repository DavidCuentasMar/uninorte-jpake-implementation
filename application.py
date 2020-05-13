from flask import Flask
from flask import request
app = Flask(__name__)

from jpake import JPAKE

secret = "1235"
alice = JPAKE(secret=secret, signer_id=b"alice")

@app.route('/')
def hello_world():
    return 'soy Alice'

@app.route('/test', methods = ['POST'])
def update_text():
    
    #print(request.json)
    obj = request.json
    #print(obj)
    print(obj.zkp_x1)
    
    #alice first process
    # alice.process_one(
        # remote_gx1=obj['gx1'], remote_zkp_x1=obj['zkp_x1'],
        # remote_gx2=obj['gx2'], remote_zkp_x2=obj['zkp_x2'],
    # )
    return {"mensaje":"ok"}

if __name__ == '__main__':
    app.run(port=3000,debug=True)