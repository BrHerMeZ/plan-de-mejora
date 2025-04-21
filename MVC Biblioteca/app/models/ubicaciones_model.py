def agregar_ubicacion(conexion, nombre, planta, estanteria, seccion):
    cursor = conexion.cursor()
    query = """
        INSERT INTO ubicaciones (nombre, planta, estanteria, seccion)
        VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (nombre, planta, estanteria, seccion))
        conexion.commit()
        return True
    except Exception as e:
        conexion.rollback()
        print(f"Error al agregar ubicación: {e}")
        return False
