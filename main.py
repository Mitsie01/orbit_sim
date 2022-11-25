import math
import pygame
from datetime import timedelta
from ambiance import Atmosphere

class Body:
    def __init__(self, name, mass, radius, velocity, direction, x, y, Cd, m_fuel, burn_rate, thrust, nozzle_r):
        self.name = name
        self.m_fuel = m_fuel
        self.mass = mass
        self.radius = radius
        self.direction = direction
        self.vx = velocity*math.cos(direction)
        self.vy = velocity*math.sin(direction)
        self.x = x
        self.y = y
        self.Cd = Cd
        self.A = math.pi*radius**2
        self.burn_rate = burn_rate
        self.thrust = thrust
        self.Ae = math.pi*nozzle_r**2

    def update(self, F, dt):
        if self.m_fuel > 0:
            self.m_fuel -= self.burn_rate*dt
        else:
            self.m_fuel = 0

        ax = F[0]/(self.mass + self.m_fuel)
        ay = F[1]/(self.mass + self.m_fuel)
        self.vx += (ax*dt)
        self.vy += (ay*dt)
        self.x += (self.vx*dt)
        self.y += (self.vy*dt)


bodies = {
    # 0: Body("Sun", 1.9885*10**30, 696_342*10**3, 0, 0, 0, 0),
    # 1: Body("Mercury", 5.97217*10**24, 4880*10**3, 47.36*10**3, 0, 0, -69_816_900*10**3),
    # 2: Body("Venus", 4.8675*10**24, 6051.8*10**3, 35.02*10**3, 0, 0, -108_939_000*10**3),
    # 3: Body("Earth", 5.97217*10**24, 6371*10**3, 29.78*10**3, math.pi, 0, 152_100_000*10**3),
    # 4: Body("Mars", 6.4171*10**23, 3389.5*10**3, 24.07*10**3, math.pi, 0, 249_261_000*10**3),
    # 5: Body("Jupiter", 1.8982*10**27, 69_911*10**3, 13.07*10**3, math.pi/2, 816.363*10**9, 0),
    # 6: Body("Saturn", 5.6834*10**26, 58_232*10**3, 9.68*10**3, math.pi/2, 1514.50*10**9, 0),
    # 7: Body("Uranus", 8.6810*10**25, 25_362*10**3, 6.80*10**3, math.pi, 0, 3006.39*10**9),
    # 8: Body("Neptune", 1.02413*10**26, 24_622*10**3, 5.43*10**3, math.pi/2, 4.54*10**12, 0),

    0: Body("Earth", 5.97217*10**24, 6371*10**3, 0, 0, 0, 0, 0.1, 0, 0, 0, 0),
    1: Body("Moon", 7.342*10**22, 1737.4*10**3, 1.022*10**3, -math.pi, 0, 384399*10**3, 0.1, 0, 0, 0, 0),
    # 2: Body("Black-Brant", 243, 0.21, 0, (11*math.pi)/20, 0, 6371.1*10**3, 0.3, 1018, 10, 69.4*10**3, 0.17),
    3: Body("b1", 3000, 3, 870, math.pi/2, 394399*10**3, 0, 0.1, 0, 0, 0, 0),
    4: Body("b2", 3000, 3, 8040, 0, 0, -12000*10**3, 0.1, 0, 0, 0, 0),
}


def Fgrav(self, obj):
    G = 6.67408*10**-11
    r = ((self.x-obj.x)**2 + (self.y-obj.y)**2)**0.5
    Fg = (G*self.mass*obj.mass)/(r**2)

    Fgx = ((obj.x-self.x)/r)*Fg
    Fgy = ((obj.y-self.y)/r)*Fg

    Fg = [Fgx, Fgy]

    return Fg

def Fdrag(earth, obj):
    r = (((earth.x-obj.x)**2 + (earth.y-obj.y)**2)**0.5) - earth.radius

    vx = obj.vx - earth.vx
    vy = obj.vy - earth.vy

    v = (vx**2 + vy**2)**0.5

    if r < 81020 and r > -5000:
        Fd = 0.5*Atmosphere(r).density[0]*obj.Cd*obj.A*(v**2)
    else:
        Fd = 0

    Fdx = (-vx/v)*Fd
    Fdy = (-vy/v)*Fd

    Fd = [Fdx, Fdy]

    return Fd


def Fthrust(earth, obj):
    H = 7640
    r = (((earth.x-obj.x)**2 + (earth.y-obj.y)**2)**0.5) - earth.radius

    vx = obj.vx - earth.vx
    vy = obj.vy - earth.vy

    v = (vx**2 + vy**2)**0.5

    if r < 81020 and r > -5000:
        Pa = Atmosphere(r).pressure[0]
    else:
        Pa = 0
    
    if obj.m_fuel > 0:
        Ft = obj.thrust+obj.Ae*Pa*(1-math.exp(-r/H))
    else:
        Ft = 0


    if abs(v) < 0.01:
        Ftx = (vx/v)*Ft
        Fty = (vy/v)*Ft
    else:
        Ftx = Ft*math.cos(obj.direction)
        Fty = Ft*math.sin(obj.direction)

    Ft = [Ftx, Fty]

    return Ft


t = 0
dt = 100

WIDTH = 1000
HEIGHT = 1000

x_max = 450_000*10**3
y_max = 450_000*10**3

xzero = WIDTH/2

yzero = HEIGHT/2

m_to_x = xzero/x_max
m_to_y = yzero/y_max


pygame.init()
scr = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SIM')
font = pygame.font.SysFont("Arial", 20)  
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    scr.fill((255, 255, 255))

    if t > (60*60*24)*365:

        y = t // (60*60*24*365)
        d = (t % (60*60*24*360))//(60*60*24)

        text = font.render(f"t = {y}y,{d}d", True, (0, 0, 0))
    else:
        td = timedelta(seconds=int(t))

        text = font.render(f"t = {td}", True, (0, 0, 0))

    pygame.draw.line(scr, (200, 200, 200), (0, HEIGHT/2), (WIDTH, HEIGHT/2), 1)
    pygame.draw.line(scr, (200, 200, 200), (WIDTH/2, 0), (WIDTH/2, HEIGHT), 1)

    # Calculate gravitational force applied on each body by all bodies
    for body in bodies.values():
        Fg = [0, 0]
        Fd = [0, 0]
        Ft = [0, 0]

        if body.name != "Earth":
            Fds = Fdrag(bodies[0], body)
            Fd[0] += Fds[0]
            Fd[1] += Fds[1]

            Fts = Fthrust(bodies[0], body)
            Ft[0] += Fts[0]
            Ft[1] += Fts[1]

        for i in bodies.values():
            if body != i:
                Fgs = Fgrav(body, i)
                Fg[0] += Fgs[0]
                Fg[1] += Fgs[1]

                alt = ((body.x-i.x)**2 + (body.y-i.y)**2)**0.5 - (body.radius + i.radius)

                # remove body in collision
                if alt <= 0:
                    if body.radius < i.radius:
                        bodies = {key:val for key, val in bodies.items() if val != body}
                    elif body.radius >= i.radius:
                        bodies = {key:val for key, val in bodies.items() if val != i}

        # Calculate sum of forces on body
        F = [0, 0]
        F[0] = Fg[0] + Fd[0] + Ft[0]
        F[1] = Fg[1] + Fd[1] + Ft[1]

        # Update forces on body
        body.update(F, dt)

        drawrad = body.radius*m_to_x
        if drawrad <= 2:
            drawrad = 2

        pygame.draw.circle(scr, (200, 0, 0), ((body.x)*m_to_x + xzero, (-body.y)*m_to_y + yzero), drawrad)

    scr.blit(text,(20, 20)) 
    pygame.display.flip()
    t += dt

pygame.quit()