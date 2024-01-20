def find_prime_number(x):
    result = True
    mid = int(x/2)
    if x == 2 or x == 3:
        return result
    for i in [2, mid]:
        if x % i == 0:
            result = False
            return result
    return result


target = int(input("请输入一个数"))
if find_prime_number(target):
    print("%d是质数" % target)
else:
    print("%d不是质数" % target)
