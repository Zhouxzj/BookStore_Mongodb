print("请输入一个数字")
s = int(input())


def find_multiply_max(num):
    x = num % 3
    y = int(num / 3)
    result = []
    if x == 0:
        for i in range(y):
            result.append(3)
    elif x == 1:
        result.append(2)
        result.append(2)
        for i in range(y - 1):
            result.append(3)
    else:
        result.append(2)
        for i in range(y):
            result.append(3)
    return result


print(find_multiply_max(s))
