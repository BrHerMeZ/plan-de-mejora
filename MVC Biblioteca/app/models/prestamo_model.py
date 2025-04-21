def registrar_prestamo(conexion, id_usuario, id_copia, fecha_devolucion_programada):
    cursor = conexion.cursor()
    query = """
        INSERT INTO prestamos (id_usuario, id_copia, fecha_devolucion_programada)
        VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(query, (id_usuario, id_copia, fecha_devolucion_programada))
        conexion.commit()
        return True
    except Exception as e:
        conexion.rollback()
        print(f"Error al registrar préstamo: {e}")
        return False
    finally:
        cursor.close()
