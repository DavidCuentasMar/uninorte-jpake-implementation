1. implementar AES con Sha

- AES en MODO CBC GSM (mejor modo) cifra y authentica
- y un sha 256 - keySha = sha(key-j-pake + id_a + id_b)

keySha = 0000000000000000000000000000000000 | 111111111111111111111111111111111

k_e = keySha.truncate(128)   0000000000000000000000000000000000 
k_m = keySha.truncate() 111111111111111111111

2. implentar HMAC

- H-MAC codigo de authenticacion (con los 128 bits qeu sobraron del trunqueo) -> me regresa C y T

m = mensaje

c <----- E_CBC(k_e, m)

c = texto cifrado con AES

t <------ HMAC(k_m, c)

3. Enviar c y t al servidor (quien en envia)

Del otro lado (del que recibe)

tomar c y computar t'<----Hmac(k_m, c)
verificar si t' es igual a t

## otra froma de verlo o como el profesor creyo que va a estar implementado
V(km, t, m) ---> Fslso o verdadero

4. descifrar
m<----D_CBC(ke, c)
