import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import rison  # noqa: E402

__all__ = ["rison"]
