from loguru import logger
import sys

project_logger = logger
logger.configure(handlers=[{"sink": sys.stderr, "level": "INFO"}])
project_logger.add(
    "file{time}.log", rotation="1 week", retention=5, format="{time} {level} {module} {name} {message}", level="DEBUG", )
