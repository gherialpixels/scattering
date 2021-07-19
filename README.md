# scattering

## Description

This program calculates the scattering behaviour of a 2D beam of
particles colliding with a 2D shape. For now, the scatterer is a
stationary and rigid is defined by a Fourier series on a circle.

## How to use

### Dependencies

``scattering`` runs solely on python and a few external modules, namely:
- matplotlib
- numpy
- pygame

### Run command

``scattering`` is run from the main file, and it accepts terminal arguments.
The input layout is as follows:

`python main.py scatter-file visuals timed 50 flux mouse brute`

`scatter-file` is the relative path of the file containing the 
data to generate the scatterer through the use of Fourier modes 
(generalised scatterer initialisation to come). ``visuals`` tells
the program whether a visualisation should be shown. Any input
apart from visuals won't show visuals. 

The parameter ``timed``
ensures that the program closes after a set number of seconds
expressed in the parameter just after (here, `50`). Any other
input gives a total visualisation time of an hour.

`flux` 
describes the type of visualisation (you also have `surface` 
and `tangents`, more on these below). The next parameter 
specifies the direction of the flux: ``mouse`` implies 
that the particles go in the direction from the mouse
position to the centre of the diagram.
Then the final parameter gives the method to determine the 
points touched by the flux: `brute` is one of these methods.

### Specific options

