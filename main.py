"""
Idea of simulation:

Consider classical mechanics. We uniform flux of balls will encounter a
surface (a large sphere). In our first examples, consider two dimensional case,
then expand to three dimensions at later date.

No graphical intnerface for the moment because that adds unnecessary complications.
Instead, plot the dynamics in a grid, then when a graphical engine comes around,
we can simply plot directly.

First the scatterinng ball will be rigid, then it will be deformable unnder
the harmoinc approximationn. A comprehensive attempt will be attacked later.
We can also consider a moving scattering ball.

A cool method would be to separate scatterer from fluxes so that we can match
flux to scatterer as we wish. For now, consider only one type of flux.
d-dimensional balls of finite radius r.

Different possible scatterers:
- balls of radius R:
    - rigid and static
    - rigid and dynamic
    - harmonic deformable and static
    - harmonic deformable and dynamic
    - deformable and static
    - deformable and dynnamic

Note: many ways that the scatterer can be dynamic. Either by spring, rope or
not at all.

Plan for simulation:
One python file can define the plane for the scattering. Then, one class for the
fluxes and a separate file for the scatterers. A couple files for the analysis.
Here the code is checked to see whether or not it is correct
"""

from scatterer import FourierMode


if __name__ == '__main__':
    print("Hello World!")

    import draw, space, scatterer, analysis, experiment
    import matplotlib.pyplot as plt
    import numpy as np
    import pygame

    import time

    display = draw.Display(space.WIDTH, space.HEIGHT, 'Simulation')

    # define scatterer
    rangeA = 0
    rangeB = 2 * np.pi

    num_modes = 3
    
    rs = [0 for i in range(num_modes - 1)] + [100]
    rc = [200] + [0 for i in range(num_modes -1)]
    w = [i for i in range(num_modes)]
    gen_mode = FourierMode(rs, rc, w, 0, 2 * np.pi)
    s = scatterer.Scatterer(gen_mode)

    # define text info object
    text = draw.Text('beep boop')

    ad = None

    start_time = time.time()
    mouse_time = []
    touch_time = []
    beam_time = []
    dist_time = []
    # plot_time = []
    # objs_time = []

    prog = experiment.Programme('mouse')

    # game loop
    while time.time() - start_time < 10:
        # mouse position
        flashlight_dir = prog.returnFluxDirection()
        mouse_time.append(time.time())

        # objects
        touched_circles = s.brute_touched_circles(flashlight_dir)
        touch_time.append(time.time())

        scattered_beams = s.scattered_beams(flashlight_dir, touched_circles)
        beam_time.append(time.time())

        # avg_scat_beam = sum(list(map(draw.Line.getGradient, scattered_beams))) / len(scattered_beams)
        # obj_avg_beam = draw.Line((space.WIDTH / 2, space.HEIGHT / 2), 5*avg_scat_beam, draw.colours['#99FF99'], 3)

        objects = [s] + touched_circles + scattered_beams

        # ad = analysis.AngleDistribution(flashlight_dir, scattered_beams, 0.1)
        # dist_time.append(time.time())

        # ad.draw()
        # plot_time.append(time.time())

        display.event_catcher()
        display.paint(objects)
        # objs_time.append(time.time())

    pygame.quit()

    final_time = time.time()

    timeHandle = analysis.TimeHandler(start_time, final_time, mouse_time, touch_time, beam_time)

    timeHandle.print_time_diffs()

    quit()
