import heapq
from file_size import get_file_size# just for test
from collections import Counter, namedtuple


class HuffmanNode(namedtuple('HuffmanNode', ['left', 'right'])):
    def __lt__(self, other):
        return True


class HuffmanLeaf(namedtuple('HuffmanLeaf', ['char'])):
    def __lt__(self, other):
        return True


def build_huffman_tree(freq_table):
    heap = []
    for char, freq in freq_table.items():
        heapq.heappush(heap, (freq, len(heap), HuffmanLeaf(char)))

    while len(heap) > 1:
        freq1, _, left = heapq.heappop(heap)
        freq2, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (freq1 + freq2, len(heap), HuffmanNode(left, right)))

    return heap[0][2]


def build_freq_table(text):
    freq_table = Counter(text)
    return freq_table


def build_huffman_codes(node, prefix='', code_table={}):
    if isinstance(node, HuffmanLeaf):
        code_table[node.char] = prefix
    elif isinstance(node, HuffmanNode):
        build_huffman_codes(node.left, prefix + '0', code_table)
        build_huffman_codes(node.right, prefix + '1', code_table)

    return code_table


def encode(text, code_table):
    encoded_text = ''
    for char in text:
        encoded_text += code_table[char]
    return encoded_text

# huffman decode function
def decode(encoded_text, huffman_tree):
    decoded_text = ''
    current_node = huffman_tree

    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if isinstance(current_node, HuffmanLeaf):
            decoded_text += current_node.char
            current_node = huffman_tree

    return decoded_text

# huffman compress function
def huffman_compress(text):
    freq_table = build_freq_table(text)
    huffman_tree = build_huffman_tree(freq_table)
    code_table = build_huffman_codes(huffman_tree)
    encoded_text = encode(text, code_table)

    return encoded_text, code_table

# huffman decompress function
def huffman_decompress(encoded_text, code_table):
    reversed_code_table = {code: char for char, code in code_table.items()}
    decoded_text = ''
    current_code = ''

    for bit in encoded_text:
        current_code += bit
        if current_code in reversed_code_table:
            decoded_text += reversed_code_table[current_code]
            current_code = ''

    return decoded_text


# write data to file
# frist the encoded text and then the code table

def write_to_file(file_path, encoded_text, code_table):
    with open(file_path, 'w') as file:
        file.write(encoded_text + '\n')
        for char, code in code_table.items():
            file.write(f'{char}:{code}\n')


# read data from file
# first the encoded text and then the code table
def read_from_file(file_path):
    code_table = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        encoded_text = lines[0].strip()
        for line in lines[1:]:
            char, code = line.strip().split(':')
            code_table[char] = code

    return encoded_text, code_table






''' # Example usage:
text = 'Hello, World!'
encoded_text, code_table = huffman_compress(text)

# Write the encoded text and code table to a file
file_path = 'compressed_data.txt'
write_to_file(file_path, encoded_text, code_table)
print('Data written to file:', file_path)

# Read the encoded text and code table from the file
read_encoded_text, read_code_table = read_from_file(file_path)
print('Encoded text read from file:', read_encoded_text)
print('Code table read from file:', read_code_table)

# Decompress using the read encoded text and code table
decoded_text = huffman_decompress(read_encoded_text, read_code_table)
print('Decoded text:', decoded_text)


compress_file_size = get_file_size(file_path)
print('File size:', compress_file_size, 'bytes')

file_size = get_file_size('data\QuedasCsv.bin')
print('File size:', file_size, 'bytes') '''

