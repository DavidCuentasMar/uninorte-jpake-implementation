import random 
from Crypto.Cipher import AES

key = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
print ('key', [x for x in key])

iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
print(iv)

aes = AES.new(key, AES.MODE_CBC, iv)
data = 'hello world 1234' # <- 16 bytes
encd = aes.encrypt(data)
print(encd)
