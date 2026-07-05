"""
AES-128 Encryption
FIPS-197 Standard
"""

from .utils import (
    text_to_hex,
    hex_to_bytes,
    bytes_to_hex
)

from .state import AESState
from .history import AESHistory

from .key_expansion import KeyExpansion
from .sub_bytes import SubBytes
from .shift_rows import ShiftRows
from .mix_columns import MixColumns
from .add_round_key import AddRoundKey


class AESEncrypt:


    def __init__(self, plaintext, key):

        self.plaintext = plaintext
        self.key = key

        self.history = AESHistory()

        self.round_keys = []

        self.key_steps = []

        self.visualization = []
        
        

    # =====================================================
    # ENCRYPT
    # =====================================================

    def encrypt(self):

        # ==========================================
        # PLAINTEXT -> STATE
        # ==========================================

        plaintext_hex = text_to_hex(
            self.plaintext
        )

        plaintext_bytes = hex_to_bytes(
            plaintext_hex
        )

        state = AESState.from_bytes(
            plaintext_bytes
        )

        # ==========================================
        # KEY EXPANSION
        # ==========================================

        key_bytes = hex_to_bytes(
            self.key
        )

        key_expansion = KeyExpansion(
            key_bytes
        )

        self.round_keys = (
            key_expansion.generate_round_keys()
        )

        self.key_steps = (
            key_expansion.get_steps()
        )

        # ==========================================
        # INITIAL ROUND (ROUND 0)
        # AddRoundKey
        # ==========================================

        before, key_matrix, after = AddRoundKey.apply(

            state.get(),

            self.round_keys[0]

        )

        self.history.add(

            round_number=0,

            operation="AddRoundKey",

            before=before,

            after=after,

            round_key=key_matrix

        )

        state.set(after)

                # ==========================================
        # ROUND 1 - ROUND 9
        # ==========================================

        for rnd in range(1, 10):

            # --------------------------------------
            # SubBytes
            # --------------------------------------

            before, after = SubBytes.encrypt(
                state.get()
            )

            self.history.add(

                round_number=rnd,

                operation="SubBytes",

                before=before,

                after=after

            )

            state.set(after)

            # --------------------------------------
            # ShiftRows
            # --------------------------------------

            before, after = ShiftRows.encrypt(
                state.get()
            )

            self.history.add(

                round_number=rnd,

                operation="ShiftRows",

                before=before,

                after=after

            )

            state.set(after)

            # --------------------------------------
            # MixColumns
            # --------------------------------------

            before, after = MixColumns.encrypt(
                state.get()
            )

            self.history.add(

                round_number=rnd,

                operation="MixColumns",

                before=before,

                after=after

            )

            state.set(after)

            # --------------------------------------
            # AddRoundKey
            # --------------------------------------

            before, key_matrix, after = AddRoundKey.apply(

                state.get(),

                self.round_keys[rnd]

            )

            self.history.add(

                round_number=rnd,

                operation="AddRoundKey",

                before=before,

                after=after,

                round_key=key_matrix

            )

            state.set(after)

                # ==========================================
        # FINAL ROUND (ROUND 10)
        # Tidak menggunakan MixColumns
        # ==========================================

        rnd = 10

        # ------------------------------------------
        # SubBytes
        # ------------------------------------------

        before, after = SubBytes.encrypt(
            state.get()
        )

        self.history.add(

            round_number=rnd,

            operation="SubBytes",

            before=before,

            after=after

        )

        state.set(after)

        # ------------------------------------------
        # ShiftRows
        # ------------------------------------------

        before, after = ShiftRows.encrypt(
            state.get()
        )

        self.history.add(

            round_number=rnd,

            operation="ShiftRows",

            before=before,

            after=after

        )

        state.set(after)

        # ------------------------------------------
        # AddRoundKey
        # ------------------------------------------

        before, key_matrix, after = AddRoundKey.apply(

            state.get(),

            self.round_keys[10]

        )

        self.history.add(

            round_number=rnd,

            operation="AddRoundKey",

            before=before,

            after=after,

            round_key=key_matrix

        )

        state.set(after)

        # ==========================================
        # STATE -> CIPHERTEXT
        # ==========================================

        ciphertext = bytes_to_hex(

            state.to_bytes()

        )

        # ==========================================
        # RETURN RESULT
        # ==========================================

        return {

            "ciphertext": ciphertext,

            "ciphertext_hex": ciphertext,

            "history": self.history.export(),

            "round_keys": self.round_keys,

            "key_steps": self.key_steps,

            "matrix": [
                step["after"]
                for step in self.history.export()
            ],

            "final_state": state.get()

        }
        