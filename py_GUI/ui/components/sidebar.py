import warnings

warnings.warn(
    "Importing from py_GUI.ui.components.sidebar is deprecated. "
    "Use py_GUI.ui.components.library.sidebar instead.",
    DeprecationWarning,
    stacklevel=2,
)
from py_GUI.ui.components.library.sidebar import *
