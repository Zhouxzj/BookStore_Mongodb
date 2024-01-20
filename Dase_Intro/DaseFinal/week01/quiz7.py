def find_even(num):
    for i in range(num):
        if i % 2 == 1:
            print("%d" % i, end=" ")


n = 100
find_even(n)
