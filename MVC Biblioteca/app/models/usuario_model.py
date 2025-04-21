from app import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id_rol'))
    fecha_registro = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    estado = db.Column(db.Boolean, default=True)

    rol = db.relationship('Rol', backref='usuarios') 
