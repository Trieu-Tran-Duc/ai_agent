import logging
import sys

def setup_logging(level=None):
    logging.basicConfig(
        level=level or logging.INFO,
        format="%(asctime)s | %(levelname)-5s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
