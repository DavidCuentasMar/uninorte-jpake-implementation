import requests

from jpake import JPAKE


url = 'http://127.0.0.1:5000/test'

secret = "1235"
bob = JPAKE(secret=secret, signer_id=b"bob")

print(bob.zkp_x1) #how to send this

r = requests.post(url, json={"gr": bob.zkp_x1['gr'], "b":bob.zkp_x1['b'],"id":bob.zkp_x1['id'].decode('utf-8')})
r.status_code


print(r.json())

