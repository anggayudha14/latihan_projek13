# AES-128 Encryption Simulator

Implementasi AES-128 (FIPS-197) dari nol menggunakan Python, dengan antarmuka
web berbasis Flask untuk memvisualisasikan setiap tahap proses enkripsi dan
dekripsi (SubBytes, ShiftRows, MixColumns, AddRoundKey, dan Key Expansion).

## Fitur

- Enkripsi & dekripsi AES-128 murni (tanpa library kriptografi eksternal)
- Visualisasi step-by-step: Round Keys, Key Expansion, History proses, dan
  Matrix State di setiap ronde
- Validasi input (plaintext, key, ciphertext) di backend maupun frontend
- REST API sederhana (`/encrypt`, `/decrypt`) yang mengembalikan JSON

## Instalasi

```bash
pip install -r requirements.txt
python app.py
```

Aplikasi akan berjalan di `http://localhost:5000`.

## Struktur Proyek

```
aes/
  constants.py       S-Box, RCON, matrix MixColumns/InvMixColumns
  utils.py           Konversi hex/byte/state, operasi Galois Field, dll
  state.py           Representasi state matrix 4x4
  sub_bytes.py        SubBytes / InvSubBytes
  shift_rows.py        ShiftRows / InvShiftRows
  mix_columns.py       MixColumns / InvMixColumns
  add_round_key.py     AddRoundKey
  key_expansion.py     Key expansion 128-bit (44 word, 11 round key)
  history.py           Recorder untuk visualisasi tiap langkah
  encrypt.py            Orkestrasi proses enkripsi
  decrypt.py            Orkestrasi proses dekripsi
app.py                 Flask backend & routing
templates/index.html   Halaman utama
static/css/style.css   Styling
static/js/script.js    Logika frontend (fetch API, render visualisasi)
test_*.py              Unit test manual untuk tiap modul
```

## API

### `POST /encrypt`
Body: `{ "plaintext": "...", "key": "32 digit hex" }`
Response: `{ "success": true, "data": { "ciphertext", "history", "round_keys", "key_steps", "matrix" } }`

### `POST /decrypt`
Body: `{ "ciphertext": "32 digit hex", "key": "32 digit hex" }`
Response: `{ "success": true, "data": { "plaintext", "history", "round_keys", "key_steps", "matrix" } }`

## Catatan

- Plaintext maksimal 16 byte (1 blok AES). Jika lebih pendek, akan di-pad
  dengan byte `0x00`.
- Key harus berupa string hexadecimal 32 digit (16 byte / AES-128).
