#!/usr/bin/env python
import random, os

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

tikzlines = []
tikzlines += [ r'\documentclass[tikz]{standalone}' ]
tikzlines += [ r'\usepackage{tikz-feynman}'        ]
tikzlines += [ r'\begin{document}'                 ]
tikzlines += [ r'\feynmandiagram [small, layered layout, vertical=a to b] {' ]

linetypes  = {'gamma':'photon','e+':'anti fermion','e-':'fermion'}
linelabels = {'gamma':'\gamma','e+':'e^{+}'       ,'e-':'e^{-}'  }

for i, p in enumerate(elist) :
  if p['gen'] == 0 :
    tikzlines += [ '  alpha -- [photon, edge label=\(\gamma_o\)] a0,' ]
  else :
    tikzlines += [ '  a%d -- [%s, edge label=\(%s\)] a%d ,' % ( p['parent'], linetypes[p['type']], linelabels[p['type']], i ) ]


tikzlines += [ '};' ]
tikzlines += [ '\end{document}' ]

tikztex = 'cascade.tex'
with open( tikztex, 'w' ) as f :
  for tl in tikzlines :
    f.write( tl + '\n' )
cmd = 'lualatex --output-format=pdf %s' % tikztex
print('$', cmd )
os.system( cmd )
