import math
from CRUD import *


#Intercalação balanceada comum
def balanced_merge_sort(crashes, file_path):
    if len(crashes) <= 1:
        return crashes

    mid = len(crashes) // 2

    left_half = crashes[:mid]
    right_half = crashes[mid:]

    left_half = balanced_merge_sort(left_half, file_path)
    right_half = balanced_merge_sort(right_half, file_path)

    return balanced_merge(left_half, right_half, file_path)

#merge two sorted lists
def balanced_merge(left_half, right_half, file_path):
    i = j = 0
    result = []

    while i < len(left_half) and j < len(right_half):
        if left_half[i].id <= right_half[j].id:
            result.append(left_half[i])
            i += 1
        else:
            result.append(right_half[j])
            j += 1

    while i < len(left_half):
        result.append(left_half[i])
        i += 1

    while j < len(right_half):
        result.append(right_half[j])
        j += 1

    save_crashes_to_file(result, file_path)

    return result




#Intercalação balanceada com blocos de tamanho variável
#split the list into smaller lists
def split_list(crashes, m):
    split_list = []
    sublist = []
    size = 0
    for crash in crashes:
        if size + sys.getsizeof(crash) > m:
            split_list.append(sublist)
            sublist = []
            size = 0
        sublist.append(crash)
        size += sys.getsizeof(crash)
    if len(sublist) > 0:
        split_list.append(sublist)
    return split_list

# sort by id using merge sort
def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i].id <= right[j].id:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result

#sort by id using merge sort with memory limit
def balanced_merge_sort(crashes, m):
    # Divide a lista em blocos menores
    blocks = split_list(crashes, m)
    # Ordena cada bloco individualmente
    for i in range(len(blocks)):
        blocks[i] = sorted(blocks[i], key=lambda crash: crash.id)
    # Mescla os blocos em pares até restar apenas uma lista
    while len(blocks) > 1:
        new_blocks = []
        for i in range(0, len(blocks), 2):
            if i + 1 < len(blocks):
                merged_block = merge(blocks[i], blocks[i+1])
            else:
                merged_block = blocks[i]
            new_blocks.append(merged_block)
        blocks = new_blocks
    return blocks[0]



#Intercalação balanceada com seleção por substituição
def merge(arr1, arr2):
    i, j = 0, 0
    merged = []
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            merged.append(arr1[i])
            i += 1
        else:
            merged.append(arr2[j])
            j += 1
    merged.extend(arr1[i:])
    merged.extend(arr2[j:])
    return merged

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def selection_sort(arr):
    for i in range(len(arr)):
        min_index = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]

def balanced_merge_sort(arr, threshold):
    if len(arr) <= threshold:
        selection_sort(arr)
        return arr
    mid = len(arr) // 2
    left = balanced_merge_sort(arr[:mid], threshold)
    right = balanced_merge_sort(arr[mid:], threshold)
    return merge(left, right)

def merge_sort_with_selection(arr, threshold):
    n = len(arr)
    subarray_size = threshold
    while subarray_size < n:
        for i in range(0, n, subarray_size*2):
            start = i
            mid = min(start+subarray_size, n)
            end = min(start+subarray_size*2, n)
            arr[start:end] = balanced_merge_sort(arr[start:end], threshold)
        subarray_size *= 2
    arr[:] = balanced_merge_sort(arr, threshold)
