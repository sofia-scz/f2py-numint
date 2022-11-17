from utils import kinetic
from plotresults import do_plots
from core import ivp_solver, mass, npart
from core import poten
import numpy as np
from time import time


# initial conditions
x0 = np.array([[-1, 0],
               [1, 0],
               [0, 0]])*1.

a, b = .417701, .303455
v0 = np.array([[a, b],
               [a, b],
               [-2*a, -2*b]])*2.


def kene(v): return kinetic(v, mass)
def toten(x, v): return poten(x) + kene(v)


t0 = time()
# do simulation
ivp_solver(dt=1e-4, x0=x0, v0=v0, tf=2.)
tf = time()
print(f'Simulation finished. Time spent: {tf-t0} sec.')

# do plots
do_plots(npart, kene, toten, poten)
