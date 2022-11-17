from foroutine import endtime_ivp, npoints_ivp, poten, constants
import utils

npart = constants.npart
ndim = constants.ndim
mass = constants.mass

methods = {'ruth': 1,
           'simpson': 2}


def ivp_solver(dt, x0, v0, npoints=1, tf=None, method='ruth'):
    # first tests
    assert utils.is_float(dt), "can't interpret dt as float."
    assert dt > 0, "dt must be greater than zero."
    assert utils.is_int(npoints), "can't interpret npoints as integer."
    assert npoints > 0, 'npoints must be greater than zero.'
    assert (npart, ndim) == x0.shape, 'x0 shape does not match number of particles and dimensions.'

    # choose method:
    try:
        dealgo = methods[method]
    except KeyError:
        raise Exception("I don't know that integration method.")

    # choose finish criteria
    if tf:
        assert utils.is_float(tf), "can't interpret tf as float."
        assert tf > 0, "tf must be greater than zero."
        endtime_ivp(dealgo=dealgo, tf=tf, dt=dt, x0=x0, v0=v0)
    elif not tf:
        npoints_ivp(dealgo=dealgo, npoints=npoints, dt=dt, x0=x0, v0=v0)
    pass
