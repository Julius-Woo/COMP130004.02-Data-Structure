def merge(left, right): # merge two sorted arrays
    result = []
    i = 0
    j = 0
    leftlen = len(left)
    rightlen = len(right)
    while i < leftlen and j < rightlen:
        if left[i] < right[j]:
            result.append(left[i]) # append the smaller value
            i += 1
        else:
            result.append(right[j])
            j +=1
    result += left[i:] # append the rest of the values
    result += right[j:] # append the rest of the values
    return result

def mergeSort(array):
    n = len(array)
    if n == 1:
        return array
    else:
        mid = int(n/2) # split the array in half
        left = array[:mid] # left half
        right = array[mid:] # right half
        left = mergeSort(left) # recursively sort the left half
        right = mergeSort(right) # recursively sort the right half
        return merge(left, right) # merge the two sorted halves