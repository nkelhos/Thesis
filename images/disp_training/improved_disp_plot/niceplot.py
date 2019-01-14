#!/usr/bin/env python
import re, math
import matplotlib.pyplot as plt

x,y,c = [],[],[]
with open('somefile.txt','r') as f :
  for g in f.readlines() :
    g = g.lstrip().rstrip()
    if not g.startswith('fSumw') : continue
    p = re.search( ']=(\d+), x=([0-9.]+), y=([\-0-9.]+)', g )
    if p :
      c += [ int(   p.groups()[0] ) ]
      x += [ float( p.groups()[1] ) ]
      y += [ float( p.groups()[2] ) ]
    
n  = len(x)
xs = sorted(list(set(x)))
xw = xs[1] - xs[0]
ys = sorted(list(set(y)))
yw = ys[1] - ys[0]

ny = []
for i in range(n) :
  ny += [ ( y[i] + x[i] ) / x[i] ]
  #ny += [  y[i] / x[i] ]

xs = sorted(list(set(x)))
print('xs:',xs)
xbars, ybars = [], []

for xi in xs :
  xilist = []
  for i in range(n) :
    if x[i] == xi :
      if c[i] > 0 :
        xilist += [ [ ny[i], c[i] ] ]
  
  xi_cts = sum([ a[1] for a in xilist ])
  if xi_cts < 2 : continue
  xi_mean = sum([ a[0] * a[1] for a in xilist ]) / xi_cts

  xi_std = 0
  for a in xilist :
    xi_std += ( ( a[0] - xi_mean )**2 ) * a[1]
  xi_std /= ( xi_cts - 1 )
  xi_std = math.sqrt( xi_std )

  xbars += [ xi ]
  ybars += [ [ xi_mean, xi_std ] ]
  print( '%6.3f %3d %f %f' % ( xi, xi_cts, xi_mean, xi_std) )
    

nsplit = 10
xsplit = 0.75
xf     = 0.25
xl, xr = 0.05, 0.95
yb, yt = 0.05, 0.92

fig = plt.figure( figsize=[7,3] )

frame1 = fig.add_axes( ( xl, yb, xf-xl, yt-yb ) )
kwa = {}
kwa['fmt'       ] = '.'
kwa['yerr'      ] = [a[1] for a in ybars][:nsplit]
kwa['markersize'] = 2
kwa['linewidth' ] = 0.5
frame1.errorbar( xbars[:nsplit], [a[0] for a in ybars][:nsplit], **kwa )
kwa = {}
kwa['color'    ] = 'gray'
kwa['linestyle'] = '--'
kwa['linewidth'] = 0.4
kwa['zorder'   ] = -3
frame1.plot( [ 0, xsplit ], [1,1], **kwa )
frame1.set_xlim( [ 0, xsplit ] )
frame1.set_ylabel( r'$\frac{\mathrm{Predicted\;Disp}}{\mathrm{True\;Disp}}$ Residual' )

frame2 = fig.add_axes( ( xf, yb, xr-xf, yt-yb ) )
kwa = {}
kwa['fmt'       ] = '.'
kwa['yerr'      ] = [a[1] for a in ybars][nsplit:]
kwa['markersize'] = 2
kwa['linewidth' ] = 0.5
frame2.errorbar( xbars[nsplit:], [a[0] for a in ybars][nsplit:], **kwa )
kwa = {}
kwa['color'    ] = 'gray'
kwa['linestyle'] = '--'
kwa['linewidth'] = 0.4
kwa['zorder'   ] = -3
frame2.plot( [xsplit,3.5], [1,1], **kwa )
frame2.yaxis.tick_right()
frame2.yaxis.set_label_position('right')
frame2.set_ylabel(   r'$\frac{\mathrm{Predicted\;Disp}}{\mathrm{True\;Disp}}$ Residual' )
frame2.set_xlim([xsplit,3.5])
frame2.set_xlabel(   'True Disp (${}^{\circ}$)', horizontalalignment='right')

fig.suptitle( 'Disp Residual' )
kwa = {}
kwa['bbox_inches'] = 'tight'
kwa['pad_inches' ] = 0
kwa['dpi'        ] = 400
plt.savefig( 'plot.pdf', **kwa )

plt.close(fig)

