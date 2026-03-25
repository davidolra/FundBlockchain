import sys
import base64
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

ARCHIVO_LLAVE_CHACHA = "llave_chacha.key"

def generar_llave():
    """Genera una llave aleatoria de 32 bytes (256 bits) para ChaCha20."""
    llave = get_random_bytes(32)
    with open(ARCHIVO_LLAVE_CHACHA, "wb") as f:
        f.write(llave)
    print(f"[*] Llave ChaCha20 generada y guardada en '{ARCHIVO_LLAVE_CHACHA}'.")

def leer_llave():
    try:
        with open(ARCHIVO_LLAVE_CHACHA, "rb") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[!] Error: No se encontró '{ARCHIVO_LLAVE_CHACHA}'.")
        sys.exit(1)

def cifrar(archivo_entrada, archivo_salida):
    llave = leer_llave()
    with open(archivo_entrada, "rb") as f:
        texto_plano = f.read()
    
    # Crear el objeto cifrador (ChaCha20 genera su propio 'nonce' automáticamente si no se le pasa uno)
    cipher = ChaCha20.new(key=llave)
    
    # Cifrar (Nota: ¡NO SE USA PADDING en ChaCha20!)
    texto_cifrado = cipher.encrypt(texto_plano)
    
    # El 'nonce' en ChaCha20 es similar al IV, por defecto en PyCryptodome mide 8 bytes
    nonce = cipher.nonce
    
    # Concatenar Nonce + Texto cifrado y codificar en Base64
    resultado_final = base64.b64encode(nonce + texto_cifrado)
    
    with open(archivo_salida, "wb") as f:
        f.write(resultado_final)
        
    # Imprimir tamaños para la tabla comparativa
    print(f"[*] Archivo cifrado con ChaCha20 en '{archivo_salida}'.")
    print(f"    - Tamaño llave: {len(llave)} bytes")
    print(f"    - Tamaño texto original: {len(texto_plano)} bytes")
    print(f"    - Tamaño datos crudos (nonce + cifrado): {len(nonce) + len(texto_cifrado)} bytes")

def descifrar(archivo_entrada, archivo_salida):
    llave = leer_llave()
    with open(archivo_entrada, "rb") as f:
        datos_base64 = f.read()
    
    datos_crudos = base64.b64decode(datos_base64)
    
    # Separar el Nonce (primeros 8 bytes) del texto cifrado
    nonce = datos_crudos[:8]
    texto_cifrado = datos_crudos[8:]
    
    # Crear descifrador y descifrar (sin unpad)
    cipher = ChaCha20.new(key=llave, nonce=nonce)
    texto_descifrado = cipher.decrypt(texto_cifrado)
    
    with open(archivo_salida, "wb") as f:
        f.write(texto_descifrado)
    print(f"[*] Archivo descifrado exitosamente en '{archivo_salida}'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python validador_chacha20.py [generar | cifrar <in> <out> | descifrar <in> <out>]")
        sys.exit(1)

    comando = sys.argv[1]
    if comando == "generar":
        generar_llave()
    elif comando == "cifrar" and len(sys.argv) == 4:
        cifrar(sys.argv[2], sys.argv[3])
    elif comando == "descifrar" and len(sys.argv) == 4:
        descifrar(sys.argv[2], sys.argv[3])