class UnquotedString(str):
    """String Wrapper with overwritten repr Function to not quote."""

    def __repr__(self):
        """String Wrapper with overwritten repr Function to not quote."""
        return self


def unquoted_string(x: str):
    """Create Instance of :meth:`cornflakes.common.UnquotedString`."""
    return UnquotedString(x)
