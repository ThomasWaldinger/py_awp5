# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

import logging
from .base.connection import Connection

__all__ = ["base", "api"]
cli_version="5.6.3"
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('awp5_cli.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
screenformater = logging.Formatter('%(levelname)s - %(message)s')
ch.setFormatter(screenformater)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)
