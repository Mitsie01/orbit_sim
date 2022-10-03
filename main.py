import math
import numpy as np
import scipy.constants
import scipy.integrate
import matplotlib as plot

import body
import satellite

# General constants
G = scipy.constants.G

dt = 0.1
tmin = 0
tmax = 100

# Initial conditions
velocity = 0
altitude = 0
pitch = 0
longitude = 0

# Initial condition convertion
r = body.radius + altitude
pitch = math.radians(pitch)
longitude = math.radians(longitude)
x0 = math.cos(longitude)*r
y0 = math.sin(longitude)*r
vx0 = math.cos(longitude+90-pitch)*velocity
vy0 = math.sin(longitude+90-pitch)*velocity


# Forces
def gravity(G, M1, M2, r):
    Fgrav = G*((M1*M2)/r**2)
    return Fgrav


#x(0) = x
#x(1) = y
#x(2) = x'
#x(3) = y'

sat1 = np.array([x0, y0, vx0, vy0])

for t in np.arange(tmin, tmax, dt):
    Fxtot = 20
    Fytot = 0

    ax = Fxtot/satellite.mass
    ay = Fytot/satellite.mass

    vx = scipy.integrate.ode(t, ax)


    print(f'{round(t, 2)}, {ax}, {vx}')