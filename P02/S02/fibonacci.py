a = 0
b = 1
series = str(a) + " " + str(b)
i = 2
while i < 11:
        c = a + b
        series = series + str(c)
        a = b
        b = c
        i = i + 1
print(series)