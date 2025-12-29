import logging
import time
from functools import wraps

class Logger:
    """
    Centralized logger for AIWork.
    """
    def __init__(self, name="AIWork"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def warning(self, msg):
        self.logger.warning(msg)

logger = Logger()

def monitor(func):
    """
    Decorator to monitor function execution time and errors.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start
            logger.info(f"Function '{func.__name__}' executed in {duration:.4f}s")
            return result
        except Exception as e:
            logger.error(f"Function '{func.__name__}' failed: {e}")
            raise e
    return wrapper
