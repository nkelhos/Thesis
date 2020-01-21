#!/usr/bin/env python
import veripy, glob, os, math, numpy, re, sys
from background import write_archive_radial_smart2
from gammalib import GCTAObservation, GCTAResponseIrf, deg2rad
from math import log10
import matplotlib.pyplot as plt
db = veripy.VeritasDB()
def pow10(x) : return math.pow(10,x)

elmin = 24
elmax = 33

fits = glob.glob( veripy.get_fits_dir() + '/sgraoff/*.fits' ) #[:60]

fitsepoch5 = []
fitsepoch6 = []
for f in fits :
  f1  = os.path.basename(f)
  run = int(re.search('VR(\d+)',f1).group(1))
  if db.run2epoch(run) == 5 : fitsepoch5 += [ f ]
  if db.run2epoch(run) == 6 : fitsepoch6 += [ f ]
  
print('%d V5 fits files' % len(fitsepoch5) )
print('%d V6 fits files' % len(fitsepoch6) )

obs = veripy.load_obs_atomic( fitsepoch6 )
nevents = sum([ len(ob.events()) for ob in obs ])
ontime  = sum([ob.ontime() for ob in obs ])
print('loaded: %d events over %.1f seconds...' % ( nevents, ontime ) )

# copy algo from write_archive_radial_smart2 on https://github.com/nkelhos/veripy/blob/0a2b7075a6dc84c1a1a000d39252ce6a3676b647/src/background.py

try:
  veripy.mkdir('output')
except :
  pass

kwa = {}
#kwa['fine_energy_hist'   ] = 'out_fine_energy_histogram.png'
#kwa['profile_plot_format'] = 'out_radial_profile_%d.png' # this is a format
#kwa['bkg_profile_plot'   ] = 'out_background_profile.png'   
#kwa['bkg_grid_plot'      ] = 'out_background_grid.png'      
kwa['perturb'] = True
fnames = []
for i in range(15) :
  kwa['seed'] = i
  f = 'output/bkg.seed%d.fits' % i
  if not os.path.exists(f) :
    write_archive_radial_smart2( obs, f, **kwa )
  fnames += [ f ]

sample_en     = 7   # TeV
sample_radius = 0.5 # deg
nradii        = 120
radius_max    = 2.3 # deg
radius_delta  = radius_max / nradii
energy_min    = 1.2 # TeV
energy_max    = 200 # TeV
nenergies     = 120
energy_logdelta = ( log10(energy_max) - log10(energy_min) ) / nenergies
rs = [ i * radius_delta for i in range( nradii ) ]
es = [ pow10( log10(energy_min) + i * energy_logdelta ) for i in range(nenergies) ]
bprofs = {}
gprofs = {}
maxb = 0
maxg = 0

for f in fnames :

  run = GCTAObservation()
  rsp = GCTAResponseIrf()
  rsp.load_background( f )
  run.response( rsp )
  
  print()
  print('f:',f)
  bs = []
  for r in rs :
    bs += [ run.response().background()( log10(sample_en), r * deg2rad, 0 ) ]
    if bs[-1] > maxb : maxb = bs[-1]
  bprofs[f] = bs
  
  for r,b in zip(rs,bs) :
    print('r b %6g %6g' % (r,b) )
  
  profile_plot = f + '.profile.png'
  if not os.path.exists( profile_plot ) :
    fig = plt.figure( figsize=(12,10) )
    ax  = fig.add_subplot( 111 )
    plt.plot( rs, bs, linewidth=3 )
    plt.yscale('log')
    plt.title( 'Background Rate at Camera Center vs Radius (@ %.1f TeV)' % sample_en, fontsize=20 )
    plt.xlabel(r'Radius $deg$', fontsize=15)
    plt.ylabel(r'Background Counts Rate $\left ( \frac{counts}{s*sr*MeV} \right )$', fontsize=15)
    plt.tick_params(axis='both', which='major', labelsize=15)
    print('writing %s...' % profile_plot )
    fig.savefig( profile_plot, dpi=90 )
    plt.close(fig)

  gs = []
  for en in es :
    gs += [ run.response().background()( log10(en), sample_radius * deg2rad, 0 ) ]
    if gs[-1] > maxg : maxg = gs[-1]
  gprofs[f] = gs

  for e,g in zip(es,gs) :
    print( 'e g %6g %6g' % (e,g) )

  energy_plot = f + '.energy.png'
  if not os.path.exists( energy_plot ) :
    fig = plt.figure( figsize=(12,10) )
    ax  = fig.add_subplot( 111 )
    plt.plot( es, gs, linewidth=3 )
    plt.xscale('log')
    plt.yscale('log')
    plt.title( 'Background Rate at Camera Center vs Radius (@ %.2f Deg Offset)' % sample_radius, fontsize=20 )
    plt.xlabel(r'Energy $log10(TeV)$', fontsize=15)
    plt.ylabel(r'Background Counts Rate $\left ( \frac{counts}{s*sr*MeV} \right )$', fontsize=15)
    plt.tick_params(axis='both', which='major', labelsize=15)
    print('writing %s...' % profile_plot )
    fig.savefig( energy_plot, dpi=90 )
    plt.close(fig)

for i in range(nradii) :
  data = [ bprofs[k][i] for k in bprofs.keys() ]
  mea  = numpy.mean( data )
  sdev = numpy.std(  data )
  perc = 100 * sdev / mea
  print('standev : r %-6.3g : mea sdev %-9.2e %-9.2e : %% %-5.2f' % ( rs[i], mea, sdev, perc ) )

radspread_plot = 'output/radspread.pdf'
if not os.path.exists( radspread_plot ) :
  fig = plt.figure( figsize=(12,10) )
  ax  = fig.add_subplot( 111 )
  for k in bprofs.keys() :
    bs = bprofs[k]
    plt.plot( rs, bs, linewidth=1, zorder=10 )

  nradbins = 47
  raddelta = 3.0 / nradbins
  grey = '#d6d6d6'
  for i in range(nradbins) :
    x = i * raddelta
    plt.plot( [x,x], [4e-8,2e-5], linewidth=0.25, color=grey, zorder=3 )
  ax.set_xlim([-0.05,2.25])
  ax.set_ylim([5e-7,maxb*1.5])
  plt.yscale('log')
  plt.title( 'Background Rate at Camera Center vs Radius (@ %.1f TeV)' % sample_en, fontsize=20 )
  plt.xlabel(r'Radius (deg)', fontsize=15)
  plt.ylabel(r'Background Counts Rate $\left ( \frac{counts}{s*sr*MeV} \right )$', fontsize=15)
  plt.tick_params(axis='both', which='major', labelsize=15)
  print('writing %s...' % radspread_plot )
  fig.savefig( radspread_plot, dpi=90 )
  plt.close(fig)
  
enspread_plot = 'output/enspread.pdf'
if not os.path.exists( enspread_plot ) :
  fig = plt.figure( figsize=(12,10) )
  ax  = fig.add_subplot( 111 )
  for k in gprofs.keys() :
    gs = gprofs[k]
    plt.plot( es, gs, linewidth=1 )
  ax.set_ylim( [ 1e-8 , maxg*5 ] )
  plt.xscale('log')
  plt.yscale('log')
  plt.title( 'Background Rate at Camera Center vs Radius (@ %.2f Deg Offset)' % sample_radius, fontsize=20 )
  plt.xlabel(r'Energy (log10(TeV))', fontsize=15)
  plt.ylabel(r'Background Counts Rate $\left ( \frac{counts}{s*sr*MeV} \right )$', fontsize=15)
  plt.tick_params(axis='both', which='major', labelsize=15)
  print('writing %s...' % enspread_plot )
  fig.savefig( enspread_plot, dpi=300 )
  plt.close(fig)


