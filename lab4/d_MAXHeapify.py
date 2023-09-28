# A: Array
# i: index
# d: d-ary tree
def max_heapify(A,i,d):
    n = len(A)
    child_1 = d*i+1
    child_rightmost = min(d*i+d, n-1) 
    if child_1 <= len(A)-1 and A[child_1] > A[i]:
        largest = child_1
    else:
        largest = i
    for j in range(child_1,child_rightmost+1):
        if j <= len(A)-1 and A[j] > A[largest]:
            largest = j
    if largest != i:
        A[i],A[largest] = A[largest],A[i]
        max_heapify(A,largest,d)
    return A