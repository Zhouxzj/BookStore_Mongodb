N = eval(input("请输入数组大小N："))
A = []
B = []
for i in range(N):
    A.append(i+1)
    B.append(1)
for i in range(N):
    for j in range(N):
        if j != i:
            B[i] *= A[j]
print(B)
