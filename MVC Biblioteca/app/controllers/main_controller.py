from flask import Blueprint, render_template, request, redirect, url_for, current_app, session, flash
from app.controllers.user_controller import validar_usuario
from app.models.book_model import (
    agregar_libro, obtener_libros, 
    buscar_o_crear_autor, buscar_o_crear_categoria
)
from app.models.prestamo_model import registrar_prestamo
from app.models.reportes_model import generar_reporte_libros_prestados, insertar_reporte
from app.models.ubicaciones_model import agregar_ubicacion


main_bp = Blueprint('main_bp', __name__)


@main_bp.route('/')
def Inicio():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        rol = request.form['rol']

        usuario = validar_usuario(current_app.connection, email, contraseña, rol)
        if usuario:
            session['usuario_id'] = usuario['id']
            return redirect(url_for('Inicio_de_sesion.html'))
        else:
            flash("Credenciales inválidas. Intenta nuevamente.")
            return redirect(url_for('Inicio_de_sesion.html'))
    else:
        return render_template('Inicio_de_sesion.html') 




@main_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        isbn = request.form['isbn']
        titulo = request.form['titulo']
        autor = request.form['autor'] 
        categoria = request.form['categoria']
        editorial = request.form['editorial']
        

        id_autor = buscar_o_crear_autor(current_app.connection, autor)

        id_categoria = buscar_o_crear_categoria(current_app.connection, categoria)
        

        fecha_publicacion = request.form.get('fecha_publicacion', None)
        resumen = request.form.get('resumen', None)
        paginas = request.form.get('paginas', 0)
        idioma = request.form.get('idioma', 'Español')
        
        conexion = current_app.connection
        exito = agregar_libro(
            conexion, isbn, titulo, id_autor, id_categoria,
            editorial, fecha_publicacion, resumen, paginas, idioma
        )
        
        if exito:
            return redirect(url_for('user_bp.login'))
        else:
            return "Error al agregar libro", 500
            
    return render_template('agregarLibro.html')




@main_bp.route('/gestionarPrestamos', methods=['GET', 'POST'])
def gestionar_prestamos():
    if request.method == 'POST':
        id_usuario = request.form['id_usuario']
        id_copia = request.form['id_copia']
        fecha_devolucion_programada = request.form['fecha_devolucion_programada']

        conexion = current_app.connection
        exito = registrar_prestamo(
            conexion, id_usuario, id_copia, fecha_devolucion_programada
        )

        if exito:
            return redirect(url_for('main_bp.gestionar_prestamos'))
        else:
            flash("Error al registrar el préstamo. Intenta nuevamente.", 'danger')
            return redirect(url_for('main_bp.gestionar_prestamos'))

    return render_template('gestionarPrestamos.html')




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
    resultado = cursor.fetchall()
    return resultado


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


@main_bp.route('/generar_reporte_libros_prestados', methods=['GET'])
def generar_reporte():
    conexion = current_app.connection
    reporte = generar_reporte_libros_prestados(conexion)
    exito = insertar_reporte(conexion, "Libros más prestados", reporte)

    if exito:
        return redirect(url_for('main_bp.Inicio'))
    else:
        return "Error al generar el reporte", 500


@main_bp.route('/gestionarUbicaciones', methods=['GET', 'POST'])
def gestionar_ubicaciones():
    if request.method == 'POST':
        nombre = request.form['nombre']
        planta = request.form['planta']
        estanteria = request.form['estanteria']
        seccion = request.form['seccion']

        conexion = current_app.connection
        exito = agregar_ubicacion(
            conexion, nombre, planta, estanteria, seccion
        )

        if exito:
            return redirect(url_for('main_bp.gestionar_ubicaciones'))
        else:
            return "Error al registrar la ubicación", 500

    return render_template('gestionarUbicaciones.html')


@main_bp.route('/catalogo')
def catalogo():
    libros = obtener_libros(current_app.connection)
    return render_template('catalogo.html', libros=libros)

