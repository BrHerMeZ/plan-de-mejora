def crear_reserva(conexion, id_usuario, id_libro, fecha_limite):
    try:
        with conexion.cursor() as cursor:
            sql = """
                INSERT INTO reservas (id_usuario, id_libro, fecha_limite)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (id_usuario, id_libro, fecha_limite))
        conexion.commit()
        return True
    except Exception as e:
        print("Error al crear reserva:", e)
        return False


def obtener_reservas_usuario(conexion, id_usuario):
    try:
        with conexion.cursor(dictionary=True) as cursor:
            sql = """
                SELECT r.*, l.titulo, u.nombre AS nombre_usuario
                FROM reservas r
                JOIN libros l ON r.id_libro = l.id_libro
                JOIN usuarios u ON r.id_usuario = u.id_usuario
                WHERE r.id_usuario = %s
            """
            cursor.execute(sql, (id_usuario,))
            return cursor.fetchall()
    except Exception as e:
        print("Error al obtener reservas del usuario:", e)
        return []


def actualizar_estado_reserva(conexion, id_reserva, estado):
    try:
        with conexion.cursor() as cursor:
            sql = "UPDATE reservas SET estado = %s WHERE id_reserva = %s"
            cursor.execute(sql, (estado, id_reserva))
        conexion.commit()
        return True
    except Exception as e:
        print("Error al actualizar estado de reserva:", e)
        return False


def obtener_reserva(conexion, id_reserva):
    try:
        with conexion.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM reservas WHERE id_reserva = %s"
            cursor.execute(sql, (id_reserva,))
            return cursor.fetchone()
    except Exception as e:
        print("Error al obtener reserva por ID:", e)
        return None
