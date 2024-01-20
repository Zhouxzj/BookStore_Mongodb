import random
import time


def create_array(length):
    arr = []
    for i in range(length):
        x = random.randint(0, 1000 * length)
        arr.append(x)
    return arr


def select_sort(arr, length):
    for m in range(length):
        minimum = m
        for j in range(m + 1, length - 1):
            if arr[j] < arr[minimum]:
                minimum = j
        arr[minimum], arr[m] = arr[m], arr[minimum]
    return


def merge(left, right):
    left_pos = 0
    right_pos = 0
    result = []
    while left_pos < len(left) and right_pos < len(right):
        if left[left_pos] < right[right_pos]:
            result.append(left[left_pos])
            left_pos += 1
        else:
            result.append(right[right_pos])
            right_pos += 1
    result += left[left_pos:]
    result += right[right_pos:]
    return result


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    num = len(arr) // 2
    left = merge_sort(arr[:num])
    right = merge_sort(arr[num:])
    return merge(left, right)


def quick_sort(arr, start, end):
    if start >= end:
        return
    mid, left, right = arr[start], start, end
    while left < right:
        while arr[right] >= mid and left < right:
            right -= 1
        arr[left] = arr[right]
        while arr[left] <= mid and left < right:
            left += 1
        arr[right] = arr[left]
    arr[left] = mid
    quick_sort(arr, start, left - 1)
    quick_sort(arr, left + 1, end)
    return


sort_time = []
merge_time = []
quick_time = []
for k in [100, 1000, 10000]:
    array = create_array(k)
    tmp1 = array
    tmp2 = array
    tmp3 = array
    start_time1 = time.time()
    select_sort(tmp1, len(tmp1))
    end_time1 = time.time()
    start_time2 = time.time()
    merge_sort(tmp2)
    end_time2 = time.time()
    sort_time.append(end_time1 - start_time1)
    merge_time.append(end_time2 - start_time2)

for k in [100, 1000, 10000]:
    array = create_array(k)
    start_time = time.time()
    quick_sort(array, 0, len(array) - 1)
    end_time = time.time()
    quick_time.append(end_time - start_time)

for k in range(3):
    size = 10 ** (k + 2)
    print("在数组长度为%d的数据规模下，选择排序用时为%.10fs，归并排序用时为%.10fs，快速排序用时为%.10fs" % (
        size, sort_time[k],
        merge_time[k], quick_time[k]))
