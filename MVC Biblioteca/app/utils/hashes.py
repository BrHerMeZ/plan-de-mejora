# app/utils/hashes.py
import hashlib
import os

def hash_password(password):
    """
    Genera un hash seguro para la contraseña proporcionada.
    """
    # En producción deberías usar bcrypt o Argon2, pero para simplificar usamos SHA-256
    salt = os.urandom(32)  # Salt de 32 bytes aleatorio
    hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
    # Devolver salt + hash concatenados
    # El salt se guarda con el hash para poder verificarlo después
    return salt.hex() + '$' + hash.hex()

def verify_password(password, stored_hash):
    """
    Verifica si la contraseña coincide con el hash almacenado.
    """
    # Separar el salt del hash
    salt_hex, hash_hex = stored_hash.split('$')
    salt = bytes.fromhex(salt_hex)
    
    # Calcular el hash de la contraseña proporcionada
    hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
    # Comparar con el hash almacenado
    return hash.hex() == hash_hex

# Crear hashes para los tres usuarios predeterminados
def create_default_users():
    default_users = [
        {
            'nombre': 'Administrador',
            'email': 'admin@biblioteca.com',
            'password': 'admin123',
            'rol': 'administrador'
        },
        {
            'nombre': 'Bibliotecario',
            'email': 'biblio@biblioteca.com',
            'password': 'biblio123',
            'rol': 'bibliotecario'
        },
        {
            'nombre': 'Estudiante',
            'email': 'estudiante@biblioteca.com',
            'password': 'estudiante123',
            'rol': 'estudiante'
        }
    ]
    
    for user in default_users:
        user['hashed_password'] = hash_password(user['password'])
    
    return default_users

# Cuando este script se ejecuta directamente, muestra los hashes
if __name__ == "__main__":
    users = create_default_users()
    for user in users:
        print(f"Usuario: {user['email']}")
        print(f"Contraseña: {user['password']}")
        print(f"Hash: {user['hashed_password']}")
        print("-" * 50)