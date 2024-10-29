--muestra los clientes llamadso Anne y Tyler de mayor a menor
SELECT customer_name, customer_surname, dob FROM cliente WHERE customer_name IN ("Anne" , "Tyler") ORDER BY dob ASC
--Ordenar clientes por DNI (de menor a mayor) con edad superior a 40 años.
SELECT 
    customer_id,
    customer_name,
    customer_surname,
    customer_DNI,
    dob
FROM 
    cliente
WHERE 
    (strftime('%Y', 'now') - strftime('%Y', dob)) - 
    (strftime('%m-%d', 'now') < strftime('%m-%d', dob)) > 40
ORDER BY 
    customer_DNI ASC;
