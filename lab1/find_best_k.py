import time
import matplotlib.pyplot as plt
import random
from collections import Counter

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

def fine_best_k(arrsize, krange):
    random.seed(203) # set seed to 203
    array = [random.randint(0, 1000000) for _ in range(arrsize)] # generate random array
    best_k = 0
    best_time = 9999999999 # set best time to a rather large number

    for k in krange: # max subarray size for insertion sort
        total_time = 0
        avg_time = 0
        for i in range(1,10): # run 10 times and take average
            start = time.time()
            combineSort(array, k) # call combineSort
            end = time.time()
            total_time += end - start
        avg_time = total_time/10
        
        if avg_time < best_time:
            best_time = avg_time
            best_k = k
    return best_k


sizerange = range(10000, 20000, 500) # array size range
k_record = [] # record best k for each array size
krange = range(10, 51, 2) # max subarray size for insertion sort. The best k mostly lies in 10~50
for arraysize in sizerange:
    k_record.append(fine_best_k(arraysize, krange))
    
count = Counter(k_record)
print(count.most_common(1)[0][0]) # print k with the most frequency
plt.plot(sizerange, k_record, 'b--') # plot array size vs best k
plt.show()
