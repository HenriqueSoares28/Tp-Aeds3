from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad

def encrypt_file(file_path, encryption_key, output_path):
    rsa_key = RSA.import_key(encryption_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    with open(file_path, 'rb') as file:
        plaintext = file.read()
    ciphertext = cipher_rsa.encrypt(plaintext)
    with open(output_path, 'wb') as file:
        file.write(ciphertext)

def decrypt_file(file_path, encryption_key, output_path):
    rsa_key = RSA.import_key(encryption_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    with open(file_path, 'rb') as file:
        ciphertext = file.read()
    decrypted = cipher_rsa.decrypt(ciphertext)
    with open(output_path, 'wb') as file:
        file.write(decrypted)

def generate_key_pair(key_size, private_key_path, public_key_path):
    key = RSA.generate(key_size)
    private_key = key.export_key()
    with open(private_key_path, 'wb') as file:
        file.write(private_key)
    public_key = key.publickey().export_key()
    with open(public_key_path, 'wb') as file:
        file.write(public_key)

# Usage example:
file_path = 'binary_file.bin'
private_key_path = 'private_key.bin'
public_key_path = 'public_key.bin'
encrypted_file_path = 'encrypted.bin'
decrypted_file_path = 'decrypted.bin'

# Generate RSA key pair (you can run this once and then reuse the keys)
generate_key_pair(2048, private_key_path, public_key_path)

# Encrypt the binary file using the public key
with open(public_key_path, 'rb') as file:
    encryption_key = file.read()
encrypt_file(file_path, encryption_key, encrypted_file_path)

# Decrypt the encrypted binary file using the private key
with open(private_key_path, 'rb') as file:
    encryption_key = file.read()
decrypt_file(encrypted_file_path, encryption_key, decrypted_file_path)
