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


if __name__ == '__main__':
    import sys
    import experiment
    print(sys.argv)
    p = experiment.Program(sys.argv)
