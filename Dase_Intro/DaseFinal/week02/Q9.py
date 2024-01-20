import random
import math

def function(x):
    return x**2 + 4*x*math.sin(x)

def monte_carlo_integration(num_samples):
    interval_start = 2
    interval_end = 3
    total_area = 0

    for _ in range(num_samples):
        x = random.uniform(interval_start, interval_end)
        y = function(x)
        total_area += y

    average_area = total_area / num_samples
    integral = (interval_end - interval_start) * average_area
    return integral

def Function(x):
    return (x**3)/3+4*(math.sin(x)-x*math.cos(x))

num_samples = 100000  # 蒙特卡罗抽样的次数，可以根据需要增加以提高精度
estimated_integral = monte_carlo_integration(num_samples)
print('估计值',estimated_integral)

print('真实值',Function(3)-Function(2))

