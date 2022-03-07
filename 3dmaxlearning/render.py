# import pymxs


# bmp = pymxs.runtime.render(pos=pymxs.runtime.name('vfb_upper_left'))


from pymxs import runtime as rt


def render():
    '''Render in the renderoutput directory.'''
    output_path = os.path.join(pymxs.runtime.getDir(pymxs.runtime.Name("renderoutput")), 'foo.jpg')
    if os.path.exists(output_path):
        os.remove(output_path)
    print(output_path)
    pymxs.runtime.render(outputFile=output_path)
    
def myPreRenderCallback():
    print('PreRender Callback Called')

print(pymxs.runtime.name('vfb_upper_left'))
rt.resetMaxFile(rt.name('noPrompt'))
t = rt.teapot()
# pymxs.runtime.execute('max tool maximize')
# cam = rt.camera(pos=rt.Point3(0, 0, 0))
ca = rt.Targetcamera(pos=rt.Point3(0,0,100))
# tobj=rt.Targetobject(pos=rt.Point3(0,0,-100)) 
tobj=rt.Targetobject()
#tobj.pos = rt.Point3(0,0,-100)
ca.target=tobj
bmp = rt.bitmap(1280, 800, color=rt.white, gamma=1.9)
pymxs.runtime.render(camera=ca,to=bmp)
# view_size = rt.getViewSize()
# anim_bmp = rt.bitmap(view_size.x, view_size.y)
# dib = rt.gw.getViewportDib()
# rt.copy(dib, anim_bmp)
# rt.save(anim_bmp)
print(type(bmp))
pymxs.runtime.display(bmp, caption='My Bitmap')

#mxs = pymxs.runtime



# mxs.callbacks.removeScripts(id=mxs.Name('MyCallbacks'))    
# mxs.callbacks.addScript(mxs.name('preRender'), myPreRenderCallback, id=mxs.name('MyCallbacks'))
# this will run the registered script first:
# mxs.render()
# render()