#!/usr/bin/env python
import veripy, os
import matplotlib.pyplot as plt
from os.path import join
db = veripy.VeritasDB()

srcs = ['Crab','Sgr A*','Sgr A* Off']
  
elmin, elmax, eldiv = 20, 40, 0.5
elevbins = []
el = elmin
while el < elmax :
  elevbins += [ [el,el+eldiv] ]
  el += eldiv

cols = {'Crab':'blue','Sgr A*':'green','Sgr A* Off':'red'}
zord = {'Crab':3     ,'Sgr A*':1      ,'Sgr A* Off':2    }

fig = plt.figure( figsize=(15,8) )
plt.title( 'Observation Elevation Distribution')
plt.xlabel( 'Elevation (deg)' )
plt.ylabel( 'Camera Center Pointing Time (min)' )
plt.xlim( [ elmin, elmax ] )
fax = plt.gca()

for src in srcs :
  csrc = veripy.clean_source_name(src)
  runlist = join( veripy.get_veripy_dir(), 'thesis/runlists', 'thesis.%s.runlist' % csrc )
  runs = veripy.read_runlist( runlist )
  expos = db.run2elevbins( runs, elevbins )
  expos = [ e / 60.0 for e in expos ]
  fax.bar( [e[0] for e in elevbins], expos, eldiv, label=src, color=cols[src], alpha=0.4 )
  
legend = fax.legend( loc='upper left', shadow=True )
plt.savefig('plot.png', dpi=100, bbox_inches='tight')
os.system('convert plot.png plot.eps')
  

  
