from aes.key_expansion import KeyExpansion

# AES-128 Key
key = "2B7E151628AED2A6ABF7158809CF4F3C"

ke = KeyExpansion(key)

round_keys = ke.generate_round_keys()

print("=" * 50)
print("AES KEY EXPANSION TEST")
print("=" * 50)

print("Jumlah Word      :", len(ke.words))
print("Jumlah RoundKey  :", len(round_keys))
print("Jumlah Steps     :", len(ke.get_steps()))

print("\nRound Key 0")
print(round_keys[0])

print("\nRound Key 10")
print(round_keys[10])