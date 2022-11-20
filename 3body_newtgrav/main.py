from foroutine import solve_ivp, constants


# -----------  aux  --------------------

def is_int(x):
    try:
        int(x)
        return True
    except (ValueError, TypeError):
        return False


def is_float(x):
    try:
        float(x)
        return True
    except (ValueError, TypeError):
        return False

# --------------------------------------


npart = constants.npart
ndim = constants.ndim

methods = {'ruth': 1,
           'simpson': 2}


def ivp_solver(dt, x0, v0, npoints=1, tf=None, method='ruth'):
    # first tests
    assert is_float(dt), "can't interpret dt as float."
    assert dt > 0, "dt must be greater than zero."
    assert is_int(npoints), "can't interpret npoints as integer."
    assert npoints > 0, 'npoints must be greater than zero.'
    assert (npart, ndim) == x0.shape, 'x0 shape does not match number of particles and dimensions.'

    # choose method:
    try:
        dealgo = methods[method]
    except KeyError:
        raise Exception("I don't know that integration method.")

    # choose finish criteria
    if tf:
        assert is_float(tf), "can't interpret tf as float."
        assert tf > 0, "tf must be greater than zero."
        cpoints = int(tf/dt)
        solve_ivp(dealgo=dealgo, npoints=cpoints, dt=dt, x0=x0, v0=v0)
    elif not tf:
        solve_ivp(dealgo=dealgo, npoints=npoints, dt=dt, x0=x0, v0=v0)
    pass
