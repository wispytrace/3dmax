from pymxs import runtime as rt

import sys

import os

import time

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "\\..\\utlis")

from plant import RuntimePlant

if __name__ == '__main__':
    
    rt.resetMaxFile(rt.name('noPrompt'))
    my = RuntimePlant()
    my.doMove(rt.point3(200,0,0))
    
    
    time.sleep(2)
    
    my.doMove(rt.point3(200,-100,0))

    
    time.sleep(2)
    
    
    my.doMove(rt.point3(100,100,100))

    time.sleep(2)

    my.hideTraces()

    time.sleep(5)
    
    my.showTraces()
    



    
    