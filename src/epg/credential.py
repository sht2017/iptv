# -*- coding: utf-8 -*-
"""Credential Management and Serialization.

This module is designed for handling, validating, and processing credentials in
a secure and efficient manner. It utilizes the `dataclass` decorator to ensure
immutability and integrity of credential instances. Functions for serialization
and deserialization are provided to enable the secure transfer and storage of
credential data.

Example:
    To create, serialize, and deserialize a Credential object, you can use the
    following code snippet:

        # Create a Credential object
        credential = Credential(
            token='encryptedToken123',
            user_id='yourusernamehere',
            password='thisispassword',
            ip='192.168.1.1',
            mac='00:1A:2B:3C:4D:5E',
            product_id='product123'
        )

        # Serialize the Credential object
        serialized_credential = Credential.dumps(credential)

        # Deserialize the string back to a Credential object
        deserialized_credential = Credential.loads(
            'pass123', serialized_credential
        )

Attributes:
    None

Todo:
    None
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Credential:
    """
    Represents authentication details, used for both serialization and
    deserialization of user credentials with strict validation rules regarding
    the content and format of the credentials' data.

    This class uses the `dataclass` decorator for attribute management and
    ensures that each attribute does not exceed predefined maximum lengths,
    does not contain illegal characters, and is not missing. It also handles
    the serialization and deserialization of credentials into a structured
    format.

    Attributes:
        token (str): Encrypted token that uniquely identifies the session
            or user.
        user_id (str): User identification string.
        password (str): User's password, not directly stored.
        ip (str): IP address associated with the credential.
        mac (str): MAC address associated with the device.
        product_id (str): Product identifier.
        ctc (str): Defaulted to "CTC", used for internal checks.
        hash (str): Generated field based on `token`.

    Note:
        The `hash` attribute is generated through hashing during
            post-initialization and does not need to be passed during object
            creation.
    """

    # constants
    _MAX_LENGTHS = {
        "token": 100,
        "user_id": 40,
        "password": 24,
        "ip": 39,
        "mac": 17,
        "product_id": 50,
    }

    # properties
    token: str
    user_id: str
    password: str
    ip: str
    mac: str
    product_id: str
    ctc: str = "CTC"
    hash: str = field(init=False)

    def __post_init__(self):
        """
        Validates the initialization of credential properties, ensuring no
        required fields are missing, no lengths are exceeded, and no illegal
        characters are present.

        Raises:
            ValueError: If any required parameters are missing.
            ValueError: If any parameter exceeds its defined maximum length.
            ValueError: If illegal characters are found in any parameters.
        """
        if not all(
            [
                self.token,
                self.user_id,
                self.password,
                self.ip,
                self.mac,
                self.product_id,
            ]
        ):
            raise ValueError("One or more required parameters are None")

        for param, max_len in Credential._MAX_LENGTHS.items():
            attr_value = getattr(self, param)
            if len(attr_value) > max_len:
                raise ValueError(
                    f"The length of {param} exceeds maximum allowed {max_len}"
                )

        if any(
            "$" in attr
            for attr in [
                self.token,
                self.user_id,
                self.password,
                self.ip,
                self.mac,
                self.product_id,
                self.ctc,
            ]
            if attr
        ):
            raise ValueError("Illegal character '$' found in parameters")
        object.__setattr__(
            self,
            "hash",
            "".join(
                [
                    char if char.isdigit() else str(ord(char) - ord("a") + 1)
                    for char in hashlib.md5(self.token.encode("utf-8"))
                    .hexdigest()[:8]
                    .lower()
                ]
            ),
        )

    def __iter__(self):
        for attr in self.__dict__:
            yield attr, getattr(self, attr)

    def __getitem__(self, item):
        return getattr(self, item)

    def __repr__(self) -> str:
        return str(dict(self))

    def __str__(self) -> str:
        return self.__repr__()

    @staticmethod
    def dumps(credential: Credential) -> str:
        """
        Serializes the Credential object into a string format using delimiters.

        Args:
            credential (Credential): The Credential object to serialize.

        Returns:
            str: The serialized string representation of the Credential object.
        """
        return (
            f"{credential.hash}"
            f"${credential.token}"
            f"${credential.user_id}"
            f"${credential.product_id}"
            f"${credential.ip}"
            f"${credential.mac}"
            f"$"
            f"${credential.ctc}"
        )

    @staticmethod
    def loads(password: str, data: str) -> Credential:
        """
        Deserializes a string into a Credential object.

        Args:
            password (str): The password to be included in the Credential
                object.
            data (str): The serialized string containing credential details.

        Raises:
            ValueError: If the input data does not contain the correct number
                of delimiters ('$').
            SyntaxError: If the input data does not have a correct token.

        Returns:
            Credential: A new Credential object created from the input data.
        """
        if data.count("$") != 7:
            raise ValueError("Illegal numbers of '$' found in parameters")
        items = data.split("$")
        result = Credential(
            token=items[1],
            user_id=items[2],
            password=password,
            ip=items[4],
            mac=items[5],
            product_id=items[3],
            ctc=items[7],
        )
        if result.hash != items[0]:
            raise SyntaxError(
                "The hash is incorrect, the token in the original data may be "
                "forged, or a different hash algorithm was used"
            )
        return result
