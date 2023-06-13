import os
from json import loads
from pathlib import Path

import pytest

from etl_data_from_vk.data_executor import DataExecuter


def get_test_data(filename: str) -> list[dict]:
    with open(os.path.join(Path(__file__).parent, filename), "r") as f:
        return loads(f.read())


test_data = get_test_data("test_data_executor/raw_data.json")


@pytest.fixture
def executor():
    return DataExecuter(test_data)


@pytest.fixture
def executor_for_convert():
    return DataExecuter(test_data[:2])


# print(test_data)
