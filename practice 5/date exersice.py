# 1. Convert degree to radian

import math

degree = 15
radian = degree * (math.pi / 180)

print("1. Degree to radian")
print("Input degree:", degree)
print("Output radian:", round(radian, 6))


# 2. Calculate the area of a trapezoid

height = 5
base1 = 5
base2 = 6
trapezoid_area = ((base1 + base2) * height) / 2

print("\n2. Area of a trapezoid")
print("Height:", height)
print("Base, first value:", base1)
print("Base, second value:", base2)
print("Expected Output:", trapezoid_area)


# 3. Calculate the area of regular polygon

n = 4
side = 25
polygon_area = (n * side ** 2) / (4 * math.tan(math.pi / n))

print("\n3. Area of regular polygon")
print("Input number of sides:", n)
print("Input the length of a side:", side)
print("The area of the polygon is:", round(polygon_area))


# 4. Calculate the area of a parallelogram

base = 5
height_parallelogram = 6
parallelogram_area = base * height_parallelogram

print("\n4. Area of a parallelogram")
print("Length of base:", base)
print("Height of parallelogram:", height_parallelogram)
print("Expected Output:", float(parallelogram_area))