from struct import *
from path import *

def compress_file(input_file, n):
    # defining the maximum table size
    # opening the input file
    # reading the input file and storing the file data into data variable
    maximum_table_size = pow(2, int(n))
    file = open(input_file, encoding="ISO-8859-1")
    data = file.read()

    # Building and initializing the dictionary.
    dictionary_size = 256
    dictionary = {chr(i): i for i in range(dictionary_size)}
    string = ""             # String is null.
    compressed_data = []    # variable to store the compressed data.

    # iterating through the input symbols.
    # LZW Compression algorithm
    for symbol in data:
        string_plus_symbol = string + symbol  # get input symbol.
        if string_plus_symbol in dictionary:
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            if(len(dictionary) <= maximum_table_size):
                dictionary[string_plus_symbol] = dictionary_size
                dictionary_size += 1
            string = symbol

    if string in dictionary:
        compressed_data.append(dictionary[string])

    # storing the compressed string into a file (byte-wise).
    output_file = open(get_lzw_compressed_file_path(), "wb")
    for data in compressed_data:
        output_file.write(pack('>H', int(data)))

    output_file.close()
    file.close()
