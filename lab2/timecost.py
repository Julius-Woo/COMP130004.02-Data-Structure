from matrix_mul_ord import matrix_multiply_ordinary
# from matrix_mul_Strassen import matrix_multiply_strassen
from matrix_mul_Strassen_re import matrix_multiply_strassen_t
import time
import matplotlib.pyplot as plt

time_ord = []
time_strassen = []
time_strassen_16 = []
time_strassen_32 = []
time_strassen_64 = []
nrange = []
for k in range(2,11):
    nrange.append(2**k)
for n in nrange:
    # construct matrix A and B
    A = [[1 for _ in range(n)] for _ in range(n)]
    B = [[1 for _ in range(n)] for _ in range(n)]
    start = time.time()
    result_ord = matrix_multiply_ordinary(A, B)
    end = time.time()
    time_ord.append(end - start)
    
    # start = time.time()
    # result_strassen = matrix_multiply_strassen(A, B)
    # end = time.time()
    # time_strassen.append(end - start)
    
    start = time.time()
    result_strassen_16 = matrix_multiply_strassen_t(A, B, 16)
    end = time.time()
    time_strassen_16.append(end - start)
    
    start = time.time()
    result_strassen_32 = matrix_multiply_strassen_t(A, B, 32)
    end = time.time()
    time_strassen_32.append(end - start)
    
    start = time.time()
    result_strassen_64 = matrix_multiply_strassen_t(A, B, 64)
    end = time.time()
    time_strassen_64.append(end - start)

# print the time cost
print('Ordinary Multiplication:',time_ord)
print('Strassen16 Multiplication:',time_strassen_16)
print('Strassen32 Multiplication:',time_strassen_32)
print('Strassen64 Multiplication:',time_strassen_64)

# plot the time cost
plt.figure(figsize=(10, 6))
plt.plot(nrange, time_ord, label='Ordinary Multiplication')
# plt.plot(nrange, time_strassen, label='Strassen Multiplication')
plt.plot(nrange, time_strassen_16, label='Strassen16 Multiplication')
plt.plot(nrange, time_strassen_32, label='Strassen32 Multiplication')
plt.plot(nrange, time_strassen_64, label='Strassen64 Multiplication')
plt.xlabel('Matrix Size (N)')
plt.ylabel('Time (seconds)')
plt.title('Matrix Multiplication Algorithms Comparison')
plt.legend()
plt.grid(True)
plt.show()
