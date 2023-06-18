import os

def generate_key(key_length, output_path):
    # Generate a random key of the specified length
    key = os.urandom(key_length)

    # Save the key to the specified output file
    with open(output_path, 'wb') as file:
        file.write(key)

    print(f"Key saved to {output_path}")

