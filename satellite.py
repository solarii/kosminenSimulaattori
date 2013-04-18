from pandac.PandaModules import Point3, Vec4
from pandac.PandaModules import LineSegs
import math

# Gravity is strong in this universe...
gravityConstant = 1e-4

class State(object):
    """"Class representing the state of the object (position and velocity in 2D)"""
    def __init__(self, x, y, vx, vy):
        self._x, self._y, self._vx, self._vy = x, y, vx, vy

    def __repr__(self):
        return 'x:{x}, y:{y}, vx:{vx}, vy:{vy}'.format(
            x=self._x, y=self._y, vx=self._vx, vy=self._vy)

class Derivative(object):
    """docstring for Derivative"""
    def __init__(self, dx, dy, dvx, dvy):
        self._dx, self._dy, self._dvx, self._dvy = dx, dy, dvx, dvy
    def __repr__(self):
        return 'dx:{x}, dy:{y}, dvx:{vx}, dvy:{vy}'.format(
            x=self._dx, y=self._dy, vx=self._dvx, vy=self._dvy)

class Satellite(object):
    """docstring for Satellite"""
    def __init__(self, name, state, mass, listOfPlanets):
        self.name = name
        self._st = state
        self._m = mass
        self.listOfPlanets = listOfPlanets
        self.points = []
        self.drawOrbit = False

    def __repr__(self):
        return repr(self._st)

    def acceleration(self, state, unused_t):
        """Calculate the acceleration caused by other planets"""
        ax = 0.0
        ay = 0.0
        for p in self.listOfPlanets:
            if p is self:
                continue
            dx = p._st._x - state._x
            dy = p._st._y - state._y
            dsq = dx*dx + dy*dy
            dr = math.sqrt(dsq)
            force = gravityConstant * self._m * p._m / dsq if dsq > 1e-10 else 0
            ax += force * dx/dr
            ay += force * dy/dr
        return (ax, ay)

    def initialDerivative(self, state, t):
        """Part of Runge-Kutta"""
        ax, ay = self.acceleration(state, t)
        return Derivative(state._vx, state._vy, ax, ay)

    def nextDerivative(self, initialState, derivative, t, dt):
        """Part of Runge-Kutta"""
        state = State(0., 0., 0., 0.)
        state._x = initialState._x + derivative._dx*dt
        state._y = initialState._y + derivative._dy*dt
        state._vx = initialState._vx + derivative._dvx*dt
        state._vy = initialState._vy + derivative._dvy*dt
        ax, ay = self.acceleration(state, t+dt)
        return Derivative(state._vx, state._vy, ax, ay)

    def updatePlanet(self, t, dt):
        """Le Magic of Runge-Kutta"""
        a = self.initialDerivative(self._st, t)
        b = self.nextDerivative(self._st, a, t, dt*0.5)
        c = self.nextDerivative(self._st, b, t, dt*0.5)
        d = self.nextDerivative(self._st, c, t, dt)
        dxdt = 1.0/6.0 * (a._dx + 2.0*(b._dx + c._dx) + d._dx)
        dydt = 1.0/6.0 * (a._dy + 2.0*(b._dy + c._dy) + d._dy)
        dvxdt = 1.0/6.0 * (a._dvx + 2.0*(b._dvx + c._dvx) + d._dvx)
        dvydt = 1.0/6.0 * (a._dvy + 2.0*(b._dvy + c._dvy) + d._dvy)
        self._st._x += dxdt*dt
        self._st._y += dydt*dt
        self._st._vx += dvxdt*dt
        self._st._vy += dvydt*dt

    # def create(self):
    #     segs = LineSegs( )
    #     segs.setThickness( 2.0 )
    #     segs.setColor( Vec4(1,0,0,1) )
    #     segs.moveTo( self.points[0] )
    #     for p in self.points[1:]:
    #         segs.drawTo( p )
    #         print "Drew"
    #     return segs.create( )
