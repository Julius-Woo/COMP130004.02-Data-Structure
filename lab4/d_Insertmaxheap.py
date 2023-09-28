from d_Increasekey_heap import increase_key
def max_heap_insert(A,key,d):
    k = float("-inf")
    A.append(k)
    increase_key(A,len(A)-1,d,key)