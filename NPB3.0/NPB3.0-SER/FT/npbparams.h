c CLASS = W
c  
c  
c  This file is generated automatically by the setparams utility.
c  It sets the number of processors and the class of the NPB
c  in this directory. Do not modify it by hand.
c  
        integer nx, ny, nz, maxdim, niter_default, ntotal
        parameter (nx=128, ny=128, nz=32, maxdim=128)
        parameter (niter_default=6)
        parameter (ntotal=nx*ny*nz)
        logical  convertdouble
        parameter (convertdouble = .false.)
        character*11 compiletime
        parameter (compiletime='15 May 2023')
        character*3 npbversion
        parameter (npbversion='3.0')
        character*3 cs1
        parameter (cs1='f77')
        character*3 cs2
        parameter (cs2='f77')
        character*6 cs3
        parameter (cs3='(none)')
        character*6 cs4
        parameter (cs4='(none)')
        character*2 cs5
        parameter (cs5='-O')
        character*6 cs6
        parameter (cs6='(none)')
        character*6 cs7
        parameter (cs7='randi8')
