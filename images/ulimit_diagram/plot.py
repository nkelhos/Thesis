#!/usr/bin/env python
import matplotlib.pyplot as plt
from math import pi, sqrt, exp

fig = plt.figure(figsize=(10,7))
frame1 = fig.add_axes(( 0.1, 0.1, 0.8, 0.8 ))

cs_min   = 1
cs_max   = 100
cs_nbins = 2000
cs_bwid  = ( cs_max - cs_min ) / (cs_nbins-1)
cs = [ cs_min + i*cs_bwid for i in range(cs_nbins) ]
dist_mean   = ( cs_max + cs_min ) / 2
dist_spread = ( cs_max - cs_min ) / 6
dist_peak   = ( 1 / sqrt(2*pi* dist_spread**2) )
thresh = 0.1*dist_peak
def loglikefn(x) :
  m = dist_mean
  s = dist_spread
  y = (1/sqrt(2*pi* s**2)) * exp( -(x-m)**2 / (2 * s**2 ) )
  if y > thresh : return y - thresh
  else          : return 0
print('gaussian mean: %.2e  spread: %.2e'%(dist_mean,dist_spread))
print('gauss peak y : %.2e' % loglikefn(dist_mean) )
  
vx, vy = [], []
for i, ics in enumerate(cs) :
  v = loglikefn(ics)
  if v > 0 :
    vx += [ ics ]
    vy += [ v   ]
for ivx,ivy in zip(vx,vy) :
  print('%.2e %.2e' % (ivx,ivy) )

fill_to = dist_mean + 1.4*dist_spread
xf, yf = [], []
for ivx, ivy in zip(vx,vy) :
  if ivx < fill_to :
    xf += [ ivx ]
    yf += [ ivy ]

kwa = {}
kwa['color' ] = 'blue'
kwa['label' ] = r'$\mathcal{L}_{\mathrm{max}}(\;\left \langle \sigma v \right \rangle\;)$'
kwa['zorder'] = 5
frame1.plot( vx, vy, '-', **kwa )
kwa = {}
kwa['alpha' ] = 0.3
kwa['color' ] = 'blue'
kwa['zorder'] = 5
frame1.fill_between( xf, yf, **kwa )

capw = 0.5
midh = ( loglikefn(dist_mean) + loglikefn(fill_to) ) / 2
kwa = {}
kwa['color' ] = 'orange'
kwa['zorder'] = 8
os = 0
frame1.plot( [os+fill_to     , os+fill_to     ], [ loglikefn(fill_to  ), loglikefn(dist_mean) ], '-', **kwa )
frame1.plot( [os+fill_to-capw, os+fill_to+capw], [ loglikefn(fill_to  ), loglikefn(fill_to  ) ], '-', **kwa )
frame1.plot( [os+fill_to-capw, os+fill_to+capw], [ loglikefn(dist_mean), loglikefn(dist_mean) ], '-', **kwa )

kwa = {}
kwa['fontsize'] = 20
kwa['color'   ] = 'orange'
kwa['ha'      ] = 'left'
kwa['va'      ] = 'center'
frame1.text( os+fill_to + 1, midh, r'$\Delta\mathcal{L}$', **kwa )

kwa = {}
kwa['ha'] = 'center'
kwa['va'] = 'center'
kwa['color'   ] = 'blue'
kwa['fontsize'] = 20
kwa['multialignment'] = 'center'
frame1.text( dist_mean, dist_peak*0.5 , r'$95\%$ area'    , **kwa )
frame1.text( dist_mean, dist_peak*0.45, r'$(\alpha=0.95)$', **kwa )

kwa['fontsize'] = 15
frame1.text( dist_mean+1.55*dist_spread, dist_peak*0.13, r'$5\%$', **kwa )


kwa = {}
kwa['color'] = 'red'
kwa['markersize'] = 10
kwa['zorder'    ] = 12
kwa['clip_on'   ] = False
frame1.plot( [fill_to,fill_to], [thresh,thresh-0.0005], **kwa)
frame1.plot( [fill_to], [thresh], '.', **kwa )
kwa = {}
kwa['color'   ] = 'red'
kwa['fontsize'] = 15
kwa['ha'      ] = 'center'
kwa['va'      ] = 'center'
tx = r'$\left \langle \sigma v \right \rangle | _{\mathrm{ul}}$'
frame1.text( fill_to, thresh-0.001, tx, **kwa )

kwa = {}
kwa['color'] = 'green'
kwa['markersize'] = 10
kwa['zorder'    ] = 15
kwa['clip_on'   ] = False
frame1.plot( [dist_mean,dist_mean], [loglikefn(dist_mean),loglikefn(dist_mean)-0.001], **kwa)
frame1.plot( [dist_mean], [loglikefn(dist_mean)], '.', **kwa )
kwa = {}
kwa['color'   ] = 'green'
kwa['fontsize'] = 15
kwa['ha'      ] = 'center'
kwa['va'      ] = 'center'
kwa['zorder'  ] = 15
tx = r'$\left \langle \sigma v \right \rangle _{\mathrm{start}}$'
frame1.text( dist_mean, loglikefn(dist_mean)-0.00175, tx, **kwa )

kwa = {}
kwa['loc'   ] = 'upper left'
kwa['shadow'] = True
kwa['prop'  ] = {'size':15}
frame1.legend( **kwa )

kwa = {}
kwa['size'] = 20
frame1.set_title('Likelihood Upper Limit Calculation', **kwa)
frame1.set_xlabel( r'Increasing $\left \langle \sigma v \right \rangle \rightarrow$', **kwa )
frame1.set_ylabel( r'Increasing Maximum Likelihood $\mathcal{L} \rightarrow$', **kwa )
frame1.set_ylim(bottom=thresh)
frame1.set_xlim([dist_mean-(2.1*dist_spread), dist_mean+(2.1*dist_spread)])
frame1.set_xticklabels([])
frame1.set_yticklabels([])
#frame1.axes.get_xaxis().set_visible(False)
#frame1.axes.get_yaxis().set_visible(False)


kwa = {}
kwa['bbox_inches'] = 'tight'
kwa['pad_inches' ] = 0
kwa['dpi'        ] = 150
plt.savefig( 'ulimdiagram.pdf', **kwa )
plt.close(fig)
