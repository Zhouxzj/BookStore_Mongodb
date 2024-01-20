import matplotlib.pyplot as plt

result_10 = 2 ** 10
result_20 = 2 ** 20
result_30 = 2 ** 30
result_40 = 2 ** 40
result_50 = 2 ** 50

print("2^10 =", result_10)
print("2^20 =", result_20)
print("2^30 =", result_30)
print("2^40 =", result_40)
print("2^50 =", result_50)

exponents = [10, 20, 30, 40, 50]
results = [2 ** exp for exp in exponents]

plt.plot(exponents, results, marker='o', linestyle='-')
plt.title('2^x for Different Exponents')
plt.xlabel('Exponent (x)')
plt.ylabel('2^x')
plt.grid(True)
plt.show()