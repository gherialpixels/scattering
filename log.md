
# Scattering DevDiary

## Things to implement
- [ ] Function/Curve classes
- [ ] Fourier sums to include more general curves (consider Nirvana implementation)
- [ ] Vibrating modes
- [ ] Algorithm to determine touched zones
  - [x] Flashlight algorithm: Brute-force method
  - [x] Local method: Determine the scattering behaviour at each point and untouched zones correspond to points whose scatter pathways enter the scatterer
  - [ ] Geometric method: Does there exist a nice method?
  - [ ] Comparison option of the touched zones
  - [ ] Shot lots of balls, determine collisions using sets and collect collision points to show touched zones (hyp; problem, numpy arrays are not inhashable)
  - [ ] Use sets. Define the set that is encompased by the curve and the set of points of the flashlight. Compute then intersection of the sets and choose the point most in the mouse's direction (hyp)
  - [ ] Take the curve and express it as points that form sets that can either be parallel to the direction of the mouse or perpendicular. Then, each "row" becomes a "cake layer". Then, take the XOR operation of each layer, starting with the first layer, taking into account the points. The points left are the touched surface. We can fill in the points randomly after by randomising the points in the individual sets. Implementation details to discover later.
- [ ] Second and higher order collisions
- [x] Determination of cross section from scattered beams: pyplot graph (simultaneous to mouse movement/curve change)
- [ ] Particles of finite size
- [ ] GUI(Tkinter) / Keyboard input
- [ ] Moving scatterer
- [ ] Keyboard input
- [ ] Non-linear spacing of curve representation
- [ ] **Particle flux implementation**
- [ ] Moveable text
- [ ] **Work out the math to check numerics & vice-versa**
- [ ] Consider combining `space.py` into `draw.py`
- [ ] Flashlight graphics
- [ ] Store angle distribution data (single integer) after each mouse movement
- [ ] Implement the moving surface vectors in practical way
- [ ] Add a better colour selector
- [ ] Try to use what you learned in class in your code... could really be useful!
- [ ]

## Parts to improve
- [ ] Evolution of moving surface vectors, better implementation
- [ ] Game loop, better implementation?
- [ ] Font issue
- [x] Reorganise the draw module to include the Line class
- [ ] Deduce the issue with brute force method; do other methods exist?
- [ ] Anomalous avg scattered beam direction

## Investigate
- markdown
- hydrogen package
- shapes produced by tangents

## Layout
I want to specify the vocabulary and structure of my code. This project is meant
to describe 2D scattering. For the momen
