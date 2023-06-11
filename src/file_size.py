import os

def get_file_size(file_path):
    try:
        file_size = os.path.getsize(file_path)
        return file_size
    except FileNotFoundError:
        print("File not found.")
        return 0

def compare_file_size(file_path1, file_path2):
    print('Normal file size:', get_file_size(file_path1), 'bytes')
    print('Compressed file size:', get_file_size('file_path2'), 'bytes')
    print('Percentage of compression: {:.2f}%'.format(100 - round((get_file_size('file_path2')/get_file_size(file_path1))*100, 2)))
    