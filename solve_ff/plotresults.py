import numpy as np
from matplotlib.ticker import AutoMinorLocator
import matplotlib.font_manager as fm
from matplotlib import pyplot as plt

fm = fm.fontManager.addfont(path='/home/sofia/fonts/Ubuntu-Regular.ttf')
plt.rc('font', family='Ubuntu', size='14')
plt.rc('lines', linewidth=1)
colors = ['#e8e', '#95c', '#38e',
          '#e8e', '#95c', '#38e', '#3bb', '#395',
          '#dc2', '#fa3',
          '#e63', '#c33', '#865']


def do_plots(npart, kene, toten, poten):
    with open('posdata', 'r') as pdata:
        lines = pdata.readlines()
        lines = [line.split() for line in lines]
        positions = []
        for n in range(npart):
            positions.append(np.array(lines[1+n::3+npart], dtype=float))
        positions = np.array(positions)

    with open('veldata', 'r') as vdata:
        lines = vdata.readlines()
        lines = [line.split() for line in lines]
        velocities = []
        for n in range(npart):
            velocities.append(np.array(lines[1+n::3+npart], dtype=float))
        velocities = np.array(velocities)

    #######################################################

    pot, k, tot = [], [], []
    nsteps = len(positions[0])
    for j in range(nsteps):
        r, v = [], []
        for i in range(npart):
            r.append(positions[i, j, :])
            v.append(velocities[i, j, :])
        r, v = np.array(r), np.array(v)
        pot.append(poten(r))
        k.append(kene(v))
        tot.append(toten(r, v))
    pot, k, tot = np.array(pot), np.array(k), np.array(tot)
    auxrange = np.arange(len(pot))

    #######################################################

    fig, axes = plt.subplots(1, 3, dpi=150, figsize=(20, 5))
    for i, p in enumerate(positions):
        clr = colors[i]
        axes[0].plot(p[:, 0], p[:, 1], color=clr)
        axes[0].scatter(p[0, 0], p[0, 1], edgecolor=clr, facecolor='#fff', s=50)
        axes[0].scatter(p[-1, 0], p[-1, 1], color=clr,
                        label=f'particle {i+1}', s=50)

    axes[0].legend(loc='upper right', fontsize=8)
    # axes[0].set_aspect('equal', 'box')

    # axes[1].plot(auxrange, tot, color='#395', label='total energy')
    axes[1].plot(auxrange, k, color='#95c', label='kinetic energy')
    axes[1].plot(auxrange, pot, color='#fa3', label='potential energy')
    axes[1].legend(loc='upper right', fontsize=8)

    axes[2].plot(auxrange, tot/tot[0]-1, color='#395', label='total energy')
    axes[2].legend(loc='upper right', fontsize=8)

    for ax in axes:
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(which='both', direction='in', top=True, right=True)
        ax.tick_params(which='major', width=.8, length=4)
        ax.tick_params(which='minor', width=.6, length=3)
        ax.grid(color='grey', linestyle='-', linewidth=.25)

    fig.tight_layout(pad=.8)
    plt.show()
    pass
