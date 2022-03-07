from pymxs import runtime as rt


class RuntimeCamera():
    
    
	def __init__(self):
		
		self.camera = rt.Targetcamera()
		
		self.camobj = rt.Targetobject()
		
		self.camera.target = self.camobj
		
		self.currentCamPos = rt.Point3(0, 0, 0)
		
		self.currentObjPos = rt.Point3(0, 0, 0)
		
		self.bmp = rt.bitmap(1280, 960, color=rt.white, gamma=1.9)
	
	
	def setPose(self, camPos, objPos):	
		
		self.currentCamPos = camPos
		
		self.currentObjPos = objPos
		
		self.camera.pos = self.currentCamPos
		
		self.camobj.pos = self.currentObjPos 
		
		rt.redrawViews()
	
	
	def getFrame(self, outputPath=None):
		
		if outputPath != None:
			if os.path.exists(outputPath):
				os.remove(outputPath)
			rt.render(camera=self.camera, to=self.bmp, outputFile=outputPath)
		else:
			rt.render(camera=self.camera,to=self.bmp)
		
		return self.bmp
	
    

