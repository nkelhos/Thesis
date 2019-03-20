#!/usr/bin/env python
import random
from scipy.integrate   import quad
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from math import exp, sqrt, pi

def roll_p(m) :
  return numpy.random.poisson( lam=m )

xmin =  0
xmax = 10
norm_true  = 0.5
sigma_true = 0.2
mu_true    = 3
bkg_true   = 2

def bkg(x) : return bkg_true
def sig(x) :
  v = -1 * (x - mu_true)**2
  v /= ( 2 * sigma_true**2 )
  v = exp(v)
  v /= sqrt( 2 * pi * sigma_true**2 )
  v *= norm_true
  return v
def truth(x) :
  return sig(x) + bkg(x)

v = quad(truth, xmin, xmax )
truth_total = v[0]
print('integrated:',v)
def pdf_true(x) :
  return truth(x) / truth_total

def cumulative_true(x) :
  return quad( pdf_true, xmin, x )[0]

fig    = plt.figure(figsize=(10,7))
frame1 = fig.add_axes(( 0.1, 0.1, 0.8, 0.8 ))

npts = 1000
xwid = (xmax-xmin) / (npts-1)
xs   = [ xmin + i*xwid for i in range(npts) ]
ys   = [ truth(x) for x in xs ]
frame1.plot(xs,ys)

frame1.set_ylim(bottom=0, top=1.5*(bkg_true+norm_true))

kwa = {}
kwa['bbox_inches'] = 'tight'
kwa['pad_inches' ] = 0
kwa['dpi'        ] = 150
plt.savefig( 'models_true.pdf', **kwa )
plt.close(fig)
  
fig    = plt.figure(figsize=(10,7))
frame1 = fig.add_axes(( 0.1, 0.1, 0.8, 0.8 ))

npts = 1000
xwid = (xmax-xmin) / (npts-1)
xs   = [ xmin + i*xwid for i in range(npts) ]
ys   = [ pdf_true(x) for x in xs ]
frame1.plot( xs, ys, label='true pdf')
ys   = [ cumulative_true(x) for x in xs ]
frame1.plot( xs, ys, label='cumulative pdf')

kwa = {}
kwa['loc'   ] = 'upper right'
kwa['shadow'] = True
kwa['prop'  ] = {'size':15}
frame1.legend( **kwa )

kwa = {}
kwa['bbox_inches'] = 'tight'
kwa['pad_inches' ] = 0
kwa['dpi'        ] = 150
plt.savefig( 'pdf_cdf.pdf', **kwa )
plt.close(fig)

npts = 1000
xwid = (xmax-xmin) / (npts-1)
xs   = [ xmin + i*xwid for i in range(npts) ]
ys   = [ cumulative_true(x) for x in xs ]
spawnf = interp1d(ys,xs, kind='cubic')
def roll() :
  return spawnf( random.uniform(0,1) )

obstime = 100
events = []
for i in range(obstime) :
  events += [ roll() ]

fig    = plt.figure(figsize=(10,7))
frame1 = fig.add_axes(( 0.1, 0.1, 0.8, 0.8 ))

nbins = 30
binw = (xmax-xmin)/nbins
binlefts = [ xmin + i*binw for i in range(nbins) ]
histbars = [ 0             for i in range(nbins) ]
for e in events :
  ibin = int( (e-xmin) / binw )
  histbars[ibin] += 1
for i in range(nbins) :
  histbars[i] /= obstime

frame1.bar(binlefts, histbars, width=binw)

kwa = {}
kwa['bbox_inches'] = 'tight'
kwa['pad_inches' ] = 0
kwa['dpi'        ] = 150
plt.savefig( 'data1.pdf', **kwa )
plt.close(fig)




