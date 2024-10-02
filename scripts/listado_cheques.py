#!/usr/bin/env python3.11
"""
Filter a list of checks in csv format to standard output or file.

Command: python listado_cheques.py input_file dni output check_type -s check_state* -d date_range*

* input_file: Indicate the path to input file. (Supported types: csv)
* dni:  Indicate the dni value to file. It has to be a string of 8 digits
* output: Select the output of the script. May be stdout for standard output or file 
          (default: output.csv)
* check_type: Filter by check type. May be "emitido" for issued or "depositado" for deposited checks
* -s check_state: Filter by check state. Options could be "pendiente", "aprobado", "rechazado" 
                  for pending, approved or rejected checks respectively
* -d date_range: Filter checks by date. Range has to be formatted as YYYYMMDDYYYYMMDD where the 
                 first YYYYMMDD group indicates FROM and second group indicates TO

Arguments with * are optionals.

"""

import sys
import os
import datetime
import csv
from time import mktime, time
from tabulate import tabulate


def limpiar_espacios(fila):
    """
    Función para eliminar los espacios en blanco alrededor de los valores en cada fila.
    """
    return [elemento.strip() for elemento in fila]


def validar_cheques_duplicados(cheques):
    """
    Verifica si hay cheques duplicados en el archivo.
    Un cheque es duplicado si tiene el mismo número de cheque y la misma cuenta de origen.
    """
    cheques_unicos = set()
    for cheque in cheques:
        key = (cheque[0], cheque[3])  # (NroCheque, NumeroCuentaOrigen)
        if key in cheques_unicos:
            print(f"Error: Cheque duplicado encontrado con NroCheque {cheque[0]} y cuenta {cheque[3]}")
            sys.exit(1)
        else:
            cheques_unicos.add(key)


def validar_fechas_cheques(cheques):
    """
    Verifica que los valores de FechaPago en los cheques sean válidos (numéricos).
    """
    for cheque in cheques:
        try:
            assert cheque[7].isnumeric(), f"Invalid FechaPago in cheque {cheque[0]}"
        except AssertionError as e:
            print("Error:", e)
            sys.exit(1)


if __name__ == "__main__":
    # Cargar los argumentos de línea de comandos
    cli_args = sys.argv

    try:
        assert len(cli_args) > 4, "Missing arguments. Expected: python listado_cheques.py [dni] [output] [check_type] [input_file]"
    except AssertionError as e:
        print("Error:", e)
        sys.exit(1)

    # Asignar correctamente los argumentos
    file_path = cli_args[1]  # Este debe ser el archivo CSV
    dni = cli_args[2]        # Este debe ser el DNI
    output = cli_args[3]     # Este es la salida (stdout o file)
    check_type = cli_args[4].lower()  # Tipo de cheque
    
    print(f"Intentando abrir el archivo: {file_path}")  # Depuración: Imprime la ruta del archivo

    # Verificar que los argumentos obligatorios son válidos
    possible_outputs = {"stdout", "file"}
    possible_check_types = {"emitido", "depositado"}

    try:
        assert os.path.isfile(file_path), "File does not exist"
        assert len(dni) == 8, "Wrong argument. DNI has to be 8 digits."
        assert dni.isnumeric(), "Wrong argument. DNI has to be numeric."
        assert output in possible_outputs, f"Wrong argument. Output must be {possible_outputs}"
        assert check_type in possible_check_types, f"Wrong argument. Check type must be {possible_check_types}"
    except AssertionError as e:
        print("Error:", e)
        sys.exit(1)

    check_state = None
    date_range = [0, 0]

    # Verificar si se especifica el estado del cheque
    if "-s" in cli_args:
        check_state = cli_args[cli_args.index("-s") + 1]
        possible_check_states = {"pendiente", "aprobado", "rechazado"}
        try:
            assert check_state in possible_check_states, f"Wrong argument. Check state must be {possible_check_states}"
        except AssertionError as e:
            print("Error:", e)
            sys.exit(1)

    # Verificar si se especifica el rango de fechas
    if "-d" in cli_args:
        raw_date_range = cli_args[cli_args.index("-d") + 1]
        try:
            assert len(raw_date_range) == 16, "Wrong argument. Date range has to be 16 digits."
            assert raw_date_range.isnumeric(), "Wrong argument. Date range has to be numeric."
        except AssertionError as e:
            print("Error:", e)
            sys.exit(1)

        date_range = [
            mktime(datetime.datetime.strptime(raw_date_range[0:8], "%Y%m%d").timetuple()),
            mktime(datetime.datetime.strptime(raw_date_range[8:16], "%Y%m%d").timetuple())
        ]

        try:
            assert (-2208973392 <= date_range[0]) & (date_range[1] < time()), "Wrong argument. Date range has to start after 01/01/1900 and end before current time"
        except AssertionError as e:
            print("Error:", e)
            sys.exit(1)

    # Abrir el archivo CSV y cargar los datos
    with open(file_path, "r", encoding="utf-8") as input_file:
        data = csv.reader(input_file, delimiter=",", skipinitialspace=True)
        header = limpiar_espacios(next(data))  # Limpiar los espacios en el encabezado

        # Validar cheques duplicados y fechas de los cheques
        cheques = [limpiar_espacios(fila) for fila in data]  # Limpiar espacios en las filas
        validar_cheques_duplicados(cheques)
        validar_fechas_cheques(cheques)

        # Filtrar los cheques por DNI, tipo, estado y rango de fechas
        filtered_data = list(
            filter(
                lambda x: ((x[8] == dni) & (x[10].lower() == check_type))
                & ((check_state is None) | (x[9].lower() == check_state))
                & (
                    (date_range == [0, 0])
                    | (date_range[0] <= int(x[7]) <= date_range[1])
                ),
                cheques,
            )
        )

        # Si el resultado se guarda en archivo
        if output == "file":
            timestamp_actual = int(time())
            nombre_archivo = f"{dni}_{timestamp_actual}.csv"
            with open(nombre_archivo, "w", encoding="utf-8") as output_file:
                output_csv = csv.writer(output_file, delimiter=",")
                output_csv.writerow(header)
                output_csv.writerows(filtered_data)
                print(f"Success: Output saved to {nombre_archivo}")
                sys.exit(0)

        # Si no hay resultados
        if len(filtered_data) == 0:
            print("No results")
            sys.exit(0)

        # Mostrar los resultados en pantalla
        print("Results:")
        print(tabulate([header] + filtered_data))
        sys.exit(0)
