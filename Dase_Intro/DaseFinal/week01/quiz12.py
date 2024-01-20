def cube_root(num):
    if num < 0:
        temp = -num
    else:
        temp = num
    pre = 0.0001
    low = 0
    high = temp / 2
    while abs(high * high * high - temp) > pre:
        if high * high * high > temp:
            high = high - (high - low) / 2
        else:
            high = high + (high - low) / 2
    return high


print("请输入一个数")
n = float(input())
if n < 0:
    print('%.5f' % -cube_root(n))
else:
    print('%.5f' % cube_root(n))
