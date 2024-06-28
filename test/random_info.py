# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
import random
import string

from epg.authenticator import Authenticator, AuthMethod
from epg.credential import Credential

BASIC_SET = (
    string.printable.replace("\t", "")
    .replace("\n", "")
    .replace("\r", "")
    .replace("\x0b", "")
    .replace("\x0c", "")
    .replace(" ", "")
)

EPG_SET = BASIC_SET.replace("$", "")


def randstr(
    string_set: str,
    fixed: bool = True,
    min_length: int = 1,
    max_length: int = -1,
) -> str:
    assert min_length > 0
    assert max_length == -1 or (max_length > 0 and min_length < max_length)
    if fixed:
        if max_length == -1:
            return "".join(
                random.choices(string_set, k=random.randint(1, 255))
            )
        return "".join(random.choices(string_set, k=max_length))
    if max_length == -1:
        return "".join(
            random.choices(string_set, k=random.randint(min_length, 255))
        )
    return "".join(
        random.choices(string_set, k=random.randint(min_length, max_length))
    )


def token() -> str:
    return randstr(EPG_SET, fixed=False, max_length=100)


def user_id() -> str:
    return randstr(EPG_SET, fixed=False, max_length=40)


def password() -> str:
    return randstr(EPG_SET, fixed=False, min_length=4, max_length=24)


def ip() -> str:
    return ".".join([f"{random.randint(0, 255)}" for _ in range(4)])


def mac() -> str:
    return ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])


def product_id() -> str:
    return randstr(EPG_SET, fixed=False, max_length=50)


def ctc() -> str:
    return randstr(EPG_SET, fixed=False, max_length=10)


def credential() -> Credential:
    return Credential(
        token(), user_id(), password(), ip(), mac(), product_id(), ctc()
    )


def batch_credential(amount: int) -> list:
    return [credential() for _ in range(amount)]


def authenticator() -> dict[Authenticator, str]:
    method = random.choice(list(AuthMethod))
    _credential = credential()
    if method == AuthMethod.SALTED_MD5:
        salt = f"{random.randint(0,99999999):08d}"
    else:
        salt = None
    _authenticator = Authenticator(_credential, method, salt)
    return {"authenticator": _authenticator, "info": _authenticator.info}


def batch_authenticator(amount: int) -> list[dict[Authenticator, str]]:
    return [authenticator() for _ in range(amount)]


def raw_authenticator() -> dict[str]:
    method = random.choice(list(AuthMethod))
    _credential = credential()
    if method == AuthMethod.SALTED_MD5:
        salt = f"{random.randint(0,99999999):08d}"
    else:
        salt = None
    _authenticator = Authenticator(_credential, method, salt)
    return {
        "credential": dict(_credential),
        "method": method.name,
        "salt": salt,
        "info": _authenticator.info,
    }


def batch_raw_authenticator(amount: int) -> list[dict[Authenticator, str]]:
    return [raw_authenticator() for _ in range(amount)]
