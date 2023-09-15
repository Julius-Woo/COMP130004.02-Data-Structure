import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

dimensions = np.array([2**i for i in range(2, 11)])  # 2^2 ~ 2^10
time_ord = [0.0, 0.0, 0.001005411148071289, 0.003017902374267578, 0.021852493286132812, 0.18645644187927246, 1.5937602519989014, 14.359130859375, 135.2789764404297]
time_strassen_32 = [0.0, 0.0, 0.0010275840759277344, 0.0029914379119873047, 0.0240323543548584, 0.16164660453796387, 1.165126085281372, 8.7085120677948, 74.90543127059937]
# calculate the root of time
time_ord_root = [t ** (1/3) for t in time_ord]
time_strassen_root = [t ** (1/2.807) for t in time_strassen_32]  # 2.807 is the exponent of n in Strassen's algorithm

# calculate the regression line
reg_ord = LinearRegression().fit(dimensions.reshape(-1, 1), time_ord_root)
reg_strassen = LinearRegression().fit(dimensions.reshape(-1, 1), time_strassen_root)

print("Ordinary method regression equation: y = {:.4f}x + {:.4f}".format(reg_ord.coef_[0], reg_ord.intercept_))
print("Strassen method regression equation: y = {:.4f}x + {:.4f}".format(reg_strassen.coef_[0], reg_strassen.intercept_))

# calculate the correlation coefficient
correlation_ord = np.corrcoef(dimensions, time_ord_root)[0, 1]
correlation_strassen = np.corrcoef(dimensions, time_strassen_root)[0, 1]

print("Correlation coefficient for Ordinary method:", correlation_ord)
print("Correlation coefficient for Strassen method:", correlation_strassen)


plt.figure(figsize=(10, 6))
# draw scatter plot of original data
plt.scatter(dimensions, time_ord_root, color='blue', label='Ordinary method data')
plt.scatter(dimensions, time_strassen_root, color='red', label='Strassen32 method data')

# plot the regression line
plt.plot(dimensions, reg_ord.predict(dimensions.reshape(-1, 1)), color='blue', linestyle='--', label='Ordinary regression line')
plt.plot(dimensions, reg_strassen.predict(dimensions.reshape(-1, 1)), color='red', linestyle='--', label='Strassen32 regression line')

plt.xlabel('Matrix Size (N)')
plt.ylabel('Root of Time')
plt.legend()
plt.title('Matrix Multiplication analysis')
plt.grid(True)
plt.show()