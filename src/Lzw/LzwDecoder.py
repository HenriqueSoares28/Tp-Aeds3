from struct import *
from path import *

def decompress_file(input_file, n):
    # defining the maximum table size
    # opening the compressed file
    # defining variables
    maximum_table_size = pow(2, int(n))
    file = open(input_file, "rb")
    compressed_data = []
    next_code = 256
    decompressed_data = ""
    string = ""

    # Reading the compressed file.
    while True:
        rec = file.read(2)
        if len(rec) != 2:
            break
        (data,) = unpack('>H', rec)
        compressed_data.append(data)

    # Building and initializing the dictionary.
    dictionary_size = 256
    dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])

    # iterating through the codes.
    # LZW Decompression algorithm
    for code in compressed_data:
        if not (code in dictionary):
            dictionary[code] = string + (string[0])
        decompressed_data += dictionary[code]
        if not (len(string) == 0):
            dictionary[next_code] = string + (dictionary[code][0])
            next_code += 1
        string = dictionary[code]

    # storing the decompressed string into a file.

    output_file = open(get_lzw_decompressed_file_path(), "w", encoding="ISO-8859-1")
    for data in decompressed_data:
        output_file.write(data)

    output_file.close()
    file.close()

