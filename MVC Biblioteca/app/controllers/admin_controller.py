from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from app.utils.hashes import hash_password

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/admin/dashboard')
def dashboard():
    if 'usuario_id' not in session or session['rol'] != 'administrador':
        return redirect(url_for('user_bp.login'))
    
    return render_template('admin/dashboard.html', nombre=session.get('nombre', 'Administrador'))

@admin_bp.route('/admin/usuarios')
def gestionar_usuarios():
    if 'usuario_id' not in session or session['rol'] != 'administrador':
        return redirect(url_for('user_bp.login'))
    
    conexion = current_app.connection
    cursor = conexion.cursor()
    
    query = """
    SELECT u.id_usuario, u.nombre, u.apellido, u.email, r.nombre AS rol, u.fecha_registro 
    FROM usuarios u
    JOIN roles r ON u.id_rol = r.id_rol
    ORDER BY u.id_usuario
    """
    cursor.execute(query)
    usuarios = cursor.fetchall()
    
    return render_template('admin/usuarios.html', usuarios=usuarios)

@admin_bp.route('/admin/usuarios/nuevo', methods=['GET', 'POST'])
def nuevo_usuario():
    if 'usuario_id' not in session or session['rol'] != 'administrador':
        return redirect(url_for('user_bp.login'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        password = request.form['password']
        rol = request.form['rol']
        
        hashed_password = hash_password(password)
        
        conexion = current_app.connection
        cursor = conexion.cursor()
        
        try:
            query = """
            INSERT INTO usuarios (nombre, apellido, email, contrasena, id_rol)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, apellido, email, hashed_password, rol))
            conexion.commit()
            
            flash('Usuario creado exitosamente', 'success')
            return redirect(url_for('admin_bp.gestionar_usuarios'))
        except Exception as e:
            flash(f'Error al crear el usuario: {str(e)}', 'danger')
    
    query_roles = "SELECT id_rol, nombre FROM roles"
    cursor.execute(query_roles)
    roles = cursor.fetchall()

    return render_template('admin/nuevo_usuario.html', roles=roles)

@admin_bp.route('/admin/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if 'usuario_id' not in session or session['rol'] != 'administrador':
        return redirect(url_for('user_bp.login'))
    
    conexion = current_app.connection
    cursor = conexion.cursor()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        rol = request.form['rol']
        
        try:
            query = """
            UPDATE usuarios SET nombre = %s, apellido = %s, email = %s, id_rol = %s
            WHERE id_usuario = %s
            """
            cursor.execute(query, (nombre, apellido, email, rol, id))
            conexion.commit()
            
            if request.form.get('password'):
                hashed_password = hash_password(request.form['password'])
                query_password = "UPDATE usuarios SET contrasena = %s WHERE id_usuario = %s"
                cursor.execute(query_password, (hashed_password, id))
                conexion.commit()
            
            flash('Usuario actualizado exitosamente', 'success')
            return redirect(url_for('admin_bp.gestionar_usuarios'))
        except Exception as e:
            flash(f'Error al actualizar el usuario: {str(e)}', 'danger')
    
    query = """
    SELECT u.id_usuario, u.nombre, u.apellido, u.email, u.id_rol
    FROM usuarios u
    WHERE u.id_usuario = %s
    """
    cursor.execute(query, (id,))
    usuario = cursor.fetchone()
    
    if not usuario:
        flash('Usuario no encontrado', 'danger')
        return redirect(url_for('admin_bp.gestionar_usuarios'))
    
    query_roles = "SELECT id_rol, nombre FROM roles"
    cursor.execute(query_roles)
    roles = cursor.fetchall()
    
    return render_template('admin/editar_usuario.html', usuario=usuario, roles=roles)

@admin_bp.route('/admin/usuarios/eliminar/<int:id>')
def eliminar_usuario(id):
    if 'usuario_id' not in session or session['rol'] != 'administrador':
        return redirect(url_for('user_bp.login'))
    
    if session['usuario_id'] == id:
        flash('No puedes eliminar tu propio usuario', 'danger')
        return redirect(url_for('admin_bp.gestionar_usuarios'))
    
    conexion = current_app.connection
    cursor = conexion.cursor()
    
    try:
        query = "DELETE FROM usuarios WHERE id_usuario = %s"
        cursor.execute(query, (id,))
        conexion.commit()
        
        flash('Usuario eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar el usuario: {str(e)}', 'danger')
    
    return redirect(url_for('admin_bp.gestionar_usuarios'))

@admin_bp.route('/admin/reportes')
def reportes():
    if 'usuario_id' not in session or session['rol'] != 'administrador':
        return redirect(url_for('user_bp.login'))
    
    conexion = current_app.connection
    cursor = conexion.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM libros")
    total_libros = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM usuarios")
    total_usuarios = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM prestamos WHERE estado = 'activo'")
    prestamos_activos = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM reservas WHERE estado = 'pendiente'")
    reservas_pendientes = cursor.fetchone()['total']
    
    cursor.execute("""
        SELECT l.titulo, COUNT(p.id_prestamo) as num_prestamos
        FROM prestamos p
        JOIN copias c ON p.id_copia = c.id_copia
        JOIN libros l ON c.id_libro = l.id_libro
        GROUP BY l.id_libro
        ORDER BY num_prestamos DESC
        LIMIT 5
    """)
    libros_populares = cursor.fetchall()
    
    estadisticas = {
        'total_libros': total_libros,
        'total_usuarios': total_usuarios,
        'prestamos_activos': prestamos_activos,
        'reservas_pendientes': reservas_pendientes,
        'libros_populares': libros_populares
    }
    
    return render_template('admin/reportes.html', estadisticas=estadisticas)
