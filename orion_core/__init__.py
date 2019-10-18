# __init__.py

import sys
import os
from orion_core.application import *
from orion_core.frontend import *
from orion_core.commands import *
from orion_core.shared import *

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logger = logging.getLogger(__name__)

if sys.version_info < (3, 7, 2):
    logger.error("Python version must be 3.7.2 or higher")
    sys.exit(1)




