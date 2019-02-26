#!/usr/bin/env python
import os

mergelist = []

preamble   = []
preamble  += [ r'\documentclass[tikz]{standalone}' ]
preamble  += [ r'\usepackage{tikz-feynman}'        ]
preamble  += [ r'\begin{document}'                 ]
postamble  = []
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
tlines += [ r'  \vertex (f1); ' ]
tlines += [ r'  \vertex [below=of f1] (f2); ' ]
tlines += [ r'  \vertex [above left=of f1 ] (d1) {\(\chi\)}; ' ]
tlines += [ r'  \vertex [below left=of f2 ] (d2) {\(\chi\)}; ' ]
tlines += [ r'  \vertex [above right=of f1] (b1) {\(b\)}   ; ' ]
tlines += [ r'  \vertex [below right=of f2] (b2) {\(\overline b\)}; ']
tlines += [ r'  \diagram* {' ]
tlines += [ r'    (f1) -- [ghost, edge label=\(\tilde f\)] (f2) ' ]
tlines += [ r'    (d1) -- [plain] (f1) ' ]
tlines += [ r'    (d2) -- [plain] (f2) ' ]
tlines += [ r'    (f1) -- [fermion] (b1) ' ]
tlines += [ r'    (b2) -- [fermion] (f2) ' ]
tlines += [ r'  };' ]
tlines += [ r'\end{feynman}' ]
tlines += [ r'\end{tikzpicture}' ]
fname = 'neutralino_superf.tex'
mergelist += [ os.path.splitext(fname)[0] + '.pdf' ]
if not os.path.exists( os.path.splitext(fname)[0] + '.pdf' ) :
  gen_pdf( fname, tlines )


tlines  = [ r'\begin{tikzpicture} ' ]
tlines += [ r'\begin{feynman} ' ]
tlines += [ r'  \vertex (f1); ' ]
tlines += [ r'  \vertex [right=of f1] (f2); ' ]
tlines += [ r'  \vertex [above left=of f1 ] (d1) {\(\chi\)}; ' ]
tlines += [ r'  \vertex [below left=of f1 ] (d2) {\(\chi\)}; ' ]
tlines += [ r'  \vertex [above right=of f2] (b1) {\(b\)}   ; ' ]
tlines += [ r'  \vertex [below right=of f2] (b2) {\(\overline b\)}; ']
tlines += [ r'  \diagram* {' ]
tlines += [ r'    (f1) -- [photon, edge label=\(Z\)] (f2) ' ]
tlines += [ r'    (d1) -- [plain] (f1) ' ]
tlines += [ r'    (d2) -- [plain] (f1) ' ]
tlines += [ r'    (f2) -- [fermion] (b1) ' ]
tlines += [ r'    (b2) -- [fermion] (f2) ' ]
tlines += [ r'  };' ]
tlines += [ r'\end{feynman}' ]
tlines += [ r'\end{tikzpicture}' ]
fname = 'neutralino_zboson.tex'
mergelist += [ os.path.splitext(fname)[0] + '.pdf' ]
if not os.path.exists( os.path.splitext(fname)[0] + '.pdf' ) :
  gen_pdf( fname, tlines )


tlines  = [ r'\begin{tikzpicture} ' ]
tlines += [ r'\begin{feynman} ' ]
tlines += [ r'  \vertex (f1); ' ]
tlines += [ r'  \vertex [right=of f1] (f2); ' ]
tlines += [ r'  \vertex [above left=of f1 ] (d1) {\(\chi\)}; ' ]
tlines += [ r'  \vertex [below left=of f1 ] (d2) {\(\chi\)}; ' ]
tlines += [ r'  \vertex [above right=of f2] (b1) {\(b\)}   ; ' ]
tlines += [ r'  \vertex [below right=of f2] (b2) {\(\overline b\)}; ']
tlines += [ r'  \diagram* {' ]
tlines += [ r'    (f1) -- [ghost, edge label=\(H\)] (f2) ' ]
tlines += [ r'    (d1) -- [plain] (f1) ' ]
tlines += [ r'    (d2) -- [plain] (f1) ' ]
tlines += [ r'    (f2) -- [fermion] (b1) ' ]
tlines += [ r'    (b2) -- [fermion] (f2) ' ]
tlines += [ r'  };' ]
tlines += [ r'\end{feynman}' ]
tlines += [ r'\end{tikzpicture}' ]
fname = 'neutralino_aghost.tex'
mergelist += [ os.path.splitext(fname)[0] + '.pdf' ]
if not os.path.exists( os.path.splitext(fname)[0] + '.pdf' ) :
  gen_pdf( fname, tlines )

