L = [1, 2, 3, 4, 5]


def for_to_sort(s):
    for i in range(len(s)):
        for k in range(i,len(s)):
            if s[i] < s[k]:
                t = s[i]
                s[i] = s[k]
                s[k] = t


def while_to_sort(s):
    first = 0
    left = 0
    right = len(s)-1
    while left < right:
        first = s[left]
        s[left] = s[right]
        s[right] = first
        left += 1
        right -= 1


for_to_sort(L)

# while_to_sort(L)
print(L)
