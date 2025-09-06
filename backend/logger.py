# logger.py
from loguru import logger
import os
from pathlib import Path

# create logs directory if it doesn't exist
log_dir = Path("./logs")
log_dir.mkdir(exist_ok=True)

logger.remove()
# console logger
logger.add(
    sink=lambda msg: print(msg, end=""),  # Print to terminal
    format="[{time:HH:mm}] {level} | {message}",
    colorize=True,
)
# file logging
logger.add(
    sink=log_dir / "app.log",
    format="[{time:YYYY-MM-DD HH:mm:ss}] {level} | {message}",
    rotation="1 day",  # rotate daily
    retention=None,
)
