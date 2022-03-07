import pymxs

rt = pymxs.runtime


teapot_position=pymxs.runtime.point3(100,20,10)

# This creates a new teapot object at position [0,0,0], with a radius of 25 and 4 segments. To change these parameters at creation time, we can specify them in the constructor:
my_teapot = pymxs.runtime.teapot(radius=50, pos=teapot_position, segments=2)

print(pymxs.runtime.isShapeObject(my_teapot))

print(pymxs.runtime.getPolygonCount(my_teapot))

# Modifying the Object

my_modifier = pymxs.runtime.taper()

my_modifier.amount = 2.0

my_modifier.curve = 1.5

pymxs.runtime.addmodifier(my_teapot, my_modifier)