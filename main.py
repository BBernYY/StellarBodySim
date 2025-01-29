import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

G = 6.6743*10**-11 # when mass is in metric tonnes and position in km
PIXEL_TO_KM = 1000
TIMESPEED = 43

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Boilerplate")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

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
        return (self.x/PIXEL_TO_KM+SCREEN_WIDTH*0.5, 0.5*SCREEN_HEIGHT-self.y/PIXEL_TO_KM)
    def get_pointing_unitvector(self, other): 
        vector = other + -1*self
        mag = vector.magnitude()
        if mag == 0:
            return Vec2(0,0)
        return (1/mag) * vector
        

class Body:
    def gravitay(self, other):
        r = (other.pos + -1*self.pos).magnitude()
        mag = G*self.mass*other.mass / r**2
        self.netF += mag * self.pos.get_pointing_unitvector(other.pos)
        

    def movement_update(self):
        self.acc = 1/self.mass * self.netF
        self.netF = Vec2(0,0)

        self.vel += (TIMESPEED*(1/60) * self.acc)

        self.pos += (TIMESPEED*(1/60) * self.vel)
        


    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos.get_absolute(), self.radius/PIXEL_TO_KM)
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

    earth = Body(color=(0, 0, 255), pos=Vec2(0, 0), radius=6371, mass=5.972*10**21)
    moon = Body(color=WHITE, pos=Vec2(384.4*10**3, 0), radius=1732.5, mass=7.348*10**19, vel=Vec2(0,800))
    boon = Body(color=(0, 255, 0), pos=Vec2(-124*10**3, 0), radius=2737.5, mass=6.348*10**19, vel=Vec2(0,-300))
    while running:
        print(boon.pos.get_absolute())
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
