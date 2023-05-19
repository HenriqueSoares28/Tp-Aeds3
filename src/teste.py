import heapq
import os
import csv


class HuffmanNode:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency


def build_frequency_table(data):
    frequency_table = {}
    for char in data:
        frequency_table[char] = frequency_table.get(char, 0) + 1
    return frequency_table


def build_huffman_tree(frequency_table):
    priority_queue = []
    for char, frequency in frequency_table.items():
        node = HuffmanNode(char, frequency)
        heapq.heappush(priority_queue, node)

    while len(priority_queue) > 1:
        left_node = heapq.heappop(priority_queue)
        right_node = heapq.heappop(priority_queue)
        merged_node = HuffmanNode(None, left_node.frequency + right_node.frequency)
        merged_node.left = left_node
        merged_node.right = right_node
        heapq.heappush(priority_queue, merged_node)

    return heapq.heappop(priority_queue)


def build_huffman_codes_helper(node, current_code, huffman_codes):
    if node is None:
        return

    if node.char is not None:
        huffman_codes[node.char] = current_code
        return

    build_huffman_codes_helper(node.left, current_code + "0", huffman_codes)
    build_huffman_codes_helper(node.right, current_code + "1", huffman_codes)


def build_huffman_codes(huffman_tree):
    huffman_codes = {}
    build_huffman_codes_helper(huffman_tree, "", huffman_codes)
    return huffman_codes


def compress_data(data, huffman_codes):
    compressed_data = ""
    for char in data:
        compressed_data += huffman_codes[char]
    return compressed_data


def pad_encoded_data(encoded_data):
    padding_amount = 8 - (len(encoded_data) % 8)
    encoded_data += padding_amount * "0"

    padding_info = "{0:08b}".format(padding_amount)
    encoded_data = padding_info + encoded_data
    return encoded_data


def get_byte_array(padded_encoded_data):
    if len(padded_encoded_data) % 8 != 0:
        raise ValueError("Padded encoded data is not a multiple of 8 bits")

    b = bytearray()
    for i in range(0, len(padded_encoded_data), 8):
        byte = padded_encoded_data[i:i + 8]
        b.append(int(byte, 2))
    return b


def compress_file(input_file, output_file):
    with open(input_file, 'r') as file:
        data = file.read()

    frequency_table = build_frequency_table(data)
    huffman_tree = build_huffman_tree(frequency_table)
    huffman_codes = build_huffman_codes(huffman_tree)
    compressed_data = compress_data(data, huffman_codes)
    padded_encoded_data = pad_encoded_data(compressed_data)
    byte_array = get_byte_array(padded_encoded_data)

    with open(output_file, 'wb') as file:
        file.write(bytes(byte_array))

    print("File compressed and saved as", output_file)


def remove_padding(padded_encoded_data):
    padding_info = padded_encoded_data[:8]
    padding_amount = int(padding_info, 2)
    padded_encoded_data = padded_encoded_data[8:]
    encoded_data = padded_encoded_data[:-padding_amount]
    return encoded_data


def decode_data(encoded_data, huffman_tree):
    decoded_data = ""
    current_node = huffman_tree

    for bit in encoded_data:
        if bit == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decoded_data += current_node.char
            current_node = huffman_tree

    return decoded_data


def decompress_file(input_file, output_file):
    with open(input_file, 'rb') as file:
        bit_string = ""
        byte = file.read(1)
        while byte != b"":
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = file.read(1)

    encoded_data = remove_padding(bit_string)
    huffman_tree = build_huffman_tree(build_frequency_table(encoded_data))
    decoded_data = decode_data(encoded_data, huffman_tree)

    with open(output_file, 'w') as file:
        file.write(decoded_data)

    print("File decompressed and saved as", output_file)


# Usage example
input_csv = 'data\QuedasCsv.csv'
compressed_file = 'compressed.bin'
decompressed_csv = 'decompressed.csv'

# Compressing the CSV file
with open(input_csv, 'r') as file:
    reader = csv.reader(file)
    data = ''.join(''.join(row) for row in reader)

compress_file(input_csv, compressed_file)

# Decompressing the file
decompress_file(compressed_file, decompressed_csv)
