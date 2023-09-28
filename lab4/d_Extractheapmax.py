from d_MAXHeapify import max_heapify
def extract_max(A,d):
    if len(A) < 1:
        raise ValueError("heap underflow")
    max = A[0]
    A[0] = A[len(A)-1]
    A.pop()
    max_heapify(A,0,d)
    return max