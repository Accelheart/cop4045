# a
def caesar_cipher(text, shift):
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    encrypted = ""

    for char in text:
        if char in lowercase:
            index = lowercase.index(char)
            new_index = (index + shift) % 26
            encrypted += lowercase[new_index]

        elif char in uppercase:
            index = uppercase.index(char)
            new_index = (index + shift) % 26
            encrypted += uppercase[new_index]

        else:
            encrypted += char

    return encrypted

#b
def caesar_decipher(cyphertext, shift):
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cleartext = ""

    for char in cyphertext:
        if char in lowercase:
            index = lowercase.index(char)
            new_index = (index - shift) % 26
            cleartext += lowercase[new_index]

        elif char in uppercase:
            index = uppercase.index(char)
            new_index = (index - shift) % 26
            cleartext += uppercase[new_index]

        else:
            cleartext += char

    return cleartext

#c
def letter_frequency(text):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    frequencies = {}

    for letter in alphabet:
        frequencies[letter] = 0

    for char in text:
        char = char.lower()

        if char in alphabet:
            frequencies[char] += 1

    return frequencies

#d
def main():
    print("Caesar Cipher Program")
    print("---------------------")

    message = input("Enter a message: ")
    shift = int(input("Enter a shift value: "))

    ciphered_text = caesar_cipher(message, shift)

    print("\nCiphered text:")
    print(ciphered_text)

    print("\nLetter frequency:")
    frequencies = letter_frequency(ciphered_text)

    for letter in frequencies:
        print(letter, ":", frequencies[letter])

    deciphered_text = caesar_decipher(ciphered_text, shift)

    print("\nDeciphered text:")
    print(deciphered_text)


main()