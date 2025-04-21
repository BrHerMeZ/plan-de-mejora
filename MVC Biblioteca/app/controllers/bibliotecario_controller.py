from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from datetime import datetime, timedelta

bibliotecario_bp = Blueprint('bibliotecario_bp', __name__)

@bibliotecario_bp.route('/bibliotecario/dashboard')
def dashboard():
    if 'usuario_id' not in session or session['rol'] != 'bibliotecario':
        return redirect(url_for('user_bp.login'))
    
    return render_template('bibliotecario/dashboard.html', nombre=session.get('nombre', 'Bibliotecario'))

@bibliotecario_bp.route('/bibliotecario/prestamos')
def listar_prestamos():
    if 'usuario_id' not in session or session['rol'] != 'bibliotecario':
        return redirect(url_for('user_bp.login'))
    
    conexion = current_app.connection
    cursor = conexion.cursor()
    
    query = """
    SELECT p.id_prestamo, u.nombre as nombre_usuario, l.titulo, p.fecha_prestamo, 
           p.fecha_devolucion_programada, p.fecha_devolucion_real, p.estado
    FROM prestamos p
    JOIN usuarios u ON p.id_usuario = u.id
    JOIN copias c ON p.id_copia = c.id_copia
    JOIN libros l ON c.id_libro = l.id_libro
    ORDER BY p.fecha_prestamo DESC
    """
    cursor.execute(query)
    prestamos = cursor.fetchall()
    
    return render_template('bibliotecario/prestamos.html', prestamos=prestamos)

@bibliotecario_bp.route('/bibliotecario/reservas')
def listar_reservas():
    if 'usuario_id' not in session or session['rol'] != 'bibliotecario':
        return redirect(url_for('user_bp.login'))
    
    conexion = current_app.connection
    cursor = conexion.cursor()
    
    query = """
    SELECT r.id_reserva, u.nombre as nombre_usuario, l.titulo, r.fecha_reserva, 
           r.estado, r.fecha_limite
    FROM reservas r
    JOIN usuarios u ON r.id_usuario = u.id
    JOIN libros l ON r.id_libro = l.id_libro
    ORDER BY r.fecha_reserva DESC
    """
    cursor.execute(query)
    reservas = cursor.fetchall()
    
    return render_template('bibliotecario/reservas.html', reservas=reservas)

@bibliotecario_bp.route('/bibliotecario/reservas/aprobar/<int:id_reserva>')
def aprobar_reserva(id_reserva):
    if 'usuario_id' not in session or session['rol'] != 'bibliotecario':
        return redirect(url_for('user_bp.login'))
    
    conexion = current_app.connection
    cursor = conexion.cursor()
    
    query = """
    SELECT r.id_reserva, r.id_usuario, r.id_libro
    FROM reservas r
    WHERE r.id_reserva = %s AND r.estado = 'pendiente'
    """
    cursor.execute(query, (id_reserva,))
    reserva = cursor.fetchone()
    
    if not reserva:
        flash('Reserva no encontrada o no está pendiente', 'danger')
        return redirect(url_for('bibliotecario_bp.listar_reservas'))
    


    query = """
    SELECT id_copia FROM copias 
    WHERE id_libro = %s AND estado = 'disponible'
    LIMIT 1
    """
    cursor.execute(query, (reserva['id_libro'],))
    copia = cursor.fetchone()
    
    if not copia:
        flash('No hay copias disponibles para este libro', 'warning')
        return redirect(url_for('bibliotecario_bp.listar_reservas'))
    
    try:
        cursor.execute("START TRANSACTION")
        
        query = "UPDATE reservas SET estado = 'activa' WHERE id_reserva = %s"
        cursor.execute(query, (id_reserva,))
        
        query = "UPDATE copias SET estado = 'prestado' WHERE id_copia = %s"
        cursor.execute(query, (copia['id_copia'],))
        
        fecha_devolucion = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        query = """
        INSERT INTO prestamos (id_usuario, id_copia, fecha_devolucion_programada, estado)
        VALUES (%s, %s, %s, 'activo')
        """
        cursor.execute(query, (reserva['id_usuario'], copia['id_copia'], fecha_devolucion))
        
        conexion.commit()
        
        flash('Reserva aprobada y préstamo registrado exitosamente', 'success')
    except Exception as e:
        conexion.rollback()
        flash(f'Error al aprobar la reserva: {str(e)}', 'danger')
    
    return redirect(url_for('bibliotecario_bp.listar_reservas'))

@bibliotecario_bp.route('/bibliotecario/prestamos/devolver/<int:id_prestamo>')
def devolver_prestamo(id_prestamo):

    if 'usuario_id' not in session or session['rol'] != 'bibliotecario':
        return redirect(url_for('user_bp.login'))
    
    conexion = current_app.connection
    cursor = conexion.cursor()
    
    query = """
    SELECT id_prestamo, id_copia
    FROM prestamos
    WHERE id_prestamo = %s AND estado = 'activo'
    """
    cursor.execute(query, (id_prestamo,))
    prestamo = cursor.fetchone()
    
    if not prestamo:
        flash('Préstamo no encontrado o ya fue devuelto', 'danger')
        return redirect(url_for('bibliotecario_bp.listar_prestamos'))
    
    try:
        cursor.execute("START TRANSACTION")
    
        query = """
        UPDATE prestamos 
        SET estado = 'devuelto', fecha_devolucion_real = CURRENT_DATE
        WHERE id_prestamo = %s
        """
        cursor.execute(query, (id_prestamo,))
        
        query = """
        UPDATE copias
        SET estado = 'disponible'
        WHERE id_copia = %s
        """
        cursor.execute(query, (prestamo['id_copia'],))
        
        conexion.commit()
        
        flash('Libro devuelto exitosamente', 'success')
    except Exception as e:
        conexion.rollback()
        flash(f'Error al registrar la devolución: {str(e)}', 'danger')
    
    return redirect(url_for('bibliotecario_bp.listar_prestamos'))