from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from datetime import datetime, timedelta

reserva_bp = Blueprint('reserva_bp', __name__)

@reserva_bp.route('/reservar-libro/<int:id_libro>', methods=['GET', 'POST'])
def reservar_libro():
    if 'usuario_id' not in session:
        return redirect(url_for('user_bp.login'))

    if request.method == 'POST':
        isbn = request.form['isbn']
        fecha_reserva = request.form['fecha']
        usuario_id = session['usuario_id']

        conexion = current_app.connection
        cursor = conexion.cursor()

        query = "SELECT id_libro FROM libros WHERE isbn = %s AND disponible = 1"
        cursor.execute(query, (isbn,))
        libro = cursor.fetchone()

        if not libro:
            flash('El libro no existe o no está disponible', 'danger')
            return render_template('estudiante/reservar_libro.html')

        libro_id = libro['id_libro']
        fecha_limite = (datetime.strptime(fecha_reserva, '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')

        try:
            query = """
            INSERT INTO reservas (id_usuario, id_libro, fecha_reserva, estado, fecha_limite)
            VALUES (%s, %s, %s, 'Pendiente', %s)
            """
            cursor.execute(query, (usuario_id, libro_id, fecha_reserva, fecha_limite))
            conexion.commit()

            flash('Reserva creada exitosamente', 'success')
            return redirect(url_for('reserva_bp.mis_reservas'))
        except Exception as e:
            flash(f'Error al crear la reserva: {str(e)}', 'danger')

    return render_template('estudiante/reservar_libro.html')

@reserva_bp.route('/mis-reservas')
def mis_reservas():
    if 'usuario_id' not in session:
        return redirect(url_for('user_bp.login'))

    usuario_id = session['usuario_id']
    conexion = current_app.connection
    cursor = conexion.cursor()

    query = """
    SELECT r.id_reserva, l.titulo, l.isbn, r.fecha_reserva, r.estado, r.fecha_limite
    FROM reservas r
    JOIN libros l ON r.id_libro = l.id_libro
    WHERE r.id_usuario = %s
    ORDER BY r.fecha_reserva DESC
    """
    cursor.execute(query, (usuario_id,))
    reservas = cursor.fetchall()

    return render_template('estudiante/mis_reservas.html', reservas=reservas)

@reserva_bp.route('/cancelar-reserva/<int:id_reserva>')
def cancelar_reserva(id_reserva):
    if 'usuario_id' not in session:
        return redirect(url_for('user_bp.login'))

    usuario_id = session['usuario_id']
    conexion = current_app.connection
    cursor = conexion.cursor()

    query = "SELECT * FROM reservas WHERE id_reserva = %s AND id_usuario = %s"
    cursor.execute(query, (id_reserva, usuario_id))
    reserva = cursor.fetchone()

    if not reserva:
        flash('Reserva no encontrada o no tienes permiso para cancelarla', 'danger')
        return redirect(url_for('reserva_bp.mis_reservas'))

    query = "UPDATE reservas SET estado = 'Cancelada' WHERE id_reserva = %s"
    cursor.execute(query, (id_reserva,))
    conexion.commit()

    flash('Reserva cancelada exitosamente', 'success')
    return redirect(url_for('reserva_bp.mis_reservas'))
