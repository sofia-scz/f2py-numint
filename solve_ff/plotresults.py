import numpy as np
from matplotlib.ticker import AutoMinorLocator
import matplotlib.font_manager as fm
from matplotlib import pyplot as plt

fm = fm.fontManager.addfont(path='/home/sofia/fonts/Ubuntu-Regular.ttf')
plt.rc('font', family='Ubuntu', size='14')
plt.rc('lines', linewidth=1)
colors = ['#c33', '#c93', '#38e',
          '#e8e', '#95c', '#38e', '#3bb', '#395',
          '#dc2', '#fa3',
          '#e63', '#c33', '#865']


def do_plots(npart, pos, vel, epot, ek, etot):

    auxrange = np.arange(len(ek))

    # #######################################################

    fig, axes = plt.subplots(1, 3, dpi=100, figsize=(20, 5))
    for i, p in enumerate(pos):
        clr = colors[i]
        axes[0].plot(p[:, 0], p[:, 1], color=clr)
        axes[0].scatter(p[0, 0], p[0, 1], edgecolor=clr, facecolor='#fff', s=50)
        axes[0].scatter(p[-1, 0], p[-1, 1], color=clr,
                        label=f'particle {i+1}', s=50)

    axes[0].legend(loc='upper right', fontsize=8)
    # axes[0].set_aspect('equal', 'box')

    # axes[1].plot(auxrange, tot, color='#395', label='total energy')
    axes[1].plot(auxrange, ek, color='#95c', label='kinetic energy')
    axes[1].plot(auxrange, epot, color='#fa3', label='potential energy')
    axes[1].legend(loc='upper right', fontsize=8)

    axes[2].plot(auxrange, etot/etot[0]-1, color='#395', label='total energy')
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
