#!/usr/bin/env python
import veripy, gammalib, numpy, os
from gammalib import GEnergy, GSkyDir
import matplotlib.pyplot as plt

runnumber = 78128
obs = veripy.load_obs_proper( ['VR%d.ReconMethodDisp.Cut-NTel2-ExtendedSource-Hard.chunk1.fits' % runnumber ] )
run = obs[0]
fname = 'psf_parameter_space.eps'
show_events = True

frac    = 0.68
thmin   = 0.0
thmax   = 2.75
thnbins = 40 # 100
enmin   = GEnergy(   2.0, 'TeV')
enmax   = GEnergy( 220.0, 'TeV')
ennbins = 40 # 100

thdelta = ( thmax - thmin ) / thnbins
endelta = ( enmax.log10TeV() - enmin.log10TeV() ) / ennbins
EN, TH, PSF = [], [], []

# loop over offset (th) and energy (en)
for j in range(ennbins) :
  en = ( (j+0.5) * endelta ) + enmin.log10TeV()
  for i in range(thnbins) :
    th = ( ( (i+0.5) * thdelta ) + thmin ) * gammalib.deg2rad
    contain_rad = veripy.containment_radius( run, en, th, contain=frac, npts=200 ) 
    contain_rad *= gammalib.rad2deg 
    EN.append(  en                    )
    TH.append(  th * gammalib.rad2deg )
    PSF.append( contain_rad           )

# reshape our lists into pcolormesh-acceptable numpy arrays
EN  = numpy.reshape( EN , (thnbins, ennbins) )
TH  = numpy.reshape( TH , (thnbins, ennbins) )
PSF = numpy.reshape( PSF, (thnbins, ennbins) )

# construct our plot
fig = plt.figure(figsize=(10,5))
ax  = fig.add_subplot( 1,1,1, adjustable='box', aspect=1.0 )
#im  = plt.pcolormesh( EN, TH, PSF, vmin=0.0, vmax=0.35)
#im  = plt.pcolormesh( EN, TH, PSF, vmin=0.0, vmax=0.45, cmap=plt.get_cmap('hot'))
im  = plt.pcolormesh( EN, TH, PSF, vmax=0.5, cmap=plt.get_cmap('afmhot'))
ax.set_aspect(0.4)
cb  = fig.colorbar( im )

# label things
cb.set_label('%.0f%% containment radii (deg)' % (frac*100.0)    )
plt.title(   'PSF %d%% Containment Radius for Galactic Center Run %d'    % ( int(frac*100.0), runnumber ) )
plt.xlabel(  'Event Energy log10(TeV)' )
plt.ylabel(  'Event Distance from Camera Center (deg)' )

# fix the x and y axes limits
plt.gca().set_xlim([enmin.log10TeV(), enmax.log10TeV()])
plt.gca().set_ylim([thmin,thmax])

# plot event positions if requested
if show_events :
  center = GSkyDir()
  center.radec(0.0,0.0)
  EN = []
  OF = []
  
  # loop over all events
  for event in run.events() :
    EN += [ event.energy().log10TeV() ]
    
    detx   = event.dir().detx() 
    dety   = event.dir().dety() 
    detdir = GSkyDir()
    detdir.radec( detx, dety )
    th  = center.dist( detdir ) * gammalib.rad2deg
    OF += [ th ]
    
  plt.scatter( EN, OF, color='black', s=1 )
  
ifname = os.path.splitext(fname)[0]+'.png'
plt.savefig( ifname , bbox_inches='tight', dpi=150 )
cmd = 'convert %s %s' % ( ifname, fname )
os.system( cmd )

