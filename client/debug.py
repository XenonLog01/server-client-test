import time

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


def debug_time(func):
    def wrapper_time(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        print(f'{INFO_DEBUG}Time: {TEXT_CYAN}' +
              f'{(time.time() - start_time) * 1000}{TEXT_RESET}ms')

    return wrapper_time
