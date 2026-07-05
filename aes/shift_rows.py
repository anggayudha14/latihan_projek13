"""
AES ShiftRows
"""


class ShiftRows:

    @staticmethod
    def encrypt(state):

        before = [row[:] for row in state]

        after = [row[:] for row in state]

        after[1] = after[1][1:] + after[1][:1]
        after[2] = after[2][2:] + after[2][:2]
        after[3] = after[3][3:] + after[3][:3]

        return before, after

    @staticmethod
    def decrypt(state):

        before = [row[:] for row in state]

        after = [row[:] for row in state]

        after[1] = after[1][-1:] + after[1][:-1]
        after[2] = after[2][-2:] + after[2][:-2]
        after[3] = after[3][-3:] + after[3][:-3]

        return before, after