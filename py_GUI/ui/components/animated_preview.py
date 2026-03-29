import warnings

warnings.warn(
    "Importing from py_GUI.ui.components.animated_preview is deprecated. "
    "Use py_GUI.ui.components.common.animated_preview instead.",
    DeprecationWarning,
    stacklevel=2,
)
from py_GUI.ui.components.common.animated_preview import *
