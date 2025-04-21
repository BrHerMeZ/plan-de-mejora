def generar_reporte_libros_prestados(conexion):
    cursor = conexion.cursor()
    query = """
        SELECT libros.id_libro, libros.titulo, COUNT(prestamos.id_prestamo) AS cantidad_prestamos
        FROM prestamos
        JOIN copias ON prestamos.id_copia = copias.id_copia
        JOIN libros ON copias.id_libro = libros.id_libro
        GROUP BY libros.id_libro
        ORDER BY cantidad_prestamos DESC;
    """
    cursor.execute(query)
    return cursor.fetchall()


def insertar_reporte(conexion, tipo_reporte, datos):
    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO reportes (tipo_reporte, datos)
            VALUES (%s, %s)
        """
        cursor.execute(query, (tipo_reporte, str(datos)))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al insertar el reporte: {e}")
        return False
