import imageio
from shutil import rmtree
from matplotlib.ticker import AutoMinorLocator
import matplotlib.font_manager as fm
from matplotlib import pyplot as plt
from load_results import get_data

fm = fm.fontManager.addfont(path='/home/sofia/fonts/Ubuntu-Regular.ttf')
plt.rc('font', family='Ubuntu', size='14')
plt.rc('lines', linewidth=1)
colors = ['#D81B60', '#1E88E5', '#FFC107', '#004D40',
          '#e8e', '#95c', '#38e', '#3bb', '#395',
          '#dc2', '#fa3',
          '#e63', '#c33', '#865']

pos, _, _, _, _ = get_data(3, 2)
npart = 3


def do_plot(j, nframes):
    nsamples = len(pos[0])
    split = nsamples//nframes
    fig, ax = plt.subplots(1, 1, dpi=100, figsize=(3, 4))
    for i, p in enumerate(pos):
        clr = colors[i]
        p = p[:j*split+1]
        ax.plot(p[:, 0], p[:, 1], color=clr)
        ax.scatter(p[0, 0], p[0, 1], edgecolor=clr, facecolor='#fff', s=50)
        ax.scatter(p[-1, 0], p[-1, 1], color=clr,
                   label=f'particle {i+1}', s=50)
        ax.set_xlim(-.5, .6)
        ax.set_ylim(-.15, 1.05)
        ax.set_aspect('equal')

        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(which='both', direction='in', top=True, right=True)
        ax.tick_params(which='major', width=.8, length=4)
        ax.tick_params(which='minor', width=.6, length=3)
        ax.grid(color='grey', linestyle='-', linewidth=.25)
    fig.tight_layout(pad=.8)
    plt.savefig(f'./img/img_{j}.png',
                transparent=False,
                facecolor='white')
    plt.close()
    pass


nframes = 200
for j in range(nframes):
    do_plot(j, nframes)

frames = []
for j in range(nframes):
    image = imageio.v2.imread(f'./img/img_{j}.png')
    frames.append(image)

imageio.mimsave('./example.gif', frames, fps=25)
