"""
AES-128 Decryption
FIPS-197 Standard
"""

from .utils import (
    hex_to_bytes,
    hex_to_text
)

from .state import AESState
from .history import AESHistory

from .key_expansion import KeyExpansion
from .sub_bytes import SubBytes
from .shift_rows import ShiftRows
from .mix_columns import MixColumns
from .add_round_key import AddRoundKey


class AESDecrypt:

    def __init__(self, ciphertext, key):

        self.ciphertext = ciphertext.upper()

        self.key = key.upper()

        self.history = AESHistory()

        self.round_keys = []

        self.key_steps = []
        
            # =====================================================
    # DECRYPT
    # =====================================================

    def decrypt(self):

        # ==========================================
        # Ciphertext
        # ==========================================

        cipher_bytes = hex_to_bytes(

            self.ciphertext

        )

        state = AESState.from_bytes(

            cipher_bytes

        )

        # ==========================================
        # Key Expansion
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
        # ROUND 10
        # Initial AddRoundKey
        # ==========================================

        before, key_matrix, after = AddRoundKey.apply(

            state.get(),

            self.round_keys[10]

        )

        self.history.add(

            round_number=10,

            operation="AddRoundKey",

            before=before,

            after=after,

            round_key=key_matrix

        )

        state.set(after)
        
                # ==========================================
        # ROUND 9 - ROUND 1
        # ==========================================

        for rnd in range(9, 0, -1):

            # ------------------------------------------
            # InvShiftRows
            # ------------------------------------------

            before, after = ShiftRows.decrypt(

                state.get()

            )

            self.history.add(

                round_number=rnd,

                operation="InvShiftRows",

                before=before,

                after=after

            )

            state.set(after)

            # ------------------------------------------
            # InvSubBytes
            # ------------------------------------------

            before, after = SubBytes.decrypt(

                state.get()

            )

            self.history.add(

                round_number=rnd,

                operation="InvSubBytes",

                before=before,

                after=after

            )

            state.set(after)

            # ------------------------------------------
            # AddRoundKey
            # ------------------------------------------

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

            # ------------------------------------------
            # InvMixColumns
            # ------------------------------------------

            before, after = MixColumns.decrypt(

                state.get()

            )

            self.history.add(

                round_number=rnd,

                operation="InvMixColumns",

                before=before,

                after=after

            )

            state.set(after)
            
                    # ==========================================
        # ROUND 0
        # ==========================================

        rnd = 0

        # ------------------------------------------
        # InvShiftRows
        # ------------------------------------------

        before, after = ShiftRows.decrypt(

            state.get()

        )

        self.history.add(

            round_number=rnd,

            operation="InvShiftRows",

            before=before,

            after=after

        )

        state.set(after)

        # ------------------------------------------
        # InvSubBytes
        # ------------------------------------------

        before, after = SubBytes.decrypt(

            state.get()

        )

        self.history.add(

            round_number=rnd,

            operation="InvSubBytes",

            before=before,

            after=after

        )

        state.set(after)

        # ------------------------------------------
        # AddRoundKey
        # ------------------------------------------

        before, key_matrix, after = AddRoundKey.apply(

            state.get(),

            self.round_keys[0]

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
        # STATE -> PLAINTEXT
        # ==========================================

        plaintext_hex = state.to_hex()

        plaintext = hex_to_text(

            plaintext_hex

        )
        
                # ==========================================
        # RETURN
        # ==========================================

        return {

            "plaintext": plaintext,

            "plaintext_hex": plaintext_hex,

            "history": self.history.export(),

            "round_keys": self.round_keys,

            "key_steps": self.key_steps,

            "matrix": [
                step["after"]
                for step in self.history.export()
            ],

            "final_state": state.get()

        }