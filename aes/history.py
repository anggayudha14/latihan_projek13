"""
history.py
===========

Recorder visualisasi AES Final Version

Semua state AES akan disimpan di sini
agar mudah divisualisasikan oleh Flask.
"""


class AESHistory:

    def __init__(self):

        self.rounds = []

    def add(
        self,
        round_number,
        operation,
        before=None,
        after=None,
        round_key=None
    ):
        """
        Menyimpan satu langkah proses AES (SubBytes, ShiftRows,
        MixColumns, AddRoundKey, dsb).

        Parameter
        ---------
        round_number : int
            Nomor ronde AES (0 - 10)
        operation : str
            Nama operasi yang dijalankan
        before : list[list] | None
            Matrix state sebelum operasi
        after : list[list] | None
            Matrix state sesudah operasi
        round_key : list[list] | None
            Matrix round key (hanya untuk AddRoundKey)
        """

        self.rounds.append({

            "round": round_number,

            "operation": operation,

            "before": [row[:] for row in before]
            if before is not None
            else None,

            "after": [row[:] for row in after]
            if after is not None
            else None,

            "round_key": [row[:] for row in round_key]
            if round_key is not None
            else None,

            "matrix": [row[:] for row in after]
            if after is not None
            else None

        })

    def export(self):

        return self.rounds

    def clear(self):

        self.rounds.clear()
