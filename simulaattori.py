# Author: Niklas Strengell
# Kosminen simulaattori

import direct.directbase.DirectStart #Panda initialize
from panda3d.core import Vec3, Vec4 #Modules
from direct.gui.DirectGui import * #The GUI objects
import sys

class Universe:  #This is our main class
    def __init__(self):

        self.title = OnscreenText(
            text="Kosminen Simulaattori",
            style=1, fg=(1, 1, 1, 1), pos=(0.95, -0.95), scale = .06)

        base.setBackgroundColor(0, 0, 0)
        base.disableMouse()
        camera.setPos(0, 0, 45)
        camera.setHpr(0, -90, 0)

        #This is for convenience, so that you could see the stars and planets
        self.scale = 0.6
        self.orbitscale = 10

        self.loadSatellites()
        self.rotateSatellites()

    def loadSatellites(self):

        #First load the model for the sky and make it a child for render
        self.sky = loader.loadModel("models/solar_sky_sphere")
        self.sky.reparentTo(render)
        self.sky.setScale(40)

        #Load the texture for the sky, and bind it to the model
        self.sky_texture = loader.loadTexture("models/stars_1k_tex.jpg")
        self.sky.setTexture(self.sky_texture, 1)

        #What would a solar system be without a sun?
        self.sun = loader.loadModel("models/planet_sphere")
        self.sun.reparentTo(render)
        self.sun_texture = loader.loadTexture("models/sun_1k_tex.jpg")
        self.sun.setTexture(self.sun_texture, 1)
        self.sun.setScale(2 * self.scale)

        #Dummy orbits for planets and let's attach them to render!
        self.orbit_root_earth = render.attachNewNode('orbit_root_earth')

        #Same for the moon
        self.orbit_root_moon = (self.orbit_root_earth.attachNewNode('orbit_root_moon'))

        #Load the satellites
        self.earth = loader.loadModel('models/planet_sphere')
        self.earth_texture = loader.loadTexture('models/earth_1k_tex.jpg')
        self.earth.setTexture(self.earth_texture, 1)
        self.earth.reparentTo(self.orbit_root_earth)
        self.earth.setScale(self.scale)
        self.earth.setPos(self.orbitscale, 0, 0)

        self.orbit_root_moon.setPos(self.orbitscale, 0, 0)
        self.moon = loader.loadModel('models/planet_sphere')
        self.moon_texture = loader.loadTexture('models/moon_1k_tex.jpg')
        self.moon.setTexture(self.moon_texture)
        self.moon.reparentTo(self.orbit_root_moon)
        self.moon.setScale(0.1 * self.scale)
        self.moon.setPos(0.1 * self.orbitscale, 0, 0)

    def rotateSatellites(self):
        self.day_period_sun = self.sun.hprInterval(40, Vec3(360, 0, 0))

        self.orbit_period_earth = self.orbit_root_earth.hprInterval(60, Vec3(360, 0, 0))
        self.day_period_earth = self.earth.hprInterval(1, Vec3(360, 0, 0))

        self.orbit_period_moon = self.orbit_root_moon.hprInterval(60 * 0.749, Vec3(360, 0, 0))
        self.day_period_moon = self.moon.hprInterval(0.0749, Vec3(360, 0, 0))

        self.day_period_sun.loop()
        self.orbit_period_earth.loop()
        self.day_period_earth.loop()
        self.day_period_moon.loop()
        self.orbit_period_moon.loop()

u = Universe()
run()