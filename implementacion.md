# 1. Calculamos el secreto compartido de alta entropía

En la primera fase de la implementación se realizan un intercambio de mensajes para llegar al secreto compartido y después de esto se procede a utilizar este secreto concatenado con los id de alice y bob para formar una nueva cadena que sera introducida en un algoritmo de hash para obtener una nueva llave y así utilizarla para establecer una comunición por un canal seguro

# 2. Calcular una nueva llave con Sha256

Concretamente el algoritmo de hash utilizado es el Sha256 el cual como su nombre lo indica nos devolverá una llave de 256 bits la cual utilizaremos 128 para el algoritmo de cifrado AES y los otros 128 restantes para el valivador HMAC 

key = sha(j-pake-key + id_bob + id_alice)

sha_e  = key.truncate(0:127) 
sha_m  = key.truncate(128:256)

# 3. Cifrar el texto plano con AES en modo CBC

se tiene un textoPlano y un iv de inicialización

textoCifrado = AES(sha_e, MODO-CBC, iv)
c <----- E_CBC(sha_e, m)

# 4. Bob calcula un t usando Hmac para validar el mensaje

luego se toma la otra parte del sha y el texto cifrado para calcular un t el cual va a validar el mensaje cuando llegue al receptor

t <------ HMAC(sha_m, c)

# 5. Enviar c y t al servidor (Bob es quien en envia)
 
se implementaron dos metodos para poder hacer este envió posible, ya que el texto cifrado y el valor de t se encontraban en bytes y era necesario llevarlo a una forma que fuesen JSON serializable

metodos implementados:

- bytesToString
- stringToBytes 


# 6. Quien recibe toma el mensaje y lo valida con t y c

Del lado de Alice en nuestra implementacion: 
tomamos c y t y computamos t'<----Hmac(sha_m, c)

si t' es igual a t entonces el mensaje es mostrado
de lo contrario el c o el t enviados fueron comprometidos

# 7. Por ultimo se descifra el mensaje del lado de Alice

mensajeOriginal <----D_CBC(sha_e, c)