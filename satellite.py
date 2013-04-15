import direct.directbase.DirectStart #Panda initialize
from panda3d.core import Vec3, Vec4, Point3 #Modules
from direct.gui.DirectGui import * #The GUI objects
import math

# Gravity is strong in this universe...
gravityConstant = 1e-4

class Satellite(object):
	"""docstring for Satellite"""
	def __init__(self, name, x, y, z, mass):
		self.name = name
		# Position
		self.x = x
		self.y = y
		self.z = z
		#Speed
		self.vx = 0
		self.vy = 0
		#Mass
		self.mass = mass
		#Acceleration
		self.ax = 0
		self.ay = 0

	def addAcceleration(self, anotherSatellite):
		# X-distance
		dx = anotherSatellite.x - self.x
		# Y-distance
		dy = anotherSatellite.y - self.y
		# Distance squared
		dsq = dx*dx + dy*dy
		# Distance
		distance = math.sqrt(dsq)
		# Calculate the force
		force = gravityConstant * self.mass * anotherSatellite.mass / dsq
		# Then add the acceleration
		self.ax += force * dx / distance
		self.ay += force * dy / distance

	def updatePosition(self):
		self.x += self.vx
		self.y += self.vy
		self.vx += self.ax
		self.vy += self.ay
		self.resetAcceleration()

	def resetAcceleration(self):
		self.ax = 0
		self.ay = 0
