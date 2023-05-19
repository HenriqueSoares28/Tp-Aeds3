from CRUD import *
from path import *
from hash import ExtendibleHashing
from hash import save_hash, read_hash, load_hash
from Crashes import save_crashes_to_file, load_crashes_from_file
import json

import csv

import clear


from Huffman import *
from file_size import get_file_size

clear.clear_terminal()

file_path = get_file_path()
index_file_path = get_index_file_path()
hash_file_path = get_hash_file_path()


# Create an empty list to hold the crashes
quedasArray = []

# Open the CSV file and read the data into a list of Crash objects

with open("data/QuedasCsv.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        quedas = Crashes(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
        quedasArray.append(quedas)
        
# Iterate over the list and fix the Ids
for i, crash in enumerate(quedasArray):
    crash.id = i


# Save the list to a binary file
save_crashes_to_file(quedasArray, file_path)
crashes = load_crashes_from_file(file_path)



# creating the index
tree = create_index(file_path)
# saving the index to a binary file
save_index(tree, index_file_path)

# loading the index from a binary file
load_index = load_index(index_file_path)

# creating the extended hash index
hash_table = ExtendibleHashing()
    
# inserting the data into the hash table
for i in load_index:
    hash_table.put(i, load_index[i])

# saving the hash table to a binary file
save_hash(hash_table, hash_file_path)

# loading the hash table from a binary file to a unique string

#------------------------------------------------------------------------------
#TODO   CORRIGIR TUDO ABAIXO, referente a compressão de dados Huffman

json_data = {'data': []}
for c in crashes:
    json_data['data'].append(c.__dict__())
with open(get_json_file_path(), 'w') as outfile:
    json.dump(json_data, outfile)

# load the json file as a string
with open(get_json_file_path(), 'r') as f:
    json_data = json.load(f)
    json_string = json.dumps(json_data)
    



encoded_text, code_table = huffman_compress(json_string)

# Write the encoded text and code table to a file
huffman_file_path = 'data/compressed_data.txt'
write_to_file(huffman_file_path, encoded_text, code_table)
print('Data written to file:', huffman_file_path)

print(f'The original file size is {get_file_size(get_json_file_path())} bytes')
print(f'The compressed file size is {get_file_size(huffman_file_path)} bytes')
print(f'The percentage of compression is {round((1 - get_file_size(huffman_file_path) / get_file_size(get_json_file_path())) * 100, 2)}%')

''' # Read the encoded text and code table from the file
read_encoded_text, read_code_table = read_from_file(huffman_file_path)
print('Encoded text read from file:', read_encoded_text)
print('Code table read from file:', read_code_table)

# Decompress using the read encoded text and code table
decoded_text = huffman_decompress(read_encoded_text, read_code_table)
print('Decoded text:', decoded_text) '''
#------------------------------------------------------------------------------

# Run the CRUD menu
while True:
    menu(file_path)
