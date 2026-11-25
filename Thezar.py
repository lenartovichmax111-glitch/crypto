a = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
k = 3
text = input("Введіть текст: ")

def encrypt(text):
    result = ""

    for char in text:
        if char.upper() in a:
            index = a.index(char.upper())
            new_index = (index + k) % len(a)
            new_char = a[new_index]

            if char.islower():
                new_char = new_char.lower()

            result += new_char
        else:
            result += char
    return result


def decrypt(text):
    result = ""

    for char in text:
        if char.upper() in a:
            index = a.index(char.upper())
            new_index = (index - k) % len(a)
            new_char = a[new_index]

            if char.islower():
                new_char = new_char.lower()

            result += new_char
        else:
            result += char
    return result

encrypted = encrypt(text)
decrypted = decrypt(encrypted)




















print("\nПочатковий текст:", text)
print("Зашифрований текст:", encrypted)
print("Розшифрований текст:", decrypted)
