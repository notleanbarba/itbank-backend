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
