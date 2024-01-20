
import decimal

def calculate_pi_leibniz(precision):
    decimal.getcontext().prec = precision + 2
    pi = decimal.Decimal(0)
    for k in range(precision):
        pi += decimal.Decimal((-1) ** k) / decimal.Decimal(2 * k + 1)
    return str(4 * pi)

precision = 1000  # 将精度设置为所需的小数点后位数
pi_leibniz = calculate_pi_leibniz(precision)
print(pi_leibniz)
# 莱布尼兹级数

import decimal
import math
def calculate_pi_leibniz(precision):
    decimal.getcontext().prec = precision + 2
    pi = decimal.Decimal(0)
    for k in range(1,precision):
        pi += decimal.Decimal(1 / decimal.Decimal(k ** 2 ))
    return str(math.sqrt((6 * pi)))

precision = 1000  # 将精度设置为所需的小数点后位数
pi_leibniz = calculate_pi_leibniz(precision)
print(pi_leibniz)
# xxx级数

import random

def estimate_pi_monte_carlo(num_samples):
    inside_circle = 0
    for _ in range(num_samples):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        distance = x**2 + y**2
        if distance <= 1:
            inside_circle += 1

    return 4 * inside_circle / num_samples

num_samples = 1000000  # 蒙特卡洛抽样的次数，可以根据需要增加以提高精度
pi_monte_carlo = estimate_pi_monte_carlo(num_samples)
print(pi_monte_carlo)
# 蒙特卡罗估计