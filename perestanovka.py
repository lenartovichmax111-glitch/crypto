text = input("Введіть текст: ").upper().replace(" ", "")
key = input("Введіть ключ: ").upper()

original_length = len(text)


while len(text) % len(key) != 0:
    text += "Х"


order = []

for char in sorted(key):
    for i in range(len(key)):
        if key[i] == char and i not in order:
            order.append(i)
            break

encrypted = ""

for col in order:
    for i in range(col, len(text), len(key)):
        encrypted += text[i]


decrypted = [""] * len(text)
pos = 0

for col in order:
    for i in range(col, len(text), len(key)):
        decrypted[i] = encrypted[pos]
        pos += 1

decrypted = "".join(decrypted)
decrypted = decrypted[:original_length]

print("\nПочатковий текст:", text[:original_length])
print("Ключ:", key)
print("Зашифрований текст:", encrypted)
print("Розшифрований текст:", decrypted)