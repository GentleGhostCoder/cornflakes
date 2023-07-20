class _StringMethodConcatenation:
    def __init__(self, callback1, callback2=None, *args, **kwargs):
        if not callable(callback1) or not self._is_valid_callback(callback1):
            raise TypeError("callback1 must be a callable that takes one string argument and returns a string")
        if callback2 is not None and (not callable(callback2) or not self._is_valid_callback(callback2)):
            raise TypeError("callback2 must be a callable that takes one string argument and returns a string")
        self.callback1 = callback1
        self.callback2 = callback2
        self.args = args
        self.kwargs = kwargs

    def __call__(self, string):
        result = self.callback1(string, *self.args, **self.kwargs)
        if self.callback2 is not None:
            result += self.callback2(string)
        return result

    def with_args(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return self

    def __rshift__(self, other):
        if not isinstance(other, _StringMethodConcatenation):
            raise TypeError(">> operator must be used with another StringMethodConcatenator")
        return _StringMethodConcatenation(other, self.__call__)

    def __lshift__(self, other):
        if not isinstance(other, _StringMethodConcatenation):
            raise TypeError("<< operator must be used with another StringMethodConcatenator")
        return _StringMethodConcatenation(self.__call__, other)

    @staticmethod
    def _is_valid_callback(callback):
        try:
            result = callback("")
            return isinstance(result, str)
        except TypeError:
            return False


def string_builder(callback=None, *args, **kwargs):
    def wrapper(c):
        return _StringMethodConcatenation(c, *args, **kwargs)

    return wrapper(callback) if callback else wrapper
