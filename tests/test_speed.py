import os
from time import perf_counter
import unittest

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
import pytest

import cornflakes


class TestSpeed(unittest.TestCase):
    """Tests for eval_datetime."""

    @pytest.mark.skipif(os.environ.get("NOX_RUNNING", "False"))
    def test_ini_load_speed(self):
        s = perf_counter()
        for _ in range(1000):
            cornflakes.ini_load("tests/configs/default.ini")
        self.assertTrue(0.11 > (perf_counter() - s))

    @pytest.mark.skipif(os.environ.get("NOX_RUNNING", "False"))
    def test_eval_csv_speed(self):
        s = perf_counter()
        with open("tests/smallwikipedia.csv", "rb") as f:
            data = f.read(10000)
            for _ in range(1000):
                cornflakes.eval_csv(data)
        self.assertTrue(0.15 > (perf_counter() - s))

    @pytest.mark.skipif(os.environ.get("NOX_RUNNING", "False"))
    def test_compare_custom_dataclass_with_padantic(self):
        """Test that compare custom dataclass with padantic."""

        @cornflakes.dataclass
        class CustomCornflakesDataclass:
            name: str
            age: int

        @cornflakes.config
        class CustomCornflakesConfig:
            name: str
            age: int

        class PydanticDataclass(BaseModel):
            name: str
            age: int

        class PydanticConfig(BaseSettings):  # type: ignore
            name: str
            age: int

            model_config = SettingsConfigDict(env_file="tests/configs/name_age", env_prefix="")

        s = perf_counter()
        for _ in range(10000):
            CustomCornflakesDataclass(name="test", age=1)
        custom = perf_counter() - s

        s = perf_counter()
        for _ in range(1000):
            CustomCornflakesConfig.from_ini("tests/configs/name_age")
        custom_config = perf_counter() - s

        s = perf_counter()
        for _ in range(10000):
            PydanticDataclass(name="test", age=1)
        pydantic = perf_counter() - s

        s = perf_counter()
        for _ in range(1000):
            PydanticConfig()
        pydantic_config = perf_counter() - s

        self.assertTrue(custom < pydantic)
        self.assertTrue(custom_config < pydantic_config)

        # compare pydantic-dict method with to_dict
        s = perf_counter()
        for _ in range(10000):
            CustomCornflakesDataclass(name="test", age=1).to_dict()
        custom_to_dict = perf_counter() - s

        s = perf_counter()
        for _ in range(10000):
            CustomCornflakesConfig(name="test", age=1).to_dict()
        custom_config_to_dict = perf_counter() - s

        s = perf_counter()
        for _ in range(10000):
            PydanticDataclass(name="test", age=1).model_dump()
        pydantic_to_dict = perf_counter() - s

        self.assertTrue(
            custom_to_dict * 0.7 < pydantic_to_dict
        )  # pydantic model_dump is faster, so check only how much faster (<30%) .. can be optimized
        self.assertTrue(custom_config_to_dict * 0.7 < pydantic_to_dict)
