# def select_sort(array):
#     for i in range(len(array)):
#         x = i
#         for j in range(i, len(array)):
#             if int(array[j]) < int(array[x]):
#                 x = j
#         array[i], array[x] = int(array[x]), int(array[i])
#     return array
#
#
# arr = list(input("请输入一个数组:\n").split(" "))
# select_sort(arr)
# print(arr)
# mine shell sort is above...


def shell_sort(arr):
    n = len(arr)
    gap = n // 2  # 初始间隔值

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i

            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap

            arr[j] = temp
        gap //= 2  # 减小间隔值

# 示例用法
arr = [12, 34, 54, 2, 3]
print("原始数组:", arr)
shell_sort(arr)