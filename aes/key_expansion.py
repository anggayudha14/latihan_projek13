"""
AES-128 Key Expansion
FIPS-197
"""

from .constants import RCON
from .utils import (
    rotate_word,
    sub_word,
    xor_bytes,
    validate_key,
    bytes_to_state,
    matrix_to_string
)


class KeyExpansion:
    """
    AES-128 Key Expansion
    Generate 44 Words
    Generate 11 Round Keys
    Save all expansion steps
    """

    def __init__(self, key):

        # --------------------------------------
        # Validasi Key
        # --------------------------------------

        if isinstance(key, str):

            validate_key(key)

            key = list(
                bytes.fromhex(key)
            )

        if len(key) != 16:

            raise ValueError(
                "AES-128 membutuhkan key 16 byte."
            )

        self.key = key.copy()

        # w0 ... w43
        self.words = []

        # Round Key 0 ... 10
        self.round_keys = []

        # History
        self.steps = []

    # ==================================================
    # SAVE HISTORY
    # ==================================================

    def save_step(
        self,
        step_type,
        round_number,
        index,
        operation,
        before,
        after
    ):

        self.steps.append({

            "type": step_type,

            "round": round_number,

            "index": index,

            "operation": operation,

            "before": before.copy()
            if before is not None
            else None,

            "after": after.copy()
            if after is not None
            else None

        })

    # ==================================================
    # SPLIT KEY
    # ==================================================

    def split_key(self):

        self.words = []

        for i in range(0,16,4):

            word = self.key[i:i+4]

            self.words.append(word)

            self.save_step(

                step_type="word",

                round_number=0,

                index=len(self.words)-1,

                operation="Initial Key",

                before=None,

                after=word

            )

        return self.words
    
        # ==================================================
    # GENERATE WORDS (w0 - w43)
    # ==================================================

    def generate_words(self):

        # --------------------------------------
        # Generate w0 - w3
        # --------------------------------------

        if len(self.words) == 0:

            self.split_key()

        # --------------------------------------
        # Generate w4 - w43
        # --------------------------------------

        for i in range(4, 44):

            previous = self.words[i - 1].copy()

            temp = previous.copy()

            operation = "XOR"

            before = temp.copy()

            # ----------------------------------
            # Setiap kelipatan 4
            # ----------------------------------

            if i % 4 == 0:

                temp = rotate_word(temp)

                temp = sub_word(temp)

                temp[0] ^= RCON[(i // 4) - 1]

                operation = "RotWord + SubWord + Rcon"

            # ----------------------------------
            # XOR dengan word 4 posisi sebelumnya
            # ----------------------------------

            new_word = xor_bytes(

                self.words[i - 4],

                temp

            )

            self.words.append(

                new_word

            )

            # ----------------------------------
            # Simpan history
            # ----------------------------------

            self.save_step(

                step_type="word",

                round_number=i // 4,

                index=i,

                operation=operation,

                before=before,

                after=new_word

            )

        return self.words
    
        # ==================================================
    # GENERATE ROUND KEYS
    # ==================================================

    def generate_round_keys(self):

        # Pastikan seluruh word sudah dibuat
        if len(self.words) != 44:

            self.generate_words()

        self.round_keys = []

        # --------------------------------------
        # Round Key 0 - Round Key 10
        # --------------------------------------

        for rnd in range(11):

            start = rnd * 4

            # Ambil 4 word (16 byte)
            key_bytes = []

            for i in range(4):

                key_bytes.extend(

                    self.words[start + i]

                )

            self.round_keys.append(

                key_bytes

            )

            # Simpan history dengan format konsisten
            self.save_step(

                step_type="round_key",

                round_number=rnd,

                index=rnd,

                operation="Generate Round Key",

                before=None,

                after=key_bytes

            )

        return self.round_keys
    
        # ==================================================
    # GET ROUND KEYS
    # ==================================================

    def get_round_keys(self):

        if len(self.round_keys) == 0:

            self.generate_round_keys()

        return self.round_keys
    
        # ==================================================
    # GET HISTORY
    # ==================================================

    def get_steps(self):
        """
        Mengembalikan seluruh proses Key Expansion.
        """

        return self.steps

    # ==================================================
    # PRINT WORDS
    # ==================================================

    def print_words(self):
        """
        Menampilkan seluruh word (w0 - w43).
        """

        if len(self.words) == 0:

            self.generate_words()

        print("\n========== WORD ==========\n")

        for i, word in enumerate(self.words):

            text = " ".join(

                "{:02X}".format(x)

                for x in word

            )

            print(f"W{i:02d} : {text}")

    # ==================================================
    # PRINT ROUND KEYS
    # ==================================================

    def print_round_keys(self):
        """
        Menampilkan seluruh Round Key.
        """

        if len(self.round_keys) == 0:

            self.generate_round_keys()

        print("\n======= ROUND KEYS =======\n")

        for rnd, key in enumerate(self.round_keys):

            print(f"Round {rnd}")

            matrix = bytes_to_state(key)

            print(

                matrix_to_string(matrix)

            )

            print()

    # ==================================================
    # STRING REPRESENTATION
    # ==================================================

    def __str__(self):

        return (

            f"<KeyExpansion "
            f"words={len(self.words)} "
            f"round_keys={len(self.round_keys)} "
            f"steps={len(self.steps)}>"

        )