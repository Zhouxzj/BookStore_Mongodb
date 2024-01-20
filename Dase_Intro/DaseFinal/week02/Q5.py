def Square_root_Q5(number):
    c=number
    g=c/2
    i=0
    while(abs(g*g-c)>0.000000000001):
        g=(g+c/g)/2
        i=i+1
        print("%d:%.13f"%(i,g))

print('c=2的情况')
Square_root_Q5(2)

print('c=20的情况')
Square_root_Q5(20)

print('c=200的情况')
Square_root_Q5(200)

print('c=2000的情况')
Square_root_Q5(2000)

# 发现随着c增大，需要迭代更多次来找到足够精度的结果