# -*- coding: utf-8 -*-

PRE_LOAD = """
import sys
from os import sep
DIR_ = '' # to be speficied
DIRDIR = sep.join((DIR_,"app","data_utils"))
if DIRDIR not in sys.path:
    sys.path.append(DIRDIR)
"""

CONSTANTS = """
ABS_DIR =
ERROR_DIR = "error.txt"
ABS_DIR_FUTOPT =
"""

steps = """
execfile('scan.py')

init_print()
connect_db()
main_daily()
check_daily()
main_daily_futopt()
check_daily(True)

update_ins()
check_dates_preliminary()

cleanup()
"""
