"""
AES Utility Functions
Compatible with AES-128 Project
Author : OpenAI + Angga Yudha
"""

from .constants import S_BOX


# =====================================================
# VALIDATION
# =====================================================

def validate_key(hex_key):
    """
    Validasi AES-128 Key (16 Byte = 32 Hex Digit)
    """

    if not isinstance(hex_key, str):
        raise TypeError("Key harus berupa string.")

    hex_key = hex_key.strip().upper()

    if len(hex_key) != 32:
        raise ValueError(
            "Key AES-128 harus terdiri dari 32 digit hexadecimal."
        )

    try:
        bytes.fromhex(hex_key)
    except ValueError:
        raise ValueError(
            "Key bukan hexadecimal yang valid."
        )

    return True


def validate_hex(hex_string):

    if len(hex_string) % 2 != 0:
        raise ValueError(
            "Panjang hexadecimal tidak valid."
        )

    try:
        bytes.fromhex(hex_string)
    except ValueError:
        raise ValueError(
            "Hexadecimal tidak valid."
        )

    return True


# =====================================================
# TEXT <-> HEX
# =====================================================

def text_to_hex(text):
    """
    Plaintext -> Hexadecimal (16 Byte)
    Jika kurang dari 16 byte akan dipadding NULL.
    """

    if not isinstance(text, str):
        raise TypeError(
            "Plaintext harus berupa string."
        )

    data = text.encode("utf-8")

    if len(data) > 16:
        raise ValueError(
            "Plaintext maksimal 16 byte."
        )

    data = data.ljust(16, b"\x00")

    return data.hex().upper()


def hex_to_text(hex_string):
    """
    Hexadecimal -> Plaintext
    """

    validate_hex(hex_string)

    data = bytes.fromhex(hex_string)

    return data.rstrip(
        b"\x00"
    ).decode(
        "utf-8",
        errors="ignore"
    )


# =====================================================
# HEX <-> BYTE
# =====================================================

def hex_to_bytes(hex_string):

    validate_hex(hex_string)

    return list(
        bytes.fromhex(hex_string)
    )


def bytes_to_hex(byte_array):

    return "".join(
        "{:02X}".format(b)
        for b in byte_array
    )


# =====================================================
# STATE MATRIX
# AES menggunakan Column Major Order
# =====================================================

def bytes_to_state(byte_array):

    if len(byte_array) != 16:
        raise ValueError(
            "State AES harus 16 byte."
        )

    state = [[0] * 4 for _ in range(4)]

    for i in range(16):

        state[i % 4][i // 4] = byte_array[i]

    return state


def state_to_bytes(state):

    if len(state) != 4:
        raise ValueError(
            "State harus berukuran 4x4."
        )

    result = []

    for c in range(4):

        for r in range(4):

            result.append(
                state[r][c]
            )

    return result


def hex_to_state(hex_string):

    return bytes_to_state(

        hex_to_bytes(hex_string)

    )


def state_to_hex(state):

    return bytes_to_hex(

        state_to_bytes(state)

    )


# =====================================================
# XOR
# =====================================================

def xor_bytes(a, b):

    return [

        x ^ y

        for x, y in zip(a, b)

    ]


# =====================================================
# WORD
# =====================================================

def rotate_word(word):

    return word[1:] + word[:1]


def sub_word(word):

    return [

        S_BOX[b]

        for b in word

    ]


# =====================================================
# MATRIX DISPLAY
# =====================================================

def matrix_to_string(state):

    lines = []

    for row in state:

        lines.append(

            " ".join(

                "{:02X}".format(x)

                for x in row

            )

        )

    return "\n".join(lines)


def print_state(state):

    print()

    print(

        matrix_to_string(state)

    )

    print()


# =====================================================
# GALOIS FIELD
# =====================================================

def xtime(a):

    a <<= 1

    if a & 0x100:

        a ^= 0x11B

    return a & 0xFF


def gmul(a, b):

    p = 0

    for _ in range(8):

        if b & 1:

            p ^= a

        hi = a & 0x80

        a <<= 1

        if hi:

            a ^= 0x11B

        a &= 0xFF

        b >>= 1

    return p


# =====================================================
# INVERSE SBOX
# =====================================================

def generate_inverse_sbox():

    inv = [0] * 256

    for i, value in enumerate(S_BOX):

        inv[value] = i

    return inv


INV_S_BOX = generate_inverse_sbox()