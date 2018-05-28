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
    

fig = plt.figure( figsize=[9,7] )
fax = fig.add_subplot(111)

fax.errorbar( xbars, [a[0] for a in ybars], yerr=[a[1] for a in ybars], fmt='o' )
fax.plot( [min(xbars),max(xbars)], [1,1], color='k', linestyle='-', linewidth=1) 

for ext in [ 'png','pdf' ] :
  plt.savefig( 'plot.'+ext, bbox_inces='tight' )
