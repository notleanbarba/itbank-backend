--Crear una vista con las columnas id, número de sucursal, nombre, apellido, DNI y edad (calculada a partir de la fecha de nacimiento).
CREATE VIEW vista_clientes_simple AS
SELECT 
    c.numero AS id,
    s.id AS numero_sucursal,
    c.nombre,
    c.apellido,
    c.dni,
    (YEAR(CURRENT_DATE) - YEAR(c.fecha_nacimiento)) AS edad
FROM clientes c
LEFT JOIN sucursales s ON c.direccion = s.id;


--muestra los clientes llamadso Anne y Tyler de mayor a menor
SELECT name, surname, dob FROM customer WHERE name IN ("Anne" , "Tyler") ORDER BY dob ASC
--Ordenar clientes por DNI (de menor a mayor) con edad superior a 40 años.
SELECT 
    id,
    name,
    surname,
    dni,
    dob
FROM 
    customers
WHERE 
    (strftime('%Y', 'now') - strftime('%Y', dob)) - 
    (strftime('%m-%d', 'now') < strftime('%m-%d', dob)) > 40
ORDER BY 
    dni ASC;

--Insertar 5 clientes nuevos en la base usando los datos de un JSON proporcionado y verificar la inserción exitosa.
BEGIN TRANSACTION;

INSERT INTO clientes (nombre, apellido, dni, direccion, fecha_nacimiento, tipo_cliente_id)
VALUES ('Julieta', 'Fernández', 37730452, 'Sucursal 80', '1984-07-07', 1);

INSERT INTO clientes (nombre, apellido, dni, direccion, fecha_nacimiento, tipo_cliente_id)
VALUES ('Luciano', 'Pérez', 40565413, 'Sucursal 45', '1968-04-30', 2);

INSERT INTO clientes (nombre, apellido, dni, direccion, fecha_nacimiento, tipo_cliente_id)
VALUES ('Sofía', 'González', 42625213, 'Sucursal 77', '1993-03-28', 3);

INSERT INTO clientes (nombre, apellido, dni, direccion, fecha_nacimiento, tipo_cliente_id)
VALUES ('Martín', 'García', 31207908, 'Sucursal 96', '1959-08-24', 1);

INSERT INTO clientes (nombre, apellido, dni, direccion, fecha_nacimiento, tipo_cliente_id)
VALUES ('Valentina', 'Rojas', 47063950, 'Sucursal 27', '1976-04-01', 2);

COMMIT;
