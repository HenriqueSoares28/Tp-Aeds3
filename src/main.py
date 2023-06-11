from CRUD import *
from path import *
from hash import ExtendibleHashing
from hash import save_hash, read_hash, load_hash
from Crashes import save_crashes_to_file, load_crashes_from_file

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


def main():
    # Run the CRUD menu
    while True:
        menu(file_path)

if __name__ == '__main__':
    main()
