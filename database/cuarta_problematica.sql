--Listar la cantidad de clientes por nombre de sucursal ordenando de mayor a menor.
SELECT 
    s.branch_name,
    COUNT(c.customer_id) AS customer_count 
FROM 
	sucursal s 
JOIN 
	cliente c on s.branch_id = c.branch_id 
GROUP BY 
	s.branch_name 
ORDER BY 
	customer_count DESC
	
--Obtener la cantidad de empleados por cliente por sucursal en un número real.
SELECT 
    s.branch_name, 
    CAST(COUNT(e.employee_id) AS REAL) / COUNT(DISTINCT c.customer_id) AS employee_per_customer
FROM 
    sucursal s
LEFT JOIN 
    empleado e ON s.branch_id = e.branch_id  -- Join employees to branches
LEFT JOIN 
    cliente c ON s.branch_id = c.branch_id  -- Optional, if you want to see customer info as well
GROUP BY 
    s.branch_id
	
-- crear tabla movimientos
CREATE TABLE movimientos (
	movement_id INTEGER PRIMARY KEY AUTOINCREMENT, 
	description TEXT NOT NULL,
	acc_number TEXT UNIQUE NOT NULL,
	ammount REAL NOT NULL,
	op_type TEXT NOT NULL,
	hour TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);
	
--prueba de insert a movimientos	
INSERT INTO movimientos (description, acc_number, ammount, op_type, hour) 
VALUES ("Deposit into savings account", "123456789", "500.00", "deposit", "2024-10-29 10:30:00");

--Restar $100 a las cuentas 10, 11, 12, 13, y 14.
SELECT 
    account_id, 
    balance - 100 AS updated_balance
FROM
    cuenta
WHERE 
    account_id IN (10, 11, 12, 13, 14);
	
--resta 100 a las cuentas y las actualiza con la plata restada
UPDATE 
	cuenta
SET 
	balance = balance + 100
WHERE account_id IN (10, 11, 12, 13, 14);

--Crear la tabla “auditoria_cuenta” para guardar los datos de movimientos
CREATE TABLE auditoria_cuenta (
    old_id INTEGER,
    new_id INTEGER,
    old_balance INTEGER,
    new_balance INTEGER,
    old_iban TEXT,
    new_iban TEXT,
    old_type TEXT,
    new_type TEXT,
    user_action TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Borrar el trigger
DROP TRIGGER IF EXISTS update_cuenta;

--Crear un trigger que, después de actualizar en la tabla "cuentas" los campos balance, IBAN o tipo de cuenta, registre en la tabla "auditoria_cuenta".
CREATE TRIGGER update_cuenta
AFTER UPDATE OF balance, iban, type ON cuenta
BEGIN
    INSERT INTO auditoria_cuenta (
        old_id,
        new_id,
        old_balance,
        new_balance,
        old_iban,
        new_iban,
        --old_type,
        --new_type,
        user_action,
        created_at
    )
    VALUES (
        old.account_id,
        new.account_id,
        old.balance,
        new.balance,
        old.iban,
        new.iban,
        --old.type,
        --new.type,
        'UPDATE',
        CURRENT_TIMESTAMP
    );
END;

--Mejorar la performance de la búsqueda de clientes por DNI mediante índices.
CREATE INDEX idx_customer_dni ON cliente (customer_DNI);

--test
SELECT * FROM cliente WHERE customer_DNI = '74701370';

