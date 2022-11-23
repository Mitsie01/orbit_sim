import math
import pygame
from datetime import timedelta

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
    1: Body("Moon", 7.342*10**22, 1737.4*10**3, 1022, math.pi/2, 390_000*10**3, 0),
    # 2: Body("cheese", 7.342*10**22, 1737.4*10**3, 1022, -math.pi/2, -390_000*10**3, 0)
}


def Fgrav(mass_self, x_self, y_self, mass2, x2, y2):
    G = 6.67408*10**-11
    r = ((x_self-x2)**2 + (y_self-y2)**2)**0.5
    Fg = (G*mass_self*mass2)/(r**2)

    Fgx = ((x2-x_self)/r)*Fg
    Fgy = ((y2-y_self)/r)*Fg

    Fg = [Fgx, Fgy]

    return Fg


t = 0
dt = 20

WIDTH = 800
HEIGHT = 800

x_max = 500000*10**3
y_max = 500000*10**3

xzero = WIDTH/2
xstep = x_max/xzero

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
        for i in bodies.values():
            if body != i:
                Fgs = Fgrav(body.mass, body.x, body.y, i.mass, i.x, i.y)
                Fg[0] += Fgs[0]
                Fg[1] += Fgs[1]

        # Calculate sum of forces on body
        F = Fg

        # Update forces on body
        body.update(F, dt)


    pygame.draw.circle(scr, (200, 0, 0), ((bodies[0].x)*m_to_x + xzero, (-bodies[0].y)*m_to_y + yzero), 15)
    pygame.draw.circle(scr, (0, 0, 200), ((bodies[1].x)*m_to_x + xzero, (-bodies[1].y)*m_to_y + yzero), 10)
    # pygame.draw.circle(scr, (0, 200, 0), ((bodies[2].x)*m_to_x + xzero, (-bodies[2].y)*m_to_y + yzero), 5)
    scr.blit(text,(20, 20)) 
    pygame.display.flip()
    t += dt

pygame.quit()