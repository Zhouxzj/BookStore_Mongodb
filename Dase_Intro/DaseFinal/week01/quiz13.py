print("请输入数字n")
num = int(input())


def fab(n):
    s = 1
    for i in range(1, n+1):
        s *= i
    return s


print(fab(num))
