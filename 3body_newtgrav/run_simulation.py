from main import ivp_solver, npart, ndim
import numpy as np
from time import time
from plotresults import do_plots
from load_results import get_data


# initial conditions
x0 = 1.*np.array([[1, 0],
                  [-1, 0],
                  [0, 0]])

vx, vy = .417701, .303455
v0 = 1.*np.array([[vx, vy],
                  [vx, vy],
                  [-2*vx, -2*vy]])


# initial conditions
x0 = 1.*np.array([[.05, 0],
                  [-.05, 0],
                  [0, 1]])

vx, vy = .5, 9.
v0 = 1.*np.array([[0, vy],
                  [0, -vy],
                  [-.5, 0]])


t0 = time()
# do simulation
ivp_solver(tf=1., dt=2e-5, x0=x0, v0=v0)
tf = time()
print(f'Simulation finished. Time spent: {tf-t0} sec.')


t0 = time()
# get data
pos, vel, epot, ek, etot = get_data(npart, ndim)

# do plots
do_plots(npart, pos, vel, epot, ek, etot)
tf = time()
print(f'Data processing finished. Time spent: {tf-t0} sec.')
