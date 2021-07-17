
import space

import draw

import numpy as np
import pygame


def get_particle_set(pos, radius, dir, perp_dir):
    num_detec = 15

    U = np.array([dir, perp_dir])
    particle_set = set([np.dot(U, radius*np.array([np.cos(k*np.pi/(num_detec-1)),
            np.sin(k*np.pi/(num_detec-1))])) + pos for k in range(num_detec)])

    return particle_set


class FourierMode(object):

    def __init__(self, a, b, w, rangeA, rangeB):
        self.radius = lambda theta: sum([a[i] * np.sin(w[i] * theta) + \
                            b[i] * np.cos(w[i] * theta) for i in range(len(a))])
        self.dradius = lambda theta: sum([a[i] * w[i] * np.cos(w[i] * theta) - \
                        b[i] * w[i] * np.sin(w[i] * theta) for i in range(len(a))])
 
        self.curve = lambda theta: np.array([self.radius(theta) * np.cos(theta) + space.WIDTH / 2,
                                    self.radius(theta) * np.sin(theta) + space.HEIGHT / 2])

        self.dcurve = lambda theta: np.array([self.dradius(theta) * np.cos(theta) - self.radius(theta) * np.sin(theta),
                                    self.dradius(theta) * np.sin(theta) + self.radius(theta) * np.cos(theta)])

        self.rangeA = rangeA
        self.rangeB = rangeB


class Scatterer(object):

    """
    Scatterer's are parameterisation. For the time being, we consider only
    elastic scattering. To initiate a scatterer, we need a curve and a range
    of values that parameterise the curve. The curve has to be a two dimensional
    curve that is a function of some parameter t.
    """

    def __init__(self, mode):
        print("I am a scatterer")
        self.curve = mode.curve
        self.dcurve = mode.dcurve
        self.rangeA = mode.rangeA
        self.rangeB = mode.rangeB

    def surface_vectors(self, point):
        # This function requires a numerical derivative
        """
        if not (self.rangeA <= point <= self.rangeB):
            raise ValueError('Point %f was not inside the range [%f, %f]' %
                (point, self.rangeA, self.rangeB))
        """
        u = space.unit(self.dcurve(point)) # tangent to curve
        v = np.dot(np.array([[0, -1], [1, 0]]), u) # normal to surface

        return np.array([u, v]).T # change of basis matrix

    def tangent_beams(self):
        points = self.get_domain_points()
        lines = []
        #line_len = 50
        for p in points:
            lines.append(draw.Line(self.curve(p), self.dcurve(p), draw.colours['magenta']))

        return lines

    def moving_surface_vectors(self, t):
        vecs = self.surface_vectors(t % (2 * np.pi)).T
        arrow_len = 50
        return [draw.Line(self.curve(t), arrow_len*vec, draw.colours['red'], 2) for vec in vecs]

    def scattered_beams(self, dir, touched_circles):
        """
        beams coming from left-hand side (fixed direction). In future,
        treat case where the direction may change (higher order collisions)
        and where the collision zone may chage (reflective of more interesting)
        geomerties

        we have to precision

        To Do: Beam passes through each point. Convert to the basis of the
        surface basis, reflect across axis, then reconvert to normal basis.
        This defines a scattering line.

        How do things change when we consider a finite radius?

        """

        scatter_points = list(map(draw.Circle.getDomainPoint, touched_circles))
        # scatter_points = self.get_domain_points()

        lines = []
        line_len = 100

        for sp in scatter_points:
            cob = self.surface_vectors(sp)
            a = dir
            b = np.dot(cob @ np.array([[1, 0], [0, -1]]) @ cob.T, a)
            lines.append(draw.Line(self.curve(sp), line_len*b, draw.colours['light yellow']))

        return lines

    def local_touched_circles(self, dir):
        touched_circle_radius = 5

        scatter_points = self.get_domain_points()
        touched_points = []
        for sp in scatter_points:
            cob = self.surface_vectors(sp)
            a = dir
            b = np.dot(cob @ np.array([[1, 0], [0, -1]]) @ cob.T, a)
            if np.dot(b, cob.T[1]) <= 0:
                touched_points.append(draw.Circle(sp, self.curve(sp), touched_circle_radius, draw.colours['yellow']))

        return touched_points

    def brute_touched_circles(self, vec):
        touched_circle_radius = 5
        touched_circle_colour = '#FF9933'

        perp_vec = np.dot(np.array([[0, -1], [1, 0]]), vec)

        mapping = self.get_shifted_mapping(space.angle(-vec))

        d_points, c_points = list(zip(*mapping))

        touched_curve_points = [draw.Circle(d_points[0], c_points[0], touched_circle_radius, touched_circle_colour),
                                draw.Circle(d_points[1], c_points[1], touched_circle_radius, touched_circle_colour),
                                draw.Circle(d_points[-1], c_points[-1], touched_circle_radius, touched_circle_colour)]

        centered_c_points = c_points - space.centre
        range_min = np.dot(perp_vec, centered_c_points[1])
        range_max = np.dot(perp_vec, centered_c_points[-1])

        for i in range(2, len(c_points)):
            index = (1 + (i // 2)) * (-1) ** (i % 2)
            dot = np.dot(perp_vec, centered_c_points[index])
            if dot >= range_max:
                range_max = dot
                touched_curve_points.append(
                    draw.Circle(d_points[i], c_points[i], touched_circle_radius, touched_circle_colour))
            elif dot <= range_min:
                range_min = dot
                touched_curve_points.append(
                    draw.Circle(d_points[i], c_points[i], touched_circle_radius, touched_circle_colour))

        return touched_curve_points

    def particle_touched_circles(self, dir, r0, r1):
        touched_circle_radius = 5
        touched_circle_colour = '#FF9933'

        """
        Number of particles set at random at each frame (periodic sending may
        forget details). The r0, r1 and w wil be reformulated later into the curve
        function. That is, the curve function will be reconstructed as a sum of
        Fourier modes, and from this it will be possible to determine the max extension
        of the curve without having to resort to summing of the length of the curve.

        """
        # some definitions
        numParticles = 1000

        centre = (space.WIDTH / 2, space.HEIGHT / 2)
        R = np.array([[0, -1], [1, 0]])
        perp_dir = np.dot(R, dir)

        # consider a line that we parametrise by t, clean up below later
        r = r0 + r1
        param = lambda t: centre - (r + 50) * dir + np.einsum('i, ij->ij', r*(t-0.5),
                                np.tile(perp_dir, (numParticles, 1)))
        points = param(np.random.random(numParticles))

        # some parameters for the particles
        vel = 1
        radius = 10

        # curve points => curve set
        curve_set = set(self.get_curve_points())

        touched_circles = set()

        for i in range(len(points)):
            points[i] += vel * dir
            print(points[i])
            particle_set = get_particle_set(points[i], radius, dir, perp_dir)
            inter = particle_set & curve_set
            if inter != set():
                touched_circles = touched_circles | inter
                if i != len(points) - 1:
                    points = points[:i] + points[i+1:]
                else:
                    points.pop()

        return [draw.Circle(point, touched_circle_radius, touched_circle_colour) for point in touched_circles]

    def cake_touched_circles(self, dir):
        # BROKEN method, needs to include domain point in Circle object
        touched_circle_radius = 5
        touched_circle_colour = '#FF9933'

        R = np.array([[0, -1], [1, 0]])
        perp_dir = np.dot(R, dir)

        dirAngle = space.angle(-dir)
        touched_centre = self.curve(dirAngle)

        point_spacing = 10
        n = 10 # n points on either side of the touched_centre

        diff_t = 0.01
        diff_curve = 2

        k = 1
        diff_k = 1
        sgn_k = 1

        touched_circles = [draw.Circle(touched_centre, touched_circle_radius, touched_circle_colour)]

        print("point_spacing: ", point_spacing)
        for j in range(2, 2*(n+1)):
            k = 1
            point = self.curve(dirAngle + k * diff_t * (-1)**j)
            point_dot = np.dot(point-space.centre, perp_dir)
            abs_dot = abs(point_dot)
            while abs(abs_dot - (j//2) * point_spacing) >= diff_curve:
                k += diff_k
                point = self.curve(dirAngle + k * diff_t * (-1)**j)
                point_dot = np.dot(point-space.centre, perp_dir)
                abs_dot = abs(point_dot)
                if k % 10 == 0:
                    print("abs_dot: ", abs_dot, ", point_dot: ", point_dot)

            touched_circles.append(draw.Circle(point, touched_circle_radius, touched_circle_colour))

        return touched_circles

    def get_domain_points(self):
        N = 1000
        return [self.rangeA + (self.rangeB - self.rangeA) * (n / N) for n in range(N)]

    def get_curve_points(self):
        # precision of representation given by N
        N = 1000
        t = lambda n : self.rangeA + (self.rangeB - self.rangeA) * (n / N)

        points = [(int(self.curve(t(n))[0]), int(self.curve(t(n))[1])) for n in range(N)]
        return points

    def get_mapping(self):
        # precision of representationn given by N
        N = 1000
        t = lambda n : self.rangeA + (self.rangeB - self.rangeA) * (n / N)

        points = [(t(n), (int(self.curve(t(n))[0]), int(self.curve(t(n))[1]))) for n in range(N)]
        return points

    def get_shifted_mapping(self, phase):
        N = 1000
        t = lambda n: self.rangeA + (self.rangeB - self.rangeA) * (n / N) + phase

        points = [(t(n), (int(self.curve(t(n))[0]), int(self.curve(t(n))[1]))) for n in range(N)]
        return points

    def draw(self, screen):
        points = self.get_curve_points()
        for point in points:
            # screen.set_at(point, (0,0,0))
            pygame.draw.circle(screen, draw.colours['black'], point, 1.5)


class GeneralisedScatterer(object):
    # scatterer,

    def __init__(self, points, closed=False):
        # numpy vectors
        self.curve = np.array(points)
        self.closed = closed
        self.create_tangent_surface()

    def create_tangent_surface(self):
        self.tangents = [draw.Line(self.curve[i], self.curve[i+1] - self.curve[i], 
                draw.colours['black']) for i in range(len(self.curve) - 1)]

        if self.closed:
            self.tangents.append(draw.Line(self.curve[-1], self.curve[0] - self.curve[-1], 
                draw.colours['black']))

    def draw(self, screen):
        for tangent in self.tangents:
            tangent.draw(screen)


class Particle(object):

    def __init__(self, pos, vel, radius):
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.radius = radius

    def update(self):
        self.pos += self.vel

    def draw(self, surface):
        pygame.draw.circle(surface, draw.colours['red'], self.pos, self.radius)
