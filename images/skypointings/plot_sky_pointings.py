#!/usr/bin/env python
import veripy, os, gammalib, aplpy, numpy
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
db = veripy.VeritasDB()

mapcenter_x, mapcenter_y = 0, 2 # lb
binsz=0.1
nbins=120  
blanksky = gammalib.GSkyMap( 'TAN', 'GAL', mapcenter_x, mapcenter_y, binsz, binsz, nbins, nbins, 1 )
fitsfile = 'blankskky.fits'
blanksky.save( fitsfile, True )
fig = aplpy.FITSFigure(fitsfile)
ax = plt.gca()
ax.set_axis_bgcolor('white')
plt.title('Galactic Center On and Off Observations')

sources = [ 'Sgr A*', 'Sgr A* Off' ]

patches = []
patchlabels = []
for src in sources : 
  csrc = veripy.clean_source_name(src)
  runlist = veripy.read_runlist( os.path.join( veripy.get_veripy_dir(), 'thesis/runlists/thesis.%s.runlist' % csrc ) )
  runlist = sorted(list(set(runlist)))
  runlist = db.smart_runlist(runlist)

  gall, galb, radii = [], [], []
  for run in runlist :
    gall  += [ run.pointing_dir.l_deg() ]
    galb  += [ run.pointing_dir.b_deg() ]
    radii += [ 1.75 ]

  if src == 'Sgr A*' :
    co = 'green'
    la = 'Data Observation Regions'
  elif src == 'Sgr A* Off' :
    co = 'blue'
    la = 'Background Observation Regions'
  patch = mpatches.Circle((0,0), radius=1, facecolor=co, edgecolor='black', linewidth=2, label=la)
  patches += [ patch ]
  fig.show_circles( gall, galb, radii, facecolor=co, zorder=2, edgecolor=None )
  fig.show_circles( gall, galb, radii, zorder=3, linewidth=1 )

cols = {'Sgr A*':'orange','Sgr A* Off':'red'}
for src in sources :
  srcdir = db.source2dir(src)
  fig.show_markers( srcdir.l_deg(), srcdir.b_deg()    , marker='v', color='black', edgecolor=cols[src], label='%s Position'%src, zorder=4 )
  fig.add_label(    srcdir.l_deg(), srcdir.b_deg()+0.4, src, color=cols[src] )
  
# galactic plane
npts   = 5
span   = binsz*nbins
pdelta = span / npts
plane_x, plane_y = [], []
for i in range(npts+1) :
  plane_x += [ mapcenter_x - (span/2) + i*pdelta ]
  plane_y += [ 0.5 ]
for i in range(npts+1) :
  plane_x += [ mapcenter_x + (span/2) - i*pdelta ]
  plane_y += [ -0.5 ]
co = '#89f5ff'
pgon = [numpy.array([[px,py] for px,py in zip(plane_x,plane_y)])]
fig.show_polygons( pgon, zorder=1, alpha=0.7, facecolor=co, edgecolor=co )
patch = mpatches.Patch( facecolor=co, edgecolor=co, alpha=0.7, label='Galactic Plane' )
patches += [ patch ]

legend = ax.legend( handles=patches, loc='upper right', shadow=True )

fig.add_grid()
fig.grid.set_xspacing(1.0) # degrees
fig.grid.set_yspacing(1.0) # degrees
fig.grid.set_color('black')
fig.grid.set_linestyle('dashed')
fig.grid.set_linewidth(0.5) # pts
fig.grid.set_alpha(0.6)
fig.grid.show()
fig.ticks.set_xspacing(1.0) # degrees
fig.ticks.set_yspacing(1.0) # degrees
fig.ticks.set_color('black')
fig.ticks.set_linewidth(0.75)
fig.ticks.set_minor_frequency(2) # number of minor ticks per major tick
fig.set_tick_labels_xformat('ddd')
fig.set_tick_labels_yformat('ddd')

for ext in ['png','pdf'] :
  fig.savefig('plot.%s'%ext)

#os.system('convert plot.png plot.eps')
