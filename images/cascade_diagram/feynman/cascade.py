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
#tikzlines += [ r'\RequirePackage{luatex85}'        ]
tikzlines += [ r'\documentclass[tikz]{standalone}' ]
tikzlines += [ r'\usepackage{tikz-feynman}'        ]
tikzlines += [ r'\begin{document}'                 ]
#tikzlines += [ r'\tikzfeynmanset{']
#tikzlines += [ r'  every particle/.style={red},']
#tikzlines += [ r'}' ]
tikzlines += [ r'\feynmandiagram [layered layout, xscale=0.5] {' ]

linetypes   = {'gamma':'photon', 'e+':'anti fermion'   , 'e-':'fermion'}
linelabels  = {'gamma':'\gamma', 'e+':'e^{+}'          , 'e-':'e^{-}'  }
labelcolors = {'gamma':'red'   , 'e+':'green!70!black' , 'e-':'blue'   }

for i, p in enumerate(elist) :
  ptype  = p['type']
  ltype  = linetypes[ptype]
  lcol   = labelcolors[ptype]
  llabel = linelabels[ptype]
  if p['gen'] == 0 :
    tikzlines += [ '  alpha[particle=\(\gamma_o\)] -- [photon] a0,' ]
  elif p['gen'] == nlayers-1 :
    tikzlines += [ '  a%d -- [%s, %s] a%d[%s, particle=\(%s\)] ,' % ( p['parent'], lcol, ltype, i, lcol, llabel ) ]
  else :
    tikzlines += [ '  a%d -- [%s, %s, edge label=\(%s\)] a%d ,'   % ( p['parent'], lcol, ltype, llabel, i ) ]

tikzlines += [ '};' ]
tikzlines += [ '\end{document}' ]

tikztex = 'cascade.tex'
with open( tikztex, 'w' ) as f :
  for tl in tikzlines :
    f.write( tl + '\n' )
cmd = 'lualatex --output-format=pdf %s' % tikztex
print('$', cmd )
os.system( cmd )
