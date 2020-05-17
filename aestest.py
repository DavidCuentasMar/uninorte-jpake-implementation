import random 
from Crypto.Cipher import AES

# key = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
# print ('key', [x for x in key])

# iv = ' ' * 16
# key = key.decode('utf-8')

# print(len(iv.encode('utf-8')))
# aes = AES.new(key, AES.MODE_CBC, iv)
# data = 'hello world 1234' # <- 16 bytes
# encd = aes.encrypt(data)
# print(encd)

obj = AES.new(b'This is a key123', AES.MODE_CBC, b'This is an IV456')
message = "The answer is no"
ciphertext = obj.encrypt(message)
print(ciphertext)

obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
mensaje = obj2.decrypt(ciphertext)
print(mensaje)
