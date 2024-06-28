# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from config import TEST_DATA
from test_data import batch_generate

with open(TEST_DATA, "w", encoding="utf-8") as file:
    file.write(batch_generate())
