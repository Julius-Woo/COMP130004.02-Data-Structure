def increase_key(A, i, d, k):
    if k < A[i]:
        raise ValueError("New key is smaller than the current key!")
    A[i] = k
    while i > 0 and A[parent(i, d)] < A[i]:
        A[i], A[parent(i, d)] = A[parent(i, d)], A[i]
        i = parent(i, d)
    return A
    
def parent(i, d):
    return (i-1) // d