import re


print("请输入字符串S")
S = input()
for i in range(len(S)):
    if i == len(S)-1:
        print("no")
        break
    res = re.findall(S[i], S)
    if len(res) > 1:
        print("yes")
        break
