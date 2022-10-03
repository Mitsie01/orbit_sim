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
velocity = 7700
altitude = 400*10**3
pitch = 0
longitude = 0


# Forces
def gravity(G, M1, M2, r):
    Fgrav = G*((M1*M2)/r**2)
    return Fgrav


# Initial condition convertion
r = body.radius + altitude
pitch = math.radians(pitch)
longitude = math.radians(longitude)
x0 = math.cos(longitude)*r
y0 = math.sin(longitude)*r
vx0 = math.cos(longitude+90-pitch)*velocity
vy0 = math.sin(longitude+90-pitch)*velocity

r_mag = math.sqrt(r)
r_x = x0/r_mag
r_y = y0/r_mag

ax0 = (gravity(G, body.mass, satellite.mass, r)/satellite.mass)*-r_x
ay0 = (gravity(G, body.mass, satellite.mass, r)/satellite.mass)*-r_y


# Initialize arrays
B1x = np.array([[x0, y0, tmin]])
B1v = np.array([[vx0, vy0, tmin]])
B1a = np.array([[ax0, ay0, tmin]])


# Start simulation
for t in np.arange(tmin, tmax, dt):
    timestamp = int(t*10)
    print(timestamp)
    print(B1x.item((timestamp,0)))
    print(type(B1x.item(timestamp,0)))

    
    r_mag = math.sqrt((B1x.item((timestamp, 0))**2)+(B1x.item((timestamp, 1))**2))
    r_x = B1x.item((timestamp, 0))/r_mag
    r_y = B1x.item((timestamp, 1))/r_mag

    Fgrav = gravity(G, body.mass, satellite.mass, r)
    Fgravx = Fgrav * -r_x
    Fgravy = Fgrav * -r_y

    Ftotx = Fgravx
    Ftoty = Fgravy

    a = np.array([Ftotx/satellite.mass, Ftoty/satellite.mass, t])

    B1a = np.r_[B1a,[a]]

    vx = scipy.integrate.cumulative_trapezoid(B1a[:,0], B1a[:,2], initial=0) + vx0
    vy = scipy.integrate.cumulative_trapezoid(B1a[:,1], B1a[:,2], initial=0) + vy0

    v = np.array([vx, vy, t])

    B1v = np.r_[B1v,[v]]

    xx = scipy.integrate.cumulative_trapezoid(B1v[:,0], B1v[:,2], initial=0) + x0
    xy = scipy.integrate.cumulative_trapezoid(B1v[:,1], B1v[:,2], initial=0) + y0

    x = np.array([xx, xy, t])

    B1x= np.r_[B1x,[x]]

    print(B1x.item((1,0)))