'''
    Creates a simple text representation of the scene graph
'''
from pymxs import runtime as rt 


def output_node(node, indent=''):
    """Print the scene graph as text to stdout."""
    print(indent, node.Name)
    for child in node.Children:
        output_node(child, indent + '--')

t = rt.Teapot()

output_node(rt.rootnode)

objs = pymxs.runtime.objects

for o in objs:
    print(o.name)
	
	
# s = pymxs.runtime.getNodeByName('Sphere002')

print(pymxs.runtime.selectionSets)


# pymxs.runtime.saveMaxFile('myMaxFile.max')

# pymxs.runtime.maxFileName

# pymxs.runtime.maxFilePath

# pymxs.runtime.checkForSave()

# pymxs.runtime.loadMaxFile('my_scene.max')