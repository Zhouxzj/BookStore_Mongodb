print("请输入一个数字")
x = int(input())


def cube_root(num):
    g = num / 2
    i = 0
    precision = 0.00000000001
    while abs(g ** 3 - num) > precision:
        g = 2 * g / 3 + num / (3 * g ** 2)
        i += 1
    print("%d:g = %.13f" % (i, g))


cube_root(x)
