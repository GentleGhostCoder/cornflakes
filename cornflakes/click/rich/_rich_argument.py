from click import Argument


class RichArg(Argument):
    """A custom argument implementation of click.

    Argument class in order to provide a short help message for each argument of a command.
    """

    def __init__(self, *args, **kwargs):
        """Init Method for Rich Argument Class."""
        self.help = kwargs.pop("help", None)
        super().__init__(*args, **kwargs)
