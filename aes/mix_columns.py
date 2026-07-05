"""
AES MixColumns
FIPS-197 Standard
"""

from .utils import gmul


class MixColumns:

    # =====================================================
    # ENCRYPT
    # =====================================================

    @staticmethod
    def encrypt(state):
        """
        MixColumns

        Parameter
        ---------
        state : list[list]
            Matrix AES 4x4

        Return
        ------
        before, after
        """

        before = [row[:] for row in state]

        after = [[0] * 4 for _ in range(4)]

        for c in range(4):

            s0 = state[0][c]
            s1 = state[1][c]
            s2 = state[2][c]
            s3 = state[3][c]

            after[0][c] = (
                gmul(s0, 2) ^
                gmul(s1, 3) ^
                s2 ^
                s3
            )

            after[1][c] = (
                s0 ^
                gmul(s1, 2) ^
                gmul(s2, 3) ^
                s3
            )

            after[2][c] = (
                s0 ^
                s1 ^
                gmul(s2, 2) ^
                gmul(s3, 3)
            )

            after[3][c] = (
                gmul(s0, 3) ^
                s1 ^
                s2 ^
                gmul(s3, 2)
            )

        return before, after

    # =====================================================
    # DECRYPT
    # =====================================================

    @staticmethod
    def decrypt(state):
        """
        Inverse MixColumns

        Parameter
        ---------
        state : list[list]
            Matrix AES 4x4

        Return
        ------
        before, after
        """

        before = [row[:] for row in state]

        after = [[0] * 4 for _ in range(4)]

        for c in range(4):

            s0 = state[0][c]
            s1 = state[1][c]
            s2 = state[2][c]
            s3 = state[3][c]

            after[0][c] = (
                gmul(s0, 14) ^
                gmul(s1, 11) ^
                gmul(s2, 13) ^
                gmul(s3, 9)
            )

            after[1][c] = (
                gmul(s0, 9) ^
                gmul(s1, 14) ^
                gmul(s2, 11) ^
                gmul(s3, 13)
            )

            after[2][c] = (
                gmul(s0, 13) ^
                gmul(s1, 9) ^
                gmul(s2, 14) ^
                gmul(s3, 11)
            )

            after[3][c] = (
                gmul(s0, 11) ^
                gmul(s1, 13) ^
                gmul(s2, 9) ^
                gmul(s3, 14)
            )

        return before, after