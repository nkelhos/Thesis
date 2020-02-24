#!/usr/bin/env python
from math import log10, exp, pi, atan, cos, sqrt
from scipy.integrate   import quad
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import veripy
from astropy.io import fits

output  = 'output/'
r_s     = 15.14 # kpc
alpha   =  0.17
r_sol   =  8.0  # kpc
rho_sol =  0.4  # GeV/cm^3
rad2deg = 180 / pi
deg2rad = pi / 180
kpc2cm  = 3.086e21
def unnorm_einasto(r) :
  f = r / r_s
  f = f**alpha - 1
  f = ( -2 / alpha ) * f
  return exp( f )
rho_s = rho_sol / unnorm_einasto( r_sol )
def einasto(r) : 
  return rho_s * unnorm_einasto(r)

rmin   = 1e-3 # kpc
rmax   = 1    # kpc
nradii = 100
rdelta = ( log10(rmax) - log10(rmin) ) / (nradii-1)
radii  = [ pow(10, log10(rmin) + i * rdelta ) for i in range(nradii) ]
angles = [ atan(r/r_sol) * rad2deg for r in radii ]
dens   = [ einasto(r) for r in radii ]
fname  = output + 'calc_densities.pdf'
fig    = plt.figure()
fax    = fig.add_subplot(111)
#plt.plot( radii, dens, label='einasto' )
#plt.xlabel( 'Radius from Galactic Center [kpc]' )
plt.plot( angles, dens, label='einasto' )
plt.xlabel( 'Angle from Galactic Center [deg]' )
plt.ylabel( 'Mass Density [GeV/cm^3]' )
plt.title( 'Dark Matter Mass Density around Galactic Center' )
plt.xscale('log')
plt.yscale('log')
legend = fax.legend( loc='lower left', shadow=True )
fax.grid()
plt.savefig( fname, dpi=300 )
plt.clf()

def jfac(ang) :
  # ang : radians, angle from GC
  # returns : integral of rho^2 function along line-of-sight l
  lmin  = 0          # kpc
  lmax  = 50 * r_sol # kpc
  rsol2 = r_sol**2
  minustwolcostheta = -2 * r_sol * cos(ang)
  def rfunc( l ) : # law of cosines
    return sqrt( l**2 + rsol2 + ( l * minustwolcostheta ) )
  def kern( l ) : return einasto( rfunc( l ) ) ** 2
  return quad( kern, lmin, lmax )[0] * kpc2cm

amin    = 1e-2 # deg
amax    = 3e0  # deg
nangles = 100
adelta  = ( log10(amax) - log10(amin) ) / (nangles-1)
angles  = [ pow(10, log10(amin) + i * adelta ) for i in range(nangles) ] # deg
radians = [ a * deg2rad for a in angles ] # radians
jfacs   = [ jfac(rad) for rad in radians ]
fname   = output + 'calc_jfacs.pdf'
fig     = plt.figure()
fax     = fig.add_subplot(111)
plt.plot( angles, jfacs, label='jfac' )
plt.xlim( amin, amax )
plt.xlabel( 'Angle from Galactic Center [deg]' )
plt.ylabel( 'jfac [GeV^2/cm^5]' )
plt.title( 'Dark Matter Mass Density around Galactic Center' )
plt.xscale('log')
plt.yscale('log')
legend = fax.legend( loc='lower left', shadow=True )
fax.grid()
plt.savefig( fname, dpi=300 )
plt.clf()

def Jfactor(ang, wid) :
  # ang : radians, angle from GC
  # wid : radians, width +- around ang
  def kern( a ) : return a * jfac(a)
  return 2 * pi * quad( kern, ang-wid, ang+wid )[0]
def Jfactor_area(ang,wid) :
  def kern( a ) : return a
  return 2 * pi * quad( kern, ang-wid, ang+wid )[0]

integ = Jfactor( 1.5*deg2rad, 1.5*deg2rad )
print('Integral: %g GeV^2/cm^5' % integ)

a_min  = 1e-5
a_max  = 5
nangs  = 200
adelta = ( log10(a_max) - log10(a_min) ) / (nangs-1)
angles_interp  = [ pow(10, log10(a_min) + i * adelta ) for i in range(nangs) ]
radians_interp = [ a*deg2rad for a in angles_interp ]
halo_l  = '../dmhalo/lowres/halo.profeinasto.core000pc.fits'
jfs_l   = veripy.spiderweb_fits( halo_l, angles_interp, nangles=17 )
interpf = interp1d( radians_interp, jfs_l )
kern    = lambda rad : rad * interpf( rad )
integ   = 2 * pi * quad( kern, 0*deg2rad, 3*deg2rad )[0]
print( '\ninteg: %g\n' % integ )
jfs_l   = [ jl / integ for jl in jfs_l ]
interpf = interp1d( radians_interp, jfs_l )
kern    = lambda rad : rad * interpf( rad )
integ   = 2 * pi * quad( kern, 0*deg2rad, 3*deg2rad )[0]
print( '\ninteg2: %g\n' % integ )
def readheader( fitsfile, header ) :
  with fits.open( fitsfile, 'update' ) as f :
    return f[0].header[header]
fits_jfactor = readheader( halo_l, 'FLUX_TOT' )
fits_jf_unit = readheader( halo_l, 'BUNIT' )
jfs_l      = [ jl * fits_jfactor for jl in jfs_l ]
jfs_l_deg2 = [ jl * (pi**2) / (180**2)  for jl in jfs_l ]
print('FITS J factor %g %s' % ( fits_jfactor, fits_jf_unit ) )
interpf = interp1d( radians_interp, jfs_l )
kern    = lambda rad : rad * interpf( rad )
integ   = 2 * pi * quad( kern, 0*deg2rad, 3*deg2rad )[0]
print( '\ninteg3: %g\n' % integ )

fname = output + 'calc_Jfactor_per_deg2.pdf'
wid = 1e-8 # radians
#wid = 0.01 * 0.5 * deg2rad  # radians, 0.01 deg integration radius
Jfactors_per_sr   = [ Jfactor(rad,wid) / Jfactor_area(rad,wid) for rad in radians ]
Jfactors_per_deg2 = [ j * (pi**2) / (180**2) for j in Jfactors_per_sr ]

Jfactors_per_sr_integ = [ Jfactor(rad,wid) / Jfactor_area(rad,wid) for rad in radians_interp ]
interpf = interp1d( radians_interp, Jfactors_per_sr_integ )
kern    = lambda rad : rad * interpf( rad )
integ   = 2 * pi * quad( kern, 0*deg2rad, 3*deg2rad )[0]
print('theory jfactor %g GeV^2/cm^5' % integ )


fig     = plt.figure()
fax     = fig.add_subplot(111)
#plt.plot( angles, Jfactors_per_sr, label='Jfactors_per_sr' )
#plt.ylabel( 'J Factor per Solid Angle [GeV^2/cm^5/sr]' )
plt.plot( angles, Jfactors_per_deg2, label='theory' )
plt.plot( angles_interp, jfs_l_deg2, label='template' )
plt.ylabel( r'J Factor per Solid Angle $\left [\frac{GeV^2}{cm^5 deg^2} \right ]$' )
plt.xlabel( 'Angle from Galactic Center [deg]' )
plt.title( 'Dark Matter J Factor per Solid Angle  around Galactic Center' )
plt.xscale('log')
plt.yscale('log')
plt.xlim( 1e-2, 5 )
#legend = fax.legend( loc='lower left', shadow=True )
fax.grid()
plt.savefig( fname, dpi=300 )


