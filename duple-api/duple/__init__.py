import logging
import sys
import os

logging.basicConfig(
    level=logging.getLevelName(os.getenv("LOG_LEVEL") or "DEBUG"),
    format="[%(asctime)s] [%(levelname)s]  %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger()
