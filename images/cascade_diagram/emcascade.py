#!/usr/bin/env python
import os, random
from graphviz import Digraph
print 'make sure to run me with python <=2.8 !!'

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
  print ielem,elem

labels = {'gamma':'\gamma{}', 'e+':'e^{+}', 'e-':'e^{-}'}

tikzlines = []
tikzlines += [ r'\documentclass[tikz]{standalone}' ]
tikzlines += [ r'\usepackage{tikz-feynman}' ]
tikzlines += [ r'\begin{document}' ]
tikzlines += [ r'\feynmandiagram [layered layout, horizontal=a to b] {' ]

dotlines = []
dotlines += [ 'digraph G {' ]
gvfile = 'emcascadegv'
g = Digraph('G', filename=gvfile, format='pdf')
asize = 15
g.attr( size = '%d' % asize )
#dotlines += [ 'node [ size=%d ]' % asize ]
g.node_attr.update(color='lightblue2', style='filled', shape='circle', fixedsize='true', width='0.35')
#dotlines += [ 'node [ color=

typecol = {'gamma':'palegreen2','e+':'gold','e-':'lightblue2'}
for iel, el in enumerate(elist) :
  if el['type'] in labels.keys() :
    l = labels[el['type']]
  else :
    l = el['type']
  if el['gen'] == 0 :
    l += 'o'
  dotlines += [ '  %d [ label="%s" ] ;' % ( iel, l ) ]
  g.node( '%d'%iel, label=l, color=typecol[ el['type'] ] )
  
for iel, el in enumerate(elist) :
  if 'children' in el.keys() :
    for c in el['children'] :
      dotlines += [ '  %d -> %d ;' % ( iel, c ) ]
      g.edge('%s'%iel,'%s'%c)

maxgen = max( [ elem['gen'] for elem in elist ] )
for i in range(maxgen+1) :
  ranklist = []
  for jel, el in enumerate( elist ) :
    if el['gen'] == i :
      ranklist += [ jel ]
  rankline = '{ rank=same ; '
  rankline += ' '.join([ '%d'%jel for jel in ranklist ])
  rankline += ' }'
  dotlines += [ rankline ]
  
dotlines += [ '}' ]

g.render()

#os.system('convert %s.png emcascade.eps' % gvfile )

dotfile = 'cascade.dot'
print 'writing', dotfile
with open( dotfile, 'w' ) as f :
  for dl in dotlines :
    f.write( dl + '\n' )

cfile = 'cascade.tex'
cmd = 'fdp -Txdot %s | dot2tex -t math -ftikz -s > %s' % ( dotfile, cfile )
print '$', cmd 
os.system( cmd )
cmd = 'pdflatex %s' % cfile
print '$', cmd
os.system( cmd )

tikzlines += [ '};' ]
tikzlines += [ '\end{document}' ]

tikztex = 'feynman/cascade.tex'
with open( tikztex, 'w' ) as f :
  for tl in tikzlines :
    f.write( tl + '\n' )
cmd = 'lualatex --output-format=pdf %s' % tikztex
print 
os.system( cmd )


