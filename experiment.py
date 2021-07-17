

import pygame
import numpy as np

import space, scatterer

class Programme(object):

    def __init__(self, type):
        self.type = type

    def returnFluxDirection(self):
        if self.type == 'mouse':
            return space.unit(space.centre - np.array(pygame.mouse.get_pos()))
        return (1, 0)


class Process(object):

    """
    The Process class takes a flux (a list of Particles) and a Scatterer
    Then, given the process
    """

    def __init__(self, flux, scatterer):
        self.flux = flux
        self.scatterer = scatterer


# LinAlg methods

# intersection method
# we will consider generalised scatterers
def findIntersections(particle, scatterer):
    collided = set()
    R = np.array([[0, -1], [1, 0]])
    for tangent in scatterer.tangents:
        if np.dot(np.dot(R, particle.vel), tangent.dir) == 0:
            continue
        intersection = space.returnLineIntersection(particle.pos, particle.vel, tangent)
        inter_tangent_diff = intersection - tangent.pos
        if 0 <= np.dot(inter_tangent_diff, tangent.dir) <= np.dot(tangent.dir, tangent.dir):
            collided |= {tuple(intersection)}

    return collided

def mouseParticle(scat):
    x, y = pygame.mouse.get_pos()
    particle = scatterer.Particle((x, y), -((x, y) - space.centre), 10)
    collided = findIntersections(particle, scat)
    circles = []
    for collid in collided:
        circles.append(scatterer.Particle(collid, (0, 0), 10))

    return circles


# set method

def createParticleBeams(particle_group):
    positions = set()
    for part in particle_group:
        while 0 <= part.pos[0] <= space.WIDTH and 0 <= part.pos[1] <= space.HEIGHT:
            part.updated()
            positions |= {part.pos}

    return positions

def setCollisions(particle_group, scat):
    """
    # BROKEN :/
    collided = set()
    particle_positions = {tuple(particle.pos) for particle in particle_group}
    radius = particle_group[0].radius
    if type(particle_group) is list:
        while not (particle_positions <= collided):
            for pos in particle_positions - collided:
                # particle.update() # problem area
                shifted = scat.curve - pos 
                inter = {point + pos for point in shifted if np.dot(point, point) <= radius ** 2}
                collided |= inter

    """

    collided = set()
    positions = createParticleBeams(particle_group)
    
        
    return collided


def mouseParticleSet(scat):
    x, y = pygame.mouse.get_pos()
    particle = scatterer.Particle((x, y), -((x, y) - space.centre), 10)
    collided = setCollisions([particle], scat)
    circles = []
    for collid in collided:
        circles.append(scatterer.Particle(collid, (0, 0), 10))

    return circles
