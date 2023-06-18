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

# Usage example:
file_path = 'data/QuedasCsv.bin'
key_file_path = 'data/aes/aes_encryption_key.key'
encrypted_file_path = 'data/aes/aes_encrypted.bin'
decrypted_file_path = 'data/aes/aes_decrypted.bin'

# Read the key from the file
encryption_key = read_key_from_file(key_file_path)

# Encrypt the binary file
encrypt_file(file_path, encryption_key, encrypted_file_path)

# Decrypt the encrypted binary file
decrypt_file(encrypted_file_path, encryption_key, decrypted_file_path)
