import pygame
from random import randint
from boid import Boid
from pygame.locals import (
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame modules
pygame.init()

# Create the screen object
pygame.display.set_caption("Flocking")
screen = pygame.display.set_mode((800, 800))
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))

# Make groups of sprites
boids = pygame.sprite.Group()

# Populate with boid
numBoids = 10
for i in range(10):
    position = (randint(0, 800), randint(0, 800))
    boids.add(Boid(position))

# Setup the clock to limit fps
clock = pygame.time.Clock()

# Running control var
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_SPACE:
                print("Space")
                # Pause the sim

    # Paint the background
    screen.blit(background, (0, 0))

    # Update then paint the boids
    boids.update()
    for boid in boids:
        screen.blit(boid.surf, boid.rect)

    pygame.display.flip()
    clock.tick(60)
