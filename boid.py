import pygame
import random
from vector2d import Vector2D

# Load the sprite
boidImages = [pygame.image.load('sprites/boid.png')]


class Boid(pygame.sprite.Sprite):
    def __init__(self, position):
        # initialize the super sprite class
        super(Boid, self).__init__()

        # Setup the movement vectors.
        self.velocity = Vector2D(random.randint(-2, 2), random.randint(-2, 2))

        self.surf = self.makeSurface()
        self.rect = self.surf.get_rect(center=position)
        self.max_velocity = 3

    def update(self):
        print("updated")

    def rotate(self, angle):
        # save the old center postion
        oldCenter = self.rect.center

        # sets the current surface to the enemy surface rotated to the
        # indicated angle
        self.surf = pygame.transform.rotate(self.makeSurface(), angle+90)

        # get the rect of the rotated surf and set it's center to the saved
        self.rect = self.surf.get_rect()
        self.rect.center = oldCenter

    def makeSurface(self):
        # Create a surface that will represent the enemy
        boidSurf = pygame.Surface((10, 20))

        # blit the image onto the Surface
        boidSurf.set_colorkey((255, 0, 255))
        boidSurf.blit(boidImages[0], (0, 0))

        return boidSurf
