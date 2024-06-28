# -*- coding: utf-8 -*-
"""DES and 3DES encryption and decryption.

This module provides functions for encrypting and decrypting data using DES or
3DES encryption algorithms. It uses ECB mode for these operations. Users can
specify the encryption key and optionally the encoding type for converting
plaintext to bytes and vice versa.

Example:
    To encrypt and decrypt data, you can use the following code snippet:

        key = 'thisis8k'
        data = 'Hello, World!'
        encrypted_data = encrypt(data, key)
        decrypted_data = decrypt(encrypted_data, key)

Attributes:
    None

Todo:
    * Consider adding support for other modes of encryption.
    * Add error handling for incorrect data formats or encoding issues.

"""

# pylint: disable=import-error, no-name-in-module
from Crypto.Cipher import DES, DES3
from Crypto.Cipher._mode_ecb import EcbMode
from Crypto.Util.Padding import pad, unpad

# pylint: enable=import-error, no-name-in-module


def cipher(key: str) -> EcbMode:
    """
    Creates and returns a cipher object in ECB mode using either DES or 3DES
    encryption based on the length of the provided key.

    Args:
        key (str): The encryption key used for securing the data. It must be
            either 8 or 24 bytes long.

    Raises:
        ValueError: If the key length is not 8 or 24 bytes, this error
        indicates that the key does not meet the requirements for DES or 3DES
        encryption.

    Returns:
        EcbMode: The cipher object initialized in ECB mode. This will be either
        a DES or 3DES cipher depending on the key length.
    """
    match len(key):
        case 8:
            return DES.new(key[:8].encode(), DES.MODE_ECB)  # Create DES cipher
        case 24:
            return DES3.new(key.encode(), DES3.MODE_ECB)  # Create 3DES cipher
        case _:
            raise ValueError(
                "Key must be either 8 or 24 bytes for DES or 3DES encryption"
            )


def encrypt(data: str, key: str, encoding: str = "utf-8") -> str:
    """
    Encrypts the given data using DES or 3DES encryption based on the length of
    the key.
    Using DES if key length is 8 bytes; using 3DES if key length is 24 bytes.

    Args:
        data (str): The plaintext data to be encrypted.
        key (str): The encryption key used.
        encoding (str | None, optional): The character encoding used to decode
            the decrypted bytes back into a string. This should match the
            encoding used when the data was originally encoded into bytes
            before encryption. If `None` is provided, the decrypted bytes will
            be returned as a raw byte string. Defaults to 'utf-8'.

    Raises:
        ValueError: If the key length is not 8 or 24 bytes, this error
        indicates that the key does not meet the requirements for DES or 3DES
        encryption.

    Returns:
        str: The encrypted data represented as a hexadecimal string.
    """
    padded_data = pad(
        data.encode(encoding), DES.block_size
    )  # Pad data to be a multiple of 8 bytes
    encrypted_data = cipher(key).encrypt(padded_data)  # Encrypt data
    return encrypted_data.hex()


def decrypt(data: str, key: str, encoding: str = "utf-8") -> str:
    """
    Decrypts the given data using DES or 3DES encryption based on the length of
    the key.

    Args:
        data (str): The data to be decrypted, represented as a hexadecimal
            string.
        key (str): The decryption key used.
        encoding (str | None, optional): The character encoding used to decode
            the decrypted bytes back into a string. This should match the
            encoding used when the data was originally encoded into bytes
            before encryption. If `None` is provided, the decrypted bytes will
            be returned as a raw byte string. Defaults to 'utf-8'.

    Raises:
        ValueError: If the key length is not 8 or 24 bytes, this error
        indicates that the key does not meet the requirements for DES or 3DES
        encryption.

    Returns:
        str: The decrypted data as a plaintext string.
    """
    padded_data = cipher(key).decrypt(
        bytes.fromhex(data)  # Convert encrypted data and key to bytes
    )  # Decrypt data
    decrypted_data = unpad(padded_data, DES.block_size)  # Unpad data
    return decrypted_data.decode(encoding)
