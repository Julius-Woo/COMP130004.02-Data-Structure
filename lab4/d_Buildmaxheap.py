from d_MAXHeapify import max_heapify
def build_max_heap(A,d):
    n = len(A)
    for i in range((n-2)//d,-1,-1): # begin from the last parent, skip the leaves
        max_heapify(A,i,d)
    return A