"""Bootstrap code to import libs_external."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

THIS_FILE = __file__
"""This file, ala ``/path/to/pkg/libs_external/__init__.py``"""

THIS_PATH = os.path.abspath(os.path.dirname(THIS_FILE))
"""The path from this file, ala ``/path/to/pkg/libs_external``"""

PATHS = [
    THIS_PATH,
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

try:
    import libs_external  # noqa
except Exception:
    raise
