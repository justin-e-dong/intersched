c CLASS = W
c  
c  
c  This file is generated automatically by the setparams utility.
c  It sets the number of processors and the class of the NPB
c  in this directory. Do not modify it by hand.
c  
        integer nx_default, ny_default, nz_default
        parameter (nx_default=64, ny_default=64, nz_default=64)
        integer nit_default, lm, lt_default
        parameter (nit_default=40, lm = 6, lt_default=6)
        integer debug_default
        parameter (debug_default=0)
        integer ndim1, ndim2, ndim3
        parameter (ndim1 = 6, ndim2 = 6, ndim3 = 6)
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
