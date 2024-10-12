#!/usr/bin/env python3
"""
CLI for itbank backend
"""
import sys
import os

argv = sys.argv

sys.path.append(os.getcwd())

match argv[1]:
    case "checks":
        match argv[2]:
            case "filter":
                import csv
                from time import time
                from tabulate import tabulate
                from itbank.checks import filter_checks

                OUTPUT_TYPES = {"stdout", "file"}
                if argv[3] in ["help", "-h"]:
                    print(
                        """
                                Filter a list of checks in csv format to standard output or file.

                                Command: itbank checks filter dni output check_type -s check_state* -d date_range* input_file

                                * input_file: Indicate the path to input file. (Supported types: csv)
                                * dni:  Indicate the dni value to file. It has to be a string of 8 digits
                                * output: Select the output of the script. May be stdout for standard output or file
                                          (default: output.csv)
                                * check_type: Filter by check type. May be "emitido" for issued or "depositado" for deposited checks
                                * -s check_state: Filter by check state. Options could be "pendiente", "aprobado", "rechazado"
                                                  for pending, approved or rejected checks respectively
                                * -d date_range: Filter checks by date. Range has to be formatted as YYYYMMDDYYYYMMDD where the
                                                 first YYYYMMDD group indicates FROM and second group indicates TO

                                Arguments with * are optionals."""
                    )
                try:
                    assert (
                        len(argv)
                        > 4
                        # pylint: disable-next=line-too-long
                    ), "Missing arguments. Expected: python listado_cheques.py [dni] [output] [check_type] [input_file]"

                    file_path = argv[-1]
                    dni = argv[3]
                    output = argv[4]
                    check_type = argv[5].lower()

                    # Verify that output argument is valid
                    assert (
                        output in OUTPUT_TYPES
                    ), f"Wrong argument. Output must be {OUTPUT_TYPES}"
                except AssertionError as e:
                    print("Error:", e)
                    sys.exit(1)

                # pylint: disable-next=invalid-name
                check_state = None
                # pylint: disable-next=invalid-name
                date_range = None

                # Verify if state is specified
                if "-s" in argv:
                    check_state = argv[argv.index("-s") + 1]

                # Verify if date is specified
                if "-d" in argv:
                    date_range = argv[argv.index("-d") + 1]

                # Open CSV and load data
                with open(file_path, "r", encoding="utf-8") as input_file:
                    checks = csv.reader(
                        input_file, delimiter=",", skipinitialspace=True
                    )
                    header = next(checks)

                    try:
                        # Filter DNI, type, state and date
                        filtered_data = filter_checks(
                            checks,
                            dni,
                            check_type,
                            check_state=check_state,
                            date_range=date_range,
                        )

                        # If it is not data
                        if len(filtered_data) == 0:
                            print("No results")
                            sys.exit(0)

                        # If result is saved to file
                        if output == "file":
                            FILE_NAME = f"{dni}_{int(time())}.csv"
                            with open(FILE_NAME, "w", encoding="utf-8") as output_file:
                                output_csv = csv.writer(output_file, delimiter=",")
                                output_csv.writerow(header)
                                output_csv.writerows(filtered_data)
                                print(f"Success: Output saved to {FILE_NAME}")
                                sys.exit(0)

                        # Show results
                        print("Results:")
                        print(tabulate([header] + filtered_data))
                        sys.exit(0)

                    except AssertionError as e:
                        print(e)
