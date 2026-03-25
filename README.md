¿Qué pasa si cambias un solo bit de la llave?
Se produce el "efecto avalancha" (avalanche effect). En criptografía, alterar un solo bit de la llave (o del mensaje original) cambia por completo el resultado final. Si intentas descifrar un texto con una llave que difiere en un solo bit de la original, el algoritmo fallará y arrojará un error de padding o devolverá basura ininteligible. La llave debe ser exacta.

¿Por qué es vital que el IV (Vector de Inicialización) cambie en cada operación?
El IV aporta aleatoriedad al proceso. Si encriptamos el mensaje "Hola" dos veces seguidas con la misma llave y el mismo IV, el texto cifrado resultante será idéntico en ambas ocasiones. Esto permitiría a un atacante detectar patrones (saber que estás enviando el mismo mensaje). Al cambiar el IV en cada operación, el mismo mensaje original generará un texto cifrado completamente distinto cada vez, ocultando los patrones.

¿Para qué sirve el padding en algoritmos de bloque como AES?
AES es un cifrador de bloques, lo que significa que procesa los datos en trozos de un tamaño fijo (en este caso, 16 bytes). La mayoría de los mensajes de texto no son múltiplos exactos de 16 bytes. El padding añade bytes de relleno al final del mensaje para completar ese último bloque y permitir que el algoritmo matemático de AES pueda ejecutarse correctamente. Al descifrar, el algoritmo detecta y elimina ese relleno para devolver el mensaje exacto original.


Al comparar ambos algoritmos, podemos observar que ambos utilizan el mismo nivel de seguridad en la llave (256 bits). Sin embargo, como AES trabaja por bloques fijos de 16 bytes, requiere agregar datos falsos (padding) alargando el archivo final. ChaCha20, al ser un cifrador de flujo, no necesita padding, haciendo que el archivo cifrado resultante (cyphertext) sea ligeramente más ligero y exacto a la longitud del mensaje original más su nonce.