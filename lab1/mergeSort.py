def merge(left, right):
    result = []
    i = 0
    j = 0
    leftlen = len(left)
    rightlen = len(right)
    while i < leftlen and j < rightlen:
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j +=1
    result += left[i:]
    result += right[j:]
    return result

def mergeSort(array):
    n = len(array)
    if n == 1:
        return array
    else:
        mid = int(n/2)
        left = array[:mid]
        right = array[mid:]
        left = mergeSort(left)
        right = mergeSort(right)
        return merge(left, right)
