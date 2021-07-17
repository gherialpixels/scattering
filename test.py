

from experiment import mouseParticle


if __name__ == '__main__':
    import draw, space, scatterer, experiment
    import pygame
    import numpy as np

    display = draw.Display(space.WIDTH, space.HEIGHT, "Testing line math")
    x = np.array([space.WIDTH / 4, 0])
    y = np.array([0, space.WIDTH / 4])

    points = [space.centre + x + y, space.centre + x - y, 
              space.centre - x - y, space.centre - x + y]

    scat = scatterer.GeneralisedScatterer(points, closed=True)
    while True:
        circles = experiment.mouseParticleSet(scat)
        objects = [scat] + circles
        display.event_catcher()
        display.paint(objects)

    pygame.quit()
