print("请输入四个数")
l1 = input().split(" ")
# 对于输入的读取是以空格分隔，比如1 2 3，得到的就是['1','2','3']
l1.sort(reverse=True)
# sort是直接对l1内部元素进行排序，reverse=True表示使用倒序，不写的话默认为False
print(l1)
