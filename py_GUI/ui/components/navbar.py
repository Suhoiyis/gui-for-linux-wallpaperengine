import warnings

warnings.warn(
    "Importing from py_GUI.ui.components.navbar is deprecated. "
    "Use py_GUI.ui.components.layout.navbar instead.",
    DeprecationWarning,
    stacklevel=2,
)
from py_GUI.ui.components.layout.navbar import *
