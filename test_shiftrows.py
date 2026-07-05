from aes.shift_rows import ShiftRows

state = [

    [0xD4,0xE0,0xB8,0x1E],
    [0x27,0xBF,0xB4,0x41],
    [0x11,0x98,0x5D,0x52],
    [0xAE,0xF1,0xE5,0x30]

]

before, after = ShiftRows.encrypt(state)

print("===== BEFORE =====")

for row in before:
    print(" ".join(f"{x:02X}" for x in row))

print()

print("===== AFTER =====")

for row in after:
    print(" ".join(f"{x:02X}" for x in row))
