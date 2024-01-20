def Square_root_Q6_1(number):
    c=number
    g=c/2
    i=0
    while(abs(g*g-c)>0.000000000001):
        g=(g+c/g)/2
        i=i+1
        print("%d:%.13f"%(i,g))

def Square_root_Q6_2(number):
    c=number
    g=c
    i=0
    while(abs(g*g-c)>0.000000000001):
        g=(g+c/g)/2
        i=i+1
        print("%d:%.13f"%(i,g))

def Square_root_Q6_3(number):
    c=number
    g=c/4
    i=0
    while(abs(g*g-c)>0.000000000001):
        g=(g+c/g)/2
        i=i+1
        print("%d:%.13f"%(i,g))

print('c=2, g=c/2的情况1')
Square_root_Q6_1(2)

print('c=2, g=c的情况2')
Square_root_Q6_2(2)

print('c=2, g=c/4的情况3')
Square_root_Q6_3(2)

