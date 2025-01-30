import pygame
import sys
from math import log, ceil
import random

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Boilerplate")

# Clock for controlling the frame rate
clock = pygame.time.Clock()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Vec2:
    x: float
    y: float
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)
    def __rmul__(self, other):
        return Vec2(self.x * other, self.y * other)
    def __repr__(self):
        return f"[{self.x},{self.y}]"
    def magnitude(self):
        return (self.x**2 + self.y**2)**0.5
    def get_absolute(self):
        return (self.x+SCREEN_WIDTH*0.5, 0.5*SCREEN_HEIGHT-self.y)
    def get_pointing_unitvector(self, other): 
        vector = other + -1*self
        mag = vector.magnitude()
        if mag == 0:
            return Vec2(0,0)
        return (1/mag) * vector
def from_absolute(xy):
    x, y = xy
    return Vec2(x - SCREEN_WIDTH*0.5, 0.5*SCREEN_HEIGHT-y)


class Slider():
    minval: float
    maxval: float
    step: float
    val: float
    label: str
    font = pygame.font.Font(None, 32)


    def __init__(self, label, rang, step, keybind, center, val=None):
        self.label = label
        self.minval, self.maxval = rang
        self.step = step
        self.increase, self.decrease = keybind
        self.center = center
    
        if not val:
            self.val = self.minval + 0.5*(self.maxval - self.minval)
    def __repr__(self):
        decimals = ceil(-log(self.step))
        if decimals > 0:
            s = str(round(self.val, decimals))
        else:
            s = str(int(self.val))
        return self.label+": "+s
    def draw(self):
        self.surface = self.font.render(str(self), True, WHITE)
        self.rect = self.surface.get_rect(center=self.center.get_absolute())
        screen.blit(self.surface, self.rect)


    def check_binds(self):
        keys = pygame.key.get_pressed()
        if keys[self.increase] and self.val + self.step <= self.maxval:
            self.val += self.step
        elif keys[self.decrease] and self.val - self.step >= self.minval:
            self.val -= self.step
grav = Slider("G", (-100, 100), 1, (pygame.K_UP, pygame.K_DOWN), Vec2(-300, -250))

timespeed = Slider("t", (-100, 100), 0.1, (pygame.K_i, pygame.K_k), Vec2(-200, -250))
timestop = False
class Body:
    drag = False
    def gravitay(self, other):
        r = (other.pos + -1*self.pos).magnitude()
        if r < self.radius + other.radius:
            self.netF += -20 * (other.pos + -1 * self.pos)
            return 
        mag = grav.val*self.mass*other.mass / r**2
        self.netF += mag * self.pos.get_pointing_unitvector(other.pos)
        

    def movement_update(self):
        if self.drag:
            keys = pygame.mouse.get_pressed()
            if keys[0]:
                self.pos = from_absolute(pygame.mouse.get_pos())
                return
        self.drag = False
        self.acc = 1/self.mass * self.netF
        self.netF = Vec2(0,0)

        self.vel += (timespeed.val*int(timestop)*(1/60) * self.acc)

        self.pos += (timespeed.val*int(timestop)*(1/60) * self.vel)


    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos.get_absolute(), self.radius)
    def __init__(self, color, pos: Vec2, radius, mass, vel=Vec2(0, 0), netF=Vec2(0, 0)):
        self.color = color
        self.pos = pos
        self.radius = radius
        self.mass = mass
        self.vel = vel
        self.acc = (1/mass) * netF
        self.netF = netF

# Main game loop
def main():
    global timestop
    running = True
    random.seed(3)
    #earth = Body(color=(0, 0, 255), pos=Vec2(0, 0), radius=63, mass=500)
    #moon = Body(color=WHITE, pos=Vec2(38, 0), radius=17, mass=74)
    #boon = Body(color=(0, 255, 0), pos=Vec2(-12, 0), radius=27, mass=63)
    bodies = []
    rancol = lambda: (random.randint(1,250), random.randint(1,250), random.randint(1,250))
    for i in range(200):
        r = random.random()*0.2+0.1
        bodies.append(Body(color=rancol(), pos=SCREEN_HEIGHT * Vec2(random.random()-0.5, random.random()-0.5), radius=r*25, mass=r*100))

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    timestop = not timestop
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = from_absolute(event.pos)
                for body in bodies:
                    dist = (body.pos + -1 * mousepos).magnitude()
                    if dist < body.radius:
                        body.drag = True
        grav.check_binds()
        timespeed.check_binds()


        # Game logic goes here
        for body in bodies:
            for otherbody in bodies:
                body.gravitay(otherbody)
        for body in bodies:
            body.movement_update()
        # Clear the screen
        screen.fill(BLACK)

        # Drawing code goes here
        for body in bodies:
            body.draw()

        grav.draw()
        timespeed.draw()
        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    main()
