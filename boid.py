import pygame
import random
from vector2d import Vector2D
import math


class Boid(pygame.sprite.Sprite):
    def __init__(self, position):
        # initialize the super sprite class
        super(Boid, self).__init__()

        # Setup the movement vectors.
        self.velocity = Vector2D(random.randint(-2, 2), random.randint(-2, 2))

        self.surf = self.makeSurface()
        self.rect = self.surf.get_rect(center=position)
        self.max_velocity = 3

        # Flocking Charactoristics
        self.sightRange = 150
        self.max_acceleration = 0.1
        self.alignWeight = 1/36
        self.avoidWeight = 0.5
        self.apprachWeight = 1/100

    def update(self, neighborBoids):
        # Loop Screen
        margin = 200
        factor = 0.1

        if(self.rect.right < margin):
            self.velocity.add(Vector2D(factor, 0))
        if(self.rect.left > 1000-margin):
            self.velocity.add(Vector2D(-factor, 0))
        if(self.rect.top > 1000-margin):
            self.velocity.add(Vector2D(0, -factor))
        if(self.rect.bottom < margin):
            self.velocity.add(Vector2D(0, factor))

        # Get accerlation
        acceleration = self.get_acceleration(neighborBoids)

        # Apply steering accerlation to velocity
        self.velocity.add(acceleration)

        # Scale back the velocity to normal speed
        self.velocity.unitize()
        self.velocity.scale(self.max_velocity)

        # Rotate to align with the new velocity
        theta = self.velocity.calc_angle()
        self.rotate(theta)

        # Move following the velocity vector
        self.rect.move_ip(self.velocity.to_tuple())

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
        boidSurf = pygame.Surface((8, 16))

        # blit the image onto the Surface
        boidSurf.fill((255, 0, 255))
        boidSurf.set_colorkey((255, 0, 255))
        triangle_points = ((4, 0), (0, 16), (8, 16))
        pygame.draw.polygon(boidSurf, (143, 200, 207), triangle_points)

        return boidSurf

    # ===============================
    # Flocking Methods
    # ===============================

    def calc_avoid(self, boids):
        """Returns the avoid accerlation"""
        avoidAccel = Vector2D(0, 0)
        position = self.rect.center

        # Add up all the separation vectors
        for boid in boids:
            xdiff = position[0]-boid.rect.center[0]
            ydiff = position[1]-boid.rect.center[1]
            diff = Vector2D(xdiff, ydiff)
            diff.scale(1/(diff.calc_magnitude()**2))
            avoidAccel.add(diff)

        avoidAccel.scale(self.avoidWeight)
        return avoidAccel

    #
    def calc_align(self, boids):
        """Returns the acceleration vector to align velocity direction with the
        average velocity direction of nearby boids."""
        velocities = Vector2D(0, 0)
        velocity = self.velocity

        # No change if there are no other boids around.
        if not(len(boids)):
            return Vector2D(0, 0)

        # Accumulates velocities
        for boid in boids:
            velocities.add_values(boid.velocity.x, boid.velocity.y)

        # Averages velocities
        if len(boids) > 1:
            velocities.scale(1/(len(boids)-1))

        xdiff = velocities.x - velocity.x
        ydiff = velocities.y - velocity.y
        alignAccel = Vector2D(xdiff, ydiff)
        alignAccel.scale(self.alignWeight)
        return alignAccel

    def calc_approach(self, boids):
        """Returns the approach accerlation"""
        approachAccel = Vector2D(0, 0)
        position = self.rect.center

        # Add up all the separation vectors
        for boid in boids:
            xdiff = boid.rect.center[0]-position[0]
            ydiff = boid.rect.center[1]-position[1]
            approachAccel.add_values(xdiff, ydiff)

        # Makes accleration based on average position
        if len(boids) > 0:
            approachAccel.scale(1/len(boids))

        approachAccel.scale(self.apprachWeight)
        return approachAccel

    def calc_target(self, targetPos):
        position = self.rect.center

        # Ignore (-1, -1) for menu animations
        if(targetPos == (-1, -1)):
            return(Vector2D(0, 0))

        weight = 1/100
        """Returns the acceleration towards the player."""
        xdiff = targetPos[0]-position[0]
        ydiff = targetPos[1]-position[1]
        playerAccel = Vector2D(xdiff, ydiff)
        playerAccel.scale(weight)
        return playerAccel

    def get_acceleration(self, boids):
        """Returns a single acceleration vector in response to nearby boids."""

        # Find the neighboring boids
        neighbors = self.find_neighbors(boids, self.sightRange)

        # Acceleration acccumulator
        # Add acceleration requests in order of importance
        accelRequests = [
            self.calc_avoid(neighbors),
            self.calc_align(neighbors),
            self.calc_approach(neighbors)]

        # Add up requests untill max acceleration is reached
        acceptedRequests = Vector2D(0, 0)
        for request in accelRequests:
            # Add if room
            if acceptedRequests.calc_magnitude() < self.max_acceleration:
                acceptedRequests.add(request)
            # Trim tail if over
            if acceptedRequests.calc_magnitude() > self.max_acceleration:
                tail = acceptedRequests.calc_magnitude()-self.max_acceleration
                request.unitize()
                request.scale(-tail)
                acceptedRequests.add(request)

        return acceptedRequests

    def find_neighbors(self, boids, sightRange):
        """Finds all the boids in a given list within the given distance of the
        indicated position."""
        position = self.rect.center

        # List to hold nearby boids
        nearbyBoids = []

        # Keep boids within distance
        for boid in boids:
            d = math.dist(position, boid.rect.center)
            if((d < sightRange) and (d > 0)):
                nearbyBoids.append(boid)

        return nearbyBoids
