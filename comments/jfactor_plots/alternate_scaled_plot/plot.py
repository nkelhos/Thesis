#!/usr/bin/env python
import veripy, sys, math, os
from math import log10, pi
import matplotlib.pyplot as plt
from scipy.integrate import quad, dblquad, nquad
from scipy.interpolate import interp1d
from astropy.io import fits

output = 'output/'
amin   = 1e-3
amax   = 5
npts   = 200
adelta_log = ( log10(amax) - log10(amin) ) / (npts-1)
angles     = [ pow( 10, log10(amin) + i * adelta_log ) for i in range(npts) ]
try : veripy.mkdir(output)
except : pass
print('angles %.2e - %.2e' % ( min(angles), max(angles) ) )
halo_l = '../dmhalo/lowres/halo.profeinasto.core000pc.fits'
jfs_l  = veripy.spiderweb_fits( halo_l , angles, nangles=10 )
interpf = interp1d( angles, jfs_l )
def kern( r ) : return r * interpf(r)
integ= 2 * pi * quad( kern, 1e-3, 3.0 )[0]
print('normalized integral: %g' % integ )
jfs_l = [ j / integ for j in jfs_l ]

fname  = output + 'jfactor normalized.pdf'
fig    = plt.figure()
fax    = fig.add_subplot(111)
plt.plot( angles, jfs_l, linewidth=1, zorder=5, label='lowres template' )
plt.xlim([ 1e-2, max(angles) ])
plt.xscale( 'log' )
plt.yscale( 'log' )
plt.title(  r'J Factor around the Halo Center'   )
plt.xlabel( r'Angle from Halo Center (${}^{\circ}$)' )
plt.ylabel( r'J Factor ??, $\frac{GeV^2}{cm^5}$'   )
legend = fax.legend( loc='lower left', shadow=True )
fax.grid()
plt.savefig( fname, dpi=300 )

def readheader( fitsfile, header ) :
  with fits.open( fitsfile, 'update' ) as f :
    return f[0].header[header]

fits_jfactor = readheader( halo_l, 'FLUX_TOT' )
fits_jf_unit = readheader( halo_l, 'BUNIT' )
jfs = [ j * fits_jfactor for j in jfs_l ]

fname  = output + 'jfactor_per_deg2.pdf'
fig    = plt.figure()
fax    = fig.add_subplot(111)
plt.plot( angles, jfs, linewidth=1, zorder=5, label='lowres template' )
plt.xlim([ 1e-2, max(angles) ])
plt.xscale( 'log' )
plt.yscale( 'log' )
plt.title(  r'J Factor around the Halo Center'   )
plt.xlabel( r'Angle from Halo Center (${}^{\circ}$)' )
plt.ylabel( r'J Factor ??, $\frac{GeV^2}{cm^5}$'   )
legend = fax.legend( loc='lower left', shadow=True )
fax.grid()
plt.savefig( fname, dpi=300 )

interpf = interp1d( angles, jfs )
def kern( r ) : return r * interpf(r)
integ = 2 * pi * quad( kern, 1e-3, 3.0 )[0]
print('final integral: %g' % integ )
print('FLUX_TOT: %g %s' % ( fits_jfactor, fits_jf_unit ) )


