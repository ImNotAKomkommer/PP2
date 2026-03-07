# 1. Match a string that has an 'a' followed by zero or more 'b''s

import re

pattern1 = r"ab*"

test1 = ["a", "ab", "abb", "ac", "b"]
print("1.")
for s in test1:
    print(f"{s}: {bool(re.fullmatch(pattern1, s))}")


# 2. Match a string that has an 'a' followed by two to three 'b'

pattern2 = r"ab{2,3}"

test2 = ["ab", "abb", "abbb", "abbbb", "a"]
print("\n2.")
for s in test2:
    print(f"{s}: {bool(re.fullmatch(pattern2, s))}")


# 3. Find sequences of lowercase letters joined with an underscore

pattern3 = r"\b[a-z]+_[a-z]+\b"

text3 = "hello_world test_value Hello_World one_two_three"
print("\n3.")
print(re.findall(pattern3, text3))


# 4. Find the sequences of one upper case letter followed by lower case letters

pattern4 = r"\b[A-Z][a-z]+\b"

text4 = "Hello world And Python USA Test"
print("\n4.")
print(re.findall(pattern4, text4))


# 5. Match a string that has an 'a' followed by anything, ending in 'b'

pattern5 = r"a.*b$"

test5 = ["ab", "axxb", "a123b", "ac", "baab"]
print("\n5.")
for s in test5:
    print(f"{s}: {bool(re.fullmatch(pattern5, s))}")


# 6. Replace all occurrences of space, comma, or dot with a colon

text6 = "Hello, world. Python is fun"
result6 = re.sub(r"[ ,\.]", ":", text6)

print("\n6.")
print(result6)


# 7. Convert snake case string to camel case string

def snake_to_camel(s):
    parts = s.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

print("\n7.")
print(snake_to_camel("this_is_snake_case"))


# 8. Split a string at uppercase letters

def split_at_uppercase(s):
    return re.findall(r"[A-Z][a-z]*", s)

print("\n8.")
print(split_at_uppercase("SplitThisStringAtUppercase"))


# 9. Insert spaces between words starting with capital letters

def insert_spaces(s):
    return re.sub(r"(?<!^)([A-Z])", r" \1", s)

print("\n9.")
print(insert_spaces("InsertSpacesBetweenWords"))


# 10. Convert a given camel case string to snake case

def camel_to_snake(s):
    return re.sub(r"(?<!^)([A-Z])", r"_\1", s).lower()

print("\n10.")
print(camel_to_snake("camelCaseString"))