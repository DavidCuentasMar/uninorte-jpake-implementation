import requests

from jpake import JPAKE


url = 'http://127.0.0.1:5000/test'

secret = "1235"
bob = JPAKE(secret=secret, signer_id=b"bob")

r = requests.post(url, json={
        "zpk_x1":{"gr": bob.zkp_x1['gr'], "b":bob.zkp_x1['b'],"id":bob.zkp_x1['id'].decode('utf-8')},
        "zpk_x2":{"gr": bob.zkp_x2['gr'], "b":bob.zkp_x2['b'],"id":bob.zkp_x2['id'].decode('utf-8')},
        "gx1": bob.gx1,
        "gx2": bob.gx2
    })
r.status_code
print(r.json())
