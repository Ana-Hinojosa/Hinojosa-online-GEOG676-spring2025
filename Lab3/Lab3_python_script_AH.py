# GEOG 676 - GIS Programming
# Lab 3: Object Oriented Programming

# Creates a class for each shape
class Shape():
    def __init__(self):
        pass

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width
    # Area = length * width
    def getArea(self):
        return self.length * self.width

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    # Area = (pi)r^2
    def getArea(self):
        return 3.14159 * (self.radius^2)

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height
    # Area = 1/2 * base * height    
    def getArea(self):
        return 0.5 * self.base * self.height

# Reads the shape.txt file
file = open("C:\Hinojosa-online-GEOG676-spring2025\Lab3\shape.txt", "r")
shape_data = file.readlines()
file.close()

# loops through each line in the txt file and then checks each if statement
for line in shape_data:
    column = line.split(',') # splits each field into a list using comma as the separator
    shape = column[0]

    if shape == 'Rectangle':
        rectangle = Rectangle(int(column[1]), int(column[2]))
        print('Area of Rectangle: ', rectangle.getArea())
    elif shape == 'Circle':
        circle = Circle(int(column[1]))
        print('Area of Circle: ', circle.getArea())
    elif shape == 'Triangle':
        triangle = Triangle(int(column[1]), int(column[2]))
        print('Area of Triangle: ', triangle.getArea())