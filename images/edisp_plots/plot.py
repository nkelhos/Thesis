#!/usr/bin/env python
import veripy, tempfile, os, numpy, gammalib
from math import log10
from gammalib import GEnergy
import matplotlib.pyplot as plt
import matplotlib, mpl_toolkits

fname = 'edisp.png'
obs = veripy.load_obs_proper( ['VR82288.chunk1.fits'] )
run = obs[0]

edisp  = run.response().edisp()
table  = edisp.table()
atheta = table.axis( 'THETA')
aetrue = table.axis( 'ETRUE')
aemigr = table.axis( 'MIGRA')
amatri = table.table('MATRIX')
ntheta = table.axis_bins( atheta )
netrue = table.axis_bins( aetrue )
nemigr = table.axis_bins( aemigr )

temp_dir = tempfile.mkdtemp()

e_nbins = 400
e_min   = GEnergy( 100, 'GeV' )
e_max   = GEnergy( 500, 'TeV' )
e_logdelta = ( e_max.log10TeV() - e_min.log10TeV() ) / e_nbins

def etrue_center(i) :
  return pow( 10, e_min.log10TeV() + ( (i+0.5)*e_logdelta ) )

def theta_center(i) :
  theta_lo = table.axis_lo( atheta, i )
  theta_hi = table.axis_hi( atheta, i )
  return ( theta_lo + theta_hi ) / 2

# fill energy columns
map_etrue = []
map_emigr = []
for ietrue in range( e_nbins ) :
  for iemigr in range( e_nbins ) :
    map_etrue += [ etrue_center( ietrue ) ]
    map_emigr += [ etrue_center( iemigr ) ]
shaped_etrue = numpy.reshape( map_etrue, (e_nbins, e_nbins) )
shaped_emigr = numpy.reshape( map_emigr, (e_nbins, e_nbins) )
emin = min( map_etrue + map_emigr )
emax = max( map_etrue + map_emigr )
  
# figure out our mean offsets
mean_theta = [ theta_center( itheta ) for itheta in range(ntheta) ]
  
# loop over theta bins
images = []
for itheta in [2] : # only 0.5 degree offset
  theta = gammalib.deg2rad * theta_center( itheta )
  
  map_matrix = []
  for ietrue in range( e_nbins) :
    etrue = etrue_center( ietrue )
    for iemigr in range( e_nbins) :
      emigr = etrue_center( iemigr )
      map_matrix += [ edisp( log10(emigr), log10(etrue), theta ) ]
  
  s_matrix = numpy.reshape( map_matrix, (e_nbins,e_nbins) )
  shaped_matrix = numpy.ma.masked_array( s_matrix, s_matrix < 0.5 )
  
  fig = plt.figure( figsize=[9,9] )
  ax  = fig.add_subplot( 1, 1, 1, adjustable='box', aspect=1.0 )
  im  = plt.pcolormesh( shaped_emigr, shaped_etrue, shaped_matrix, vmax=30 )
  plt.title( 'Energy Migration Matrix for Galactic Center Run 82288 (Offset %.2fdeg)' % (theta*gammalib.rad2deg) )
  plt.plot( [emin,emax], [emin,emax], 'r--' )
  plt.xlabel( 'E_Reco [TeV]' )
  plt.ylabel( 'E_True [TeV]' )
  plt.xscale( 'log' )
  plt.yscale( 'log' )
  plt.gca().set_xlim( [ emin, emax ] )
  plt.gca().set_ylim( [ emin, emax ] )
  divider = mpl_toolkits.axes_grid1.make_axes_locatable(ax)
  cax = divider.append_axes('right', size='5%', pad=0.05 )
  cb  = plt.colorbar( im, cax=cax)
  cb.set_label('# of Events [1/s]')
  image = os.path.join( temp_dir, 'migmatrix_itheta%d.png'%itheta )
  plt.savefig( image, bbox_inches='tight', dpi=100 )
  plt.close()
  print('writing %s' % image )
  images += [ image ]
  
cmd = 'montage -mode concatenate -tile 1x%d %s %s' % ( len(images), ' '.join(images), fname )
os.system( cmd )

cmd = 'convert %s %s' % ( fname, os.path.splitext(fname)[0]+'.eps' )
os.system( cmd )
