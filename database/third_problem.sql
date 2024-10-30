--Seleccionar las cuentas con saldo negativo

SELECT *
FROM cuenta
WHERE balance < 0

--Seleccionar el nombre, apellido y edad de
--los clientes que tengan en el apellido la letra Z

SELECT 
    customer_name,
    customer_surname,
    (strftime('%Y', 'now') - strftime('%Y', dob)) - 
    (strftime('%m-%d', 'now') < strftime('%m-%d', dob)) AS edad
FROM 
    cliente
WHERE 
    customer_surname LIKE '%Z%';

--Seleccionar el nombre, apellido, edad y nombre de sucursal de las personas cuyo nombre sea “Brendan” y ordenar por nombre de sucursal
SELECT 
    cliente.customer_name,
    cliente.customer_surname,
    (strftime('%Y', 'now') - strftime('%Y', cliente.dob)) - 
    (strftime('%m-%d', 'now') < strftime('%m-%d', cliente.dob)) AS edad,
    sucursal.branch_name AS nombre_sucursal
FROM 
    cliente
JOIN 
    sucursal ON cliente.branch_id = sucursal.branch_id
WHERE 
    cliente.customer_name = 'Brendan'
ORDER BY 
    branch_name;
	
--Seleccionar los préstamos personales y prendarios utilizando la unión de tablas/consultas

SELECT *
FROM prestamo
WHERE loan_type IN ('PERSONAL', 'PRENDARIO');

--Seleccionar los préstamos cuyo importe sea mayor que el importe medio de todos los préstamos
SELECT *
FROM prestamo
WHERE loan_total > (SELECT AVG(loan_total) FROM prestamo);

--Contar la cantidad de clientes menores a 50 años
SELECT COUNT(*) AS cantidad_clientes_menores_50
FROM cliente
WHERE 
    (strftime('%Y', 'now') - strftime('%Y', dob)) - 
    (strftime('%m-%d', 'now') < strftime('%m-%d', dob)) < 50;
	
--Seleccionar las primeras 5 cuentas con saldo mayor a 8,000
SELECT *
FROM cuenta
WHERE balance > 800000  -- 8000.00
ORDER BY balance
LIMIT 5;

--Seleccionar los préstamos que tengan fecha en abril, junio y agosto, ordenándolos por importe
SELECT *
FROM prestamo
WHERE 
    strftime('%m', loan_date) IN ('04', '06', '08')
ORDER BY 
    loan_total;
	
--Obtener el importe total de los préstamos agrupados por tipo de préstamo, renombrando la columna
SELECT 
    loan_type,
    SUM(loan_total) AS loan_total_accu
FROM 
    prestamo
GROUP BY 
    loan_type;