
def myfunction(a, *args, **kwargs):
    print("a", a)
    print("args", args)
    print("kwargs", kwargs)



myfunction(10, 12, 14, 15, 16, price=100, color='gray', size='M')