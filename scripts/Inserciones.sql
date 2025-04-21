USE bibliooteca;

-- Inserción de roles
INSERT INTO roles (nombre, descripcion) 
VALUES 
('Administrador', 'Control total del sistema');


-- Inserción de ubicaciones
INSERT INTO ubicaciones (nombre, planta, estanteria, seccion) 
VALUES 
('Sección Literatura', 'Planta 1', 'A', '1'),
('Sección Ciencias', 'Planta 1', 'B', '2'),
('Sección Historia', 'Planta 2', 'A', '1'),
('Sección Tecnología', 'Planta 2', 'B', '2'),
('Sección Arte', 'Planta 3', 'A', '1');


-- Inserción de autores
INSERT INTO autores (nombre, apellido)
VALUES 
('Gabriel', 'García Márquez'),
('J.K.', 'Rowling'),
('Stephen', 'King'),
('Isabel', 'Allende'),
('George', 'Orwell'),
('Ernest', 'Hemingway');



-- Inserción de categorías
INSERT INTO categorias (nombre_categoria)
VALUES 
('Novela'),
('Ciencia Ficción'),
('Historia'),
('Ciencia'),
('Informática'),
('Arte'),
('Filosofía'),
('Psicología'),
('Biografía'),
('Poesía'),
('Drama'),
('Terror'),
('Romance'),
('Policíaca'),
('Misterio'),
('Aventura'),
('Fantasía'),
('Autoayuda'),
('Educación'),
('Economía'),
('Religión'),
('Política'),
('Cómics'),
('Ensayo'),
('Viajes'),
('Medicina'),
('Astronomía'),
('Ingeniería'),
('Cocina'),
('Deportes'),
('Música'),
('Ecología'),
('Derecho'),
('Negocios'),
('Fotografía'),
('Marketing'),
('Idiomas'),
('Manualidades'),
('Animales'),
('Anime'),
('Tecnología');







-- Inserción de copias
INSERT INTO copias (id_libro, numero_copia, estado, id_ubicacion, fecha_adquisicion) 
VALUES 
(1, 1, 'Disponible', 1, '2020-01-15'),
(1, 2, 'Disponible', 1, '2020-01-15'),
(2, 1, 'Disponible', 2, '2020-02-20'),
(2, 2, 'Prestado', 2, '2020-02-20'),
(3, 1, 'Disponible', 1, '2020-03-10'),
(4, 1, 'Prestado', 1, '2020-04-05'),
(5, 1, 'Disponible', 3, '2020-05-12'),
(6, 1, 'Reservado', 1, '2020-06-22'),
(7, 1, 'Disponible', 1, '2020-07-18'),
(8, 1, 'Prestado', 2, '2020-08-30'),
(9, 1, 'Disponible', 3, '2021-01-10'),
(10, 1, 'Disponible', 2, '2021-02-15');

INSERT INTO prestamos (id_usuario, id_copia, fecha_prestamo, fecha_devolucion_programada, fecha_devolucion_real, estado)
VALUES
(6, 2, '2023-04-01', '2023-04-16', NULL, 'Activo'),
(7, 4, '2023-04-05', '2023-04-20', NULL, 'Activo'),
(8, 6, '2023-04-10', '2023-04-25', NULL, 'Activo'),
(6, 8, '2023-03-15', '2023-03-30', '2023-03-28', 'Devuelto'),
(7, 10, '2023-03-20', '2023-04-04', NULL, 'Atrasado');



INSERT INTO reservas (id_usuario, id_libro, fecha_reserva, estado, fecha_limite)
VALUES
(6, 3, '2023-04-12', 'Pendiente', '2023-04-19'),
(7, 5, '2023-04-14', 'Pendiente', '2023-04-21'),
(8, 7, '2023-04-16', 'Pendiente', '2023-04-23'),
(6, 9, '2023-04-01', 'Completada', '2023-04-08'),
(7, 1, '2023-04-02', 'Cancelada', '2023-04-09');


-- Inserción de productos
INSERT INTO productos (nombre, descripcion, precio, stock, categoria)
VALUES 
('Lápiz HB', 'Lápiz estándar para escritura', 1.50, 100, 'Papelería'),
('Cuaderno universitario', 'Cuaderno de 100 hojas cuadriculadas', 5.00, 50, 'Papelería'),
('Memoria USB 32GB', 'Dispositivo de almacenamiento portátil', 15.00, 20, 'Electrónica'),
('Marcador de libros', 'Marcador con diseños de literatura clásica', 2.00, 80, 'Accesorios');

INSERT INTO libros (isbn, titulo, id_autor, id_categoria, editorial, fecha_publicacion, resumen, paginas, idioma) 
VALUES 
('9781234567890', 'El viaje al centro de la Tierra', 1, 1, 'Editorial XYZ', '1864-11-25', 'Un viaje de aventuras que lleva a los protagonistas al centro de la Tierra.', 400, 'Español'),
('9782345678901', 'La sombra del viento', 2, 2, 'Editorial ABC', '2001-04-25', 'Un joven encuentra un libro olvidado que cambia su vida.', 500, 'Español'),
('9783456789012', 'Crónica de una muerte anunciada', 3, 1, 'Editorial DEF', '1981-06-06', 'Una novela que narra el asesinato de Santiago Nasar en un pequeño pueblo.', 200, 'Español'),
('9784567890123', 'Don Quijote de la Mancha', 4, 3, 'Editorial GHI', '1605-01-16', 'Las aventuras de un caballero loco y su fiel escudero.', 1100, 'Español'),
('9785678901234', 'El principito', 5, 2, 'Editorial JKL', '1943-04-06', 'La historia de un niño que viaja por diferentes planetas, aprendiendo lecciones de vida.', 120, 'Español');



INSERT INTO usuarios (nombre, apellido, email, contrasena, telefono, direccion, id_rol) 
VALUES 
 ('Carlos', 'Lopez', 'carlos.lopez@example.com', SHA2('carlos123', 256), '3123456789', 'Calle 1 #10-20', 2);
('Ana', 'Pérez', 'ana.perez1@mail.com', SHA2('ana123', 256), '3101234567', 'Calle 15 #20-10', 1),
('Luis', 'Martínez', 'luis.martinez1@mail.com', SHA2('luis456', 256), '3112345678', 'Avenida 30 #40-50', 1),
('Marta', 'Gómez', 'marta.gomez1@mail.com', SHA2('marta789', 256), '3123456789', 'Carrera 12 #60-70', 2),
('Carlos', 'López', 'carlos.lopez1@mail.com', SHA2('carlos321', 256), '3134567890', 'Diagonal 25 #80-90', 2),
('José', 'Ramírez', 'jose.ramirez1@mail.com', SHA2('jose654', 256), '3145678901', 'Transversal 35 #100-110', 3);
