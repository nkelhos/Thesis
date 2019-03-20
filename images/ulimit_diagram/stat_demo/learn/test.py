#!/usr/bin/env python
import numpy
from math import log
import matplotlib.pyplot as plt
from scipy.stats import chi2

niter = 5000
lambda_true = 0.8
nsamples = 500

samples = [ 0 for i in range(niter) ]

for i in range(niter) :
  data = [ numpy.random.poisson( lam=lambda_true ) for i in range(nsamples) ]
  m  = numpy.mean(data)

  s  = m * log(m/lambda_true)
  s += lambda_true
  s += -m
  s *= 2 * nsamples

  samples[i] = s

fig = plt.figure(figsize=(10,7))
frame1 = fig.add_axes(( 0.1, 0.1, 0.8, 0.8 ))

kwa = {}
kwa['zorder'] = 5
frame1.hist( samples, **kwa )

xmin, xmax = 0, 12
npts = 30
xwid = (xmax-xmin)/(npts-1)
x = [ xmin + i*xwid for i in range(npts) ]
y = [ chi2.pdf( ix, 1 ) for ix in x ]
kwa = {}
kwa['zorder'] = 8
frame1.plot( x, y, **kwa )

frame1.set_xlabel('Sampled Values')
frame1.set_ylabel('Probability Density')
  
kwa = {}
kwa['bbox_inches'] = 'tight'
kwa['pad_inches' ] = 0
kwa['dpi'        ] = 150
plt.savefig( 'hist.pdf', **kwa )
plt.close(fig)


