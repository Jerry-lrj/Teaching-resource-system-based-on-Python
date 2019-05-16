def f1(a):
    a = a + 5
    print('f1')
    a = f2(a)
    return a


def f2(x):
    return x - 1


p = f1(3)
print(p)


