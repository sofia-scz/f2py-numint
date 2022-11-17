from main import ivp_solver, npart, ndim
import numpy as np
from time import time
from plotresults import do_plots
from load_results import get_data


# initial conditions
x0 = np.array([[-1, 0],
               [1, 0],
               [0, 0]])*1.

a, b = .417701, .303455
v0 = np.array([[a, b],
               [a, b],
               [-2*a, -2*b]])*2


t0 = time()
# do simulation
ivp_solver(tf=2., dt=1e-5, x0=x0, v0=v0)
tf = time()
print(f'Simulation finished. Time spent: {tf-t0} sec.')


t0 = time()
# get data
pos, vel, epot, ek, etot = get_data(npart, ndim)

# do plots
do_plots(npart, pos, vel, epot, ek, etot)
tf = time()
print(f'Data processing finished. Time spent: {tf-t0} sec.')
