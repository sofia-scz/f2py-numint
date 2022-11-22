import numpy as np


def is_float(x):
    try:
        float(x)
        return True
    except (ValueError, TypeError):
        return False


def line_to_1darr(line):
    aaa = [float(x) for x in line.split() if is_float(x)]
    return np.array(aaa)


def get_data(npart, ndim, fname='outfile'):
    with open(fname, 'r') as df:
        array, epot, ek, etot = [], [], [], []
        for line in df:
            try:
                arr = line_to_1darr(line)
                if len(arr) == 2*ndim:
                    array.append(arr)
                elif len(arr) == 3:
                    epot.append(arr[0])
                    ek.append(arr[1])
                    etot.append(arr[2])
                else:
                    pass
            except:
                pass
        df.close()
        array = np.array(array)
    posarr, velarr = array[:, :ndim], array[:, ndim:]
    pos, vel = [], []
    for i in range(npart):
        p, v = posarr[i::npart], velarr[i::npart]
        pos.append(p)
        vel.append(v)
    return [np.array(ds) for ds in [pos, vel, epot, ek, etot]]
