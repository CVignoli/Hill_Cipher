import numpy as np
import string
from sympy import Matrix


def letterToNumber(letter):  # trasforma le lettere nella corrispettiva posizione nell' alfabeto (a -> 0, b_-> 1, .. )
    return string.ascii_lowercase.index(letter)


def numberToLetter(number):  # inverso di letterToNumber
    alphabeth = string.ascii_lowercase
    letter = alphabeth[number]
    return letter


def encrypt(message, key):  # funzione che cripta il messaggio data la chiave
    message = np.array(message)
    message_length = message.shape[0]

    encryption = np.asarray([])
    for i in range(0, message_length, key.shape[0]):
        encryption = np.append(encryption, np.matmul(key, message[i:i + key.shape[0]])).astype(
            int) % 26  # si considerano m lettere alla volta
    return encryption


def decrypt(encryption, key):  # funzione che decripta la cifratura data la chiave
    decrypted_lenght = encryption.shape[0]
    inverse_key = Matrix(key).inv_mod(26)
    inverse_key = np.array(inverse_key)

    decryption = np.asarray([])
    for i in range(0, decrypted_lenght, inverse_key.shape[0]):
        decryption = np.append(decryption, np.matmul(inverse_key, encryption[i:i + inverse_key.shape[0]])).astype(
            int) % 26  # si considerano m lettere alla volta

    decrypted_message = ""
    for i in range(0, len(decryption)):
        letter_num = int(decryption[i])
        letter = numberToLetter(int(decryption[i]))
        decrypted_message = decrypted_message + letter
    return decrypted_message


def attack_Hill(plaintext, ciphertext, m):  # funzione che prova l'attacco al cifrario di Hill
    plaintext.resize((len(plaintext) // m, m))
    ciphertext.resize((len(ciphertext) // m, m))
    p_star = np.asarray([]).astype(int)
    c_star = np.asarray([]).astype(int)
    for i in range(m):
        p_star = np.concatenate((p_star, plaintext[i]))
        c_star = np.concatenate((c_star, ciphertext[i]))
    p_star.resize((m, m))
    c_star.resize((m, m))
    p_star = np.transpose(p_star)
    c_star = np.transpose(c_star)
    inverse_p_star = Matrix(p_star).inv_mod(26)
    key = np.matmul(c_star, inverse_p_star) % 26
    return key


key = np.array([
    [7, 8],
    [19, 3]
])

print("Key :", key.flatten())

key_f = key.flatten()
key_text = []
key_text = np.asarray(key_text)

for i in range(0, len(key_f)):
    key_text = np.append(key_text, numberToLetter(key_f[i]))
print("Key as text:", key_text)

key_rows = key.shape[0]
key_columns = key.shape[1]

if key_rows != key_columns:
    raise Exception('key must be square matrix!')

if np.linalg.det(key) == 0:
    raise Exception('matrix must have an inverse matrix')

raw_message = "friday"
print("Plaintext:", raw_message)

message = []

for i in range(0, len(raw_message)):
    current_letter = raw_message[i:i + 1].lower()
    if current_letter != ' ':  # rimuove gli spazi
        letter_index = letterToNumber(current_letter)
        message.append(letter_index)

if len(message) % key_rows != 0:  #
    for i in range(0, len(message)):
        message.append(message[i])
        if len(message) % key_rows == 0:
            break

encryption = encrypt(message, key)

# ........... codice per mostrare il ciphertext come sequenza di lettere ...........

c_text = encryption.flatten()
ciphertext = []
ciphertext = np.asarray(ciphertext)

for i in range(0, len(c_text)):
    ciphertext = np.append(ciphertext, numberToLetter(c_text[i]))
print("Ciphertext as text:", ciphertext)

# ................

decrypted_message = decrypt(encryption, key)

print("Decrypted message : " + decrypted_message)

key = attack_Hill(np.array(message), encryption, key_rows)

print("Key from attack: ", key.flatten())
