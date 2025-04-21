DROP DATABASE IF EXISTS bibliooteca;
CREATE DATABASE bibliooteca;
USE bibliooteca;




CREATE TABLE autores (
    id_autor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL
);


CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(50) NOT NULL
);



CREATE TABLE ubicaciones (
    id_ubicacion INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    planta VARCHAR(20),
    estanteria VARCHAR(20),
    seccion VARCHAR(20)
);

CREATE TABLE roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT
);


CREATE TABLE usuarios (
	id_usuario INT AUTO_INCREMENT PRIMARY KEY,
	nombre VARCHAR(100) NOT NULL,
	apellido VARCHAR(100) NOT NULL,
	email VARCHAR(100) UNIQUE NOT NULL,
	contrasena VARCHAR(255) NOT NULL,
	telefono VARCHAR(20),
	direccion VARCHAR(200),
	id_rol INT,
	fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	estado BOOLEAN DEFAULT TRUE,
	FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
    );

CREATE TABLE libros (
    id_libro INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    id_autor INT,
    id_categoria INT,
    editorial VARCHAR(100),
    fecha_publicacion DATE,
    resumen TEXT,
    paginas INT,
    idioma VARCHAR(50),
    FOREIGN KEY (id_autor) REFERENCES autores(id_autor),
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);




CREATE TABLE copias (
    id_copia INT AUTO_INCREMENT PRIMARY KEY,
    id_libro INT,
    numero_copia INT NOT NULL,
    estado ENUM('Disponible', 'Prestado', 'Reservado', 'En reparación', 'Extraviado') DEFAULT 'Disponible',
    id_ubicacion INT,
    fecha_adquisicion DATE,
    FOREIGN KEY (id_libro) REFERENCES libros(id_libro),
    FOREIGN KEY (id_ubicacion) REFERENCES ubicaciones(id_ubicacion)
);

select * from prestamos;
CREATE TABLE prestamos (
    id_prestamo INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    id_copia INT,
    fecha_prestamo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_devolucion_programada DATE,
    fecha_devolucion_real DATE,
    estado ENUM('Activo', 'Devuelto', 'Atrasado') DEFAULT 'Activo',
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_copia) REFERENCES copias(id_copia)
);


CREATE TABLE reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    id_libro INT,
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('Pendiente', 'Completada', 'Cancelada') DEFAULT 'Pendiente',
    fecha_limite DATE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_libro) REFERENCES libros(id_libro)
);


CREATE TABLE reportes (
    id_reporte INT AUTO_INCREMENT PRIMARY KEY,
    tipo_reporte VARCHAR(255),
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    datos TEXT
);



CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2),
    stock INT DEFAULT 0,
    categoria ENUM('Papelería', 'Accesorios', 'Electrónica', 'Otros') DEFAULT 'Otros'
);