import math
import random
import copy

class SimpleControl:

    def __init__(self, model):

        self.sampleNum = 100
        self.model = model
        self.controls = self.getSample()

    def getSample(self):

        controls = []

        for i in range(self.sampleNum):
            control = copy.deepcopy(self.model)
            for key, item in self.model.constrains.items():
                setattr(control, key, random.uniform(item[0], item[1]))
            controls.append(control)

        return controls

    def getNextPosition(self, sx, sy, control):

        distance = 1 / 2 * control.speedUp * (control.upTime ** 2) + 1 / 2 * control.speedDown * (
                    control.speedUp * control.upTime / control.speedDown) ** 2
        deg = control.angle
        x = sx + math.cos(deg) * distance
        y = sy + math.sin(deg) * distance

        return x, y

    def getControl(self, sx, sy, gx, gy):

        costs = []

        for control in self.controls:
            x, y = self.getNextPosition(sx, sy, control)
            dx = x - gx
            dy = y - gy
            costs.append(math.hypot(dx, dy))

        index = costs.index(min(costs))
        control = self.controls[index]

        return control
