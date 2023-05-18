from inverted_list import InvertedList
from CRUD import load_crashes_from_file
from path import *
file_path = get_file_path()

# Initialize new inverted list.
iList1 = InvertedList()
iList2 = InvertedList()


#================================ Inverted List 1 =================================

# Create an inverted list based on the crashes operator.
crashes = load_crashes_from_file(file_path)

# Save all operators to the inverted list.
for c in crashes:
    iList1.add_item(c.id, [c.operator])

# return the list of document IDs that contain the key operator.
def search_operator(operator):
    result = iList1.get_items(operator)
    print(result)

#================================ Inverted List 1 =================================

# Create an inverted list based on the crashes year.
crashes = load_crashes_from_file(file_path)

# Save all operators to the inverted list.
for c in crashes:
    iList2.add_item(c.id, [c.get_year()])

# return the list of document IDs that contain the key year.
def search_year(year):
    result = iList2.get_items(year)
    print(result)