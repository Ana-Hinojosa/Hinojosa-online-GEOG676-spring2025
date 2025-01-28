# GEOG 676 - GIS Programming
# Lab 2: Fun with loops

# Part 1. Multiply all list items together
part1 = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
# Start with 1 since it's multiplication
result1 = 1

for value in part1:
    result1 *= value
print("The result for Part 1 is:", result1)



# Part 2. Add all list items together.
part2 = [-1, 23, 483, 8573, -13847, -381569, 1652337, 718522177]
# Start with 0 since it's addition
result2 = 0

for value in part2:
    result2 += value
print("The result for Part 2 is:", result2)



# Part 3. Only adds items in the list that are even numbers. 
part3 = [146, 875, 911, 83, 81, 439, 44, 5, 46, 76, 61, 68, 1, 14, 38, 26, 21]
# Start with 0 since it's addition 
result3 = 0

for value in part3:
    # Using modulo (%) to check if the value is even
    if value % 2 == 0:
        result3 += value
print("The result for Part 3 is:", result3)