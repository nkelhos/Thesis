#!/usr/bin/env python
import veripy, aplpy, numpy, matplotlib
import matplotlib.pyplot as plt

"""
Exception: WARNING: projection is Plate Caree (-CAR) and
                CRVALy is not zero. This can be interpreted either according to
                Wells (1981) or Calabretta (2002). The former defines the
                projection as rectilinear regardless of the value of CRVALy,
                whereas the latter defines the projection as rectilinear only when
                CRVALy is zero. You will need to specify the convention to assume
                by setting either convention='wells' or convention='calabretta'
                when initializing the FITSFigure instance.
"""
db    = veripy.VeritasDB()
sgra  = db.source2dir('Sgr A*')
db    = veripy.VeritasDB()
lwid  = 1
lsize = 18

fig = aplpy.FITSFigure('halo.profeinasto.core000pc.fits', convention='calabretta')
fig.recenter( sgra.l_deg(), sgra.b_deg(), radius=2.5 )
fax = plt.gca()

plt.title('Dark Matter Halo J-Factor Skymap', fontsize=lsize )

fax.set_axis_bgcolor('black')
fig.set_theme('publication')
fig.add_grid()
fig.grid.set_xspacing(1.0) # degrees
fig.grid.set_yspacing(1.0) # degrees
fig.grid.set_color('white')
fig.grid.set_linestyle('dashed')
fig.grid.set_linewidth( lwid ) # pts
fig.grid.set_alpha( 0.6 )
fig.grid.show()
fig.ticks.set_xspacing(1.0) # degrees
fig.ticks.set_yspacing(1.0) # degrees
fig.ticks.set_color('white')
fig.ticks.set_linewidth( lwid+0.37 )
fig.ticks.set_minor_frequency(4) # number of minor ticks per major tick
fig.set_tick_labels_xformat('ddd')
fig.set_tick_labels_yformat('ddd')
fig.axis_labels.set_xtext('Galactic l')
fig.axis_labels.set_ytext('Galactic b')
fig.axis_labels.set_font(size=lsize*0.75)
fig.tick_labels.set_font(size=lsize*0.5)

zmin  = 0 # numpy.min(fig._data)
zmax  = numpy.max(fig._data)
cmap1 = 'afmhot'
fig.show_colorscale( cmap=cmap1, vmin=zmin, vmax=zmax )
norm1  = matplotlib.colors.Normalize( vmin=zmin, vmax=zmax ) # ??
cbax   = fig._figure.add_axes([0.89,0.12,0.03,0.76])
colbar = matplotlib.colorbar.ColorbarBase( cbax, cmap=cmap1, norm=norm1, orientation='vertical' )
colbar.ax.tick_params(labelsize=lsize*0.5)

bartitle = r'J-Factor ($\mathrm{GeV}^{2} \mathrm{cm}^{-5}$)'
colbar.set_label( bartitle, fontsize=15 )

runs = veripy.read_runlist( veripy.get_veripy_dir() + '/thesis/runlists/thesis.sgra.runlist' )
print('%d runs...' % len(runs) )
pointings = []
for run in runs :
  pdir = db.run2dir(run)
  if pdir not in pointings :
    pointings += [ pdir ]
print('%d pointings...' % len(pointings) )

c = '#41d350'
for p in pointings :
  fig.show_circles( p.l_deg(), p.b_deg(), 1.75, facecolor='none', alpha=0.7, linewidth=1, edgecolor=c )
fig.add_label(  sgra.l_deg() + 0.45    , \
                sgra.b_deg() + 1.5    , \
                'Observation\nRegions', \
                color=c               , \
                alpha=0.7             , \
                verticalalignment   ='bottom', \
                horizontalalignment ='center' )


fig.refresh()
for ext in ['pdf','png'] :
  plt.savefig( 'plot.%s'%ext, bbox_inches='tight', dpi=100 )

