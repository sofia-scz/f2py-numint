!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                      aux
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! compute vector norm
subroutine vnorm(v, output)
use constants
implicit none
real*8,intent(in),dimension(ndim) :: v
real*8,intent(out) :: output

! do stuff
real*8 :: s
integer :: i

s = .0
do i=1,ndim
  s = s + v(i)**2
end do

output = dsqrt(s)

! finish
return
end subroutine vnorm


! -------------------------------------------------------


! compute ek
subroutine kinetic(v, output)
use constants
implicit none
real*8,intent(in),dimension(npart, ndim) :: v
real*8,intent(out) :: output

! do stuff
real*8 :: s
integer :: n, i

output = .0
do n=1,npart
    s = .0
    do i=1, ndim
      s = s + v(n, i)**2
    end do
    s = s/2.*mass(n)
output = output + s
end do

! finish
return
end subroutine kinetic

! -------------------------------------------------------


! compute numerical gradient
subroutine afun(x, output)
use constants
implicit none
real*8,intent(in),dimension(npart, ndim) :: x
real*8,intent(out),dimension(npart, ndim) :: output

! do stuff
integer :: i, j
real*8 :: h, uf, ub
real*8,dimension(npart, ndim) :: xb, xf

h = 6.8e-6

do i=1,npart
do j=1, ndim
    xb = x
    xf = x
    xb(i,j) = xb(i,j)-h
    xf(i,j) = xf(i,j)+h
    call poten(xb, ub)
    call poten(xf, uf)
    output(i, j) = (ub-uf)/2./h/mass(i)
end do
end do

! finish
return
end subroutine afun


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                      integration steps
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! ----------------------------------
! 3/8 rule - simpson 4th order runge kutta integration step

! declarations
subroutine simpson(dt, xin, vin, xout, vout)
use constants
implicit none
real*8,intent(in) :: dt
real*8,intent(in),dimension(npart, ndim) :: xin, vin
real*8,intent(out),dimension(npart, ndim) :: xout, vout

! do stuff
real*8,dimension(npart, ndim) :: k, k1, k2, k3, k4, d1, d2, d3, d4

d1 = dt*vin
call afun(xin, k)
k1 = dt*k

d2 = dt*(vin+k1/3)
call afun(xin+d1/3, k)
k2 = dt*k

d3 = dt*(vin+k2-k1/3)
call afun(xin+d2-d1/3, k)
k3 = dt*k

d4 = dt*(vin+k3-k2+k1)
call afun(xin+d3-d2+d1, k)
k4 = dt*k

xout = xin + (d1+d4+3*d2+3*d3)/8
vout = vin + (k1+k4+3*k2+3*k3)/8

! finish
return
end subroutine simpson

! ----------------------  END  ----------------------------------


! ----------------------------------
! ruth method 4th order sympletic integration step

! declarations
subroutine ruth(dt, xin, vin, xout, vout)
use constants
implicit none
real*8,intent(in) :: dt
real*8,intent(in),dimension(npart, ndim) :: xin, vin
real*8,intent(out),dimension(npart, ndim) :: xout, vout

! do stuff
real*8 :: q, c14, c23, d13, d2
real*8,dimension(npart, ndim) :: x, v, a

q=2.**(1./3.)
c14=1./2./(2-q)
c23=(1.-q)/2./(2.-q)
d13=1./(2.-q)
d2=q/(q-2.)

x = xin + dt*c14*vin
call afun(x, a)
v = vin + dt*d13*a

x = x + dt*c23*v
call afun(x, a)
v = v + dt*d2*a

x = x + dt*c23*v
call afun(x, a)
v = v + dt*d13*a

xout = x + dt*c14*v
vout = v

! finish
return
end subroutine ruth

! ----------------------  END  ----------------------------------


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                      IVP SOLVERS 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


! ----------------------------------
! aux write data

! declarations
subroutine writedata(oi, n, x, v)
use constants
implicit none
integer,intent(in) :: oi, n
real*8,intent(in),dimension(npart, ndim) :: x, v

! do stuff
integer :: i
real*8 :: epot, ek

call poten(x, epot)
call kinetic(v, ek)

write(oi,*) 'STEP', n
write(oi,*) ''
do i=1,npart
    write(oi,*) x(i,:), v(i,:)
end do
write(oi,*) ''
write(oi,*) 'EPOT=', epot, 'EK=', ek, 'ETOT=', epot+ek
write(oi,*) ''
write(oi,*) '--------------------------------------------------------------------'
write(oi,*) ''
write(oi,*) ''

! finish
return
end subroutine writedata
! ----------------------  END  ----------------------------------


! ----------------------------------
! solve ivp for given n points

! declarations
subroutine solve_ivp(dealgo, npoints, dt, x0, v0)
use constants
implicit none
integer,intent(in) :: dealgo, npoints
real*8,intent(in) :: dt
real*8,intent(in),dimension(npart, ndim) :: x0, v0

! do stuff
integer :: n, oi
real*8,dimension(npart, ndim) :: x, v

oi = 10
open(oi, file = 'outfile')

n = 1
x = x0
v = v0

call writedata(oi, n, x, v)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! choose int algo !!!!!!!!!!!!
if (dealgo == 1) then
    do n=2,npoints
        call ruth(dt, x, v, x, v)
        ! write data
        call writedata(oi, n, x, v)
    end do
else if (dealgo == 2) then
    do n=2,npoints
        call simpson(dt, x, v, x, v)
        ! write data
        call writedata(oi, n, x, v)
    end do
end if

write(oi,*) 'PROGRAM EXECUTION FINISHED.'
close(oi)

! finish
return
end subroutine solve_ivp

! ----------------------  END  ----------------------------------
