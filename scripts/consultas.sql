USE bibliooteca;

-- joins

-- join de libros con sus autores y categorías
SELECT l.id_libro, l.titulo, l.isbn, 
       CONCAT(a.nombre, ' ', a.apellido) AS autor, 
       c.nombre_categoria AS categoria
FROM libros l
JOIN autores a ON l.id_autor = a.id_autor  -- Corregí el alias de 'id'
JOIN categorias c ON l.id_categoria = c.id_categoria
ORDER BY l.titulo;


-- join de préstamos activos con información de libro y estudiante
SELECT p.id_prestamo, p.fecha_prestamo, p.fecha_devolucion_programada,
       l.titulo, l.isbn,
       CONCAT(u.nombre, ' ', u.apellido) AS estudiante,
       u.email
FROM prestamos p
JOIN copias c ON p.id_copia = c.id_copia
JOIN libros l ON c.id_libro = l.id_libro
JOIN usuarios u ON p.id_usuario = u.id_usuario
WHERE p.estado = 'Activo'
ORDER BY p.fecha_devolucion_programada;

-- join de libros más prestados con información de categoría
SELECT l.id_libro, l.titulo, c.nombre_categoria AS categoria,
       COUNT(p.id_prestamo) AS cantidad_prestamos
FROM libros l
JOIN copias co ON l.id_libro = co.id_libro
JOIN prestamos p ON co.id_copia = p.id_copia
JOIN categorias c ON l.id_categoria = c.id_categoria
GROUP BY l.id_libro, l.titulo, c.nombre_categoria
ORDER BY cantidad_prestamos DESC;

-- reservas pendientes con información de libro y usuario
SELECT r.id_reserva, r.fecha_reserva, r.fecha_limite,
       l.titulo, l.isbn,
       CONCAT(u.nombre, ' ', u.apellido) AS usuario,
       u.email
FROM reservas r
JOIN libros l ON r.id_libro = l.id_libro
JOIN usuarios u ON r.id_usuario = u.id_usuario
WHERE r.estado = 'Pendiente'
ORDER BY r.fecha_limite;

-- libros con copias disponibls y su ubicación
SELECT l.id_libro, l.titulo, l.isbn,
       COUNT(c.id_copia) AS copias_disponibles,
       u.nombre AS ubicacion, u.planta, u.estanteria, u.seccion
FROM libros l
JOIN copias c ON l.id_libro = c.id_libro
JOIN ubicaciones u ON c.id_ubicacion = u.id_ubicacion
WHERE c.estado = 'Disponible'
GROUP BY l.id_libro, l.titulo, l.isbn, u.nombre, u.planta, u.estanteria, u.seccion
ORDER BY l.titulo;

-- apartado de consyultas sencillas 

-- libros publicados después de 2020
SELECT id_libro, titulo, isbn, editorial, fecha_publicacion
FROM libros
WHERE YEAR(fecha_publicacion) > 2020
ORDER BY fecha_publicacion;

-- Usuarios con más de 3 préstamos atrasados
SELECT u.id_usuario, CONCAT(u.nombre, ' ', u.apellido) AS usuario, 
       u.email, COUNT(p.id_prestamo) AS prestamos_atrasados
FROM usuarios u
JOIN prestamos p ON u.id_usuario = p.id_usuario
WHERE p.estado = 'Atrasado'
GROUP BY u.id_usuario, u.nombre, u.apellido, u.email
HAVING COUNT(p.id_prestamo) > 3
ORDER BY prestamos_atrasados DESC;

--  Autores con más libros en el sistema
SELECT a.id_autor, CONCAT(a.nombre, ' ', a.apellido) AS autor, 
       COUNT(l.id_libro) AS cantidad_libros
FROM autores a
LEFT JOIN libros l ON a.id_autor = l.id_autor
GROUP BY a.id_autor, a.nombre, a.apellido
ORDER BY cantidad_libros DESC
LIMIT 0, 10000;


--  Préstamos que vencerán en los próximos 3 días
SELECT p.id_prestamo, p.fecha_prestamo, p.fecha_devolucion_programada,
       l.titulo, CONCAT(u.nombre, ' ', u.apellido) AS usuario, u.email
FROM prestamos p
JOIN copias c ON p.id_copia = c.id_copia
JOIN libros l ON c.id_libro = l.id_libro
JOIN usuarios u ON p.id_usuario = u.id_usuario
WHERE p.estado = 'Activo' 
AND p.fecha_devolucion_programada BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 3 DAY)
ORDER BY p.fecha_devolucion_programada;

--  Libros nunca prestados
SELECT l.id_libro, l.titulo, l.isbn, 
       CONCAT(a.nombre, ' ', a.apellido) AS autor
FROM libros l
JOIN autores a ON l.id_autor = a.id_autor
LEFT JOIN copias c ON l.id_libro = c.id_libro
LEFT JOIN prestamos p ON c.id_copia = p.id_copia
WHERE p.id_prestamo IS NULL
ORDER BY l.titulo;

-- apartadp de subconsultas

--  Libros con más préstamos que el promedio
SELECT l.id_libro, l.titulo, COUNT(p.id_prestamo) AS num_prestamos
FROM libros l
JOIN copias c ON l.id_libro = c.id_libro
JOIN prestamos p ON c.id_copia = p.id_copia
GROUP BY l.id_libro, l.titulo
HAVING COUNT(p.id_prestamo) > (
    SELECT AVG(prestamos_por_libro)
    FROM (
        SELECT COUNT(p.id_prestamo) AS prestamos_por_libro
        FROM libros l
        JOIN copias c ON l.id_libro = c.id_libro
        JOIN prestamos p ON c.id_copia = p.id_copia
        GROUP BY l.id_libro
    ) AS subconsulta
)
ORDER BY num_prestamos DESC;

--  Usuarios que nunca han reservado un libro
SELECT u.id_usuario, CONCAT(u.nombre, ' ', u.apellido) AS usuario, u.email
FROM usuarios u
WHERE u.id_usuario NOT IN (
    SELECT DISTINCT id_usuario
    FROM reservas
)
ORDER BY usuario;

--  Libros disponibles que están actualmente reservados
SELECT DISTINCT l.id_libro, l.titulo, l.isbn
FROM libros l
JOIN copias c ON l.id_libro = c.id_libro
JOIN reservas r ON l.id_libro = r.id_libro
WHERE c.estado = 'Disponible'
AND r.estado = 'Pendiente'
AND l.id_libro IN (
    SELECT id_libro
    FROM copias
    WHERE estado = 'Disponible'
)
ORDER BY l.titulo;

-- Categorías con menos libros que la media
SELECT c.id_categoria, c.nombre_categoria, COUNT(l.id_libro) AS cantidad_libros
FROM categorias c
LEFT JOIN libros l ON c.id_categoria = l.id_categoria
GROUP BY c.id_categoria, c.nombre_categoria
HAVING COUNT(l.id_libro) < (
    SELECT AVG(libros_por_categoria)
    FROM (
        SELECT COUNT(id_libro) AS libros_por_categoria
        FROM libros
        GROUP BY id_categoria
    ) AS subconsulta
)
ORDER BY cantidad_libros;

--  Préstamos de usuarios con morosidad previa
SELECT p.id_prestamo, p.fecha_prestamo, p.fecha_devolucion_programada,
       l.titulo, CONCAT(u.nombre, ' ', u.apellido) AS usuario
FROM prestamos p
JOIN copias c ON p.id_copia = c.id_copia
JOIN libros l ON c.id_libro = l.id_libro
JOIN usuarios u ON p.id_usuario = u.id_usuario
WHERE p.id_usuario IN (
    SELECT DISTINCT id_usuario
    FROM prestamos
    WHERE estado = 'Atrasado'
)
AND p.estado = 'Activo'
ORDER BY p.fecha_devolucion_programada;
