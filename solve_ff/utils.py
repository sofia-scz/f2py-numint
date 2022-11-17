import numpy as np


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


def array_to_lines(array):
    number_rows = [[str(number) for number in row] for row in array]
    lines = []
    for rows in number_rows:
        line = ''
        for number in rows:
            line += number + '   '
        line += '\n'
        lines.append(line)
    return lines


def divide(array, vector):
    carray = array.copy()
    for i, row in enumerate(array):
        carray[i] = row/vector[i]
    return carray


def multiply(array, vector):
    carray = array.copy()
    for i, row in enumerate(array):
        carray[i] = row*vector[i]
    return carray


def speeds(varray):
    sarray = np.zeros(len(varray))
    for i, v in enumerate(varray):
        sarray[i] = np.linalg.norm(v)
    return sarray


def kinetic(v, m):
    ss = .5*speeds(v) ** 2
    return np.sum(multiply(ss, m))
