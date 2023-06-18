from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt_file(file_path, encryption_key, output_path):
    cipher = AES.new(encryption_key, AES.MODE_ECB)
    with open(file_path, 'rb') as file:
        plaintext = file.read()
    padded_plaintext = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    with open(output_path, 'wb') as file:
        file.write(ciphertext)

def decrypt_file(file_path, encryption_key, output_path):
    cipher = AES.new(encryption_key, AES.MODE_ECB)
    with open(file_path, 'rb') as file:
        ciphertext = file.read()
    decrypted = cipher.decrypt(ciphertext)
    plaintext = unpad(decrypted, AES.block_size)
    with open(output_path, 'wb') as file:
        file.write(plaintext)

def read_key_from_file(key_file_path):
    with open(key_file_path, 'rb') as file:
        encryption_key = file.read()
    return encryption_key

