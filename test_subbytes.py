from aes.sub_bytes import SubBytes

state = [
    [0x19,0xA0,0x9A,0xE9],
    [0x3D,0xF4,0xC6,0xF8],
    [0xE3,0xE2,0x8D,0x48],
    [0xBE,0x2B,0x2A,0x08]
]

before, after = SubBytes.encrypt(state)

print("===== BEFORE =====")
for row in before:
    print(" ".join(f"{x:02X}" for x in row))

print()

print("===== AFTER =====")
for row in after:
    print(" ".join(f"{x:02X}" for x in row))
