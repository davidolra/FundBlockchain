import sys
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Nombre del archivo donde guardaremos la llave
ARCHIVO_LLAVE = "llave.key"

def generar_llave():
    """Genera una llave aleatoria de 32 bytes (256 bits) para AES-256."""
    llave = get_random_bytes(32)
    with open(ARCHIVO_LLAVE, "wb") as f:
        f.write(llave)
    print(f"[*] Llave generada y guardada en '{ARCHIVO_LLAVE}'.")

def leer_llave():
    """Lee la llave desde el archivo."""
    try:
        with open(ARCHIVO_LLAVE, "rb") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[!] Error: No se encontró '{ARCHIVO_LLAVE}'. Ejecuta primero 'python encriptador.py generar'.")
        sys.exit(1)

def cifrar(archivo_entrada, archivo_salida):
    """Cifra el contenido de un archivo usando AES-256 en modo CBC."""
    llave = leer_llave()
    
    # 1. Leer el texto plano
    with open(archivo_entrada, "rb") as f:
        texto_plano = f.read()
    
    # 2. Generar un IV aleatorio de 16 bytes
    iv = get_random_bytes(16)
    
    # 3. Crear el objeto cifrador
    cipher = AES.new(llave, AES.MODE_CBC, iv)
    
    # 4. Aplicar Padding y cifrar
    texto_cifrado = cipher.encrypt(pad(texto_plano, AES.block_size))
    
    # 5. Concatenar IV + Texto cifrado y codificar en Base64
    resultado_final = base64.b64encode(iv + texto_cifrado)
    
    # Guardar en el archivo de salida
    with open(archivo_salida, "wb") as f:
        f.write(resultado_final)
    print(f"[*] Archivo '{archivo_entrada}' cifrado exitosamente en '{archivo_salida}'.")

def descifrar(archivo_entrada, archivo_salida):
    """Descifra un archivo previamente cifrado con esta herramienta."""
    llave = leer_llave()
    
    # 1. Leer el archivo cifrado
    with open(archivo_entrada, "rb") as f:
        datos_base64 = f.read()
    
    # 2. Decodificar el Base64
    datos_crudos = base64.b64decode(datos_base64)
    
    # 3. Separar el IV (primeros 16 bytes) del texto cifrado (el resto)
    iv = datos_crudos[:16]
    texto_cifrado = datos_crudos[16:]
    
    # 4. Crear el objeto descifrador
    cipher = AES.new(llave, AES.MODE_CBC, iv)
    
    # 5. Descifrar y remover el padding
    try:
        texto_descifrado = unpad(cipher.decrypt(texto_cifrado), AES.block_size)
        
        # Guardar el resultado recuperado
        with open(archivo_salida, "wb") as f:
            f.write(texto_descifrado)
        print(f"[*] Archivo '{archivo_entrada}' descifrado exitosamente en '{archivo_salida}'.")
        
    except ValueError:
        print("[!] Error al descifrar: La llave es incorrecta o los datos están corruptos/modificados.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python encriptador.py generar")
        print("  python encriptador.py cifrar <archivo_entrada> <archivo_salida>")
        print("  python encriptador.py descifrar <archivo_entrada> <archivo_salida>")
        sys.exit(1)

    comando = sys.argv[1]

    if comando == "generar":
        generar_llave()
    elif comando == "cifrar" and len(sys.argv) == 4:
        cifrar(sys.argv[2], sys.argv[3])
    elif comando == "descifrar" and len(sys.argv) == 4:
        descifrar(sys.argv[2], sys.argv[3])
    else:
        print("[!] Comando no reconocido o faltan argumentos.")