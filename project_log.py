from loguru import logger
import sys
import os

project_logger = logger
logger.configure(handlers=[{"sink": sys.stderr, "level": "INFO"}])

if not os.path.isdir('logs'):
   os.mkdir('logs')

project_logger.add(
    "logs/file{time}.log", rotation="1 week", retention=5, format="{time} {level} {module} {name} {message}", level="DEBUG", )
