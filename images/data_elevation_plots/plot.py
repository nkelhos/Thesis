#!/usr/bin/env python
import veripy, os
import matplotlib.pyplot as plt
from os.path import join
db = veripy.VeritasDB()

srcs = ['Crab','Sgr A*','Sgr A* Off']
  
elmin, elmax, eldiv = 20, 40, 0.0625
elevbins = []
el = elmin
while el < elmax :
  elevbins += [ [el,el+eldiv] ]
  el += eldiv

cols = {'Crab':'blue','Sgr A*':'green','Sgr A* Off':'red'}
zord = {'Crab':3     ,'Sgr A*':1      ,'Sgr A* Off':2    }

fig = plt.figure( figsize=(15,8) )
plt.title( 'Observation Elevation Distribution')
plt.xlabel( r'Camera Center Elevation (${}^{\circ}$)' )
plt.ylabel( 'Pointing Time (min)' )
plt.xlim( [ elmin, elmax ] )
fax = plt.gca()

for src in srcs :
  csrc    = veripy.clean_source_name(src)
  runlist = join( veripy.get_veripy_dir(), 'thesis/runlists', 'thesis.%s.runlist' % csrc )
  runs    = veripy.read_runlist( runlist )
  expos   = db.run2elevbins( runs, elevbins )
  expos   = [ e / 60.0 for e in expos ]
  if src == 'Crab' :
    for i in range(len(elevbins)) :
      if elevbins[i][0] < 27.5 or elevbins[i][1] > 32.5 :
        expos[i] = 0
  fax.bar( [e[0] for e in elevbins], expos, eldiv, label=src, color=cols[src], alpha=0.6 )
  
legend = fax.legend( loc='upper left', shadow=True )
fax.set_xlim([22,33])
for ext in ['pdf','png'] :
  plt.savefig('plot.%s'%ext, dpi=100, bbox_inches='tight')
#os.system('convert plot.png plot.eps')
fig.clf()
  
fig = plt.figure( figsize=(15,8) )
plt.title( 'Sgr A* Observation Elevation Distribution by Wobbles')
plt.xlabel( r'Camera Center Elevation (${}^{\circ}$)' )
plt.ylabel( 'Pointing Time (min)' )
plt.xlim( [ elmin, elmax ] )
fax = plt.gca()
src = 'Sgr A*'
cols = {'N':'red','E':'blue','W':'green','S':'orange'}
csrc    = veripy.clean_source_name(src)
runlist = join( veripy.get_veripy_dir(), 'thesis/runlists', 'thesis.%s.runlist' % csrc )
for wobble in ['N','E','S','W'] :
  runs    = veripy.read_runlist( runlist )
  print('%d runs'%len(runs))
  runs    = [ run for run in runs if db.run2wobble(run) == wobble ]
  print('%d %s runs'%(len(runs),wobble))
  expos   = db.run2elevbins( runs, elevbins )
  expos   = [ e / 60.0 for e in expos ]
  fax.bar( [e[0] for e in elevbins], expos, eldiv, color=cols[wobble], alpha=0.6, label='Wobble %s' % wobble )
legend = fax.legend( loc='upper left', shadow=True )
fax.set_xlim([22,33])
for ext in ['png','pdf'] :
  plt.savefig('plot.wobbles.%s'%ext, dpi=100, bbox_inches='tight')
#os.system('convert plot.png plot.eps')

