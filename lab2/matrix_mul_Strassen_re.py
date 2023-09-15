# squre matrix multiplication using revised Strassen algorithm, 2^k * 2^k
def matrix_multiply_strassen_t(A, B, t):
    n = len(A)  
    if n <= t: # set the threshold
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    # divide matrix A and B into four sub-matrices
    mid = n // 2
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]
    
    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]
    
    # calculate the 7 products of the sub-matrices
    P1 = matrix_multiply_strassen_t(A11, matrix_add_sub(B12, B22,2))
    P2 = matrix_multiply_strassen_t(matrix_add_sub(A11, A12,1), B22)
    P3 = matrix_multiply_strassen_t(matrix_add_sub(A21, A22,1), B11)
    P4 = matrix_multiply_strassen_t(A22, matrix_add_sub(B21, B11,2))
    P5 = matrix_multiply_strassen_t(matrix_add_sub(A11, A22,1), matrix_add_sub(B11, B22,1))
    P6 = matrix_multiply_strassen_t(matrix_add_sub(A12, A22,2), matrix_add_sub(B21, B22,1))
    P7 = matrix_multiply_strassen_t(matrix_add_sub(A11, A21,2), matrix_add_sub(B11, B12,1))
    
    # calculate the four sub-matrices of the result matrix C
    C11 = matrix_add_sub(matrix_add_sub(matrix_add_sub(P5, P4,1), P2,2), P6,1)
    C12 = matrix_add_sub(P1, P2,1)
    C21 = matrix_add_sub(P3, P4,1)
    C22 = matrix_add_sub(matrix_add_sub(P5, P1,1), matrix_add_sub(P3, P7,1),2)
    
    # merge the four sub-matrices into one
    result = []
    for i in range(n):
        if i < mid:
            result.append(C11[i] + C12[i])  # merge C11 and C12
        else:
            result.append(C21[i - mid] + C22[i - mid])  # merge C21 and C22
    
    return result

def matrix_add_sub(A, B, flag):
    if flag == 1:
        return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    if flag == 2:
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]