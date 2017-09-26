


l1 = [1,2,3]
l2 = [3,4]
ls_com_v = ["1,3", "1,4", "2,3", "2,4", "3,3","3,4"]
print(len(l1), len(l2))
ls = []
for i in range(0, len(l1)-1):
    print(i)
    for j in range(0 + len(l2) * i, len(l2) - 1 + len(l2) * i):
        print(j)
        a = ls_com_v[j]
        b = ls_com_v[j + len(l2) + 1]
        ab = a + ',' + b
        ls.append(ab)
        print(ab)