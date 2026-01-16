"""
MediaManager UI - Qt6 Interface for MediaManager.
"""

import sys
from pathlib import Path

# Add this directory to sys.path for clean imports
_module_root = Path(__file__).parent.resolve()
if str(_module_root) not in sys.path:
    sys.path.insert(0, str(_module_root))

__version__ = "0.1.0"

# Optional exports
try:
    from backend import MockBackend
    from backend.interface import IMediaManagerBackend

    __all__ = ['MockBackend', 'IMediaManagerBackend']
except ImportError:
    __all__ = []