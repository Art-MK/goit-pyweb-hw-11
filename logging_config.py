import logging
import os
from colorlog import ColoredFormatter
import logging

os.makedirs('./logs', exist_ok=True)

# formatter with colors for console output
console_formatter = ColoredFormatter(
    "[%(log_color)s%(levelname)s%(reset)s] %(asctime)s \"%(log_color)s%(message)s%(reset)s\"",
    datefmt='%Y-%m-%d %H:%M:%S',
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

# formatter for file output
file_formatter = logging.Formatter(
    "[%(levelname)s] %(asctime)s \"%(message)s\"",
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Configure logging
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(console_formatter)

file_handler = logging.FileHandler("./logs/app.log")
file_handler.setFormatter(file_formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, stream_handler]
)
