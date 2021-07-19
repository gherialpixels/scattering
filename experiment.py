
import time

import pygame

import numpy as np

import space
import scatterer
import draw


class MouseProgramme(object):

    def __init__(self, type):
        self.type = type

    def returnFluxDirection(self):
        if self.type == 'mouse':
            return space.unit(space.centre - np.array(pygame.mouse.get_pos()))
        return (1, 0)


class Program(object):

    """
    We should have parameters for:
    - the scatter file
    - whether we're treating a flux, tangent or scatter simulation
    - visuals
    - time interval, duration of time interval
    - mouse control
    """

    def __init__(self, args):
        self.filename = args[0]
        self.scatter_file = args[1]
        self.s = scatterer.Scatterer(Program.create_scatterer(self.scatter_file))

        self.config = args[2:][::-1]
        print("last term: ", self.config[-1])
        self.time_limit = 0

        if self.config.pop() == 'visuals':
            self.do_visuals()
        else:
            pass

    def do_visuals(self):
        self.do_timer()
        display = draw.Display(space.WIDTH, space.HEIGHT, 'Simulation')
        visuals_type = self.config.pop()

        if visuals_type == 'flux':
            mouse_proc = MouseProgramme(self.config.pop())
            touched_points_type = self.config.pop()
            if touched_points_type == 'local':
                start_time = time.time()
                # game loop
                while time.time() - start_time < self.time_limit:
                    # mouse position
                    flashlight_dir = mouse_proc.returnFluxDirection()

                    # objects
                    touched_circles = self.s.brute_touched_circles(flashlight_dir)

                    scattered_beams = self.s.scattered_beams(flashlight_dir, touched_circles)

                    avg_scat_beam = sum(list(map(draw.Line.getGradient, scattered_beams))) / len(scattered_beams)
                    obj_avg_beam = draw.Line((space.WIDTH / 2, space.HEIGHT / 2), 5 * avg_scat_beam,
                                             draw.colours['#99FF99'], 3)

                    objects = [self.s] + touched_circles + scattered_beams + [obj_avg_beam]

                    display.event_catcher()
                    display.paint(objects)

                pygame.quit()

                quit()
            elif touched_points_type == 'brute':
                start_time = time.time()
                # game loop
                while time.time() - start_time < self.time_limit:
                    # mouse position
                    flashlight_dir = mouse_proc.returnFluxDirection()

                    # objects
                    touched_circles = self.s.brute_touched_circles(flashlight_dir)

                    scattered_beams = self.s.scattered_beams(flashlight_dir, touched_circles)

                    avg_scat_beam = sum(list(map(draw.Line.getGradient, scattered_beams))) / len(scattered_beams)
                    obj_avg_beam = draw.Line((space.WIDTH / 2, space.HEIGHT / 2), 5 * avg_scat_beam,
                                             draw.colours['#99FF99'], 3)

                    objects = [self.s] + touched_circles + scattered_beams + [obj_avg_beam]

                    display.event_catcher()
                    display.paint(objects)

                pygame.quit()

                quit()
            else:
                raise ValueError('Have to enter either `local` or `brute`')
        elif visuals_type == 'surface':
            pass
        elif visuals_type == 'tangents':
            pass
        else:
            raise ValueError('Have to enter either `surface`, `tangent` or `flux`')

    def do_timer(self):
        if self.config.pop() == 'timed':
            self.time_limit = float(self.config.pop())
        else:
            self.time_limit = 3600

    @staticmethod
    def create_scatterer(filename):
        mode_lists = []
        with open(filename, 'r') as f:
            for line in f.readlines():
                l = list(map(float, line.split(',')))
                mode_lists.append(l)

        return scatterer.FourierMode(*zip(*mode_lists))


"""
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
"""