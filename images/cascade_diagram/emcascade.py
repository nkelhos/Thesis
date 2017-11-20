#!/usr/bin/env python
import os
from graphviz import Digraph

nlayers = 4
elist = []
elist += [ {'type':'gamma','gen':0} ]

gen=0
for i in range(nlayers-1) :
  for j in range(len(elist)) :
    if elist[j]['gen'] == i :
      if elist[j]['type'] == 'gamma' :
        elist += [ {'type':'e+','gen':i+1,'parent':j} ]
        elist += [ {'type':'e-','gen':i+1,'parent':j} ]
        elist[j]['children'] = [ len(elist)-2, len(elist)-1 ]
      elif elist[j]['type'] in ['e+','e-'] :
        elist += [ {'type':'gamma','gen':i+1,'parent':j} ]
        elist += [ {'type':'gamma','gen':i+1,'parent':j} ]
        elist[j]['children'] = [ len(elist)-2, len(elist)-1 ]

for ielem, elem in enumerate(elist) :
  print(ielem,elem)

labels = {'gamma':'\u0263'}

gvfile = 'emcascade.gv'
g = Digraph('G', filename=gvfile, format='png')

print()
print('digraph G {')
for iel, el in enumerate(elist) :
  if el['type'] in labels.keys() :
    l = labels[el['type']]
  else :
    l = el['type']
  print('  %d [ label=%s ]' % ( iel, l ) )
  g.node('%d'%iel,label=l)
  
for iel, el in enumerate(elist) :
  if 'children' in el.keys() :
    for c in el['children'] :
      print('  %d -> %d' % ( iel, c ) )
      g.edge('%s'%iel,'%s'%c)
  
print('}')

g.render()

os.system('convert %s.png emcascade.eps' % gvfile )
