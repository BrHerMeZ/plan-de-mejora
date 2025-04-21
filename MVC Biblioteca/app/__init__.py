# app/__init__.py
from flask import Flask
from config import Config
import pymysql.cursors

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'], 
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )

    # Registrar Blueprints
    from app.controllers.main_controller import main_bp
    from app.controllers.user_controller import user_bp
    from app.controllers.reserva_controller import reserva_bp
    from app.controllers.bibliotecario_controller import bibliotecario_bp
    from app.controllers.admin_controller import admin_bp
    from app.controllers.auth_controller import auth_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(reserva_bp)
    app.register_blueprint(bibliotecario_bp)
    app.register_blueprint(admin_bp)

    # Guardar la conexión como propiedad de la app
    app.connection = connection

    return app
