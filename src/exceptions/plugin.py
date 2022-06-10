class InvalidPluginError(Exception):
    """Raised when a plugin is invalid (i.e. plugin main file does
    not contain a class whose name matches the plugin title)."""
