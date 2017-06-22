#!/usr/bin/env python
import veripy, os
import matplotlib.pyplot as plt

db = veripy.VeritasDB()

fitsfiles = veripy.scan_for_fits_files( '/Users/nkelhos/Software/veripy/fits/crab/' )
obs = veripy.load_obs_proper( fitsfiles )
runlist = veripy.get_obs_runlist( obs )

elmin, elmax, eldiv = 20, 45, 0.5
elevbins = []
el = elmin
while el < elmax :
  elevbins += [ [el,el+eldiv] ]
  el += eldiv
print(elevbins)
expos = db.run2elevbins( runlist, elevbins )
expos = [ e / 60.0 for e in expos ]

fig = plt.figure(figsize=(18,7))
plt.title( 'Crab Observation Elevation Distribution')
plt.xlabel( 'Elevation (deg)' )
plt.ylabel( 'Camera Center Pointing Time (min)' )
plt.xlim( [ elmin, elmax ] )
ax = plt.gca()
ax.bar( [e[0] for e in elevbins], expos, eldiv )
plt.savefig('plot.png')
os.system('convert plot.png plot.eps')

