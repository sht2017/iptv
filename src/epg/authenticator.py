# -*- coding: utf-8 -*-
"""Authentication and Encryption Utility Module.

This module provides comprehensive tools and classes for authenticating users
and managing encryption processes. It leverages enums to define authentication
methods and includes utility functions for cipher operations. Authentication
can be performed using plain text, MD5, or salted MD5 methods, with support for
credentials serialization.

Example:
    from epg.credential import Credential
    credential = Credential(...)
    authenticator = Authenticator(
        credential = credential,
        auth_method = AuthMehod.SALTED_MD5,
        salt = "01234567"
    )
    encrypted_info = authenticator.info

Attributes:
    AuthMehod (Enum): An enumeration of supported authentication methods.
    CipherUtils (class): Utility class for cipher-related operations.
    Authenticator (class): Handles authentication processes.

Todo:
    * Extend support for additional encryption algorithms.
    * Improve error handling and validation of input parameters.
"""

import hashlib
from enum import Enum, auto

from epg import crypto
from epg.credential import Credential


class AuthMehod(Enum):
    """Enumeration for different authentication methods.

    This enumeration defines various methods that can be used for
    authenticating users. Each method has a unique name and
    automatically assigned value.

    Attributes:
        PLAIN: Plain text authentication method.
        MD5: MD5 hashing authentication method.
        SALTED_MD5: Salted MD5 hashing authentication method.
    """

    PLAIN = auto()
    MD5 = auto()
    SALTED_MD5 = auto()


class CipherUtils:
    """Utility class for performing cipher-related operations.

    This class provides static methods to pad ciphers and generate MD5 hashes.
    """

    @staticmethod
    def pad(cipher: str) -> str:
        """Pads the given cipher to a specific length.

        If the length of the cipher is less than 8 characters, it is padded
            with zeros up to 8 characters.
        If the length is between 8 and 24 characters, it is padded with zeros
            up to 24 characters.
        If the length is more than 24 characters, it is truncated to 24
            characters.

        Args:
            cipher (str): The input cipher string to be padded.

        Returns:
            str: The padded or truncated cipher string.
        """
        length = len(cipher)
        if length in (8, 24):
            return cipher
        if length < 8:
            return cipher + "0" * (8 - length)
        if length < 24:
            return cipher + "0" * (24 - length)
        return cipher[:24]

    @staticmethod
    def md5(cipher: str) -> str:
        """Generates an MD5 hash of the given cipher and pads it.

        The resulting hash is padded or truncated to ensure its length is
            either 8 or 24 characters.

        Args:
            cipher (str): The input cipher string to be hashed.

        Returns:
            str: The padded or truncated MD5 hash of the cipher.
        """
        return CipherUtils.pad(hashlib.md5(cipher.encode("utf-8")).hexdigest())

    @staticmethod
    def salted_md5(cipher: str, salt: str) -> str:
        """Generates a salted MD5 hash of the given cipher and pads it.

        The cipher is concatenated with the salt before hashing. The resulting
        hash is then padded or truncated to ensure its length is 8 characters.

        Args:
            cipher (str): The input cipher string to be hashed.
            salt (str): The salt string to be added to the cipher before
                hashing.

        Returns:
            str: The padded MD5 hash of the salted cipher.
        """
        return CipherUtils.pad(
            hashlib.md5((cipher + salt).encode("utf-8")).hexdigest()[:8]
        )


class Authenticator:
    """Class to handle authentication methods for credentials.

    This class provides mechanisms to authenticate credentials using different
    methods such as plain text, MD5, and salted MD5. It also supports
    serialization of the credentials with encryption based on the chosen
    authentication method.

    Attributes:
        _credential (Credential): The credential object containing user
            credentials.
        auth_method (AuthMehod): The method to use for authentication.
        salt (str): The salt to use for SALTED_MD5 authentication, if
            applicable.

    Raises:
        TypeError: If 'salt' is required but not provided.
        ValueError: If an invalid authentication method is used.
    """

    # constants

    # properties
    _credential: Credential
    auth_method: AuthMehod
    salt: str

    # properties @getter/@setter
    info: str  # @getter

    def __init__(
        self,
        credential: Credential,
        auth_method: AuthMehod = AuthMehod.PLAIN,
        salt: str | None = None,
    ):
        """Initializes the Authenticator with given credentials and method.

        The constructor sets up the authentication method and optionally uses a
        salt if the method requires it. For SALTED_MD5 authentication, the salt
        must be provided.

        Args:
            credential (Credential): The credential object containing user
                credentials.
            auth_method (AuthMehod, optional): The method to use for
                authentication. Defaults to AuthMehod.PLAIN.
            salt (str, optional): The salt to use for SALTED_MD5
                authentication. Required if auth_method is
                AuthMehod.SALTED_MD5. Defaults to None.

        Raises:
            TypeError: If 'salt' is required for SALTED_MD5 but not provided.
        """
        self._credential = credential
        self.auth_method = auth_method
        if auth_method == AuthMehod.SALTED_MD5:
            if salt is not None:
                self.salt = salt
            else:
                raise TypeError("missing required positional argument: 'salt'")

    def __iter__(self):
        for attr in self.__dict__:
            yield attr, getattr(self, attr)

    def __getitem__(self, item):
        return getattr(self, item)

    def __repr__(self) -> str:
        return str(dict(self))

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def info(self) -> str:
        """Encrypts and returns the credential information based on the method.

        This property generates an encryption key based on the chosen
        authentication method and uses it to encrypt the serialized credential
        information. It raises a ValueError if an invalid authentication method
        is used.

        Raises:
            ValueError: If an invalid authentication method is used.

        Returns:
            str: The encrypted credential information.
        """
        credential = self._credential

        match self.auth_method:
            case AuthMehod.PLAIN:
                key = CipherUtils.pad(credential.password)
            case AuthMehod.MD5:
                key = CipherUtils.md5(credential.password)
            case AuthMehod.SALTED_MD5:
                key = CipherUtils.salted_md5(credential.password, self.salt)
            case _:
                raise ValueError("Invalid auth key")
        encrypted_data = crypto.encrypt(Credential.dumps(credential), key)
        return encrypted_data
