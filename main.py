import pygame
import sys

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


class Slider():
    minval: float
    maxval: float
    step: float
    val: float
    font = pygame.font.Font(None, 74)


    def __init__(self, rang, step, keybind, center, val=None):
        self.minval, self.maxval = rang
        self.step = step
        self.increase, self.decrease = keybind
        self.center = center
        if not val:
            self.val = self.minval + 0.5*(self.maxval - self.minval)
    def draw(self):
        self.surface = self.font.render(str(self.val), True, WHITE)
        self.rect = self.surface.get_rect(center=self.center.get_absolute())
        screen.blit(self.surface, self.rect)


    def check_binds(self):
        keys = pygame.key.get_pressed()
        if keys[self.increase] and self.val + self.step < self.maxval:
            self.val += self.step
        elif keys[self.decrease] and self.val - self.step > self.minval:
            self.val -= self.step
grav = Slider((-100, 100), 1, (pygame.K_UP, pygame.K_DOWN), Vec2(0, 0))

timespeed = Slider((-10, 10), 0.1, (pygame.K_i, pygame.K_k), Vec2(0, 100))

class Body:
    def gravitay(self, other):
        r = (other.pos + -1*self.pos).magnitude()
        mag = grav.val*self.mass*other.mass / r**2
        self.netF += mag * self.pos.get_pointing_unitvector(other.pos)
        

    def movement_update(self):
        self.acc = 1/self.mass * self.netF
        self.netF = Vec2(0,0)

        self.vel += (timespeed.val*(1/60) * self.acc)

        self.pos += (timespeed.val*(1/60) * self.vel)
        


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
    running = True

    earth = Body(color=(0, 0, 255), pos=Vec2(0, 0), radius=63, mass=50)
    moon = Body(color=WHITE, pos=Vec2(38, 0), radius=17, mass=74, vel=Vec2(0,8))
    boon = Body(color=(0, 255, 0), pos=Vec2(-12, 0), radius=27, mass=63, vel=Vec2(0,-3))
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        grav.check_binds()
        timespeed.check_binds()


        # Game logic goes here
        earth.gravitay(moon)
        earth.gravitay(boon)
        moon.gravitay(earth)
        moon.gravitay(boon)
        boon.gravitay(earth)
        boon.gravitay(moon)
        earth.movement_update()
        moon.movement_update()
        boon.movement_update()
        # Clear the screen
        screen.fill(BLACK)

        # Drawing code goes here
        earth.draw()
        moon.draw()
        boon.draw()
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
