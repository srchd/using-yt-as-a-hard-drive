import logging
import functools
from datetime import datetime

now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
log_filename = f'logs/{now}.log'
logging.basicConfig(format='Date-Time : %(asctime)s : Line No. : %(lineno)d - %(message)s', filename=log_filename, level=logging.INFO)
logger = logging.getLogger()

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception(f'Exception raised in {func.__name__}. Exception: {str(e)}')
            raise e
        
    return wrapper
