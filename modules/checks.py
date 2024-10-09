"""
Module to handle checks

Available functions:
    - filter_checks: Receives an array of checks and filter by dni and check_type or optionally by check_state or date_range
"""

import datetime
from time import mktime, time

CHECK_TYPES = {"emitido", "depositado"}
CHECK_STATES = {"pendiente", "aprobado", "rechazado"}

(
    CHECK_NUMBER,
    BANK_CODE,
    BRANCH_CODE,
    SOURCE_ACCOUNT_NUMBER,
    DESTINATION_ACCOUNT_NUMBER,
    AMOUNT,
    ORIGIN_DATE,
    PAYMENT_DATE,
    DNI,
    STATE,
    CHECK_TYPE,
) = range(11)


def filter_checks(checks, dni, check_type, check_state=None, date_range=None):
    """
    Filter a list of checks with structure by DNI, check type, and optionally by check state or date_range.

    Parameters:
        checks: an orderly list of list of [CHECK_NUMBER, BANK_CODE, BRANCH_CODE, SOURCE_ACCOUNT_NUMBER, DESTINATION_ACCOUNT_NUMBER, AMOUNT, ORIGIN_DATE, PAYMENT_DATE, DNI, STATE, CHECK_TYPE]
        dni: an 8 digit number representing an Argentine DNI
        check_type: the type of check ("emitido", "depositado")
        check_state: the state of the check ("pendiente", "aprobado", "rechazado")
        date_range: a date range to use as filter. 16 digits formatted as YYYYMMDDYYYYMMDD, first YYYYMMDD group for "since", second group for "until"
    """

    assert len(dni) == 8, "Wrong argument. DNI has to be 8 digits."
    assert dni.isnumeric(), "Wrong argument. DNI has to be numeric."
    assert (
        check_type in CHECK_TYPES
    ), f"Wrong argument. Check type must be {CHECK_TYPES}"
    assert (
        len(date_range) == 16 if date_range is not None else True
    ), "Wrong argument. Date range has to be 16 digits."
    assert (
        date_range.isnumeric() if date_range is not None else True
    ), "Wrong argument. Date range has to be numeric."

    if check_state is not None:
        assert (
            check_state in CHECK_STATES
        ), f"Wrong argument. Check state must be {CHECK_STATES}"

    if date_range is not None:
        date_range = [
            mktime(datetime.datetime.strptime(date_range[0:8], "%Y%m%d").timetuple()),
            mktime(datetime.datetime.strptime(date_range[8:16], "%Y%m%d").timetuple()),
        ]
        assert (-2208973392 <= int(date_range[0])) & (
            int(date_range[1])
            < time()
            # pylint: disable-next=line-too-long
        ), "Wrong argument. Date range has to start after 01/01/1900 and end before current time"

    unique_checks = set()
    filtered_checks = []
    for check in checks:
        key = (
            check[CHECK_NUMBER],
            check[SOURCE_ACCOUNT_NUMBER],
        )  # (NroCheque, NumeroCuentaOrigen)
        assert (
            key not in unique_checks
        ), f"Error: Cheque duplicado encontrado con NroCheque {check[CHECK_NUMBER]} y cuenta {check[SOURCE_ACCOUNT_NUMBER]}"
        unique_checks.add(key)

        assert check[PAYMENT_DATE].isnumeric(), "Error: check date is non numeric"

        if (
            ((check[DNI] == dni) & (check[CHECK_TYPE].lower() == check_type))
            & (
                (check[STATE].lower() == check_state)
                if check_state is not None
                else True
            )
            & (
                (date_range[0] <= int(check[PAYMENT_DATE]) <= date_range[1])
                if date_range is not None
                else True
            )
        ):
            filtered_checks.append(check)

    # Filter DNI, type, state and date
    return filtered_checks
