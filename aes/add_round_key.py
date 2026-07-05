"""
AES AddRoundKey
"""


class AddRoundKey:

    @staticmethod
    def apply(state, round_key):

        before = [row[:] for row in state]

        key_matrix = [[0]*4 for _ in range(4)]

        for i in range(16):

            key_matrix[i % 4][i // 4] = round_key[i]

        after = [[0]*4 for _ in range(4)]

        for r in range(4):

            for c in range(4):

                after[r][c] = state[r][c] ^ key_matrix[r][c]

        return before, key_matrix, after