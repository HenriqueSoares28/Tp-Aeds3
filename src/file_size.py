import os

def get_file_size(file_path):
    try:
        file_size = os.path.getsize(file_path)
        return file_size
    except FileNotFoundError:
        print("File not found.")
        return 0

