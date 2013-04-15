# Author: Niklas Strengell
# Kosminen simulaattori

import direct.directbase.DirectStart #Panda initialize
from panda3d.core import Vec3, Vec4, Point3, LineSegs #Modules
from direct.gui.DirectGui import * #The GUI objects
from satellite import Satellite #The actual gravity simulation
from direct.task import Task
from direct.showbase import DirectObject
import sys

class Universe:  #This is our main class
    def __init__(self, satelliteList):

        self.title = OnscreenText(
            text="Kosminen Simulaattori",
            style=1, fg=(1, 1, 1, 1), pos=(0.95, -0.95), scale = .06)

        base.setBackgroundColor(0, 0, 0)
        base.disableMouse()
        camera.setPos(0, 0, 360)
        camera.setHpr(0, -90, 0)

        self.satellites = satelliteList

        self.points = []

        #This is for convenience, so that you could see the stars and planets
        self.scale = 0.05
        self.orbitscale = 10

        self.loadSatellites()
        #self.rotateSatellites()

        taskMgr.add(self.moveSatellites, 'Move satellites')

    def loadSatellites(self):

        #First load the model for the sky and make it a child for render
        self.sky = loader.loadModel("models/solar_sky_sphere")
        self.sky.reparentTo(render)
        self.sky.setScale(400)

        #Load the texture for the sky, and bind it to the model
        #self.sky_texture = loader.loadTexture("models/stars_1k_tex.jpg")
        #self.sky.setTexture(self.sky_texture, 1)

        print "loading satellites"
        for satellite in self.satellites:
            satellite.node = render.attachNewNode(satellite.name)
            satellite.sphere = loader.loadModel("models/planet_sphere")
            if satellite == sun:
                satellite.texture = loader.loadTexture("models/sun_1k_tex.jpg")
            elif satellite.mass > 2:
                satellite.texture = loader.loadTexture("models/earth_1k_tex.jpg")
            elif satellite.mass <= 2:
                satellite.texture = loader.loadTexture("models/venus_1k_tex.jpg")
            satellite.sphere.setTexture(satellite.texture)
            satellite.sphere.reparentTo(satellite.node)
            if satellite == sun:
                satellite.sphere.setScale(2)
            else:
                satellite.sphere.setScale(1)
                satellite.vx = -0.04
                satellite.vy = 0.08
            satellite.node.setPos(satellite.x, satellite.y, satellite.z)

    # def rotateSatellites(self):
    #     self.day_period_sun = self.sun.hprInterval(40, Vec3(360, 0, 0))

    #     self.orbit_period_earth = self.orbit_root_earth.hprInterval(60, Vec3(360, 20, 40))
    #     self.day_period_earth = self.earth.hprInterval(1, Vec3(360, 0, 0))

    #     self.orbit_period_moon = self.orbit_root_moon.hprInterval(60 * 0.749, Vec3(360, 0, 0))
    #     self.day_period_moon = self.moon.hprInterval(0.0749, Vec3(360, 0, 0))

    #     self.day_period_sun.loop()
    #     self.orbit_period_earth.loop()
    #     self.day_period_earth.loop()
    #     self.day_period_moon.loop()
    #     self.orbit_period_moon.loop()

    def moveSatellites(self, task):
        i = False
        for p1 in self.satellites:
            if p1 is sun:
                continue
            for p2 in self.satellites:
                if p2 is p1:
                    continue
                p1.addAcceleration(p2)
            p1.updatePosition()
            p1.node.setPos(p1.x, p1.y, p1.z)
            self.points.append( p1.node.getPos( ) )
            print str(p1.name) + ' x-coordinate: ' + str(p1.x)
            print str(p1.name) + ' y-coordinate: ' + str(p1.y)
            print 'X-speed: ' + str(p1.vx)
            print 'Y-speed: ' + str(p1.vy)
            if i is False:
                render.attachNewNode( self.create( ) )
                i = True
        return task.cont

    def create( self ):
        segs = LineSegs( )
        segs.setThickness( 2.0 )
        segs.setColor( Vec4(1,1,0,1) )
        segs.moveTo( self.points[0] )
        for p in self.points[1:]: segs.drawTo( p )
        return segs.create( )

class Camera(DirectObject.DirectObject):
    def __init__(self):
        self.accept('wheel_down',self.cameraDown)
        self.accept('wheel_up',self.cameraUp)
        self.cameraZ = 360
    def cameraDown(self):
        camera.setPos(0,0,self.cameraZ/2)
    def cameraUp(self):
        camera.setPos(0,0,self.cameraZ)

c = Camera()


starList = []
venus = Satellite('Venus', -15, -30, 0, 2)
earth = Satellite('Earth', 30, 30, 0, 3)
sun = Satellite('Sun', 0, 0, 0, 1600)
#starList.append(venus)
starList.append(earth)
starList.append(sun)

u = Universe(starList)
run()