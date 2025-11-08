from src.utils.logger import setup_central_logger

logger = setup_central_logger()

# logger.info("Hello, world!")
# logger.debug("This is a debug message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")
# logger.critical("This is a critical message")


from src.utils.exception import MyException
import sys
try:
    val = 1 + 'a'
except Exception as e:
    logger.info(e)
    raise MyException(e, sys) from e