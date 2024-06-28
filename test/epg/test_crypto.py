# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, redefined-outer-name

import pytest

# pylint: disable=import-error, no-name-in-module
from Crypto.Cipher._mode_ecb import EcbMode

# pylint: enable=import-error, no-name-in-module
from epg.crypto import cipher, decrypt, encrypt


@pytest.fixture
def test_data():
    return {
        "key_8": "thisis8k",
        "key_24": "thisisthe24byteslongkey!",
        "utf8_data": "Hello, World!",
        "utf16_data": "Привет, мир!",
    }


def test_invalid_key_length(test_data):
    assert isinstance(cipher(test_data["key_8"]), EcbMode)
    assert isinstance(cipher(test_data["key_24"]), EcbMode)

    with pytest.raises(ValueError) as excinfo:
        cipher("")
    assert (
        "Key must be either 8 or 24 bytes for DES or 3DES encryption"
        in str(excinfo.value)
    )

    with pytest.raises(ValueError) as excinfo:
        cipher(test_data["key_8"][1])
    assert (
        "Key must be either 8 or 24 bytes for DES or 3DES encryption"
        in str(excinfo.value)
    )

    with pytest.raises(ValueError) as excinfo:
        cipher(test_data["key_8"][:-1])
    assert (
        "Key must be either 8 or 24 bytes for DES or 3DES encryption"
        in str(excinfo.value)
    )

    with pytest.raises(ValueError) as excinfo:
        cipher(test_data["key_8"] + "x")
    assert (
        "Key must be either 8 or 24 bytes for DES or 3DES encryption"
        in str(excinfo.value)
    )

    with pytest.raises(ValueError) as excinfo:
        cipher(test_data["key_24"][:-1])
    assert (
        "Key must be either 8 or 24 bytes for DES or 3DES encryption"
        in str(excinfo.value)
    )

    with pytest.raises(ValueError) as excinfo:
        cipher(test_data["key_24"] + "y")
    assert (
        "Key must be either 8 or 24 bytes for DES or 3DES encryption"
        in str(excinfo.value)
    )


def test_encrypt_decrypt(test_data):
    encrypted_data_utf8_key_8 = encrypt(
        test_data["utf8_data"], test_data["key_8"]
    )
    decrypted_data_utf8_key_8 = decrypt(
        encrypted_data_utf8_key_8, test_data["key_8"]
    )
    assert (
        decrypted_data_utf8_key_8 == test_data["utf8_data"]
    ), "DES decryption did not return the original data on utf-8"

    encrypted_data_utf16_key_8 = encrypt(
        test_data["utf16_data"], test_data["key_8"], encoding="utf-16"
    )
    decrypted_data_utf16_key_8 = decrypt(
        encrypted_data_utf16_key_8, test_data["key_8"], encoding="utf-16"
    )
    assert (
        decrypted_data_utf16_key_8 == test_data["utf16_data"]
    ), "DES decryption did not return the original data on utf-16"

    encrypted_data_utf8_key_24 = encrypt(
        test_data["utf8_data"], test_data["key_24"]
    )
    decrypted_data_utf8_key_24 = decrypt(
        encrypted_data_utf8_key_24, test_data["key_24"]
    )
    assert (
        decrypted_data_utf8_key_24 == test_data["utf8_data"]
    ), "3DES decryption did not return the original data on utf-8"

    encrypted_data_utf16_key_24 = encrypt(
        test_data["utf16_data"], test_data["key_24"], encoding="utf-16"
    )
    decrypted_data_utf16_key_24 = decrypt(
        encrypted_data_utf16_key_24, test_data["key_24"], encoding="utf-16"
    )
    assert (
        decrypted_data_utf16_key_24 == test_data["utf16_data"]
    ), "3DES decryption did not return the original data on utf-16"
