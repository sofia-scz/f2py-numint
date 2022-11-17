import numpy.f2py as f2py
import sys
import os


def compiler(acode, modname='foroutine'):
    # load fortran source
    with open("fsource.f90", "r") as ff:
        fsource = ff.read()

    directory = "."
    test = os.listdir(directory)

    for item in test:
        if item.endswith(".so"):
            os.remove(os.path.join(directory, item))

    # compile fortran module
    out = f2py.compile(acode+fsource, modulename=modname,
                       verbose=False, extension='.f90')

    if not out == 0:
        sys.exit("Error compiling Fortran routines.")


# define acceleration subroutine
acode = """
module constants
implicit none

integer, parameter :: npart=3, ndim=2
real*8,dimension(3), parameter :: mass = (/ 1., 1., 1. /)

end module constants

! ----------------------------------------

subroutine poten(x, output)
use constants
implicit none
real*8,intent(in),dimension(npart, ndim) :: x
real*8,intent(out) :: output

! do stuff
integer :: i, j
real*8 :: u, k, r, mi, mj
real*8,dimension(ndim) :: ri, rj

k=10.

u = .0
do i=1,npart
    mi = mass(i)
    ri = x(i,:)
    do j=i+1,npart
        rj = x(j,:)
        mj = mass(j)
        call vnorm(ri-rj, r)
        u = u - k*mi*mj/r
    end do
end do

output = u

! finish
return
end subroutine poten

"""

# compile fortran solvers
compiler(acode)
