USE bibliooteca;


-- 1. Actualizar el estado de un préstamo de activo o devuelto 
UPDATE prestamos
SET estado = 'Devuelto', 
    fecha_devolucion_real = CURDATE()
WHERE id_prestamo = 1;

-- 2. consulta para actualizar la informacion de un libro
UPDATE libros
SET editorial = 'Editorial Actualizada',
    paginas = 450,
    resumen = 'Resumen actualizado del libro con nuevos detalles.'
WHERE id_libro = 3;

-- 3. Cambiar la categoría de un libro
UPDATE libros
SET id_categoria = 2
WHERE id_libro = 5;

-- 4. Actualizar la ubicación de una copia
UPDATE copias
SET id_ubicacion = 3,
    estado = 'Disponible'
WHERE id_copia = 6;

-- 5. Actualizar información de contacto de un usuario
UPDATE usuarios
SET email = 'nuevo.email@estudiante.edu',
    telefono = '555999888',
    direccion = 'Nueva dirección 123'
WHERE id_usuario = 4;

-- =================== 5 ELIMINACIONES ===================

-- 1. Eliminar una reserva cancelada
DELETE FROM reservas
WHERE estado = 'Cancelada' AND id_reserva = 5;

-- 2. Eliminar un producto sin stock
DELETE FROM productos
WHERE stock = 0 AND id_producto = 3;

-- 3. Eliminar un préstamo antiguo ya devuelto
-- Primero creamos un préstamo antiguo para poder eliminarlo
INSERT INTO prestamos (id_usuario, id_copia, fecha_prestamo, fecha_devolucion_programada, fecha_devolucion_real, estado)
VALUES (3, 1, '2022-01-15', '2022-01-30', '2022-01-28', 'Devuelto');

-- Ahora lo eliminamos
DELETE FROM prestamos
WHERE fecha_prestamo < '2022-12-31' 
AND estado = 'Devuelto'
AND id_prestamo = LAST_INSERT_ID();

-- 4. Eliminar una copia de libro en mal estado
-- Primero aseguramos que no haya préstamos o reservas asociadas
-- Creamos una copia en mal estado
INSERT INTO copias (id_libro, numero_copia, estado, id_ubicacion, fecha_adquisicion)
VALUES (1, 3, 'En reparación', 1, '2019-01-15');

-- Ahora eliminamos la copia
DELETE FROM copias
WHERE estado = 'En reparación'
AND id_copia = LAST_INSERT_ID();

-- 5. Eliminar un autor sin libros asociados
-- Primero añadimos un autor para poder eliminarlo
INSERT INTO autores (nombre, apellido, nacionalidad, fecha_nacimiento, biografia)
VALUES ('Autor', 'Temporal', 'Desconocida', '1980-01-01', 'Autor creado temporalmente para demostración');

-- Ahora eliminamos el autor
DELETE FROM autores
WHERE id_autor = LAST_INSERT_ID()
AND id_autor NOT IN (SELECT DISTINCT id_autor FROM libros WHERE id_autor IS NOT NULL);