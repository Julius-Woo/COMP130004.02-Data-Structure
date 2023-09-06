import random
k = 25

def insertionSort(array):
    n = len(array)
    for j in range(1,n):
        key = array[j]
        i = j - 1
        while i >= 0 and key < array[i]:
            array[i+1] = array[i]
            i = i - 1
        array[i+1] = key
    return array

def merge(left, right):
    i = j = 0
    result = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]) 
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result

def combineSort(array, k):
    n = len(array)
    if n <= k: # if array size is less than k, use insertion sort
        return insertionSort(array)
    else: # else, split array in half and recursively call combineSort
        mid = n//2
        left = array[:mid]
        right = array[mid:]
        left = combineSort(left, k)
        right = combineSort(right, k)
        return merge(left, right)

arrsize = 50
random.seed(203)
array = [random.randint(0, 100) for _ in range(arrsize)]
print('original array:', array)
print('sorted array:', combineSort(array, k))