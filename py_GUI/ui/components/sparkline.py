import warnings

warnings.warn(
    "Importing from py_GUI.ui.components.sparkline is deprecated. "
    "Use py_GUI.ui.components.performance.sparkline instead.",
    DeprecationWarning,
    stacklevel=2,
)
from py_GUI.ui.components.performance.sparkline import *
