from uuid import UUID

from cornflakes.decorator.dataclass import dataclass as data
from cornflakes.decorator.datalite.datalite_decorator import datalite


def test_datalite():
    """Test datalite decorator."""

    @datalite(db_path="test_datalite.db", type_overload={bytes: "BLOB", UUID: "BLOB"})
    @data(
        dict_factory=None,
        tuple_factory=None,
        slots=False,  # TODO: add obj_id to slots if using db_path
        eval_env=True,
        validate=True,
        updatable=True,
    )
    class TestDataLite:
        string_value: str = "blub"
        integer_value: int = 0
        float_value: float = 0.0
        bytes_value: bytes = b"blub"
        uuid_value: UUID = UUID("00000000-0000-0000-0000-000000000000")

    test = TestDataLite("blub1", 1, 1.0, b"blub1")
    test.create_entry()


"""
TODO:
- add obj_id to slots
- check that no field of __dataclass_fields__ overrides the annotation type or dataclass type

"""
