# scripts/create_default_users.py
import sys
import os
import pymysql.cursors

# Agregar el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.utils.hashes import create_default_users
from config import Config

def main():
    # Conexión a la base de datos
    connection = pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        cursor = connection.cursor()
        
        # Obtener usuarios predeterminados
        default_users = create_default_users()
        
        for user in default_users:
            # Verificar si el usuario ya existe
            check_query = "SELECT id FROM usuarios WHERE email = %s"
            cursor.execute(check_query, (user['email'],))
            existing_user = cursor.fetchone()
            
            if existing_user:
                print(f"El usuario {user['email']} ya existe. Actualizando contraseña...")
                update_query = "UPDATE usuarios SET password = %s WHERE email = %s"
                cursor.execute(update_query, (user['hashed_password'], user['email']))
            else:
                print(f"Creando usuario: {user['email']}")
                insert_query = """
                INSERT INTO usuarios (nombre, email, password, rol)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    user['nombre'],
                    user['email'],
                    user['hashed_password'],
                    user['rol']
                ))
        
        connection.commit()
        print("Usuarios creados/actualizados exitosamente")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    main()