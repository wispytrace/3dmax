
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import qtmax
import time

from pymxs import runtime as rt

def make_cylinder():
    cyl = rt.Cylinder(radius=10, height=30)
    rt.redrawViews()

    return    


class PyMaxDockWidget(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(PyMaxDockWidget, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle('Pyside Qt  Dock Window')
        self.initUI()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.step = 0
        self.t = rt.Teapot()

    def initUI(self):
        main_layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("Click button to create a cylinder in the scene")
        main_layout.addWidget(label)

        cylinder_btn = QtWidgets.QPushButton("Cylinder")
        cylinder_btn.clicked.connect(make_cylinder)
        
        move_btn = QtWidgets.QPushButton("move")
        move_btn.clicked.connect(self.do_move)
        main_layout.addWidget(cylinder_btn)
        main_layout.addWidget(move_btn)
        widget = QtWidgets.QWidget()
        widget.setLayout(main_layout)
        self.setWidget(widget)
        self.resize(250, 100)

        
    def do_move(self):
        self.step = self.step + 1
        self.t.pos = rt.Point3(self.step*20, 0, 0)
        rt.redrawViews()
        time.sleep(2)
    



# animate 

# attime

# with pymxs.animate(True):
#     with pymxs.attime(0):
#         t.pos = rt.Point3(-100, 0, 0)
#     with pymxs.attime(100):
#         t.pos = rt.Point3(100, 0, 0)

# pymxs.runtime.playAnimation(immediateReturn=True)


# pymxs.runtime.stopAnimation()

# pymxs.runtime.timeConfiguration.playbackSpeed = 4

# rt.currentTime

# rt.currentTime.frame

def main():
    rt.resetMaxFile(rt.name('noPrompt'))
    #main_window = qtmax.GetQMaxMainWindow()
    #w = PyMaxDockWidget(parent=main_window)
    #w.setFloating(True)
    #w.show()
    t = rt.Teapot()
    t.pos = rt.Point3(20, 0, 0)
    rt.redrawViews()
    time.sleep(2)
    t.pos = rt.Point3(100, 0, 0)
    rt.redrawViews()


if __name__ == '__main__':
    main()