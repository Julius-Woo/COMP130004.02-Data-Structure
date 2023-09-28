from d_Buildmaxheap import build_max_heap
from d_Extractheapmax import extract_max
from d_Increasekey_heap import increase_key

# construct a 3-ary heap
A = range(1,31)
A = list(A)
build_max_heap(A,3)
print('The initial 3-ary heap is: ', A)
# extract the maximum element
extract_max(A,3)
print('After one extraction, the 3-ary heap is: ', A)
# increase the key of A[9] to 28
increase_key(A,9,3,28)  # increase the 10-th element
print('After increasing the key of A[9] to 28, the 3-ary heap is: ', A)