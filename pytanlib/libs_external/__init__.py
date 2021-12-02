"""Adds this path to the PYTHONPATH so normal import usage can occur for external packages."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
# import platform
import sys
# import warnings

THIS_FILE = __file__
"""This file, ala ``/path/to/pkg/libs_external/__init__.py``"""

THIS_PATH = os.path.abspath(os.path.dirname(THIS_FILE))
"""The path from this file, ala ``/path/to/pkg/libs_external``"""

# NON PLATFORM SPECIFIC EXTERNAL LIBRARIES
ANY_DIR = "any"
"""Non-platform specific directory for this system."""

ANY_PATH = os.path.join(THIS_PATH, ANY_DIR)
"""The non-platform specific library path, ala ``/path/to/pkg/libs_external/any``"""

'''# PLATFORM SPECIFIC EXTERNAL LIBRARIES
PLATFORM_MAP = {
    "darwin": "osx",
    "windows": "win",
    "linux": "linux",
}
"""Mapping of platform.system().lower() to platform specific library directories."""

THIS_PLATFORM = platform.system().lower()
"""Platform for this system."""

PLATFORM_DIR = PLATFORM_MAP.get(THIS_PLATFORM, "")
"""Platform specific directory for this system."""

PLATFORM_PATH = os.path.join(THIS_PATH, PLATFORM_DIR)
"""The platform specific library path, ala ``/path/to/pkg/libs_external/osx``"""

if not PLATFORM_DIR:
    w = "No platform specific binary packages provided in this tool for platform {}"
    w = w.format(THIS_PLATFORM)
    warnings.warn(w)
'''

PATHS = [
    ANY_PATH,
    # PLATFORM_PATH,
]


def add_path(p, first=True):
    """Add a path to beginning or end of sys.path."""
    if p not in sys.path:
        if first:
            sys.path.insert(0, p)
        else:
            sys.path.append(p)


def add_paths():
    """Add all paths in PATHS to sys.path."""
    for p in PATHS:
        add_path(p, True)


add_paths()
