import functools
from loguru import logger
from timeit import default_timer as timer
import sys
from pprint import pprint

sys.traceback = -10


def logfunc(func):
    @functools.wraps(func)
    def wrapper_logfunc(*args, **kwargs):
        try:
            value = func(*args, **kwargs)
        except Exception as e:
            logger.remove()
            logger.add(
                sys.stdout,
                colorize=True,
                format="<green>{time: YYYY-MM-DD at HH:mm:ss}</green> <level>{message}</level>",
            )
            logger.add("logs/logfile.log", rotation="500 MB")
            logger.exception(e)
            sys.exit()
        return value

    return wrapper_logfunc


def timefunc(func):
    @functools.wraps(func)
    def wrapper_timefunc(*args, **kwargs):
        start_time = timer()
        value = func(*args, **kwargs)
        end_time = timer()
        run_time = end_time - start_time
        print(f"Function {func.__name__} took {run_time} seconds to execute")
        return value

    return wrapper_timefunc
