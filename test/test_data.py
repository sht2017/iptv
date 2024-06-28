# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
import json
import random

from config import TEST_DATA
from random_info import batch_raw_authenticator


def batch_generate():
    random.seed(24)  # magic number, don't ask about it
    return json.dumps(
        batch_raw_authenticator(128), ensure_ascii=False, indent=4
    )


def test_data():
    with open(TEST_DATA, "r", encoding="utf-8") as file:
        assert file.read() == batch_generate()
