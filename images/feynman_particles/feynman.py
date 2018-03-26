#!/usr/bin/env python
import os

mergelist = []

preamble   = []
preamble  += [ r'\documentclass[tikz]{standalone}' ]
preamble  += [ r'\usepackage{tikz-feynman}'        ]
preamble  += [ r'\begin{document}'                 ]
#preamble  += [ r'\feynmandiagram [layered layout, xscale=0.5] {' ]
#preamble  += [ r'\feynmandiagram [horizontal] {' ]
postamble  = []
#postamble += [ r'};' ]
postamble += [ r'\end{document}' ]

linetypes  = {'gamma':'photon', 'e+':'anti fermion'   , 'e-':'fermion'}
linelabels = {'gamma':'\gamma', 'e+':'e^{+}'          , 'e-':'e^{-}'  }


def gen_pdf( texname, texlines ) :
  with open( texname, 'w' ) as f :
    for pa in preamble :
      f.write( pa + '\n' )
    for l in texlines :
      f.write( l + '\n' )
    for pa in postamble :
      f.write( pa + '\n' )

  cmd = 'lualatex --output-format=pdf %s' % texname
  print('$', cmd )
  os.system( cmd )

tlines  = [ r'\begin{tikzpicture} ' ]
tlines += [ r'\begin{feynman} ' ]
tlines += [ r'  \vertex (u1) {\(u\)}; ' ]
tlines += [ r'  \vertex [right=of u1] (a); ' ]
tlines += [ r'  \vertex [below=of u1] (u2) {\(\overline u\)}; ' ]
tlines += [ r'  \vertex [right=of u2, below=of a] (b); ' ]
tlines += [ r'  \vertex [right=of a]  (g1) {\(\gamma\)};' ]
tlines += [ r'  \vertex [right=of b]  (g2) {\(\gamma\)};' ]
tlines += [ r'  \diagram* {' ]
tlines += [ r'    (u1) -- [fermion] (a) ,' ]
tlines += [ r'    (b)  -- [fermion] (u2),' ]
tlines += [ r'    (a)  -- [fermion] (b) ,' ]
tlines += [ r'    (a)  -- [photon ] (g1),' ]
tlines += [ r'    (b)  -- [photon ] (g2) ' ]
tlines += [ r'  };' ]
tlines += [ r'  \draw [decoration={brace}, decorate] (u2.south west) -- (u1.north west) node [pos=0.5, left] {\(\pi^{0}\)}; ' ]
tlines += [ r'\end{feynman}' ]
tlines += [ r'\end{tikzpicture}' ]
fname = 'pion_gamma.tex'
mergelist += [ os.path.splitext(fname)[0] + '.pdf' ]
if not os.path.exists( os.path.splitext(fname)[0] + '.pdf' ) :
  gen_pdf( fname, tlines )



#tlines  = [ r'\feynmandiagram [layered layout, horizontal=w1 to w2] {' ]
#tlines += [ r'  u [particle=\(u\)]  -- [fermion] w1 -- [photon, edge label=\(W^{+}\)] w2 -- [fermion] m [particle=\(\nu_{\mu}\)],']
#tlines += [ r'  d [particle=\(\overline d\)] -- [anti fermion] w1,']
#tlines += [ r'  w2 -- [fermion] n [particle=\(\mu^{+}\)]']
#tlines += [ r'};' ]

tlines  = [ r'\begin{tikzpicture} ' ]
tlines += [ r'\begin{feynman} ' ]
tlines += [ r'\diagram[layered layout, horizontal=w1 to w2] {' ]
tlines += [ r'  u [particle=\(u\)]  -- [fermion] w1,']
tlines += [ r'  w1 -- [photon, edge label=\(W^{+}\)] w2,']
tlines += [ r'  w2 -- [fermion] m [particle=\(\nu_{\mu}\)],']
tlines += [ r'  d [particle=\(\overline d\)] -- [anti fermion] w1,']
tlines += [ r'  w2 -- [anti fermion] n [particle=\(\mu^{+}\)]']
tlines += [ r'};' ]
tlines += [ r'\draw [decoration={brace}, decorate] (d.south west) -- (u.north west) node [pos=0.5, left] {\(\pi^{+}\)}; ' ]
tlines += [ r'\end{feynman}' ]
tlines += [ r'\end{tikzpicture}' ]

fname = 'pionplus.tex'
mergelist += [ os.path.splitext(fname)[0] + '.pdf' ]
if not os.path.exists( os.path.splitext(fname)[0] + '.pdf' ) :
  gen_pdf( fname, tlines )

