from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from app.utils.hashes import verify_password

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        rol = request.form['rol']
        
        if rol == 'administrador':
            try:
                conexion = current_app.connection
                cursor = conexion.cursor()
                
                query = "SELECT * FROM usuarios WHERE email = %s AND id_rol = 1"
                cursor.execute(query, (email,))
                admin = cursor.fetchone()
                
                if admin and verify_password(password, admin['contrasena']):
                    session['usuario_id'] = admin['id_usuario']
                    session['rol'] = 'administrador'
                    session['nombre'] = admin['nombre']
                    
                    return redirect(url_for('user_bp.login'))
                else:
                    flash('Credenciales incorrectas. Verifique su correo y contraseña.', 'danger')
            except Exception as e:
                flash('Error al iniciar sesión', 'danger')
                print("Error en inicio de sesión: {e}")
        else:
            flash('Seleccione el rol de administrador', 'warning')
            
    return render_template('auth/login.html')

@user_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('user_bp.login'))

@user_bp.route('/dashboard/estudiante')
def dashboard_estudiante():
    if 'usuario_id' not in session or session['rol'] != 'estudiante':
        return redirect(url_for('user_bp.login'))
    
    return render_template('estudiante/dashboard.html', nombre=session.get('nombre', 'Estudiante'))

def validar_usuario(conexion, email, contraseña, rol):
    cursor = conexion.cursor()
    query = """
        SELECT * FROM usuarios 
        WHERE email = %s AND contraseña = %s AND rol = %s
    """
    cursor.execute(query, (email, contraseña, rol))
    usuario = cursor.fetchone()
    cursor.close()
    return usuario