#!/usr/bin/env python
import glob, veripy, numpy, gammalib, sys, re, os, random
from math import log10
from gammalib import GEnergy
import mpl_toolkits
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
db = veripy.VeritasDB()

enbins = 100
nruns  = 1000
emin   = GEnergy( 300, 'GeV' )
emax   = GEnergy( 500, 'TeV' )
elogd  = ( emax.log10TeV() - emin.log10TeV() ) / enbins

def etrue_center(i) :
  return pow( 10, emin.log10TeV() + ( (i+0.5)*elogd ) )

total = numpy.full( [enbins,enbins], 1e-99, dtype=numpy.float64 )
fdir  = veripy.get_fits_dir() + '/sgra/*.fits'
fits  = glob.glob( fdir )
random.shuffle(fits)
fits  = sorted( fits[:nruns] )

nr = 0
totallive = 0
for f in fits :
  #r  = int( re.search( 'VR(\d+)', os.path.basename(f) ).group(1) )
  #ep = db.run2epoch( r )
  #if ep != target_epoch : continue
  #nr += 1
  #if nr > nruns : continue
  #print('%d %d %s' % (r,ep,f) )
  print(f)

  obs    = veripy.load_obs_atomic([f])
  run    = obs[0]
  edisp  = run.response().edisp()
  table  = edisp.table()
  atheta = table.axis( 'THETA')
  aetrue = table.axis( 'ETRUE')
  aemigr = table.axis( 'MIGRA')
  amatri = table.table('MATRIX')
  ntheta = table.axis_bins( atheta )
  netrue = table.axis_bins( aetrue )
  nemigr = table.axis_bins( aemigr )
  live   = run.livetime()
  totallive += live

  def theta_center(i) :
    theta_lo = table.axis_lo( atheta, i )
    theta_hi = table.axis_hi( atheta, i )
    return ( theta_lo + theta_hi ) / 2

  # fill energy columns
  map_etrue = []
  map_emigr = []
  for ietrue in range( enbins ) :
    for iemigr in range( enbins ) :
      map_etrue += [ etrue_center( ietrue ) ]
      map_emigr += [ etrue_center( iemigr ) ]
  shaped_etrue = numpy.reshape( map_etrue, (enbins, enbins) )
  shaped_emigr = numpy.reshape( map_emigr, (enbins, enbins) )
  iemin = min( map_etrue + map_emigr )
  iemax = max( map_etrue + map_emigr )

  # figure out our mean offsets
  mean_theta = [ theta_center( itheta ) for itheta in range(ntheta) ]
  
  # loop over theta bins
  images = []
  #for itheta in [2] : # only 0.5 degree offset
  itheta = 2
  theta  = gammalib.deg2rad * theta_center( itheta )

  map_matrix = []
  for ietrue in range( enbins ) :
    etrue = etrue_center( ietrue )
    for iemigr in range( enbins ) :
      emigr = etrue_center( iemigr )
      total[ietrue][iemigr] += edisp( log10(emigr), log10(etrue), theta ) * live

for ietrue in range( enbins ) :
  for iemigr in range( enbins ) :
    total[ietrue][iemigr] /= totallive

#print('total:')
for i in total :
  for j in i :
    s = '   --    '
    if j > 1.0e-99 : s = '%.2e '% j
    #print(s,end='')
  #print()

# this hides all values below a certain value in the plot
# (makes their bins transparent)
total = numpy.ma.masked_array( total, total < 0.1 )
print(total)

fig  = plt.figure( figsize=[9,9] )
ax   = fig.add_subplot( 1, 1, 1, adjustable='box', aspect=1.0 )
poly = Polygon( [(4,0.3),(4,500),(70,500),(70,0.3),(4,0.3)], facecolor='gray', alpha=0.4 )
paco = PatchCollection( [ poly ] )
ax.add_collection( paco )
im   = plt.pcolor( shaped_emigr, shaped_etrue, total, vmax=30, rasterized=True, cmap='rainbow' )

n = len(fits)
plt.title( r'Energy Migration Matrix for Sgr A* (%d Time-Weighted Runs) (Offset %.1f${}^{\circ}$)' % (n,theta*gammalib.rad2deg), fontsize=15 )
plt.plot( [emin.TeV(),emax.TeV()], [emin.TeV(),emax.TeV()], 'r--' )
plt.xlabel( r'E${}_{\mathrm{Reconstructed}}$ [TeV]', fontsize=15 )
plt.ylabel( r'E${}_{\mathrm{True}}$ [TeV]', fontsize=15 )
plt.xscale( 'log' )
plt.yscale( 'log' )
plt.gca().set_xlim( [ emin.TeV(), emax.TeV() ] )
plt.gca().set_ylim( [ emin.TeV(), emax.TeV() ] )
divider = mpl_toolkits.axes_grid1.make_axes_locatable(ax)
cax = divider.append_axes('right', size='5%', pad=0.05 )
cb  = plt.colorbar( im, cax=cax)
cb.set_label(r"$\frac{\# \; of \; Events}{MeV}$", fontsize=15)
plt.tick_params( axis='both', which='major', labelsize=15 )
for ext in ['pdf','png'] :
  image = 'ethresh.%s' % ext
  print('writing %s' % image )
  plt.savefig( image, bbox_inches='tight', dpi=100 )
plt.close()

  
