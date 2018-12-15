#!/usr/bin/env python
import veripy, glob, matplotlib
import matplotlib.pyplot as plt
db = veripy.VeritasDB()

dt = 0.5
sources = ['Sgr A*', 'Sgr A* Off', 'Crab']

elevs = {}
for src in sources :
  fitsdir  = veripy.get_veripy_dir() + '/fits'
  csrc     = veripy.clean_source_name(src)
  sfitsdir = fitsdir + '/%s'%csrc
  fits     = sorted(glob.glob( sfitsdir + '/*fits' ))[:20]
  obs = veripy.load_obs_proper( fits, bkg='powerlaw' )
  obs_hrs = sum([o.ontime() for o in obs])/3600.0
  obs_n   = sum([ len(ob.events()) for ob in obs ])
  els, azs = db.obs2elevsazs( obs, inc=dt )
  elevs[src] = els
  print('%-12s : %5.1f hours of data, %5d events' % ( src, obs_hrs, obs_n ) )
  obs_hrs = len(elevs[src]) * dt / 3600.0
  print('%-12s : %5.1f hours of data, %5d events' % ( src, obs_hrs, obs_n ) )


elmin   = 20
elmax   = 40
elnbins = int((elmax-elmin)*10)
elbinw  = (elmax-elmin)/elnbins
elbins_left   = [ elmin + j*elbinw for j in range(elnbins) ]
elbins_counts = {}
for src in sources : 
  elbins_counts[src] = [ 0 for j in range(elnbins) ]

for src in sources :
  for el in elevs[src] :
    i = int( (el-elmin)/elbinw )
    elbins_counts[src][i] += 1

fig1   = plt.figure(1)
frame1 = fig1.add_axes(( 0.1, 0.1, 0.8, 0.5 ))
lighterblue  = '#5f87cc'
lightergreen = '#95cc5f'
lighterred   = '#f45942'
colors = {'Sgr A*':lightergreen,'Sgr A* Off':lighterred, 'Crab':lighterblue}
kwa = {}
kwa['align'    ] = 'edge'
kwa['edgecolor'] = 'none'
kwa['zorder'   ] = -6

i = -6
for src in sources :
  kwa['color' ]  = colors[src]
  kwa['zorder'] += 1
  frame1.bar( elbins_left, elbins_counts[src], elbinw, **kwa )
  
frame1.set_rasterization_zorder(-2)
frame1.set_title('Telescope Pointing Elevation')
frame1.set_xlabel(r'Elevation (${}^{\circ}$)')
frame1.set_ylabel('Seconds')
frame1.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1))
frame1.set_xlim([elmin,elmax])
pname = 'elevhist.pdf'
kwa = {}
kwa['dpi'        ] = 400
kwa['bbox_inches'] = 'tight'
kwa['pad_inches' ] = 0
plt.savefig( pname, **kwa )





