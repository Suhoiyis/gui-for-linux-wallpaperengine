import warnings

warnings.warn(
    "Importing from py_GUI.ui.components.command_palette is deprecated. "
    "Use py_GUI.ui.components.common.command_palette instead.",
    DeprecationWarning,
    stacklevel=2,
)
from py_GUI.ui.components.common.command_palette import *
