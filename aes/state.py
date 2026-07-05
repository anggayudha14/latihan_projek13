"""
AES State Matrix
FIPS-197
"""


from .utils import (

    bytes_to_state,
    state_to_bytes,
    state_to_hex,
    matrix_to_string

)


class AESState:

    def __init__(self, matrix):

        self.matrix = matrix

    # ==========================================

    @classmethod
    def from_bytes(cls, byte_array):

        return cls(

            bytes_to_state(byte_array)

        )

    # ==========================================

    @classmethod
    def from_hex(cls, hex_string):

        from .utils import hex_to_bytes

        return cls.from_bytes(

            hex_to_bytes(hex_string)

        )

    # ==========================================

    def get(self):

        return [

            row[:]

            for row in self.matrix

        ]

    # ==========================================

    def set(self, matrix):

        self.matrix = [

            row[:]

            for row in matrix

        ]

    # ==========================================

    def copy(self):

        return AESState(

            self.get()

        )

    # ==========================================

    def to_bytes(self):

        return state_to_bytes(

            self.matrix

        )

    # ==========================================

    def to_hex(self):

        return state_to_hex(

            self.matrix

        )

    # ==========================================

    def to_string(self):

        return matrix_to_string(

            self.matrix

        )

    # ==========================================

    def print(self):

        print()

        print(

            self.to_string()

        )

        print()

    # ==========================================

    def __str__(self):

        return self.to_string()