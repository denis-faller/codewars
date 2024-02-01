def dbl_linear(n):
    s = set()
    list = []
    s.add(1)
    res = 0
    arr_size = 0
    for x in range(1, n * n, 1):
        y = 2 * x + 1
        z = 3 * x + 1
        if x in s:
            s.add(y)
            s.add(z)
            list.append(x)
            arr_size += 1
        if arr_size == n + 1:
            res = list[arr_size - 1]
            break
    return res

print(dbl_linear(10))