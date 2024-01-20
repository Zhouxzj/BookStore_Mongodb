print("请输入第一个整数：")
a = int(input())
print("请输入第二个整数：")
b = int(input())

common_divisor = a if a < b else b
for i in range(common_divisor, 0, -1):
    if a % i == 0 and b % i == 0:
        print("%d和%d的最大公约数为%d" % (a, b, i))
        break
