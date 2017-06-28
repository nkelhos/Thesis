#!/usr/bin/env python
import veripy, os, gammalib, aplpy
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
db = veripy.VeritasDB()

  
blanksky = gammalib.GSkyMap( 'TAN', 'GAL', 0, 2.0, 0.1, 0.1, 120, 120, 1 )
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
    la = 'Sgr A* Observations'
  elif src == 'Sgr A* Off' :
    co = 'blue'
    la = 'Sgr A* Off (Background) Observations'
  patch = mpatches.Patch(color=co, label=la)
  patches += [ patch ]
  fig.show_circles( gall, galb, radii, facecolor=co, zorder=1, edgecolor=None )
  fig.show_circles( gall, galb, radii, zorder=2, linewidth=1 )

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

fig.savefig('plot.png')

os.system('convert plot.png plot.eps')
