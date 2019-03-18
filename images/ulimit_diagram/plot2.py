#!/usr/bin/env python
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10,7))
frame1 = fig.add_axes(( 0.1, 0.1, 0.8, 0.8 ))

xmin, xmax = -30, 50
npts = 2000
ythresh = -120 # y location of bottom of plot
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



kwa = {}
kwa['color' ] = 'orange'
kwa['zorder'] = 8
frame1.plot( [x_deltaL,x_deltaL], [y_deltaL,ypeak], **kwa )
frame1.plot( 

midh = (y_deltaL + ypeak) / 2
kwa = {}
kwa['fontsize'] = 20
kwa['color'   ] = 'orange'
kwa['ha'      ] = 'left'
kwa['va'      ] = 'center'
frame1.text( x_deltaL + 1, midh, r'$\Delta\mathcal{L}$', **kwa )


kwa = {}
kwa['size'] = 20
frame1.set_title('Likelihood Upper Limit Calculation', **kwa)
frame1.set_xlabel( r'Increasing $\left \langle \sigma v \right \rangle \rightarrow$', **kwa )
frame1.set_ylabel( r'Increasing Maximum Likelihood $\mathcal{L} \rightarrow$', **kwa )
frame1.set_ylim(bottom=ythresh)
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
