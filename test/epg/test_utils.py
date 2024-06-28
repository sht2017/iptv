# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
import json
import random

import pytest
import random_info
from config import TEST_DATA
from epg.authenticator import Authenticator, AuthMethod
from epg.credential import Credential
from epg.utils import EvaluateTools, reverse


def test_reverse():
    with pytest.raises(TypeError) as excinfo:
        reverse("", "", AuthMethod.SALTED_MD5)
    assert "missing required positional argument: 'salt'" in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        reverse("", "", -1)
    assert "Invalid auth method" in str(excinfo.value)
    with open(TEST_DATA, "r", encoding="utf-8") as file:
        for authenticator_set in json.loads(file.read()):
            _credential = authenticator_set["credential"]
            credential = Credential(
                _credential["token"],
                _credential["user_id"],
                _credential["password"],
                _credential["ip"],
                _credential["mac"],
                _credential["product_id"],
                _credential["ctc"],
            )
            print(AuthMethod[authenticator_set["method"]])
            print(authenticator_set["salt"])
            assert Credential.dumps(
                reverse(
                    _credential["password"],
                    authenticator_set["info"],
                    AuthMethod[authenticator_set["method"]],
                    authenticator_set["salt"],
                )
            ) == Credential.dumps(credential)


def test_EvaluateTools():
    credential = random_info.credential()
    salt = f"{random.randint(1,9999):05d}"
    assert salt in EvaluateTools().test_salt(
        credential,
        Authenticator(credential, AuthMethod.SALTED_MD5, salt).info,
        5,
    )
