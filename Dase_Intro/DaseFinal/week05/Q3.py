def insertion_sort(array):
    for i in range(len(array)):
        index = i - 1
        current = int(array[i])
        while index >= 0 and int(array[index]) > current:
            array[index + 1] = array[index]
            index -= 1
        array[index + 1] = current
    return array


arr = list(input("请输入一个数组\n").split(" "))
insertion_sort(arr)
print(arr)
