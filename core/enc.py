"""
backend/saiki_site/enc.py

Encryption and Coding module.
"""

"""
    Encryption
"""

import hashlib
from typing import Iterable


def prf(data: bytes) -> int:
    return int.from_bytes(hashlib.sha256(data).digest(), 'big')


def next_pow2(n: int) -> int:
    return 1 << (n - 1).bit_length()


def feistel_round(L: int, R: int, key: str, round_num: int, mask: int) -> (int, int):
    F = prf(f"{R}_{round_num}_{key}".encode()) & mask
    return R, L ^ F


def feistel_encrypt(i: int, key: str, N: int, rounds: int, mask: int) -> int:
    # i must be < N = 2^m
    m = N.bit_length() // 2
    L = i >> m
    R = i & ((1 << m) - 1)
    for r in range(rounds):
        L, R = feistel_round(L, R, key, r, mask)
    return (L << m) | R


def feistel_decrypt(y: int, key: str, N: int, rounds: int, mask: int) -> int:
    m = N.bit_length() // 2
    L = y >> m
    R = y & ((1 << m) - 1)
    for r in reversed(range(rounds)):
        # inverse of (L, R) = (R, L ^ F)
        F = prf(f"{L}_{r}_{key}".encode()) & mask
        L, R = R ^ F, L
    return (L << m) | R


def permute(real: int, key: str, domain_size: int, rounds: int = 4) -> int:
    # cycle-walking to next power of two
    N = next_pow2(domain_size)
    m = N.bit_length() // 2
    mask = (1 << m) - 1
    x = real
    while True:
        y = feistel_encrypt(x, key, N, rounds, mask)
        if y < domain_size:
            return y
        x = y  # cycle-walk


def unpermute(hide: int, key: str, domain_size: int, rounds: int = 4) -> int:
    N = next_pow2(domain_size)
    m = N.bit_length() // 2
    mask = (1 << m) - 1
    y = hide
    while True:
        x = feistel_decrypt(y, key, N, rounds, mask)
        if x < domain_size:
            return x
        y = x  # reverse cycle-walk


def generate_key() -> str:
    from time import time_ns

    def random_string(n: int) -> str:
        from random import choice
        import string
        return "".join(choice(string.ascii_letters) for _ in range(n))

    timestamp: int = time_ns()
    timestamp_str: str = str(timestamp)
    from hashlib import sha256

    string_key: str = str(timestamp) + random_string(64 - len(timestamp_str))
    return sha256(string_key.encode(encoding="utf-8")).hexdigest()


"""
    Coding
"""

import base64


def int_to_base64(integer_value: int, string_size: int = 64) -> str:
    """Encodes an integer into URL-safe b64 string, padded with `string_size` characters. """

    # from math import ceil, log
    # print(f"int_to_base64({integer_value}, {string_size})")
    # print(ceil(log(integer_value, 64)))
    # print(ceil(integer_value.bit_length() / 8))

    # converting to bytes...
    byte_length: int = (integer_value.bit_length() + 7) // 8
    value_in_bytes: bytes = integer_value.to_bytes(byte_length, byteorder="big")

    # encoding int...
    b64_encode: str = base64.urlsafe_b64encode(value_in_bytes).decode("ascii")
    b64_unpadded = b64_encode.rstrip("=")

    if len(b64_unpadded) > string_size:
        raise ValueError

    # b64_encoding = b64_encoding.rstrip(b"=")
    # decoding to ascii...
    # return b64_encoding.decode("ascii")

    # padding it accordingly
    return b64_unpadded.ljust(string_size, "=")


def base64_to_int(b64_str: str) -> int:
    """Decodes a b64 string, potentially padded, into its respective integer."""
    # print(b64_str)

    # unpadding it.
    core_str: str = b64_str.rstrip("=")
    # unpadded: str = b64_str.lstrip("A")
    # padding_count: int = len(core_str) - len(unpadded)

    # reconstructing the unpadded b64...
    # padding the string to a multiple of 4.
    padded_b64 = core_str + "=" * ((4 - len(core_str) % 4) % 4)

    # decoding to bytes...
    decoded_bytes: bytes = base64.urlsafe_b64decode(padded_b64)

    # converting to integer...
    return int.from_bytes(decoded_bytes, byteorder="big")


def b64_encoding_max(string_size: int) -> int:
    """Computes the base64 string size representation."""

    # base63 characters encodes 6 bits.
    max_of_bytes: int = (string_size * 6) // 8

    # (- 1) + 2 ** max_of_bytes
    return (1 << (8 * max_of_bytes)) - 1


def int_list_to_b64(__iterable: Iterable[int], string_size: int) -> str:
    return "".join(int_to_base64(v, string_size) for v in __iterable)


def b64_to_int_list(b64_str, string_size: int) -> list[int]:
    total_b64_len: int = len(b64_str)
    if total_b64_len % string_size != 0:
        raise ValueError("Incompatible sizes")

    b64s: list[str] = [b64_str[ç:ç + string_size] for ç in range(0, total_b64_len, string_size)]
    return list(map(lambda s: base64_to_int(s), b64s))


"""
    Testing
"""


class EncTest(object):
    """Tests the module."""

    def __init__(self):
        self.test()

    @staticmethod
    def test() -> None:
        EncTest.__test_permutation_enc()
        EncTest.__test_b64_encoding()
        EncTest.__assert_b64_full_correctness(string_size=4)
    
    @staticmethod
    def __assert_b64_full_correctness(string_size: int) -> None:
        """Asserts the encoding-decoding scheme for all sizes for the string size used in the application."""

        n_max: int = b64_encoding_max(string_size)

        for ç in range(n_max):
            b_64: str = int_to_base64(ç, string_size)
            assert base64_to_int(b_64) == ç

        return None

    @staticmethod
    def __test_b64_encoding() -> None:

        overflow_values: list[tuple[int, int]] = [
            # (256, 2), (4096, 3), ...
            (b64_encoding_max(ç) + 1, ç) for ç in range(2, 17)
        ]

        # testing overflow
        for values in overflow_values:
            values: tuple[int, int]

            try:
                int_to_base64(* values)
                raise AssertionError(* values)

            except ValueError:
                pass

        assert base64_to_int(int_to_base64(4, 4)) == 4

        x = [1, 2, 3, 4]
        y = int_list_to_b64(x, 4)
        print(y)
        z = b64_to_int_list(y, 4)
        print(z)
        assert x == z

        return None

    @staticmethod
    def __test_permutation_enc() -> None:
        k = 250
        key_data = "user_key1"

        print("(key, hide, recovered)")
        for i in range(k):
            h = permute(i, key_data, k)
            r = unpermute(h, key_data, k)

            # print(f"({i}, {h}, {r})")
            assert i == r


if __name__ == "__main__":
    EncTest.test()
