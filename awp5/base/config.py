# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
Default Config Settings used for creating new Connection Objects.
The default is a localhost connection to the default port 8000/9001.
Username and Password will most like need to be set.
"""
import sys

p5_user = 'Administrator'
p5_pass = 'password'
p5_ip = '127.0.0.1'
"""The Ip Address to the P5 Server / Client to connect to"""
p5_port_nr = 8000
"""
The Port-Number as in config/lexxsrv.xxxx. The value will be incrementet by
1001 for the CLI access
"""
p5_path = r'C:\Program Files\ARCHIWARE\Data_Lifecycle_Management_Suite'
"""The Filepath to the Archiware P5 Installation Directory."""
if sys.platform == 'win32':
    p5_path = r'C:\Program Files\ARCHIWARE\Data_Lifecycle_Management_Suite'
elif sys.platform == 'darwin' or sys.platform.startswith('linux'):
    p5_path = r'/usr/local/aw'
