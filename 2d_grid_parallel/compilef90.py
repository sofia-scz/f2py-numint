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
                       extension='.f90', verbose=False,
                       extra_args='--f90flags=-fopenmp')

    if not out == 0:
        sys.exit("Error compiling Fortran routines.")


# define acceleration subroutine
acode = """
module constants
implicit none

integer, parameter :: npart=36, ndim=2
real*8, dimension(npart), parameter :: mass=(/ 2.2, 3.5, 2.2, 3.5, 2.2, 3.5, &
                                             2.2, 3.5, 2.2, 3.5, 2.2, 3.5, &
                                             2.2, 3.5, 2.2, 3.5, 2.2, 3.5, &
                                             2.2, 3.5, 2.2, 3.5, 2.2, 3.5, &
                                             2.2, 3.5, 2.2, 3.5, 2.2, 3.5, &
                                             2.2, 3.5, 2.2, 3.5, 2.2, 3.5/), &
                                            charge=(/ 1., -1., 1., -1., 1., -1., &
                                                    -1., 1., -1., 1., -1., 1., &
                                                    1., -1., 1., -1., 1., -1., &
                                                    -1., 1., -1., 1., -1., 1., &
                                                    1., -1., 1., -1., 1., -1., &
                                                    -1., 1., -1., 1., -1., 1. /)


end module constants

! ----------------------------------------

subroutine poten(x, output)
use constants
implicit none
real*8,intent(in),dimension(npart, ndim) :: x
real*8,intent(out) :: output

! general values
integer :: i, j
real*8 :: u, r, mi, mj, ci, cj
real*8,dimension(ndim) :: ri, rj

! short range exp barrier                        a*exp(w/r)
real*8 :: a=50., w=5.

! mid range lennard jones                     e*( (s/r)**12 - 2*(s/r)**6 )
real*8 :: e=1., s=1.

! mid range crystaline                        b/r**6
real*8 :: b=1., c

! mid range harmonic                           k*(r-r0)**2
real*8 :: h=1., r0=.9

! coulomb (long range)                        k*ci*cj/r
real*8 :: k=3.

! cut off                                     *(1/(1+exp((r-rc)*q)))
real*8 :: rc=.5, q=10.

! do stuff



u = .0
do i=1,npart
    ri = x(i,:)
    ci = charge(i)
    do j=i+1,npart
        rj = x(j,:)
        cj = charge(j)
        call vnorm(ri-rj, r)
        u = u + k*ci*cj/r + e*(s/r**12 - s/r**6)
    end do
end do

output = u

! finish
return
end subroutine poten


"""

# compile fortran solvers
compiler(acode)
