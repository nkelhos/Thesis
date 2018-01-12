#!/usr/bin/env python
import os, random
from graphviz import Digraph

nlayers = 5
elist = []
elist += [ {'type':'gamma','gen':0} ]
random.seed(15)
def roll_brem_or_pair() :
  return random.uniform(0,1) > 0.5

gen=0
for i in range(nlayers-1) :
  for j in range(len(elist)) :
    if elist[j]['gen'] == i :
      if elist[j]['type'] == 'gamma' :
        elist += [ {'type':'e+','gen':i+1,'parent':j} ]
        elist += [ {'type':'e-','gen':i+1,'parent':j} ]
        elist[j]['children'] = [ len(elist)-2, len(elist)-1 ]
      elif elist[j]['type'] in ['e+','e-'] :
        brem = roll_brem_or_pair()
        brem = True # 
        if brem :
          elist += [ {'type':'gamma','gen':i+1,'parent':j} ]
          elist += [ {'type':elist[j]['type'],'gen':i+1,'parent':j} ]
          elist[j]['children'] = [ len(elist)-2, len(elist)-1 ]
        else :
          elist += [ {'type':'gamma','gen':i+1,'parent':j} ]
          elist += [ {'type':'gamma','gen':i+1,'parent':j} ]
          elist[j]['children'] = [ len(elist)-2, len(elist)-1 ]

for ielem, elem in enumerate(elist) :
  print(ielem,elem)

labels = {'gamma':'\u0263'}

gvfile = 'emcascade.gv'
g = Digraph('G', filename=gvfile, format='png')
g.attr(size='15')
g.node_attr.update(color='lightblue2', style='filled', shape='circle', fixedsize='true', width='0.35')

typecol = {'gamma':'palegreen2','e+':'gold','e-':'lightblue2'}
print()
print('digraph G {')
for iel, el in enumerate(elist) :
  if el['type'] in labels.keys() :
    l = labels[el['type']]
  else :
    l = el['type']
  print('  %d [ label=%s ]' % ( iel, l ) )
  if el['gen'] == 0 :
    l += 'o'
  g.node( '%d'%iel, label=l, color=typecol[ el['type'] ] )
  
for iel, el in enumerate(elist) :
  if 'children' in el.keys() :
    for c in el['children'] :
      print('  %d -> %d' % ( iel, c ) )
      g.edge('%s'%iel,'%s'%c)
  
print('}')

g.render()

os.system('convert %s.png emcascade.eps' % gvfile )
