#!/usr/bin/env python
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10,7))
frame1 = fig.add_axes(( 0.1, 0.1, 0.8, 0.8 ))

xmin, xmax = -30, 50
npts = 2000
ythresh = -110 # y location of bottom of plot
x_deltaL = 40 # x location of delta-log-likelihood bar

xwid = (xmax-xmin)/(npts-1)
xs = [ xmin + i*xwid for i in range(npts) ]
#print('xs:',xs)

def poly(x) :
  y  = -0.00001 * (x-40)**4
  y += -0.01 * x**2
  y += - 2 * x
  return y

y_deltaL = poly( x_deltaL )
ys = [ poly(x) for x in xs ]
xpeak = xs[0]
ypeak = ys[0]
vx,vy = [], []
for x, y in zip(xs,ys) :
  if y > ythresh :
    vx += [ x ]
    vy += [ y ]
  if y > ypeak :
    xpeak = x
    ypeak = y
  
kwa = {}
kwa['color' ] = 'blue'
kwa['label' ] = r'$\mathcal{L}_{\mathrm{max}}(\;\left \langle \sigma v \right \rangle\;)$'
kwa['zorder'] = 5
frame1.plot( vx, vy, **kwa )


# Orange Bar and Label
xorange = x_deltaL + 3
xp = xorange
capw = 0.5
kwa = {}
kwa['color' ] = 'orange'
kwa['zorder'] = 15
frame1.plot( [xp     ,xp     ], [y_deltaL,ypeak   ], **kwa )
frame1.plot( [xp-capw,xp+capw], [y_deltaL,y_deltaL], **kwa )
frame1.plot( [xp-capw,xp+capw], [ypeak   ,ypeak   ], **kwa )
midh = (y_deltaL + ypeak) / 2
kwa = {}
kwa['fontsize'] = 20
kwa['color'   ] = 'orange'
kwa['ha'      ] = 'left'
kwa['va'      ] = 'center'
kwa['zorder'  ] = 15
frame1.text( xp + 1, midh, r'$\Delta\mathcal{L}$', **kwa )

# Green Upper Limit Start
kwa = {}
kwa['color'] = 'green'
kwa['markersize'] = 10
kwa['zorder'    ] = 15
kwa['clip_on'   ] = False
frame1.plot( [xpeak,xpeak], [ypeak,ypeak-5], **kwa)
frame1.plot( [xpeak], [ypeak], '.', **kwa )
kwa = {}
kwa['color'    ] = 'green'
kwa['alpha'    ] = 0.5
kwa['linestyle'] = 'dotted'
kwa['zorder'   ] = 5
frame1.plot( [xpeak,xorange], [ypeak,ypeak], **kwa)
kwa = {}
kwa['color'   ] = 'green'
kwa['fontsize'] = 15
kwa['ha'      ] = 'center'
kwa['va'      ] = 'center'
kwa['zorder'  ] = 15
tx = r'$\left \langle \sigma v \right \rangle _{\mathrm{start}}$'
frame1.text( xpeak, ypeak-8, tx, **kwa )


xspots = [6,12,18,24]
for i, xs in enumerate(xspots) :
  xs = xpeak + xs
  ys = poly(xs)
  kwa = {}
  kwa['color'] = 'gray'
  kwa['markersize'] = 10
  kwa['zorder'    ] = 15
  kwa['clip_on'   ] = False
  frame1.plot( [xs,xs], [ys,ys-5], **kwa)
  frame1.plot( [xs], [ys], '.', **kwa )
  kwa = {}
  kwa['color'   ] = 'gray'
  kwa['fontsize'] = 10
  kwa['ha'      ] = 'center'
  kwa['va'      ] = 'center'
  kwa['zorder'  ] = 15
  tx = r'$\left \langle \sigma v \right \rangle _{%d}$'%(i+1)
  if i == len(xspots)-1 :
    tx = r'$\left \langle \sigma v \right \rangle _{\mathrm{...}}$'
  frame1.text( xs, ys-8, tx, **kwa )


# Red Upper Limit End
xp, yp = x_deltaL, y_deltaL 
kwa = {}
kwa['color'] = 'red'
kwa['markersize'] = 10
kwa['zorder'    ] = 12
kwa['clip_on'   ] = False
frame1.plot( [xp,xp], [yp,yp-3], **kwa)
frame1.plot( [xp], [yp], '.', **kwa )
kwa['linestyle'] = 'dotted'
kwa['alpha'    ] = 0.7
frame1.plot( [xp,xp], [yp,yp], **kwa)
kwa = {}
kwa['color'    ] = 'red'
kwa['alpha'    ] = 0.5
kwa['linestyle'] = 'dotted'
kwa['zorder'   ] = 5
frame1.plot( [xp,xorange], [yp,yp], **kwa)
kwa = {}
kwa['color'   ] = 'red'
kwa['fontsize'] = 15
kwa['ha'      ] = 'center'
kwa['va'      ] = 'center'
tx = r'$\left \langle \sigma v \right \rangle | _{\mathrm{ul}}$'
frame1.text( xp-3, yp-5, tx, **kwa )


kwa = {}
kwa['size'] = 20
frame1.set_title('Likelihood Upper Limit Calculation', **kwa)
frame1.set_xlabel( r'Increasing $\left \langle \sigma v \right \rangle \rightarrow$', **kwa )
frame1.set_ylabel( r'Increasing Maximum Likelihood $\mathcal{L} \rightarrow$', **kwa )
frame1.set_xlim(right=55)
frame1.set_ylim(bottom=ythresh,top=-10)
frame1.set_xticklabels([])
frame1.set_yticklabels([])
kwa = {}
kwa['loc'   ] = 'upper left'
kwa['shadow'] = True
kwa['prop'  ] = {'size':15}
frame1.legend( **kwa )

kwa = {}
kwa['bbox_inches'] = 'tight'
kwa['pad_inches' ] = 0
kwa['dpi'        ] = 150
plt.savefig( 'ulimdiagram2.pdf', **kwa )
plt.close(fig)
