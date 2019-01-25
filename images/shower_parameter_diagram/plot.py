#!/usr/bin/env python
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, RegularPolygon
from matplotlib.collections import PatchCollection

pixfile = os.environ['VERITAS_EVNDISP_AUX_DIR'] + '/DetectorGeometry/EVN_V5_Oct2012_newArrayConfig_20121027_v420.txt'

pixcoords  = []
pixnumbers = []
r = 14
with open( pixfile, 'r' ) as f :
  for line in f.readlines() :
    if 'PMPIX 1' not in line : continue
    line = line.rstrip().split()
    i  = int(   line[3] )
    x  = float( line[6] ) # mm
    y  = float( line[7] ) # mm
    r  = float( line[8] ) # mm
    pixcoords  += [ [x,y] ]
    pixnumbers += [ i     ]

fig   = plt.figure(1)
frame = fig.add_axes(( 0.1, 0.1, 0.8, 0.8 ))

kwa = {}
kwa['fontsize'] = 3
kwa['ha'      ] = 'center'
kwa['va'      ] = 'center'
kwa['zorder'  ] = 9
pixels = []
for pxy, ip in zip( pixcoords, pixnumbers ) :
  #pixels += [ Circle( pxy, r ) ]
  pixels += [ RegularPolygon( pxy, 6, 2*r/np.sqrt(3) ) ]
  #plt.text( pxy[0], pxy[1], str(ip), **kwa )
    
kwa = {}
kwa['alpha'    ] = 0.5
kwa['color'    ] = '#fefefe'
kwa['facecolor'] = 'None'
kwa['edgecolor'] = 'gray'
kwa['linewidth'] = 0.25
p = PatchCollection(pixels, **kwa )
frame.add_collection(p)

kwa = {}
kwa['facecolor'] = 'None'
kwa['edgecolor'] = 'black'
frame.add_artist( Circle((0,0), 383, **kwa ) )

#kwa = {}
#kwa['facecolor'] = 'None'
#kwa['edgecolor'] = 'black'
#frame.add_artist( Ellipse([-30,-200], 330, 120, angle=25, **kwa ) )

heat = {}
heat[1.0] = [ 236, 235, 185, 184, 140, 183, 139, 138, 100, 99 ]
heat[0.5] = [ 234, 186, 141, 101, 137, 182 ]
heat[0.1] = [ 292, 291, 293, 355, 290, 233, 237, 232, 136, 180, 142, 103, 102, 69, 68, 67, 98, 97, 181 ]

pixels=[]
for h in heat.keys() :
  pixels = []
  for pxy, ip in zip( pixcoords, pixnumbers ) :
    if ip in heat[h] :
      #pixels += [ Circle( pxy, r ) ]
      pixels += [ RegularPolygon( pxy, 6, 2*r/np.sqrt(3) ) ]
  kwa = {}
  kwa['color'    ] = 'red'
  kwa['facecolor'] = 'red'
  kwa['edgecolor'] = 'none'
  kwa['zorder'   ] = 8
  kwa['alpha'    ] = h
  p = PatchCollection(pixels, **kwa )
  frame.add_collection(p)

pixels2 = []
iss = [ 0, 1, 2, 3 ]
hs = [   0, 0.1, 0.5, 1.0 ]
zs = [ 283, 282, 342, 407 ]
for h,z,i in zip(hs,zs, iss) :
  pixels1 = []
  for pxy, ip in zip( pixcoords, pixnumbers ) :
    if ip == z :
      #pixels += [ Circle( pxy, r ) ]
      shift = 350
      pixels1 += [ RegularPolygon( [pxy[0]+shift, pxy[1]], 6, 2*r/np.sqrt(3) ) ]
      pixels2 += [ RegularPolygon( [pxy[0]+shift, pxy[1]], 6, 2*r/np.sqrt(3) ) ]
  kwa = {}
  kwa['color'    ] = 'red'
  kwa['facecolor'] = 'red'
  kwa['edgecolor'] = 'none'
  kwa['zorder'   ] = 8
  kwa['alpha'    ] = h
  p = PatchCollection(pixels1, **kwa )
  frame.add_collection(p)

kwa = {}
kwa['alpha'    ] = 0.5
kwa['color'    ] = '#fefefe'
kwa['facecolor'] = 'None'
kwa['edgecolor'] = 'gray'
kwa['linewidth'] = 0.25
p = PatchCollection(pixels2, **kwa )
frame.add_collection(p)

frame.axes.get_xaxis().set_visible(False)
frame.axes.get_yaxis().set_visible(False)
frame.axis('off')
plt.autoscale()
frame.set_aspect(1.0)
kwa = {}
kwa['pad_inches' ] = 0
kwa['dpi'        ] = 400
kwa['bbox_inches'] = 'tight'
fig.savefig('plot.pdf', **kwa)


