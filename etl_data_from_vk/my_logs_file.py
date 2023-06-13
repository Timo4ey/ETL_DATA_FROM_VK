import functools
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def print_elapsed_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_timestamp = time.time()
        print('LOG: Running job "%s"' % func.__name__)
        result = func(*args, **kwargs)
        print(
            'LOG: Job "%s" completed in %d seconds'
            % (func.__name__, time.time() - start_timestamp)
        )
        return result

    return wrapper


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logger.info(result)
            return result
        except Exception as e:
            logger.exception(
                f"Exception raised in {func.__name__}\
                             .exception: {str(e)}"
            )
            raise e

    return wrapper
