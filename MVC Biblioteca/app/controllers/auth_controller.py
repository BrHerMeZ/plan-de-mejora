from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
import pymysql
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['GET'])
def mostrar_registro():
    return render_template('auth/registrar.html')


@auth_bp.route('/registro', methods=['POST'])
def registrar_usuario():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    contrasena = request.form['contrasena']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    id_rol = 3  

    hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

    try:
        connection = current_app.connection
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO usuarios (nombre, apellido, email, contrasena, telefono, direccion, id_rol)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nombre, apellido, email, hashed_password, telefono, direccion, id_rol))
            connection.commit()
            flash('Usuario registrado correctamente', 'success')
            return redirect(url_for('auth.mostrar_login'))
    except Exception as e:
        print(f"Error al registrar: {e}")
        flash('Hubo un error al registrar el usuario', 'danger')
        return redirect(url_for('auth.mostrar_registro'))


@auth_bp.route('/loginn', methods=['GET'])
def mostrar_login():
    return render_template('auth/loginn.html')

@auth_bp.route('/loginn', methods=['POST'])
def login_usuario():
    email = request.form['email']
    contrasena = request.form['contrasena']

    try:
        connection = current_app.connection
        with connection.cursor() as cursor:
            sql = "SELECT * FROM usuarios WHERE email = %s AND estado = TRUE"
            cursor.execute(sql, (email,))
            usuario = cursor.fetchone()

            if usuario and bcrypt.checkpw(contrasena.encode('utf-8'), usuario['contrasena'].encode('utf-8')):
                session['usuario_id'] = usuario['id_usuario']
                session['usuario_nombre'] = usuario['nombre']
                session['rol'] = usuario['id_rol']
                flash('Bienvenido, {}'.format(usuario['nombre']), 'success')
                return redirect(url_for('main.index')) 
            else:
                flash('Credenciales incorrectas', 'danger')
                return redirect(url_for('auth.mostrar_loginn'))

    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        flash('Error al iniciar sesión', 'danger')
        return redirect(url_for('auth.mostrar_loginn'))


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('auth.mostrar_loginn'))
