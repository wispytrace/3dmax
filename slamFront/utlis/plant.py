from pymxs import runtime as rt


class RuntimePlant():
	
	
	def __init__(self, initPos=rt.Point3(0,0,0), initRadius=5):
		
		self.currentPos = initPos
		
		self.nextPos = initPos
		
		self.object = rt.Sphere(pos=initPos, radius=initRadius)
		
		self.traces = []
		
		self.minRadius = 0.001
		
		self.maxRadius = 0.1



	def makeTrace(self):
		
		trace = rt.Cylinder(radius=self.maxRadius, pos=self.currentPos, dir=(self.nextPos - self.currentPos), height=rt.distance(self.nextPos, self.currentPos))
		
		self.traces.append(trace)


	def showTraces(self):

		for trace in self.traces:

			trace.radius = self.maxRadius
		
		rt.redrawViews()


	def hideTraces(self):
		
		for trace in self.traces:
		
			trace.radius = self.minRadius
		
		rt.redrawViews()
		
				
	def doMove(self, pos):
		
		self.nextPos = pos
		
		self.makeTrace()
		
		self.object.pos = self.nextPos
		
		self.currentPos = self.nextPos
		
		rt.redrawViews()

		
