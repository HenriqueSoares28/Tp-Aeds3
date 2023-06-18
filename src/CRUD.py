import struct
import pickle
from bintrees import FastRBTree


from hash import read_hash

from Crashes import *

from path import *
file_path = get_file_path()
csv_file_path = get_csv_file_path()
index_file_path = get_index_file_path()
hash_file_path = get_hash_file_path()

from iList import search_operator, search_year

from Lzw import LzwEncoder as lzwE
from Lzw import LzwDecoder as lzwD

from Huffman import huffman as huf

from Kmp import Kmp as kmp
from Bmh import Bmh as bmh


from file_size import get_file_size



    
    
    
#----Arvore B----#

# Create a binary file with the list of crashes positions in the file
def create_index(file_path):
    crashes = load_crashes_from_file(file_path)
    index = FastRBTree()
    position = 0
    for c in crashes:
        index[c.id] = position
        position += c.get_size()
    return index

# Save the index to a binary file
def save_index(index, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(index, f)
        
# Load the index from a binary file
def load_index(file_path):
    with open(file_path, 'rb') as f:
        index = pickle.load(f)
    return index

# Search for a crash in the index
def search_index(index, id):
    return int(index.get(id)) 

def read_index(file_path, index_file_path, id):
    position = search_index(load_index(index_file_path), id)
    with open(file_path, 'rb') as f:
        content = f.read()
        i = position 
        try:
            valid = struct.unpack('?', content[i:i+1])[0]
            i += 1
            id = struct.unpack('i', content[i:i+4])[0]
            i += 4
            date_len = struct.unpack('i', content[i:i+4])[0]
            i += 4
            date = content[i:i+date_len].decode(errors='ignore')
            i += date_len
            time_len = struct.unpack('i', content[i:i+4])[0]
            i += 4
            time = content[i:i+time_len].decode(errors='ignore')
            i += time_len
            location_len = struct.unpack('i', content[i:i+4])[0]
            i += 4
            location = content[i:i+location_len].decode(errors='ignore')
            i += location_len
            operator_len = struct.unpack('i', content[i:i+4])[0]
            i += 4
            operator = content[i:i+operator_len].decode(errors='ignore')
            i += operator_len
            flight_len = struct.unpack('i', content[i:i+4])[0]
            i += 4
            flight = content[i:i+flight_len].decode(errors='ignore')
            i += flight_len
            route_len = struct.unpack('i', content[i:i+4])[0]
            i += 4
            route = content[i:i+route_len].decode(errors='ignore')
            i += route_len
            model_len = struct.unpack('i', content[i:i+4])[0]
            i += 4
            model = content[i:i+model_len].decode(errors='ignore')
            i += model_len
            aboard = struct.unpack('i', content[i:i+4])[0]
            i += 4
            fatalities = struct.unpack('i', content[i:i+4])[0]
            i += 4
            c = Crashes(id, date, time, location, operator, flight, route, model, aboard, fatalities)
            if valid:
                return(c)
            else:
                return None
        except:
            pass
        

#----Arvore Binaria----#



    




#=======================================================-- CRUD --=======================================================


 

#=======================================================-- CRUD --=======================================================

#returns the next available id
def get_next_id(file_path):
    crashes = load_crashes_from_file(file_path)
    return len(crashes) + 1

# user input for creating a new crash
def write_crash(id):
    date = input("Enter crash date: ")
    time = input("Enter crash time: ")
    location = input("Enter crash location: ")
    operator = input("Enter operator: ")
    flight = input("Enter flight number: ")
    route = input("Enter flight route: ")
    model = input("Enter aircraft model: ")
    aboard = int(input("Enter number aboard: "))
    fatalities = int(input("Enter number of fatalities: "))
    return Crashes(id, date, time, location, operator, flight, route, model, aboard, fatalities)

# prints the menu
def menu(file_path):
    print()
    print("Select an option:")
    print("1. Create a new crash")
    print("2. Read an existing crash")
    print("3. Update an existing crash")
    print("4. Delete an existing crash")
    print("5. Sort crashes by id")
    print("6. Read an existing crash using index file")
    print("7. Read an existing crash using hash file")
    print("8. Show all ids determined by a given operator")
    print("9. Show all ids that occur in some year")
    print("10. Compress file using LZW")
    print("11. Decompress file using LZW")
    print("12. Compress file using Huffman")
    print("13. Decompress file using Huffman")
    print("14. Find a pattern using KMP")
    print("15. Find a pattern using BMH")
    print("16. Exit")

    option = int(input("Enter option number: "))

    if option == 1:
        next_id = get_next_id(file_path)
        new_crash = write_crash(next_id)
        create_crash(file_path, new_crash)
        print(f"Crash created successfully. Id = {next_id}")

    elif option == 2:
        id = int(input("Enter crash id: "))
        crash = read_crash(file_path, id)
        if crash:
            print(crash)
        else:
            print("Crash not found.")

    elif option == 3:
        id = int(input("Enter crash id: "))
        new_crash = write_crash(id=id)
        update_crash(file_path, id, new_crash)

    elif option == 4:
        id = int(input("Enter crash id: "))
        delete_crash(file_path, id)

    elif(option == 5):
        crashes = load_crashes_from_file(file_path)
        crashes.sort(key=lambda x: x.id)
        save_crashes_to_file(crashes, file_path)
        print("Crashes sorted by id.")
    
    elif(option == 6):
        id = int(input("Enter crash id: "))
        print(read_index(file_path, index_file_path, id))
        
    elif(option == 7):
        id = int(input("Enter crash id: "))
        print(read_hash(file_path, hash_file_path, id))
        
    elif(option == 8):
        operator = input("Enter operator: ")
        print(search_operator(operator))
    
    elif(option == 9):
        year = int(input("Enter year: "))
        print(search_year(year))
        
    elif option == 10:
        compressFilePath = get_lzw_compressed_file_path()
        lzwE.compress_file(file_path, 12)
        print("File compressed successfully.")
        print('Normal file size:', get_file_size('data\QuedasCsv.bin'), 'bytes')
        print('Compressed file size:', get_file_size(compressFilePath), 'bytes')
        print('Percentage of compression: {:.2f}%'.format(100 - round((get_file_size(compressFilePath)/get_file_size('data\QuedasCsv.bin'))*100, 2)))
    
    elif option == 11:
        compressFile = get_lzw_compressed_file_path()
        lzwD.decompress_file(compressFile, 12)
        print("File decompressed successfully.")
        id = int(input("Enter crash id to search: "))
        crash = read_crash(file_path, id)
        print(crash)
        
    elif option == 12:
        compressFilePath = get_huf_compressed_file_path()
        with open(file_path, 'rb') as f:
            binary_data = f.read()
        frequency_dic = huf.calculate_frequency(binary_data)
        encoding, code_book = huf.create_encoding(frequency_dic, binary_data)
        output_file = compressFilePath
        huf.write_binary_encoding(encoding, output_file)
        print("File compressed successfully.")
        print('Normal file size:', get_file_size(get_file_path()), 'bytes')
        print('Compressed file size:', get_file_size(compressFilePath), 'bytes')
        print('Percentage of compression: {:.2f}%'.format(100 - round((get_file_size(compressFilePath)/get_file_size(get_file_path()))*100, 2)))
    
        code_book_file = get_code_book_file_path()
        huf.write_code_book(code_book, code_book_file)
    elif option == 13:
        compressFilePath = get_huf_compressed_file_path()
        code_book_file = get_code_book_file_path()
        

        decoded_data = huf.decode_file(code_book_file, compressFilePath)
        decompressFilePath = get_huf_decompressed_file_path()
        with open(decompressFilePath, "wb") as file:
            file.write(decoded_data)
        print('Decompressed file successfully') 
        
        id = int(input("Enter crash id to search: "))
        crash = read_crash(decompressFilePath, id)
        print(crash)
        
    elif option == 14:
        key = input("Enter pattern to search using KMP: ")
        kmp.find_matches(csv_file_path, key)
    
    elif option == 15:
        key = input("Enter pattern to search using BMH: ")
        bmh.find_matches(csv_file_path, key)
        
        
    elif option == 16:
        exit()

    else:
        print("Invalid option. Please try again.")


