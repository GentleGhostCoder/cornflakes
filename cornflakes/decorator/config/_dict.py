def to_dict(self) -> dict:
    """Method to convert Dataclass with slots to dict."""
    return {key: getattr(self, key) for key in self.__slots__}
