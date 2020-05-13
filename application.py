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
    print(request.json)
    return {"mensaje":"ok"}

if __name__ == '__main__':
    app.run(port=3000,debug=True)