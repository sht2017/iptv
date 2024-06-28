# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from test_data import batch_generate

with open("test_data.json", "w", encoding="utf-8") as file:
    file.write(batch_generate())
