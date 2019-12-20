#!/usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from math import exp, log10, atan, pi, tan
pow10 = lambda x : pow(10,x)
deg2rad = pi / 180
rad2deg = 180 / pi

# halo parameters
fn = '../dmhalo_lowres/halo.profeinasto.core000pc.txt'
alpha              = 0.0
r_earth, rho_earth = 0.0, 0.0
r_scale, rho_scale = 0.0, 0.0
alpha_tags = ['gMW_TOT_SHAPE_PARAMS[0]','gMW_TOT_SHAPE_PARAMS_0'] # keyword for alpha is different in different clumpy versions
with open(fn,'r') as f :
  for l in f.readlines() :
    l = l.rstrip().split()
    if isinstance(l,list) :
      if len(l) >= 3 :
        if   l[0] in alpha_tags       : alpha     = float( l[2] )
        elif l[0] == 'gMW_TOT_RSCALE' : r_scale   = float( l[2] )
        elif l[0] == 'gMW_RSOL'       : r_earth   = float( l[2] )
        elif l[0] == 'gMW_RHOSOL'     : rho_earth = float( l[2] )
print('alpha    :',alpha)
print('r_scale  :',r_scale,'kpc')
print('r_earth  :',r_earth,'kpc')
print('rho_earth:',rho_earth,'GeV/cm^3')

def einasto_unnorm(r) :
  a = r / r_scale
  a = ( a ** alpha ) - 1
  return exp( (-2/alpha) * a )

rho_scale = rho_earth / einasto_unnorm(r_earth)
def einasto( r ) : return rho_scale * einasto_unnorm(r)
def kpc2deg( k ) : return atan( k / r_earth ) * rad2deg
def deg2kpc( d ) : return r_earth * tan( d * deg2rad )

amin  = 0.01
amax  = 5
nangs = 80
delta_angs_log = ( log10(amax) - log10(amin) ) / (nangs-1)
angs = [ pow10( log10(amin) + i*delta_angs_log ) for i in range(nangs) ]
#print('angs:',angs)
es = [ einasto( deg2kpc( d ) ) for d in angs ]

ymin = min(es) / 2
ymax = max(es) * 3

# init plot
fig = plt.figure(figsize=(7,6))
fax = fig.add_subplot(111)

# halo density line
plt.plot( angs, es, label='Einasto Halo Density', zorder=3 )

# blue rectangle
boxright = 3 # analysis radius, deg?
c = 'lightblue'
fax.add_patch( patches.Rectangle( (amin,ymin), boxright-amin, ymax-ymin, linewidth=0, facecolor=c, zorder=1, label='Observation Radius' ) )

# plot extras
s = 12
#plt.title(  r'J Factor around Galactic Center', y=1.13,  )
plt.title( 'Einasto Halo Density', y=1.13, fontsize=16)
plt.xlabel( r'Angle from Galactic Center $ \left \{ {}^{\circ} \right \} $', fontsize=s )
plt.ylabel( r'Mass Density $\left \{ \frac{\mathrm{GeV}}{{\mathrm{cm}^3}} \right \} $', fontsize=s )
plt.xscale('log')
plt.yscale('log')
plt.xlim([ amin, amax ])
print('ylims:',[ymin,ymax])
plt.ylim([ ymin, ymax ])
fax.grid()
legend = fax.legend( loc='lower left', shadow=True )

ax  = fax.twiny()
ax.set_xscale('log')
#ax.set_yscale('log')
#print( 'kpc lim:', [ deg2kpc(amin), deg2kpc(amax) ] )
ax.set_xlim( [ deg2kpc(amin), deg2kpc(amax) ] )
ax.set_xlabel( r'Distance from Galactic Center $ \left \{ \mathrm{kpc} \right \}$', fontsize=s)
#ax.set_ylim( [ ymin, ymax ] )

plt.savefig( 'gc_einasto_profile.pdf', dpi=300, bbox_inches='tight' )
plt.clf()
plt.close( fig )


