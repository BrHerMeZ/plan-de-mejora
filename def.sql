DROP DATABASE IF EXISTS MiAmigoFiel;
CREATE DATABASE MiAmigoFiel;
USE MiAmigoFiel;

DROP TABLE IF EXISTS Rol;

CREATE TABLE Rol (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE
);

# 1--Tabla de usuarios
CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    imagen_perfil VARCHAR(255) default 'static/uploads/default.png',
    nombre VARCHAR(255) COLLATE utf8mb4_unicode_ci NOT NULL,
    apellido VARCHAR(255) COLLATE utf8mb4_unicode_ci NOT NULL,
    tipo_documento varchar(255),
    numero_documento varchar(15),
    correoElectronico VARCHAR(255) COLLATE utf8mb4_unicode_ci NOT NULL,
    numero_celular VARCHAR(255) NOT NULL,
    contrasena VARCHAR(255) COLLATE utf8mb4_unicode_ci NOT NULL,
    id_rol INT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES Rol(id_rol)
);


INSERT INTO Rol (id_rol, nombre) VALUES 
(1, 'Administrador'),
(2, 'Estudiante');

-- 1# Inserciones de los usuarios --
INSERT INTO Usuario(nombre,apellido,tipo_documento,numero_documento,correoElectronico,numero_celular,contrasena,id_rol, imagen_perfil)
VALUES 
('Brayan', 'Herrera', 'C.C', 1099544210, 'sr.mateusstiven@gmail.com','3212000771', '$2b$12$XtbY.vQwHdi90o3KgvO.re/IyJfevrciJjs0cJ9BaNsrDXohjuSm6', '1', '/img/default-profile.jpg');