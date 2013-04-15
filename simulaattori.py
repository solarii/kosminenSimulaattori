# Author: Niklas Strengell
# Kosminen simulaattori

import direct.directbase.DirectStart #Panda initialize
from panda3d.core import Vec3, Vec4, Point3 #Modules
from direct.gui.DirectGui import * #The GUI objects
from satellite import Satellite #The actual gravity simulation
from direct.task import Task
import sys

class Universe:  #This is our main class
    def __init__(self, satelliteList):

        self.title = OnscreenText(
            text="Kosminen Simulaattori",
            style=1, fg=(1, 1, 1, 1), pos=(0.95, -0.95), scale = .06)

        base.setBackgroundColor(0, 0, 0)
        base.disableMouse()
        camera.setPos(0, 0, 45)
        camera.setHpr(0, -90, 0)

        self.satellites = satelliteList

        #This is for convenience, so that you could see the stars and planets
        self.scale = 0.05
        self.orbitscale = 10

        self.loadSatellites()
        #self.rotateSatellites()
        #self.moveSatellites()

        taskMgr.add(self.moveSatellites, 'Move satellites')

    def loadSatellites(self):

        #First load the model for the sky and make it a child for render
        self.sky = loader.loadModel("models/solar_sky_sphere")
        self.sky.reparentTo(render)
        self.sky.setScale(400)

        #Load the texture for the sky, and bind it to the model
        self.sky_texture = loader.loadTexture("models/stars_1k_tex.jpg")
        self.sky.setTexture(self.sky_texture, 1)

        # #What would a solar system be without a sun?
        # self.sun = loader.loadModel("models/planet_sphere")
        # self.sun.reparentTo(render)
        # self.sun_texture = loader.loadTexture("models/sun_1k_tex.jpg")
        # self.sun.setTexture(self.sun_texture, 1)
        # self.sun.setScale(2 * self.scale)

        # #Dummy orbits for planets and let's attach them to render!
        # self.orbit_root_earth = render.attachNewNode('orbit_root_earth')

        # #Same for the moon
        # self.orbit_root_moon = (self.orbit_root_earth.attachNewNode('orbit_root_moon'))

        #Load the satellites
        # self.earth = loader.loadModel('models/planet_sphere')
        # self.earth_texture = loader.loadTexture('models/earth_1k_tex.jpg')
        # self.earth.setTexture(self.earth_texture, 1)
        # self.earth.reparentTo(self.orbit_root_earth)
        # self.earth.setScale(self.scale)
        # self.earth.setPos(self.orbitscale, 4, 0)

        # self.orbit_root_moon.setPos(self.orbitscale, 0, 0)
        # self.moon = loader.loadModel('models/planet_sphere')
        # self.moon_texture = loader.loadTexture('models/moon_1k_tex.jpg')
        # self.moon.setTexture(self.moon_texture)
        # self.moon.reparentTo(self.orbit_root_moon)
        # self.moon.setScale(0.1 * self.scale)
        # self.moon.setPos(0.1 * self.orbitscale, 0, 0)


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
                satellite.sphere.setScale(0.5)
            else:
                satellite.sphere.setScale(0.2)
            satellite.node.setPos(satellite.x, satellite.y, satellite.z)

    def rotateSatellites(self):
        self.day_period_sun = self.sun.hprInterval(40, Vec3(360, 0, 0))

        self.orbit_period_earth = self.orbit_root_earth.hprInterval(60, Vec3(360, 20, 40))
        self.day_period_earth = self.earth.hprInterval(1, Vec3(360, 0, 0))

        self.orbit_period_moon = self.orbit_root_moon.hprInterval(60 * 0.749, Vec3(360, 0, 0))
        self.day_period_moon = self.moon.hprInterval(0.0749, Vec3(360, 0, 0))

        self.day_period_sun.loop()
        self.orbit_period_earth.loop()
        self.day_period_earth.loop()
        self.day_period_moon.loop()
        self.orbit_period_moon.loop()

    def moveSatellites(self, task):
        for p1 in self.satellites:
            if p1 is sun:
                continue
            for p2 in self.satellites:
                if p2 is p1:
                    continue
                p1.addAcceleration(p2)
            p1.updatePosition()
            p1.node.setPos(p1.x, p1.y, p1.z)
            print p1.x
            print p1.y
        return task.cont

starList = []
venus = Satellite('Venus', 5, 1, 0, 2)
earth = Satellite('Earth', 15, 4, 0, 3)
sun = Satellite('Sun', 0, 0, 0, 15)
starList.append(venus)
starList.append(earth)
starList.append(sun)
u = Universe(starList)
run()