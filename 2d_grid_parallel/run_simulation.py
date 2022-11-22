from main import ivp_solver, npart, ndim
from scipy.stats import maxwell
import numpy as np
from time import time
from plotresults import do_plots
from load_results import get_data


def random_speeds(T, npart, ndim):
    V2 = (maxwell.rvs(loc=0, scale=T**.5, size=npart))**2
    vx2 = np.array([np.random.uniform(0, v2) for v2 in V2])
    vy2 = V2 - vx2
    vx, vy = vx2**.5, vy2**.5
    rx, ry = np.random.uniform(-1, 1, npart), np.random.uniform(-1, 1, npart)
    vx, vy = vx*np.where(rx < 0, -1, 1), vy*np.where(ry < 0, -1, 1)
    return np.vstack((vx, vy)).transpose()

# initial conditions


ngrid = 6
x, y = np.arange(ngrid), np.arange(ngrid)

X, Y = [Q.flatten() for Q in np.meshgrid(x, y)]

x0 = np.vstack((X, Y)).transpose()*1.

seed = 421
np.random.seed(seed)

v0 = random_speeds(1e-2, npart, ndim)


t0 = time()
# do simulation
ivp_solver(tf=120., dt=1e-2, x0=x0, v0=v0, method='ruth')
tf = time()
print(f'Simulation finished. Time spent: {tf-t0} sec.')


t0 = time()
# get data
pos, vel, epot, ek, etot = get_data(npart, ndim)

# do plots
do_plots(npart, pos, vel, epot, ek, etot)
tf = time()
print(f'Data processing finished. Time spent: {tf-t0} sec.')
