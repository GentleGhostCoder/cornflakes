def get_command_name(callback):
    """Recursively build the command name from the callback and its parents."""
    if hasattr(callback, "parent") and callback.parent:
        return f"{get_command_name(callback.parent)} {callback.name}"
    elif hasattr(callback, "name"):
        return callback.name
    return ""
