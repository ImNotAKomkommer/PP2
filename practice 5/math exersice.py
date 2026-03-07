# 1. Generator that generates the squares of numbers up to N

def generate_squares(n):
    for i in range(n + 1):
        yield i * i

print("1. Squares up to N:")
for value in generate_squares(5):
    print(value)


# 2. Print even numbers between 0 and n in comma-separated form

def even_numbers(n):
    for i in range(0, n + 1):
        if i % 2 == 0:
            yield str(i)

print("\n2. Even numbers:")
n = int(input("Enter n: "))
print(",".join(even_numbers(n)))


# 3. Generator for numbers divisible by 3 and 4 between 0 and n

def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

print("\n3. Numbers divisible by 3 and 4:")
for value in divisible_by_3_and_4(50):
    print(value)


# 4. Generator squares from a to b

def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

print("\n4. Squares from a to b:")
for value in squares(3, 7):
    print(value)


# 5. Generator that returns all numbers from n down to 0

def countdown(n):
    for i in range(n, -1, -1):
        yield i

print("\n5. Countdown from n to 0:")
for value in countdown(10):
    print(value)