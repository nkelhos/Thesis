#!/usr/bin/env python
import numpy
import matplotlib.pyplot as plt
from scipy.stats import chi2

def roll_n() :
  return numpy.random.normal()
def roll_p(m) :
  return numpy.random.poisson( lam=m )

#for i in range(10):
  #print( '%6.3f'%roll_n(), roll_p(1.8) )
  
fig = plt.figure(figsize=(10,7))
frame1 = fig.add_axes(( 0.1, 0.1, 0.8, 0.8 ))

dof = 4
nexperiments = 30000
data = []
for i in range(nexperiments) :
  v = 0
  for i in range(dof) :
    v += roll_n()**2
  data += [ v ]

xmin, xmax = 0, 30
nbins = 30
xbinw = (xmax-xmin)/nbins
binlefts = [ xmin + i*xbinw for i in range(nbins) ]
bindata  = [ 0 for i in range(nbins) ]
naccum = 0
for d in data :
  ibin = int( (d-xmin) / xbinw )
  if ibin < nbins :
    bindata[ibin] += 1
    naccum += 1
for i in range(nbins) :
  bindata[i] /= naccum

kwa = {}
kwa['width' ] = xbinw
kwa['align' ] = 'edge'
kwa['label' ] = 'data'
kwa['zorder'] = 5
frame1.bar( binlefts, bindata, **kwa )

npts = 500
xwid = (xmax-xmin)/(npts-1)
xs = [ xmin + i*xwid for i in range(npts) ]
kwa = {}
kwa['zorder'] = 8
for j in [1,2,3,4,5,6] :
  ys = [ chi2.pdf(x,j) for x in xs ]
  kwa['label'] = 'dof=%d' % j 
  frame1.plot( xs, ys, **kwa )

kwa = {}
kwa['loc'   ] = 'upper right'
kwa['shadow'] = True
kwa['prop'  ] = {'size':15}
frame1.legend( **kwa )
frame1.set_xlim([xmin,xmax])

kwa = {}
kwa['bbox_inches'] = 'tight'
kwa['pad_inches' ] = 0
kwa['dpi'        ] = 150
plt.savefig( 'hist2.pdf', **kwa )
plt.close(fig)
