##############################################################################
# (c) Crown copyright Met Office. All rights reserved.
# For further details please refer to the file COPYRIGHT
# which you should have received as part of this distribution
##############################################################################
"""
Build steps for pulling source code from remote repos and local folders.

"""
import logging
import os
from pathlib import Path
from typing import Union

from fab.tools import run_command


logger = logging.getLogger(__name__)
