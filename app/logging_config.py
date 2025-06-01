import logging
import sys

def setup_logging(level=logging.DEBUG):
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout
    )
