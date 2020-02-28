#!/usr/bin/env python
import veripy, aplpy, numpy, matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits
from matplotlib import rc
rc('text',usetex=True)

halo_l = '../dmhalo/lowres/halo.profeinasto.core000pc.fits'
output  = 'output/'
fname = output + 'calc_skymap.pdf'
print('preparing skymap...')
lwid  =  1
lsize = 21
db   = veripy.VeritasDB()
sgra = db.source2dir('Sgr A*')
fig  = aplpy.FITSFigure( halo_l, convention='calabretta' )
fig.recenter( sgra.l_deg(), sgra.b_deg(), radius=2.5 )
fax  = plt.gca()
plt.title('Dark Matter Halo J-Factor Skymap', fontsize=lsize )

def readheader( fitsfile, header ) :
  with fits.open( fitsfile, 'update' ) as f :
    return f[0].header[header]
fits_jfactor = readheader( halo_l, 'FLUX_TOT' )
fits_jf_unit = readheader( halo_l, 'BUNIT' )
pixel_xwid   = readheader( halo_l, 'CDELT1' ) # deg
pixel_ywid   = readheader( halo_l, 'CDELT2' ) # deg
pixel_area   = abs( pixel_xwid * pixel_ywid ) # deg2
print('pixel area: %g deg^2' % pixel_area )

print('dim: %g' % len(fig._data) )
#fig._data[90][90] = fig._data[90][90] * 10
pixels = []
for i in range(len(fig._data)) :
  for j in range(len(fig._data[i])) :
    v = fig._data[i][j]
    if v > 0 : pixels += [ v ]
integ = sum(pixels)
print('integ: %g' % integ)
for i in range(len(fig._data)) :
  for j in range(len(fig._data[i])) :
    v = fig._data[i][j] * fits_jfactor / integ
    v = v / pixel_area
    fig._data[i][j] = v

#fax.set_axis_bgcolor('black')
fax.set_facecolor('black')
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
#fig.axis_labels.set_font( family='serif' )
fig.axis_labels.set_xtext( r'Galactic Longitude $l$')
fig.axis_labels.set_ytext( r'Galactic Latitude $b$')
fig.axis_labels.set_font(size=lsize*0.8)
fig.tick_labels.set_font(size=lsize*0.7)

# histogram
pixels = []
for i in range(len(fig._data)) :
  for j in range(len(fig._data[i])) :
    v = fig._data[i][j]
    if v > 0 :
      pixels += [ v ]
kwa = {}
kwa['cmap'  ] = cmap1 = 'afmhot'
kwa['vmin'  ] = zmin  = min(pixels)
kwa['vmax'  ] = zmax  = numpy.max(fig._data)
#kwa['smooth'] = 1
#kwa['kernel'] = 'box'
#kwa['kernel'] = numpy.array([[0,0,0],[0,1,0],[0,0,0]])
kwa['interpolation'] = 'none'
fig.show_colorscale( **kwa )
norm1  = matplotlib.colors.Normalize( vmin=zmin, vmax=zmax ) # ??
cbax   = fig._figure.add_axes([0.89,0.12,0.03,0.76])
colbar = matplotlib.colorbar.ColorbarBase( cbax, cmap=cmap1, norm=norm1, orientation='vertical' )
colbar.ax.tick_params(labelsize=lsize*0.7)
bartitle = r'J-Factor per Solid Angle $\left [ \mathrm{GeV}^{2} \; \mathrm{cm}^{-5} \; \mathrm{deg}^{-2} \right ] $'
colbar.set_label( bartitle, fontsize=15 )

runs = veripy.read_runlist( 'sgra.runlist' )
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
fig.add_label(  sgra.l_deg() + 0.525    , \
                sgra.b_deg() + 1.375    , \
                'Observation\nRegions'  , \
                color=c                 , \
                alpha=0.7               , \
                size=13                 , \
                verticalalignment   ='bottom', \
                horizontalalignment ='center' )

fig.refresh()
plt.savefig( fname, bbox_inches='tight', dpi=1000 )

# histogram
pixels = []
for i in range(len(fig._data)) :
  for j in range(len(fig._data[i])) :
    v = fig._data[i][j]
    if v > 0 :
      pixels += [ v ]
print('pixels : |%g - %g - %g|' % ( min(pixels), sum(pixels)/len(pixels), max(pixels) ) )
fig = plt.figure(figsize=(10,5))
fax = fig.add_subplot(111)
plt.hist( pixels, bins=120 )
fig.savefig( output + 'calc_skymap_pixelhist.pdf', bbox_inches='tight', dpi=300, max_dpi=300 )


