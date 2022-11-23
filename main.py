import math
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Body:
    def __init__(self, name, mass, radius, velocity, direction, x, y):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.vx = velocity*math.cos(direction)
        self.vy = velocity*math.sin(direction)
        self.x = x
        self.y = y

    def update(self, F, dt):
        ax = F[0]/self.mass
        ay = F[1]/self.mass
        self.vx += (ax*dt)
        self.vy += (ay*dt)
        self.x += (self.vx*dt)
        self.y += (self.vy*dt)


bodies = {
    0: Body("Earth", 5.97217*10**24, 6371*10**3, 0, 0, 0, 0),
    1: Body("Moon", 7.342*10**22, 1737.4*10**3, 1022, math.pi/2, 390_000*10**3, 0)
}


def Fgrav(mass_self, x_self, y_self, mass2, x2, y2):
    G = 6.67408*10**-11
    r = ((x_self-x2)**2 + (y_self-y2)**2)**0.5
    Fg = (G*mass_self*mass2)/(r**2)

    Fgx = ((x2-x_self)/r)*Fg
    Fgy = ((y2-y_self)/r)*Fg

    Fg = [Fgx, Fgy]

    return Fg



dt = 10000


for t in range(0, 500):
    
    # Calculate gravitational force applied on each body by all bodies
    for body in bodies.values():
        Fg = [0, 0]
        for i in bodies.values():
            if body != i:
                Fgs = Fgrav(body.mass, body.x, body.y, i.mass, i.x, i.y)
                Fg[0] += Fgs[0]
                Fg[1] += Fgs[1]

        # Calculate sum of forces on body
        F = Fg

        # Update forces on body
        body.update(F, dt)
        plt.scatter(body.x, body.y)

plt.show()