# -*- coding: utf-8 -*-
"""Authentication Tools for Cryptography Testing.

This module offers tools for performing cryptographic tests, particularly
focusing on authentication methods such as plain, MD5, and salted MD5. It
features functions and classes for reversing authentication processes and
testing various salts in parallel. The primary purpose is to facilitate the
decryption of ciphertexts using different methods, with extension to parallel
processing scenarios.

Example:
    Using the reverse function to decrypt a ciphertext:

        password = 'password'
        cipertext = 'encrypted_string_here'
        decrypted_data = reverse(password, cipertext, AuthMehod.MD5)

    Testing salts using the EvaluateTools class:

        matches = EvaluateTools().test_salt(credential, cipertext, 8, True, 12)

Attributes:
    None

Todo:
    None

"""
from multiprocessing import Manager, Process

from epg import crypto
from epg.authenticator import Authenticator, AuthMehod, CipherUtils
from epg.credential import Credential


def reverse(
    password: str,
    cipertext: str,
    auth_method: AuthMehod = AuthMehod.PLAIN,
    salt: str | None = None,
) -> Credential:
    """
    Attempts to reverse-engineer the authentication process by decrypting a
    given ciphertext using the provided password and authentication method.
    Optionally, a salt can be used if the authentication method requires it.

    Args:
        password (str): The password used for generating the key to decrypt the
            ciphertext.
        cipertext (str): The encrypted string that needs to be decrypted.
        auth_method (AuthMehod, optional): The method of authentication to use
            for decrypting the ciphertext. Defaults to AuthMehod.PLAIN.
        salt (str | None, optional): An optional salt that is required if the
            authentication method is salted. Defaults to None.

    Raises:
        TypeError: Raised if a necessary 'salt' is not provided when required
            by the authentication method.
        ValueError: Raised if an invalid authentication method is provided.

    Returns:
        Credential: The Credential object generated from the decrypted data.
    """
    if auth_method == AuthMehod.SALTED_MD5 and salt is None:
        raise TypeError("missing required positional argument: 'salt'")
    match auth_method:
        case AuthMehod.PLAIN:
            key = CipherUtils.pad(password)
        case AuthMehod.MD5:
            key = CipherUtils.md5(password)
        case AuthMehod.SALTED_MD5:
            key = CipherUtils.salted_md5(password, salt)
        case _:
            raise ValueError("Invalid auth method")
    return Credential.loads(password, crypto.decrypt(cipertext, key))


class EvaluateTools:
    """
    Provides a utility scope for salt testing against a given ciphertext using
    various authentication methods. This class is designed not as a traditional
    class but rather as a scope for parallel processing of salt testing. This
    design helps encapsulate related methods that are essential for the
    operation of the `test_salt` method.

    Attributes:
        _credential (Credential): Credential object for authentication.
        _cipertext (str): Ciphertext against which salts are tested.
        _max_digitals (int): Maximum number of digits for salt values.
        _padding (bool): Flag to determine if padding should be applied to
            salts.

    The class does not return any objects but serves as a namespace to organize
    related cryptographic operations effectively.
    """
    _credential: Credential
    _cipertext: str
    _max_digitals: int
    _padding: bool

    def _pad(self, salt: int) -> str:
        """
        Pads the given integer 'salt' to a fixed number of digits determined by
        'self._max_digitals'.
        This method will pad the integer with leading zeros if 'self._padding'
        is set to True, otherwise, it will return the integer as a plain string
        without padding.

        Args:
            salt (int): The integer to be padded.

        Returns:
            str: The padded string representation of 'salt' if padding is
                enabled, or the plain string representation of 'salt' if no
                padding is applied.
        """
        return f"{salt:0{self._max_digitals}d}" if self._padding else str(salt)

    def _worker(self, result: list, start: int, amount: int) -> None:
        """
        Executes a worker function that iterates from a starting point over a
        specified amount, attempting to authenticate and find matches based on
        a provided method.
        This function prints progress updates and appends successful matches to
        the 'result' list.

        Args:
            result (list): The list to which matching indices will be appended
                if authentication is successful.
            start (int): The starting index from which the worker begins its
                processing.
            amount (int): The total number of iterations the worker should
                process from the starting index.

        """
        print(f"worker started #{start}")
        for location in range(amount):
            if location % 100000 == 0:
                print(
                    f"at {
                        location + start
                    }, progress {
                        location / (amount - 1) *100:.2f
                    }%"
                )
            try:
                if (
                    Authenticator(
                        self._credential,
                        AuthMehod.SALTED_MD5,
                        self._pad(location + start),
                    ).info
                    == self._cipertext
                ):
                    result.append(location + start)
            except ValueError:
                pass

    def test_salt(
        self,
        credential: Credential,
        cipertext: str,
        max_digitals: int = 8,
        padding: bool = True,
        processes: int = 4,
    ) -> list:
        """
        Tests various salt values against a ciphertext using parallel
        processing.
        This method distributes the workload among a specified number of
        processes to test different salt values generated based on the maximum
        number of digits. Successful matches (where the hashed version of the
        salt matches the ciphertext) are collected and returned.

        Args:
            credential (Credential): The credentials to use for authentication.
            cipertext (str): The encrypted string to be matched against.
            max_digitals (int, optional): The maximum number of digits for the
                salt values to be generated. Defaults to 8.
            padding (bool, optional): Specifies whether the salt should be
                zero-padded to the length of `max_digitals`. Defaults to True.
            processes (int, optional): The number of parallel processes to use
                for the computation. Defaults to 4.

        Returns:
            list: A list of salt values that successfully match the ciphertext.
        """
        self._credential=credential
        self._cipertext=cipertext
        self._max_digitals=max_digitals
        self._padding=padding
        total = 10**max_digitals
        divided_batch = total // processes
        remaining=total%processes
        with Manager() as manager:
            result = manager.list()
            tasks = [
                Process(
                    target=self._worker,
                    args=(result, process * divided_batch, divided_batch),
                )
                if process < processes - 1
                else Process(
                    target=self._worker,
                    args=(
                        result,
                        process * divided_batch,
                        divided_batch + remaining,
                    ),
                )
                for process in range(processes)
            ]
            for task in tasks:
                task.start()
            for task in tasks:
                task.join()
            return list(result)
