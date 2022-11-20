import numpy as np
from matplotlib.ticker import AutoMinorLocator
import matplotlib.font_manager as fm
from matplotlib import pyplot as plt

fm = fm.fontManager.addfont(path='/home/sofia/fonts/Ubuntu-Regular.ttf')
plt.rc('font', family='Ubuntu', size='14')
plt.rc('lines', linewidth=1)
colors = ['#D81B60', '#1E88E5', '#FFC107', '#004D40',
          '#e8e', '#95c', '#38e', '#3bb', '#395',
          '#dc2', '#fa3',
          '#e63', '#c33', '#865']


def do_plots(npart, pos, vel, epot, ek, etot):

    auxrange = np.arange(len(ek))

    # #######################################################

    fig, axes = plt.subplot_mosaic([['top', 'top'], ['left', 'right']], dpi=100, figsize=(12, 9))
    for i, p in enumerate(pos):
        clr = colors[i]
        axes['top'].plot(p[:, 0], p[:, 1], color=clr)
        axes['top'].scatter(p[0, 0], p[0, 1], edgecolor=clr, facecolor='#fff', s=50)
        axes['top'].scatter(p[-1, 0], p[-1, 1], color=clr,
                            label=f'particle {i+1}', s=50)
    axes['top'].set_aspect('equal')
    axes['top'].legend(loc='upper right', fontsize=8)

    axes['left'].plot(auxrange, ek-ek[0], color='#95c', label=r'$\Delta$ kinetic energy')
    axes['left'].plot(auxrange, epot-epot[0], color='#fa3', label=r'$\Delta$ potential energy')
    axes['left'].legend(loc='upper right', fontsize=8)

    axes['right'].plot(auxrange, etot/etot[0]-1, color='#395', label='total energy error')
    axes['right'].legend(loc='upper right', fontsize=8)

    for key in axes:
        axes[key].xaxis.set_minor_locator(AutoMinorLocator())
        axes[key].yaxis.set_minor_locator(AutoMinorLocator())
        axes[key].tick_params(which='both', direction='in', top=True, right=True)
        axes[key].tick_params(which='major', width=.8, length=4)
        axes[key].tick_params(which='minor', width=.6, length=3)
        axes[key].grid(color='grey', linestyle='-', linewidth=.25)

    fig.tight_layout(pad=.8)
    plt.show()
    pass
