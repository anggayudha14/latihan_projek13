"""
AES SubBytes
"""

from .constants import S_BOX
from .utils import INV_S_BOX


class SubBytes:

    @staticmethod
    def encrypt(state):

        before = [row[:] for row in state]

        after = [[0]*4 for _ in range(4)]

        for r in range(4):

            for c in range(4):

                after[r][c] = S_BOX[state[r][c]]

        return before, after

    @staticmethod
    def decrypt(state):

        before = [row[:] for row in state]

        after = [[0]*4 for _ in range(4)]

        for r in range(4):

            for c in range(4):

                after[r][c] = INV_S_BOX[state[r][c]]

        return before, after