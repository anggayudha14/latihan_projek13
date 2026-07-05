from aes.encrypt import AESEncrypt

plaintext = "Two One Nine Two"

key = "5468617473206D79204B756E67204675"

aes = AESEncrypt(plaintext, key)

result = aes.encrypt()

print("="*50)
print("CIPHERTEXT")
print("="*50)

print(result["ciphertext"])

print()

print("="*50)
print("ROUND")
print("="*50)

for item in result["history"]:

    if "round" in item:

        print("Round :", item["round"])