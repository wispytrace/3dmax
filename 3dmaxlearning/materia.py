import pymxs

t = pymxs.runtime.teapot()

m = pymxs.runtime.standardMaterial()

t.material=m

m.diffuse = pymxs.runtime.color(10,10,10)

m.specular = pymxs.runtime.color(255,255,255)

pymxs.runtime.MatEditor.mode = pymxs.runtime.name('basic')

mat = pymxs.runtime.PhysicalMaterial()

pymxs.runtime.setMeditMaterial(1, mat)

pymxs.runtime.MatEditor.open()