from memoize import memoize

@memoize
def some_function():
    print("Getting the thing")
    return "The thing"

x = some_function()
y = some_function()
print(x)
print(y)

@memoize
def power_up(value, by=2):
    print(f"Powering up {value} by {by}")
    return value ** by

def square_this(value):
    return power_up(value, by=2)

print(square_this(4))
print(square_this(5))
print(square_this(4))
print(square_this(5))

print(power_up(4, by=3))
print(power_up(5, by=4))
print(power_up(4, by=3))
print(power_up(5, by=4))
print(power_up(4, by=4))
print(power_up(5, by=2))
print(power_up(4, by=4))
print(power_up(5, by=2))
