# Author: Niklas Strengell
# Kosminen simulaattori

import direct.directbase.DirectStart #Panda initialize
from panda3d.core import Vec3, Vec4, Point3, LineSegs #Modules
from direct.gui.DirectGui import * #The GUI objects
from satellite import Satellite, State, Derivative #The actual gravity simulation
from direct.task import Task
from direct.showbase import DirectObject
import sys

t, dt = 0., 1.
i = False

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
        # taskMgr.doMethodLater(0.01, self.drawLines, 'Draw Orbits')

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
            elif satellite._m > 2:
                satellite.texture = loader.loadTexture("models/earth_1k_tex.jpg")
            elif satellite._m <= 2:
                satellite.texture = loader.loadTexture("models/venus_1k_tex.jpg")
            satellite.sphere.setTexture(satellite.texture)
            satellite.sphere.reparentTo(satellite.node)
            if satellite == sun:
                satellite.sphere.setScale(2)
            else:
                satellite.sphere.setScale(1)

            satellite.node.setPos(satellite._st._x, satellite._st._y, 0)

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
        # i = False
        # a = False
        # counter = 0
        for p1 in self.satellites:
            if p1 is sun:
                continue
            p1.updatePlanet(t, dt)
            p1.node.setPos(p1._st._x, p1._st._y, 0)

        #     if counter % 1e32 == 0:
        #         print "Added point"
        #         p1.points.append( p1.node.getPos( ) )

        #     if i or a is False:
        #         node = self.create(p1)
        #         render.attachNewNode(node)
        #         if i is True:
        #             a = False
        #         i = True
        # counter += 1
        return task.cont

    def drawLines(self, task):
        global i
        earth.points.append(earth.node.getPos())
        if i is False:
            node = self.create(earth)
            render.attachNewNode(node)
            i = True
            print "Derb"
        print i, task.delayTime
        return task.again

    def create(self, s):
        segs = LineSegs( )
        segs.setThickness( 2.0 )
        segs.setColor( Vec4(1,0,0,1) )
        segs.moveTo( s.points[0] )
        for p in s.points[1:]:
            segs.drawTo( p )
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

earthState = State(30, 30, -0.04, 0.08)
venusState = State(8, 10, -0.04, 0.08)
sunState = State(0, 0, 0, 0)

venus = Satellite('Venus', venusState, 1, starList)
earth = Satellite('Earth', earthState, 3, starList)
sun = Satellite('Sun', sunState, 1600, starList)
starList.append(venus)
starList.append(earth)
starList.append(sun)

u = Universe(starList)
run()