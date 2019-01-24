#!/usr/bin/env python
import veripy, gammalib, numpy, os, math
from gammalib import GEnergy, GSkyDir
import matplotlib
import matplotlib.pyplot as plt

runnumber = 78128
obs = veripy.load_obs_proper( ['VR%d.ReconMethodDisp.Cut-NTel2-ExtendedSource-Hard.chunk1.fits' % runnumber ] )
run = obs[0]
fname = 'psf_parameter_space.pdf'
show_events = True

frac    = 0.68
thmin   = 0.0001
thmax   = 2.15
thnbins = 80
enmin   = GEnergy(   1.5, 'TeV')
enmax   = GEnergy( 150.0, 'TeV')
ennbins = 120

thdelta = ( thmax - thmin ) / thnbins
endelta = ( enmax.log10TeV() - enmin.log10TeV() ) / ennbins
EN, TH, PSF = [], [], []

# loop over offset (th) and energy (en)
for j in range(ennbins) :
  en = ( (j+0.5) * endelta ) + enmin.log10TeV()
  for i in range(thnbins) :
    th = ( ( (i+0.5) * thdelta ) + thmin ) * gammalib.deg2rad
    contain_rad = run.response().psf().containment_radius( frac, en, th )
    contain_rad *= gammalib.rad2deg 
    EN.append(  en                    )
    TH.append(  th * gammalib.rad2deg )
    PSF.append( contain_rad           )

print('len(EN):',len(EN))

# reshape our lists into pcolormesh-acceptable numpy arrays
EN  = numpy.reshape( EN , (ennbins,thnbins) )
TH  = numpy.reshape( TH , (ennbins,thnbins) )
PSF = numpy.reshape( PSF, (ennbins,thnbins) )

print('dim(EN):',EN.shape)

# construct our plot
fig = plt.figure(figsize=(10,5))
ax  = fig.add_subplot( 1,1,1, adjustable='box', aspect=1.0 )
im  = plt.pcolormesh( EN, TH, PSF, vmax=0.5, cmap=plt.get_cmap('jet'), linewidth=0, rasterized=True )
ax.set_aspect(0.6)
cb  = fig.colorbar( im )

# label things
cb.set_label(r'%.0f%% Containment Radius [${}^{\circ}$]' % (frac*100.0)    )
plt.title(   'PSF %d%% Containment Radius for Sgr A* Run %d' % ( int(frac*100.0), runnumber ), fontsize=15 )
plt.xlabel(  r'Event Energy [TeV]', fontsize=15 )
plt.ylabel(  r'Angle from Camera Center [${}^{\circ}$]', fontsize=15 )
plt.tick_params(axis='both', which='major', labelsize=15 )

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

xvals = [2,3,5,10,20,30,50,100]
ax.set_xticks(      [ math.log10(x) for x in xvals ] )
ax.set_xticklabels( [ str(x)        for x in xvals ] )
plt.gca().set_xlim([enmin.log10TeV()+(endelta*0.5), enmax.log10TeV()-(endelta*0.5)])
plt.gca().set_ylim([thmin           +(thdelta*0.5), thmax           -(thdelta*0.5)])
  
plt.savefig( fname , bbox_inches='tight', dpi=300 )
#plt.savefig( os.path.splitext(fname)[0]+'.png' , bbox_inches='tight', dpi=300 )

