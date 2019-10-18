
import threading
import logging
from . import backend
from orion_core.frontend.base_frontend import frontend_run

logger = logging.getLogger(__name__)


def init():
    logger.info("initializing backend . . .")
    base_backend = threading.Thread(target=backend.test, daemon=True)
    base_backend.start()

    logger.info("initializing frontend . . .")
    pass


def run():
    logger.info("starting frontend run level . . .")
    frontend_run()


