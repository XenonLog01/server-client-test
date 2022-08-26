"""
util.py

Author: Xenon

A file with a bunch of useful helper functions and variables.

Constants:
 - TEXT_{COLOR} : Various variables to format text with color.
 - INFO_{TAG} : Information callouts to draw attention to data.
 - INFO_{TAG}_nCL : Information callouts, without the color.

Decorators:
 - debug_time : Prints how long the attached function took.
 - debug_time_no_col : debug_time, but colorless to be Windows-friendly.

Functions:
 -

"""

import time

# NOTE: text coloring does NOT work in Windows terminals.
# However, it *will* work in jetbrains terminals, for whatever reason,
# despite not working in powershell normally.
TEXT_RESET   = '\033[0m'
TEXT_BLACK   = '\033[0;30m'
TEXT_RED     = '\033[0;31m'
TEXT_GREEN   = '\033[0;32m'
TEXT_YELLOW  = '\033[0;33m'
TEXT_BLUE    = '\033[0;34m'
TEXT_MAGENTA = '\033[0;35m'
TEXT_CYAN    = '\033[0;36m'
TEXT_L_GREY  = '\033[0;37m'

INFO_NOTE    = f'{TEXT_L_GREY}[NOTE]{TEXT_RESET}'
INFO_ERROR   = f'{TEXT_RED}[ERR] {TEXT_RESET}'
INFO_INFO    = f'{TEXT_L_GREY}[INFO]{TEXT_RESET}'
INFO_EXECUTE = f'{TEXT_CYAN}[EXEC]{TEXT_RESET}'
INFO_INPUT   = f'{TEXT_CYAN}[INPT]{TEXT_RESET}'
INFO_DEBUG   = f'{TEXT_CYAN}[DBG] {TEXT_RESET}'
INFO_CMD     = f'{TEXT_CYAN}[CMD] {TEXT_RESET}'
INFO_RESULT  = f'{TEXT_CYAN}[RES] {TEXT_RESET}'
INFO_OUTPUT  = f'{TEXT_CYAN}[OUT] {TEXT_RESET}'

# Colorless variants of the info tags.
INFO_NOTE_nCL    = f'[NOTE]'
INFO_ERROR_nCL   = f'[ERR] '
INFO_INFO_nCL    = f'[INFO]'
INFO_EXECUTE_nCL = f'[EXEC]'
INFO_INPUT_nCL   = f'[INPT]'
INFO_DEBUG_nCL   = f'[DBG] '
INFO_CMD_nCL     = f'[CMD] '
INFO_RESULT_nCL  = f'[RES] '
INFO_OUTPUT_nCL  = f'[OUT] '

def debug_time(func):
    """A Decorator function which simply executes
    the function, and then reports how long it took to execute.
    """
    def wrapper_time(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        print(f'{INFO_DEBUG}Time: {TEXT_CYAN}' +
              f'{(time.time() - start_time) * 1000}{TEXT_RESET}ms')

    return wrapper_time

def debug_time_no_col(func):
    """A Decorator function which simply executes
    the function, and then reports how long it took to execute.
    Unlike debug_time, however, this excludes the colors, so
    as to be Windows-friendly.
    """
    def wrapper_time_nop_col(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        print(f'{INFO_DEBUG_nCL}Time:' +
              f'{(time.time() - start_time) * 1000}ms')

    return wrapper_time_nop_col
