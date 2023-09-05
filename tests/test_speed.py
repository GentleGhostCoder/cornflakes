from dataclasses import asdict
import os
from time import perf_counter
import unittest

from pydantic import BaseModel, RootModel
from pydantic.dataclasses import dataclass as pd_dataclass
from pydantic_settings import BaseSettings, SettingsConfigDict
import pytest
from typeguard import suppress_type_checks

import cornflakes
from cornflakes.decorator.dataclasses import config, dataclass


class TestSpeed(unittest.TestCase):
    """Tests for eval_datetime."""

    # this speed measurement is very inaccurate and
    # only for a custom indicator whether it is faster or slower when changing something

    @pytest.mark.skipif(os.environ.get("NOX_RUNNING", "False"))
    def test_ini_load_speed(self):
        s = perf_counter()
        for _ in range(1000):
            cornflakes.ini_load("tests/configs/default.ini")
        self.assertTrue(0.2 > (perf_counter() - s))

    @pytest.mark.skipif(os.environ.get("NOX_RUNNING", "False"))
    def test_eval_csv_speed(self):
        s = perf_counter()
        with open("tests/smallwikipedia.csv", "rb") as f:
            data = f.read(10000)
            for _ in range(1000):
                cornflakes.eval_csv(data)
        self.assertTrue(0.2 > (perf_counter() - s))

    @pytest.mark.skipif(os.environ.get("NOX_RUNNING", "False"))
    def test_compare_custom_dataclass_with_padantic(self):
        """Test that compare custom dataclass with padantic."""

        @dataclass
        class CustomCornflakesDataclass:
            name: str
            age: int

        @config(files="tests/configs/name_age")
        class CustomCornflakesConfig:
            name: str
            age: int

        @pd_dataclass
        class PydanticDataclass:
            name: str
            age: int

        class PydanticBaseModel(BaseModel):
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
            CustomCornflakesConfig()
        custom_config = perf_counter() - s

        s = perf_counter()
        for _ in range(10000):
            PydanticBaseModel(name="test", age=1)
        pydantic_dataclass = perf_counter() - s

        s = perf_counter()
        for _ in range(10000):
            PydanticBaseModel(name="test", age=1)
        pydantic_base_model = perf_counter() - s

        s = perf_counter()
        for _ in range(1000):
            PydanticConfig()
        pydantic_config = perf_counter() - s

        self.assertTrue(custom < pydantic_dataclass)
        self.assertTrue(custom < pydantic_base_model)
        self.assertTrue(custom_config < pydantic_config)

        def dict_passing(**kwargs):
            pass

        s = perf_counter()
        custom = CustomCornflakesDataclass(name="test", age=1)
        for _ in range(10000):
            dict_passing(**asdict(custom))
        dc_builtin_as_dict = perf_counter() - s

        # compare pydantic-dict method with to_dict
        s = perf_counter()
        for _ in range(10000):
            dict_passing(**custom)
        custom_to_dict = perf_counter() - s

        s = perf_counter()
        custom_config = CustomCornflakesConfig()
        for _ in range(10000):
            dict_passing(**custom_config)
        custom_config_to_dict = perf_counter() - s

        s = perf_counter()
        pydantic_dataclass = RootModel[PydanticDataclass](PydanticDataclass(name="test", age=1))
        for _ in range(10000):
            dict_passing(**pydantic_dataclass.model_dump())
        pydantic_dataclass_to_dict = perf_counter() - s

        s = perf_counter()
        pydantic_base_model = PydanticBaseModel(name="test", age=1)
        for _ in range(10000):
            dict_passing(**pydantic_base_model.model_dump())
        pydantic_base_model_to_dict = perf_counter() - s

        # print(custom_to_dict)
        # print(custom_config_to_dict)
        # print(dc_builtin_as_dict)
        # print(pydantic_dataclass_to_dict)
        # print(pydantic_base_model_to_dict)

        # builtin is slower
        self.assertTrue(custom_to_dict < dc_builtin_as_dict)

        self.assertTrue(
            custom_to_dict * 0.5 < pydantic_dataclass_to_dict
        )  # pydantic model_dump is faster, so check only how much faster ... can be optimized maybe
        self.assertTrue(custom_config_to_dict * 0.5 < pydantic_dataclass_to_dict)
        self.assertTrue(
            custom_to_dict * 0.4 < pydantic_base_model_to_dict
        )  # pydantic model_dump is faster, so check only how much faster ... can be optimized maybe
        self.assertTrue(custom_config_to_dict * 0.4 < pydantic_base_model_to_dict)
