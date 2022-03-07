import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from pymxs import runtime as rt
from utlis.camera import RuntimeCamera
from utlis.plant import RuntimePlant



def easyMove(plant):

    for i in range(0,3):

        plant.doMove(rt.point3(-60+i*10,-80,0))
    
    for j in range(0,4):

        plant.doMove(plant.currentPos+rt.point3(0,(j+1)*10,0))











if __name__ == '__main__':

    rt.resetMaxFile(rt.name('noPrompt'))

    rt.loadMaxFile("H:\\code\\3dmax\\3dmodel\\demo1.max")

    runtimeCamera = RuntimeCamera()

    runtimeCamera.setPose(camPos=rt.point3(0,0,400), objPos=rt.point3(0,0,-200))

    runtimePlant = RuntimePlant(initPos=rt.point3(-70,-80, 0))

    # rt.redrawViews()


    easyMove(runtimePlant)

    runtimeCamera.getFrame()
