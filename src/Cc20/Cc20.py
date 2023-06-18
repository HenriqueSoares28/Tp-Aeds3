from Crypto.Cipher import ChaCha20, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def encrypt_file(file_path, encryption_key, output_path):
    # Generate a random ChaCha20 encryption key and nonce
    chacha_key = get_random_bytes(32)
    nonce = get_random_bytes(8)

    # Encrypt the file using ChaCha20
    cipher_chacha = ChaCha20.new(key=chacha_key, nonce=nonce)
    with open(file_path, 'rb') as file:
        plaintext = file.read()
    ciphertext = cipher_chacha.encrypt(plaintext)

    # Encrypt the ChaCha20 key and nonce using RSA
    rsa_key = RSA.import_key(encryption_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    encrypted_key = cipher_rsa.encrypt(chacha_key + nonce)

    # Write the encrypted key and ciphertext to the output file
    with open(output_path, 'wb') as file:
        file.write(encrypted_key)
        file.write(ciphertext)

def decrypt_file(file_path, encryption_key, output_path):
    # Read the encrypted key and ciphertext from the file
    with open(file_path, 'rb') as file:
        encrypted_key = file.read(256)
        ciphertext = file.read()

    # Decrypt the ChaCha20 key and nonce using RSA
    rsa_key = RSA.import_key(encryption_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    chacha_key_nonce = cipher_rsa.decrypt(encrypted_key)
    chacha_key = chacha_key_nonce[:32]
    nonce = chacha_key_nonce[32:]

    # Decrypt the ciphertext using ChaCha20
    cipher_chacha = ChaCha20.new(key=chacha_key, nonce=nonce)
    plaintext = cipher_chacha.decrypt(ciphertext)

    # Write the decrypted plaintext to the output file
    with open(output_path, 'wb') as file:
        file.write(plaintext)


# Generate RSA key pair (you can run this once and then reuse the keys)
def generateKey(key_file_path):
    key = RSA.generate(2048)
    private_key = key.export_key()
    with open(key_file_path, 'wb') as file:
        file.write(private_key)

def read_key_from_file(key_file_path):
    with open(key_file_path, 'rb') as file:
        encryption_key = file.read()
    return encryption_key