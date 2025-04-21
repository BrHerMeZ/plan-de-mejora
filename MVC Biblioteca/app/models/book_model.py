def agregar_libro(conexion, isbn, titulo, id_autor, id_categoria, editorial, fecha_publicacion, resumen, paginas, idioma):
    try:
        with conexion.cursor() as cursor:
            sql = """
                INSERT INTO libros (
                    isbn, titulo, id_autor, id_categoria,
                    editorial, fecha_publicacion, resumen,
                    paginas, idioma
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                isbn, titulo, id_autor, id_categoria,
                editorial, fecha_publicacion, resumen,
                paginas, idioma
            ))
        conexion.commit()
        return True
    except Exception as e:
        print("Error al insertar libro:", e)
        return False
    
def obtener_libros(conexion):
    try:
        with conexion.cursor(dictionary=True) as cursor:
            sql = """
                SELECT
                    l.id_libro as id_libro,
                    l.isbn,
                    l.titulo,
                    a.nombre as autor,
                    c.nombre as categoria,
                    l.editorial,
                    l.fecha_publicacion,
                    l.resumen,
                    l.paginas,
                    l.idioma,
                    l.imagen_url
                FROM libros l
                JOIN autores a ON l.id_autor = a.id_autor
                JOIN categorias c ON l.id_categoria = c.id_categoria
            """
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        print("Error al consultar libros:", e)
        return []

    

def buscar_o_crear_autor(conexion, nombre_autor):
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT id_autor FROM autores WHERE nombre = %s"
            cursor.execute(sql, (nombre_autor,))
            resultado = cursor.fetchone()
            
            if resultado:
                return resultado[0]
            
            sql = "INSERT INTO autores (nombre) VALUES (%s)"
            cursor.execute(sql, (nombre_autor,))
            conexion.commit()
            return cursor.lastrowid 
            
    except Exception as e:
        print("Error con el autor:", e)
        return None

def buscar_o_crear_categoria(conexion, nombre_categoria):
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT id_categoria FROM categorias WHERE nombre = %s"
            cursor.execute(sql, (nombre_categoria,))
            resultado = cursor.fetchone()
            
            if resultado:
                return resultado[0]
            
            sql = "INSERT INTO categorias (nombre) VALUES (%s)"
            cursor.execute(sql, (nombre_categoria,))
            conexion.commit()
            return cursor.lastrowid
            
    except Exception as e:
        print("Error con la categoría:", e)
        return None


def obtener_autores(conexion):
    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id_autor, nombre FROM autores")
            return cursor.fetchall()
    except Exception as e:
        print("Error al consultar autores:", e)
        return []


def obtener_categorias(conexion):
    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id_categoria, nombre FROM categorias")
            return cursor.fetchall()
    except Exception as e:
        print("Error al consultar categorías:", e)
        return []


def obtener_idiomas(conexion):
    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT DISTINCT idioma FROM libros WHERE idioma IS NOT NULL")
            return [row['idioma'] for row in cursor.fetchall()]
    except Exception as e:
        print("Error al consultar idiomas:", e)
        return []


def obtener_libro_por_id(conexion, id_libro):
    try:
        with conexion.cursor(dictionary=True) as cursor:
            sql = """
                SELECT *
                FROM libros
                WHERE id_libro = %s
            """
            cursor.execute(sql, (id_libro,))
            return cursor.fetchone()
    except Exception as e:
        print("Error al obtener libro por ID:", e)
        return None
