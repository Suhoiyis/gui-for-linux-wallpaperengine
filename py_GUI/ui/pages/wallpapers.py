import warnings

warnings.warn(
    "Importing from py_GUI.ui.pages.wallpapers is deprecated. "
    "Use py_GUI.ui.pages.library instead.",
    DeprecationWarning,
    stacklevel=2,
)
from py_GUI.ui.pages.library import *
