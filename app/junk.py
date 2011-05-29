def a():
    yield 1

def b():
    return a()

print b()
print b().next()
