def fibosum(n):
    a = 0
    summ = 1
    b = 1
    i = 2
    while i < n:
        c = a + b
        a = b
        b = c
        summ = summ + c
        i = i + 1
    return summ
print("The sum of the first 5 numbers of the fibonacci series: ", fibosum(5))
print("The sum of the first 10 numbers of the fibonacci series: ", fibosum(10))