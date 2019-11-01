import functools
import logging
import os
from protomate.settings import RUNTIME_ENVIRONMENT


def create_logger(log_path="logs/logs.log"):
    """Create a logger object with custom handlers. One handler
    sends data to console and another one sends data to logfile.
    Parameters
    ----------
    log_path : str
    Returns
    -------
    logger: logging.Logger
    """

    # create log folder if it doesn't exist
    if os.path.exists(log_path.split('/')[0]):
        with open(log_path, 'a'):
            pass
    else:
        os.mkdir(log_path.split("/")[0])
        with open(log_path, 'a'):
            pass

    # create a custom logger
    logger = logging.getLogger(__name__)
    if RUNTIME_ENVIRONMENT == "production":
        logger.disabled = True
    else:
        logger.disabled = False

    # create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_path)

    # set handler level
    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)

    # create formatters
    console_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    file_format = logging.Formatter(
        "\n%(asctime)s - %(name)s - %(levelname)s - %(message)s \n"
    )

    # add formatters to handlers
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# calling the logger
logger = create_logger()


# logfunc
def logfunc(_func=None, *, logger=logger):
    """A decorator that wraps the passed in function and logs
    exceptions should one occur
    Returns
    -------
    Any
        Output of the inner function 'func'
    Raises
    ------
    Exception of the inner function 'func'
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                value = func(*args, **kwargs)
                return value
            except Exception:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)

        return wrapper

    # this ensures that logfunc can be used with or without args
    if _func is None:
        return decorator
    else:
        return decorator(_func)
