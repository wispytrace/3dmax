from pymxs import runtime as rt

import sys

import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "\\..\\utlis")

from camera import RuntimeCamera

if __name__ == '__main__':
    
    rt.resetMaxFile(rt.name('noPrompt'))

    teapot = rt.Teapot()
    
    my = RuntimeCamera()

    my.setPose(camPos=rt.Point3(200,0,0), objPos=rt.Point3(-200,0,0))

    my.getFrame()
    
    print(os.path.dirname(os.path.realpath(__file__)) + "\\..\\utlis")