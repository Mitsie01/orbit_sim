import math
import pygame
from datetime import timedelta
from ambiance import Atmosphere

class Body:
    def __init__(self, name, type, mass, radius, velocity, direction, x, y, Cd):
        self.name = name
        self.type = type
        self.mass = mass
        self.radius = radius
        self.direction = direction
        self.vx = velocity*math.cos(direction)
        self.vy = velocity*math.sin(direction)
        self.x = x
        self.y = y
        self.Cd = Cd
        self.A = math.pi*radius**2

    def update(self, F, dt):
        ax = F[0]/self.mass
        ay = F[1]/self.mass
        self.vx += (ax*dt)
        self.vy += (ay*dt)
        self.x += (self.vx*dt)
        self.y += (self.vy*dt)

class Vehicle:
    def __init__(self, name, type, launch_planet, mass, radius, velocity, launch_angle, launch_position, Cd, m_fuel, burn_rate, thrust, nozzle_r):
        self.name = name
        self.type = type
        self.launch_planet = launch_planet
        self.m_fuel = m_fuel
        self.mass = mass
        self.radius = radius
        self.direction = math.radians(launch_angle+(launch_position-90))
        self.vx = velocity*math.cos(self.direction)
        self.vy = velocity*math.sin(self.direction)
        self.launch_position = math.radians(launch_position)
        self.x = (launch_planet.radius+1)*math.cos(self.launch_position) + launch_planet.x
        self.y = (launch_planet.radius+1)*math.sin(self.launch_position) + launch_planet.y
        self.Cd = Cd
        self.A = math.pi*radius**2
        self.burn_rate = burn_rate
        self.thrust = thrust
        self.Ae = math.pi*nozzle_r**2
        self.status = "On launchpad"
        self.alt = 0

    def update(self, F, dt, launch_planet):
        if self.status == "On launchpad":
            self.launch_planet = launch_planet
            self.x = (launch_planet.radius+1)*math.cos(self.launch_position) + launch_planet.x
            self.y = (launch_planet.radius+1)*math.sin(self.launch_position) + launch_planet.y
        else:
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
    ## body inputs: self, name, type, mass, radius, velocity, direction, x, y, Cd
    # # Solar system demo
    # 0: Body("Sun", "Body", 1.9885*10**30, 696_342*10**3, 0, 0, 0, 0, 0.1),
    # 1: Body("Mercury", "Body", 5.97217*10**24, 4880*10**3, 47.36*10**3, 0, 0, -69_816_900*10**3, 0.1),
    # 2: Body("Venus", "Body", 4.8675*10**24, 6051.8*10**3, 35.02*10**3, 0, 0, -108_939_000*10**3, 0.1),
    # 3: Body("Earth", "Body", 5.97217*10**24, 6371*10**3, 29.78*10**3, math.pi, 0, 152_100_000*10**3, 0.1),
    # 4: Body("Mars", "Body", 6.4171*10**23, 3389.5*10**3, 24.07*10**3, math.pi, 0, 249_261_000*10**3, 0.1),
    # 5: Body("Jupiter", "Body", 1.8982*10**27, 69_911*10**3, 13.07*10**3, math.pi/2, 816.363*10**9, 0, 0.1),
    # 6: Body("Saturn", "Body", 5.6834*10**26, 58_232*10**3, 9.68*10**3, math.pi/2, 1514.50*10**9, 0, 0.1),
    # 7: Body("Uranus", "Body", 8.6810*10**25, 25_362*10**3, 6.80*10**3, math.pi, 0, 3006.39*10**9, 0.1),
    # 8: Body("Neptune", "Body", 1.02413*10**26, 24_622*10**3, 5.43*10**3, math.pi/2, 4.54*10**12, 0, 0.1),

    # Missile demo
    0: Body("Earth", "Body", 5.97217*10**24, 6371*10**3, 0, 0, 0, 0, 0.1),
    1: Body("Moon", "Body", 7.342*10**22, 1737.4*10**3, 1.022*10**3, -math.pi, 0, 384399*10**3, 0.1),

    ## Multibody demo
    # 0: Body("Earth", 5.97217*10**24, 6371*10**3, 0, 0, 0, 0, 0.1),
    # 1: Body("Moon", 7.342*10**22, 1737.4*10**3, 1.022*10**3, -math.pi, 0, 384399*10**3, 0.1),
    # 2: Body("Tesla", 3000, 3, 870, math.pi/2, 394399*10**3, 0, 0.1),
    # 3: Body("Moonsat", 3000, 3, 1.488*10**3, -math.pi, 0, 400399*10**3, 0.1),
}

vehicles = {
    # vehicle inputs: name, launch_planet, mass, radius, velocity, launch_angle(deg), launch_positition(deg), Cd, m_fuel, burn_rate, thrust, nozzle_r
    0: Vehicle("Black-Brant","Vehicle", bodies[0], 243, 0.21, 0, 73, 90, 0.3, 1018, 32.42, 69.4*10**3, 0.17),
    1: Vehicle("Black-Brant-XL","Vehicle", bodies[0], 443, 0.31, 0, 40, 100, 0.3, 4518, 32.42, 100.4*10**3, 0.25),
}


for vehicle in vehicles:
    bodies[len(bodies)] = vehicles[vehicle]


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

    if v != 0:
        Fdx = (-vx/v)*Fd
        Fdy = (-vy/v)*Fd
    else:
        Fdx = 0
        Fdy = 0

    Fd = [Fdx, Fdy]

    return Fd


def Fthrust(obj):
    H = 7640
    r = (((obj.launch_planet.x-obj.x)**2 + (obj.launch_planet.y-obj.y)**2)**0.5) - obj.launch_planet.radius

    obj.alt = r

    vx = obj.vx - obj.launch_planet.vx
    vy = obj.vy - obj.launch_planet.vy

    v = (vx**2 + vy**2)**0.5


    if r < 81020 and r > -5000 and obj.launch_planet.name == "Earth":
        Pa = Atmosphere(r).pressure[0]
    else:
        Pa = 0
    
    if obj.m_fuel > 0 and obj.status == "In flight":
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
dtbase = 0.001
dt = dtbase

WIDTH = 1000
HEIGHT = 1000

xzero = WIDTH/2

yzero = HEIGHT/2

x_max = 450_000*10**3
y_max = x_max

veh = 0

x_offset = 0
y_offset = 0

toggle_altitude = False
moving = False


pygame.init()
scr = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SIM')
font = pygame.font.SysFont("Arial", 20)  
pfont = pygame.font.SysFont("Arial", 14)
running = True

# pygame.mixer.init()
# pygame.mixer.music.load("mii.wav")
# pygame.mixer.music.set_volume(1)

# pygame.mixer.music.play()

while running:

    m_to_x = xzero/x_max
    m_to_y = yzero/y_max

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and dt != 0:
                dtp = dt
                dt = 0
            elif event.key == pygame.K_SPACE and dt == 0:
                dt = dtp

            if event.key == pygame.K_UP:
                dt *= 10
            if event.key == pygame.K_DOWN:
                dt /= 10
            if event.key == pygame.K_KP_ENTER:
                dt = dtbase

            if event.key == pygame.K_l:
                vehicles[veh].status = "In flight"
                veh += 1

            if event.key == pygame.K_i:
                if toggle_altitude == False:
                    toggle_altitude = True
                elif toggle_altitude == True:
                    toggle_altitude = False

            if event.key == pygame.K_w:
                y_offset += 20
            if event.key == pygame.K_a:
                x_offset += 20
            if event.key == pygame.K_s:
                y_offset -= 20
            if event.key == pygame.K_d:
                x_offset -= 20

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                x_max /= 1.2
                y_max /= 1.2
            elif event.button == 5:
                x_max *= 1.2
                y_max *= 1.2

            moving = True

        elif event.type == pygame.MOUSEBUTTONUP:
                moving = False

            # Make your image move continuously
        elif event.type == pygame.MOUSEMOTION and moving:
            x_offset += event.rel[0]
            y_offset += event.rel[1]
    
    scr.fill((255, 255, 255))

    if t > (60*60*24)*365:

        y = t // (60*60*24*365)
        d = (t % (60*60*24*360))//(60*60*24)

        t_text = font.render(f"t = {y}y,{d}d", True, (0, 0, 0))
    else:
        td = timedelta(seconds=int(t))
        t_text = font.render(f"t = {td}", True, (0, 0, 0))

    dt_text = font.render(f"Simstep: dt = {dt} sec", True, (0, 0, 0))

    pygame.draw.line(scr, (200, 200, 200), (0, (HEIGHT/2) + y_offset), (WIDTH, (HEIGHT/2) + y_offset), 1)
    pygame.draw.line(scr, (200, 200, 200), ((WIDTH/2) + x_offset, 0), ((WIDTH/2) + x_offset, HEIGHT), 1)

    # Calculate gravitational force applied on each body by all bodies
    for body in bodies.values():
        Fg = [0, 0]
        Fd = [0, 0]
        Ft = [0, 0]

        if body.name != "Earth":
            Fds = Fdrag(bodies[0], body)
            Fd[0] += Fds[0]
            Fd[1] += Fds[1]

            if body.type == "Vehicle":
                Fts = Fthrust(body)
                Ft[0] += Fts[0]
                Ft[1] += Fts[1]

        for i in bodies.values():
            if body != i:
                Fgs = Fgrav(body, i)
                Fg[0] += Fgs[0]
                Fg[1] += Fgs[1]

                alt = ((body.x-i.x)**2 + (body.y-i.y)**2)**0.5 - (body.radius + i.radius)

                # remove body in collision
                if alt <= 0 and body.type == "Body":
                    if body.radius < i.radius:
                        bodies = {key:val for key, val in bodies.items() if val != body}
                    elif body.radius >= i.radius:
                        bodies = {key:val for key, val in bodies.items() if val != i}

        # Calculate sum of forces on body
        F = [0, 0]
        F[0] = Fg[0] + Fd[0] + Ft[0]
        F[1] = Fg[1] + Fd[1] + Ft[1]

        # Update forces on body
        if body.type == "Body":
            body.update(F, dt)
        elif body.type == "Vehicle":
            body.update(F, dt, bodies[0])


        drawrad = body.radius*m_to_x
        if drawrad <= 2:
            drawrad = 2

        if body.type == "Body":
            ptext = pfont.render(f"{body.name}", True, (0, 0, 0))
        elif body.type == "Vehicle":
            ptext = pfont.render(f"{body.name} ({body.status})", True, (0, 0, 0))

        if body.type == "Body":
            pygame.draw.circle(scr, (200, 0, 0), ((body.x)*m_to_x + xzero + x_offset, (-body.y)*m_to_y + yzero + y_offset), drawrad)
        elif body.type == "Vehicle":
            pygame.draw.circle(scr, (0, 0, 200), ((body.x)*m_to_x + xzero + x_offset, (-body.y)*m_to_y + yzero + y_offset), drawrad)
            if toggle_altitude:
                alttext = pfont.render(f"Altitude: {body.alt//1000} km", True, (0, 0, 0))
                scr.blit(alttext,((body.x)*m_to_x + xzero + x_offset + drawrad, (-body.y)*m_to_y + yzero + y_offset + drawrad + 12))
        
        scr.blit(ptext,((body.x)*m_to_x + xzero + x_offset + drawrad, (-body.y)*m_to_y + yzero + y_offset + drawrad))
        

    scr.blit(t_text, (20, 20))
    scr.blit(dt_text, (20, 40)) 
    pygame.display.flip()
    t += dt

pygame.quit()