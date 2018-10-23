#!/usr/bin/env python
import numpy, math
from math import pi
import matplotlib.pyplot as plt
from math import log10, exp

g = 3
m = 1

# from Jungman 1995, Supersymmetric Dark Matter, Section 3.1: Simple estimates
def neq(T) :
  return g * (m*T/(2*pi))**(3/2) * exp(-m/T)

xmin, xmax = 1e-3  , 1e3
ymin, ymax = 1e-20, 1e10
x  = numpy.logspace(log10(xmin), log10(xmax), 50)
xr = [ m / xi  for xi in x ]
y  = [ neq(xi) for xi in x ]
print('T   neq')
for i in range(len(x)) :
  print( '%.3e %.3e' % ( x[i], y[i] ) )

fig = plt.figure( figsize=(9,6) )
plt.plot( xr, y , 'k-' )
plt.xscale( 'log' )
plt.yscale( 'log' )
plt.title(  'Relic Abundance' )
plt.xlabel( r'$x = \frac{m}{T} \;\;,\;\; \mathrm{time}\rightarrow$')
plt.ylabel( '$n^{eq}$' )
#plt.gca().set_xlim( [ xmin, xmax ] )
#plt.gca().set_ylim( [ ymin, ymax ] )
#plt.grid()
plt.savefig( 'relic.pdf', dpi=300 )
plt.close(fig)

