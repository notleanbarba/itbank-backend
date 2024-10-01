#!/usr/bin/env python3.11
"""
Filter a list of checks in csv format to standard output or file.

Command: python input_file dni output check_type -s check_state* -d date_range* listado_cheques.py 

* input_file: Indicate the path to input file. (Supported types: csv)
* dni:  Indicate the dni value to file. It has to be a string of 8 digits
* output:   Select the output of the script. May be stdout for standard output or file \\
        (default: output.csv)
* check_type:   Filter by check type. May be "emitido" for issued or "depositado" for deposited \\
        checks
* -s check_state:  Filter by check state. Options could be "pendiente", "aprobado", "rechazado" \\
        for pending, approved or rejected checks respectively
* -d date_range:   Filter checks by date. Range has to be formatted as YYYYMMDDYYYYMMDD where the \\
        first YYYYMMDD group indicates FROM and second group indicates TO

Arguments with * are optionals.

"""

import sys
import os
import datetime
import csv
from time import mktime, time
from tabulate import tabulate

if __name__ == "__main__":
    cli_args = sys.argv

    try:
        assert (
            len(cli_args)
            > 4
            # pylint: disable-next=line-too-long
        ), "Missing arguments. Expected: python listado_cheques.py [dni] [output] [check_type] [input_file]"
    except AssertionError as e:
        print("Error:", e)
        sys.exit(1)

    file_path = cli_args[-1]

    dni = cli_args[1]
    file_path = cli_args[-1]

    output = cli_args[2]
    possible_outputs = {"stdout", "file"}

    check_type = cli_args[3].lower()
    possible_check_types = {"emitido", "depositado"}

    try:
        assert os.path.isfile(file_path), "File does not exists"
        assert len(dni) == 8, "Wrong argument. DNI has to be 8 digits."
        assert dni.isnumeric(), "Wrong argument. DNI has to be numeric."
        assert (
            output in possible_outputs
        ), f"Wrong argument. Output must be {possible_outputs}"
        assert (
            check_type in possible_check_types
        ), f"Wrong argument. Check type must be {possible_check_types}"
    except AssertionError as e:
        print("Error:", e)
        sys.exit(1)

    # pylint: disable-next=invalid-name
    check_state = None
    date_range = [0, 0]

    if "-s" in cli_args:
        check_state = cli_args[cli_args.index("-s") + 1]
        possible_check_states = {"pendiente", "aprobado", "rechazado"}
        try:
            assert (
                check_state in possible_check_states
            ), f"Wrong argument. Check state must be {possible_check_states}"
        except AssertionError as e:
            print("Error:", e)
            sys.exit(1)

    if "-d" in cli_args:
        raw_date_range = cli_args[cli_args.index("-d") + 1]
        try:
            assert (
                len(raw_date_range) == 16
            ), "Wrong argument. Date range has to be 16 digits."
            assert (
                raw_date_range.isnumeric()
            ), "Wrong argument. Date range has to be numeric."
        except AssertionError as e:
            print("Error:", e)
            sys.exit(1)

        date_range = [
            mktime(
                datetime.datetime.strptime(raw_date_range[0:8], "%Y%m%d").timetuple()
            ),
            mktime(
                datetime.datetime.strptime(raw_date_range[8:16], "%Y%m%d").timetuple()
            ),
        ]
        try:
            assert (-2208973392 <= date_range[0]) & (
                date_range[1] < time()
            ), "Wrong argument. Date range has to start after 01/01/1900 and end before current time"
        except AssertionError as e:
            print("Error:", e)
            sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as input_file:
        data = csv.reader(input_file, delimiter=",", skipinitialspace=True)
        header = list(next(data))

        filtered_data = list(
            filter(
                lambda x: ((x[8] == dni) & (x[10].lower() == check_type))
                & ((check_state is None) | (x[9] == check_state))
                & (
                    (date_range == [0, 0])
                    | (date_range[0] <= int(x[7]) <= date_range[1])
                ),
                data,
            )
        )

        if output == "file":
            with open("output.csv", "w", encoding="utf-8") as output_file:
                output = csv.writer(output_file, delimiter=",")
                output.writerow(header)
                output.writerows(filtered_data)
                print("Success: Output saved to output.csv")
                sys.exit(0)

        if len(filtered_data) == 0:
            print("No results")
            sys.exit(0)

        print("Results:")
        print(tabulate([header] + filtered_data))
        sys.exit(0)
