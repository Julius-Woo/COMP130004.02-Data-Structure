def insertionSort(array):
    n = len(array)
    for j in range(1,n):
        key = array[j] # key is the value we are trying to insert
        i = j - 1 # i is the index of the value to the left of key
        while i >= 0 and key < array[i]: # while i is not out of bounds and key is less than the value to the left of it
            array[i+1] = array[i] # move the value to the left of key one index to the right
            i = i - 1
        array[i+1] = key # insert key into the correct position
    return array